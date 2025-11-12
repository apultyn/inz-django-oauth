from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Book, Review


class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="author.email", read_only=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ("id", "stars", "comment", "author", "book", "user_email")
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=["author", "book"],
                message="You can write only one review per book",
            )
        ]


class BookSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ("id", "title", "author", "reviews")
        validators = [
            UniqueTogetherValidator(
                queryset=Book.objects.all(),
                fields=["title", "author"],
                message="Books must have unique combination of title and author",
            )
        ]
