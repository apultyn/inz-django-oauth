from rest_framework.routers import DefaultRouter

from .views import BookViewSet, ReviewViewSet

app_name = "review_app"

router = DefaultRouter()
router.register("books", BookViewSet, basename="book")
router.register("reviews", ReviewViewSet, basename="review")

urlpatterns = []

urlpatterns += router.urls
