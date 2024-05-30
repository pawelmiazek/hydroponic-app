from functools import wraps
from typing import Type

from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer
from users.models import User


class ContextUserSerializer:
    context_user: User


def context_user_required(maybe_cls: Type[ModelSerializer] = None):
    @wraps(Type[ModelSerializer])
    def decorator(
        cls: Type[ModelSerializer],
    ) -> Type[ModelSerializer | ContextUserSerializer]:
        def _context_user(self) -> User | None:
            return getattr(
                getattr(self, "context", {}).get("request", None), "user", None
            )

        cls.context_user = property(_context_user, None)

        if not hasattr(cls, "default_error_messages"):
            cls.default_error_messages = {}

        cls.default_error_messages["no_user_in_request"] = _(
            "No user provided in request"
        )
        original_validate = cls.validate

        @wraps(original_validate)
        def _validate(self, attrs):
            if not self.context_user:
                self.fail("no_user_in_request")

            return original_validate(self, attrs)

        cls.validate = _validate

        return cls

    if maybe_cls is not None:
        return decorator(maybe_cls)
    else:
        return decorator
