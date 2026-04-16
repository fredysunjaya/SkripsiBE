from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.users import User
from skripsiBE.app.models.user_groups import UserGroup
from skripsiBE.app.serializers.users import UserSerializer
from skripsiBE.app.serializers.user_groups import UserGroupSerializer
from deepface import DeepFace
from deepface.modules.verification import find_threshold
from deepface.modules.verification import find_euclidean_distance
from rest_framework.settings import api_settings
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from skripsiBE.app.custom_is_authenticated import IsAuthenticatedUser, IsAdminUser, IsSupervisorUser
import bcrypt
import os
import tempfile

class UsersList(APIView):
  # maybe unused
  authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
  permission_classes = [IsAdminUser | IsSupervisorUser]

  def get(self, request, group):
    users = UserGroup.objects.all()

    paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    result_page = paginator.paginate_queryset(users, request)

    serializers = UserGroupSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializers.data)

class UserDetails(APIView):
  authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
  permission_classes = [IsAuthenticatedUser]

  def getUser(id):
    try:
      user = User.objects.get(pk=id)
      return user
    except User.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    except:
      return Response(status=status.HTTP_400_BAD_REQUEST)
  
  def get(self, request, id):
    serializer = UserSerializer(self.getUser(id))
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def put(self, request, id):
    serializer = UserSerializer(self.getUser(id), data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
      
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request, id):
    user = self.getUser(id)
    user.delete()
    return Response("User Deleted", status=status.HTTP_204_NO_CONTENT)

class UserLogin(APIView):
  def post(self, request):
    email = request.data.get("email")
    password = request.data.get("password")
    
    try:
      user = User.objects.get(email=email)

      if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
      
      serializer = UserSerializer(user)

      # save user id in session — Django sets cookie automatically
      request.session['user_id'] = user.id
      request.session.save()

      return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
      return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
      return Response(status=status.HTTP_400_BAD_REQUEST)
  
class UserLogout(APIView):
  authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
  permission_classes = [IsAuthenticatedUser]
  
  def post(request):
    request.session.flush()
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class UserRegister(APIView):
  def post(self, request):
    file = request.FILES.get("file")

    if not file:
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
      
    embeddings = DeepFace.represent(img_path = file, model_name = "Facenet512")
    
    data = request.data.copy()
    data["face_vector"] = embeddings[0]["embedding"]
    data["password"] = bcrypt.hashpw(serializer.data.get("password").encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserFaceLogin(APIView):
  def post (self, request):
    file = request.FILES.get('file')
    if not file:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # save file temporarily — DeepFace needs a file path or numpy array
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp:
            for chunk in file.chunks():
                temp.write(chunk)
            temp_path = temp.name

        # get embedding from uploaded image
        embeddings = DeepFace.represent(
            img_path=temp_path,
            model_name='Facenet512'
        )
        input_vector = embeddings[0]['embedding']
        input_vector_str = '[' + ','.join(map(str, input_vector)) + ']'  # format for pgvector

    except Exception as e:
        return Response(
            {'error': f'Face processing failed: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    finally:
        # always delete temp file
        os.unlink(temp_path)

    # find nearest face in DB using pgvector
    try:
        nearest_users = User.objects.raw("""
            SELECT id, face_vector, email
            FROM users
            ORDER BY face_vector <-> %s::vector
            LIMIT 1
        """, [input_vector_str])

        nearest_user = list(nearest_users)
        if not nearest_user:
            return Response(
                {'error': 'No users found'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        nearest_user = nearest_user[0]

    except Exception as e:
        return Response(
            {'error': f'DB query failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # verify distance
    stored_vector = nearest_user.face_vector
    distance = find_euclidean_distance(input_vector, stored_vector)
    threshold = find_threshold('Facenet512', 'euclidean')

    if distance > threshold:
        return Response(
            {'error': 'Face does not match'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # set session — user is now logged in
    request.session['user_id'] = nearest_user.id
    request.session.save()

    serializer = UserSerializer(nearest_user)
    return Response(serializer.data, status=status.HTTP_200_OK)