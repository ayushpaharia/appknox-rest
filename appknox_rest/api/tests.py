from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Question


class QuestionAPITestCase(APITestCase):
    def setUp(self):
        self.question = Question.objects.create(
            title="Test Question", body="This is a test question body."
        )

    def test_list(self):
        url = reverse("question-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.question.title)

    def test_create(self):
        url = reverse("question-list")
        data = {"title": "New Question", "body": "This is a new question body."}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)
        self.assertEqual(Question.objects.last().title, "New Question")

    def test_retrieve(self):
        url = reverse("question-detail", args=[self.question.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.question.title)

    def test_update(self):
        url = reverse("question-detail", args=[self.question.pk])
        data = {
            "title": "Updated Question",
            "body": "This is an updated question body.",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.question.refresh_from_db()
        self.assertEqual(self.question.title, "Updated Question")

    def test_delete(self):
        url = reverse("question-detail", args=[self.question.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Question.objects.filter(pk=self.question.pk).exists())
