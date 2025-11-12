from rest_framework.urls import path

from .views import UserRegister, CustomTokenObtainPairView

app_name = "users"

urlpatterns = [
    path("register/", UserRegister.as_view()),
    path("login/", CustomTokenObtainPairView.as_view()),
]
