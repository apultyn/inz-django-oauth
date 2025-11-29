from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Book, Review


class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="author.email", read_only=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    bookId = serializers.PrimaryKeyRelatedField(
        source="book",
        queryset=Book.objects.all(),
        write_only=False,
    )

    class Meta:
        model = Review
        fields = ("id", "stars", "comment", "author", "bookId", "user_email")

    def validate(self, attrs):
        author = attrs.get("author")
        book = attrs.get("book")

        if self.instance is None:
            if Review.objects.filter(author=author, book=book).exists():
                raise serializers.ValidationError(
                    {"bookId": "You can write only one review per book"}
                )

        return attrs


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
