from collections import OrderedDict

from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password")
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def create(self, validated_data: OrderedDict) -> User:
        return User.objects.create_user(**validated_data)
