from django.urls import include
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from users import views


urlpatterns = [
    path(
        r"users/",
        include(
            [
                path(
                    r"register/", views.RegisterUserViewSet.as_view({"post": "create"})
                ),
                path(r"current_user/", views.CurrentUserView.as_view()),
            ]
        ),
    ),
    path(r"token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(r"token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
]
