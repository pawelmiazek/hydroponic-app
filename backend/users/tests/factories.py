import factory
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    password = factory.Faker("pystr")
    email = factory.Faker("email")
    username = factory.Faker("pystr")

    class Meta:
        model = User
