from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", views.UserRetrieveUpdateView.as_view(), name="user_retrieve_update"),
    path("list/", views.UserListCreateView.as_view(), name="user_list"),
    path("register/", views.UserRegisterView.as_view(), name="user_register"),
]
