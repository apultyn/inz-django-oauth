from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookViewSet, ReviewViewSet

app_name = "review_app"

router = DefaultRouter()
router.register("books", BookViewSet, basename="book")
router.register("reviews", ReviewViewSet, basename="review")

urlpatterns = [
    path("auth/", include("users.urls", namespace="users")),
]

urlpatterns += router.urls
