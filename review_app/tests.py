from django.urls import path, include
from django.contrib.auth.models import Group

from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Book, Review
from users.models import NewUser


class BaseITTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("api/", include("review_app.urls"))]

    def setUp(self):
        self.book1 = Book.objects.create(id="1", title="1984", author="George Orwell")
        self.book2 = Book.objects.create(
            id="2", title="Brave New World", author="Aldous Huxley"
        )

        self.user = NewUser.objects.create_user(
            password="passwd", email="user@example.com"
        )
        self.admin = NewUser.objects.create_user(
            password="passwd", email="admin@example.com"
        )

        self.group = Group.objects.create(name="book_admin")
        self.admin.groups.add(self.group)
        self.admin.save()

        self.review1 = Review.objects.create(
            id="1", stars="5", comment="Awesome book", author=self.user, book=self.book1
        )

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class BookITTests(BaseITTests):
    def test_view_books(self):
        response = self.client.get("/api/books/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_view_books_searchstring(self):
        Book.objects.create(id="3", title="The story of george", author="Some author")
        Book.objects.create(
            id="4", title="The other story of george", author="Some author"
        )
        response = self.client.get("/api/books/?searchString=george", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_view_book(self):
        response = self.client.get("/api/books/1/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "title": "1984",
                "author": "George Orwell",
                "reviews": [
                    {
                        "id": 1,
                        "stars": 5,
                        "comment": "Awesome book",
                        "user_email": "user@example.com",
                        "book": 1,
                    }
                ],
            },
        )

    def test_create_book_unauth(self):
        response = self.client.post(
            "/api/books/",
            format="json",
            data={"title": "Dune", "author": "Frank Herbert"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_user(self):
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(
            "/api/books/",
            format="json",
            data={"title": "Dune", "author": "Frank Herbert"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_admin(self):
        token = self.get_jwt_token(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(
            "/api/books/",
            format="json",
            data={"title": "Dune", "author": "Frank Herbert"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book_unauth(self):
        response = self.client.patch(
            "/api/books/1/",
            format="json",
            data={"title": "Dune", "author": "Frank Herbert"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_user(self):
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.patch(
            "/api/books/1/",
            format="json",
            data={"title": "Dune", "author": "Frank Herbert"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_admin(self):
        token = self.get_jwt_token(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.patch(
            "/api/books/1/",
            format="json",
            data={"title": "Dune"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_book = Book.objects.get(id=1)
        self.assertEqual(updated_book.title, "Dune")
        self.assertEqual(updated_book.author, "George Orwell")

    def test_delete_book_unauth(self):
        response = self.client.delete(
            "/api/books/1/",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_user(self):
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(
            "/api/books/1/",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_admin(self):
        token = self.get_jwt_token(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(
            "/api/books/1/",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ReviewITTests(BaseITTests):
    def test_view_reviews(self):
        response = self.client.get("/api/reviews/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_view_review(self):
        response = self.client.get("/api/reviews/1/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["comment"], "Awesome book")
        self.assertEqual(data["stars"], 5)

    def test_create_review_unauth(self):
        response = self.client.post(
            "/api/reviews/",
            format="json",
            data={"stars": 4, "comment": "A little too short", "book": 1},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_review_user(self):
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(
            "/api/reviews/",
            format="json",
            data={"stars": 4, "comment": "A little too short", "book": 2},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        book1_reviews = Review.objects.filter(book=2)
        review = Review.objects.get(stars=4)
        self.assertEqual(book1_reviews.count(), 1)
        self.assertEqual(review.author.id, self.user.id)

    def test_create_review_admin(self):
        token = self.get_jwt_token(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(
            "/api/reviews/",
            format="json",
            data={"stars": 4, "comment": "A little too short", "book": 1},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        book1_reviews = Review.objects.filter(book=1)
        self.assertEqual(book1_reviews.count(), 2)
        review = Review.objects.get(stars=4)
        self.assertEqual(book1_reviews.count(), 2)
        self.assertEqual(review.author.id, self.admin.id)

    def test_update_review_unauth(self):
        response = self.client.patch(
            "/api/reviews/1/",
            format="json",
            data={"stars": 3},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_review_user(self):
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.patch(
            "/api/reviews/1/",
            format="json",
            data={"stars": 3},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_review_admin(self):
        token = self.get_jwt_token(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.patch(
            "/api/reviews/1/",
            format="json",
            data={"stars": 3},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        review = Review.objects.get(id=1)
        self.assertEqual(review.stars, 3)
        self.assertEqual(review.comment, "Awesome book")

    def test_delete_review_unauth(self):
        response = self.client.delete("/api/reviews/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_review_user(self):
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete("/api/reviews/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review_admin(self):
        token = self.get_jwt_token(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete("/api/reviews/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        book1_reviews = Review.objects.filter(book=1)
        self.assertEqual(book1_reviews.count(), 0)
