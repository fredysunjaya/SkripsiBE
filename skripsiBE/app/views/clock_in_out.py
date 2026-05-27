import cv2
from rest_framework import status
from django.db.models import Q
from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.users import User
from skripsiBE.app.models.user_logs import UserLog
from skripsiBE.app.serializers.users import UserSerializer
from deepface import DeepFace
from deepface.modules.verification import find_threshold
from deepface.modules.verification import find_euclidean_distance
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from skripsiBE.app.custom_is_authenticated import (
    IsAuthenticatedUser,
    IsAdminUser,
    IsSupervisorUser,
)
from django.utils.dateparse import parse_datetime
import numpy as np


class UserFaceLogin(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
    permission_classes = [IsAuthenticatedUser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"})

        # save file temporarily — DeepFace needs a file path or numpy array
        try:
            file_bytes = np.frombuffer(file.read(), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            if img is None:
                return Response({"error": "Invalid image file"})

            embeddings = DeepFace.represent(
                img_path=img,
                model_name="Facenet512",
                enforce_detection=True,  # Ensures a face is actually present
            )

            if not embeddings:
                return Response(
                    {"error": "No face detected in image", "error_code": 2},
                )

            input_vector = np.array(embeddings[0]["embedding"])
        except Exception as e:
            return Response(
                {"error": f"Face processing failed: {str(e)}"},
            )

        # find nearest face in DB using pgvector
        try:
            input_vector_str = (
                "[" + ",".join(map(str, input_vector.tolist())) + "]"
            )  # format for pgvector

            nearest_users = User.objects.raw(
                """
                SELECT id, face_vector, email
                FROM users
                ORDER BY face_vector <-> %s::vector
                LIMIT 1
                """,
                [input_vector_str],
            )

            nearest_user = list(nearest_users)
            if not nearest_user:
                return Response({"error": "No users found"})
            nearest_user = nearest_user[0]

        except Exception as e:
            return Response(
                {"error": f"DB query failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # verify distance
        stored_vector = np.array(nearest_user.face_vector)
        distance = find_euclidean_distance(input_vector, stored_vector)
        threshold = find_threshold("Facenet512", "euclidean")

        if distance > threshold:
            return Response(
                {
                    "error": "Face does not match",
                    "distance": distance,
                    "threshold": threshold,
                },
            )

        user_id = request.POST.get("user_id")
        group_id = request.POST.get("group_id")
        date_time = request.POST.get("date_time")

        user_log = (
            UserLog.objects.filter(
                user_id=user_id,
                group_id=group_id,
            )
            .filter(
                Q(start_date_time__date=parse_datetime(date_time).date())
                | Q(end_date_time__date=parse_datetime(date_time).date())
            )
            .first()
        )

        start_date_time = None
        end_date_time = None

        # create new user log
        if request.POST.get("type") == "clock in":
            start_date_time = date_time
        elif request.POST.get("type") == "clock out":
            end_date_time = date_time

        if user_log is None:
            user_log = UserLog.objects.create(
                user_id=user_id,
                group_id=group_id,
                start_date_time=start_date_time,
                end_date_time=end_date_time,
            )

        # update user log based on leave
        else:
            user_log.start_date_time = start_date_time or user_log.start_date_time
            user_log.end_date_time = end_date_time or user_log.end_date_time

            user_log.save()
        return Response(status=status.HTTP_200_OK)
