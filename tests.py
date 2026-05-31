import bcrypt
import faker

fake = faker.Faker("id_ID")
password = "#33XJOjFc*"

print(password)
print(bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"))
