import cv2
from django.shortcuts import get_object_or_404
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
from skripsiBE.app.custom_is_authenticated import (
    IsAuthenticatedUser,
    IsAdminUser,
    IsSupervisorUser,
)
import bcrypt
import numpy as np


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

    def get_user(self, email):
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        serializer = UserSerializer(get_object_or_404(User, pk=id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    # maybe unused
    def put(self, request, id):
        serializer = UserSerializer(self.get_user(id), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # maybe unused
    def delete(self, request, id):
        user = self.get_user(id)
        user.delete()
        return Response("User Deleted", status=status.HTTP_204_NO_CONTENT)


class UserLogin(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)

            if not bcrypt.checkpw(
                password.encode("utf-8"), user.password.encode("utf-8")
            ):
                return Response(
                    {"error": "Invalid email or password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            serializer = UserSerializer(user)

            # save user id in session — Django sets cookie automatically
            request.session["user_id"] = user.id
            request.session.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"error_code": 4},
            )
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
    permission_classes = [IsAuthenticatedUser]

    def post(self, request):
        request.session.flush()
        return Response(status=status.HTTP_200_OK)


class UserRegister(APIView):
    def post(self, request):
        if User.objects.filter(email=request.data.get("email")).exists():
            return Response(
                {"error_code": 3},
            )

        data = request.data.copy()
        data["password"] = bcrypt.hashpw(
            data.get("password").encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        user = User.objects.create(
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),
        )

        user.save()
        request.session["user_id"] = user.id
        request.session.save()

        return Response(status=status.HTTP_201_CREATED)


class UserFaceRegister(APIView):
    def post(self, request):
        files = request.FILES.getlist("files")  # get multiple files

        if not files:
            return Response({"error": "No files provided"})

        if len(files) < 1 or len(files) > 10:
            return Response({"error": "Please provide between 1 and 10 images"})

        all_embeddings = []

        for file in files:
            try:
                # Convert Django InMemoryUploadedFile → numpy array
                file_bytes = np.frombuffer(file.read(), dtype=np.uint8)
                img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                embeddings = DeepFace.represent(img_path=img, model_name="Facenet512")
                if embeddings:
                    all_embeddings.append(embeddings[0]["embedding"])
            except Exception as e:
                return Response({"error": f"Face detection failed: {str(e)}"})

        if not all_embeddings:
            return Response(
                {"error": "No faces detected in any image", "error_code": 2}
            )

        # Average all embeddings into one combined vector
        averaged_vector = np.mean(all_embeddings, axis=0).tolist()

        user = User.objects.get(pk=request.session["user_id"])
        user.face_vector = averaged_vector
        user.save()
        return Response(status=status.HTTP_200_OK)
