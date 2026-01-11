from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from skripsiBE.app.models.users import User
from skripsiBE.app.serializers.users import UserSerializer
from deepface import DeepFace
from deepface.modules.verification import find_threshold
from deepface.modules.verification import find_euclidean_distance

@api_view(["GET"])
def UsersList(request):
  if request.method == "GET":
    users = User.objects.all()
    serializers = UserSerializer(users, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

@api_view(["GET", "PUT", "DELETE"])
def UserDetails(request, id):
  try:
    user = User.objects.get(pk=id)
  except User.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  except:
    return Response(status=status.HTTP_400_BAD_REQUEST);
  
  if request.method == "GET":
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  if request.method == "PUT":
    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
      
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == "DELETE":
    user.delete()
    return Response("User Deleted", status=status.HTTP_204_NO_CONTENT)
  
@api_view(["POST"])
def UserLogin(request):
  if request.method == "POST":
    email = request.data.get("email")
    password = request.data.get("password")
    
    try:
      user = User.objects.get(email=email, password=password)
      serializer = UserSerializer(user)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
      return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
      return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def UserRegister(request):
  if request.method == "POST":
    file = request.FILES.get("file")

    if not file:
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
      
    embeddings = DeepFace.represent(img_path = file, model_name = "Facenet512")
    
    request.data["face_vector"] = embeddings[0]["embedding"]
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
@api_view(["POST"])
def UserFaceLogin(request):
  if request.method == "POST":
    file = request.FILES.get("file")

    if not file:
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    embeddings = DeepFace.represent(img_path = file, model_name = "Facenet512")
    input_vector = embeddings[0]["embedding"]
    
    nearestFace = User.objects.raw("""
      SELECT id, face_vector <-> %s
      """, [input_vector]) 
    nearestFace = nearestFace[0].face_vector
    
    distance = find_euclidean_distance(input_vector, nearestFace)
    threshold = find_threshold("Facenet512", "euclidean")
    
    if distance < threshold:
      return True
    
    # users = User.objects.all()
    # for user in users:
    #   stored_vector = user.face_vector
    #   distance = DeepFace.distance(input_vector, stored_vector, metric = "euc")
      
    #   if distance < 0.4:
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({"error": "No matching user found"}, status=status.HTTP_401_UNAUTHORIZED)