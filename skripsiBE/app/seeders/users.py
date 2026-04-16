from faker import Faker
from skripsiBE.app.models.users import User
import os
from deepface import DeepFace

def UserSeeder():
    fake = Faker("id_ID")
    folder = "static/images/faces/"
    images = [
        os.path.join(folder, file) for file in os.listdir(folder)
    ]
    images = tuple(images)
    
    for i in range(10):
        try:
            image = fake.unique.random_element(images)
            vector = DeepFace.represent(img_path=image, model_name="Facenet512")[0]["embedding"]
            
            User.objects.create(
                name = fake.name(),
                email = fake.unique.email(),
                password = fake.password(),
                face_vector = vector
            )
        except:
            print(image)
            continue