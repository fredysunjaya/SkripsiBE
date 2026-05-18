import bcrypt
import faker

fake = faker.Faker("id_ID")
password = fake.password(
    length=12, special_chars=True, digits=True, upper_case=True, lower_case=True
)

print(password)
print(bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"))
