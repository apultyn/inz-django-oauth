from django.db import models

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)

from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer


class BookPermission(BasePermission):
    message = "You have to be admin for this operation"

    def has_permission(self, request, _):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="book_admin").exists()
        )

    def has_object_permission(self, request, view, _):
        return self.has_permission(request, view)


class ReviewPermission(BasePermission):
    def has_permission(self, request, _):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.is_authenticated
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="book_admin").exists()
        )

    def has_object_permission(self, request, view, _):
        return self.has_permission(request, view)


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [BookPermission]

    def get_queryset(self):
        return Book.objects.all()

    def list(self, request, *args, **kwargs):
        search = request.query_params.get("searchString", "").strip().lower()
        queryset = self.get_queryset()

        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) | models.Q(author__icontains=search)
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewPermission]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
