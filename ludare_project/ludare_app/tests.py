from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Todos
from .serializers import TodosSerializer


# Create your tests here.


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_todo(state="", due_date="", text=""):
        if state != "" and due_date != "" and text != "":
            Todos.objects.create(
                    state=state,
                    due_date=due_date,
                    text=text
            )

    def setUp(self):
        # add test data
        self.create_todo("todo", "2018-12-25", "buy eggs")
        self.create_todo("in-progress", "2018-12-25", "buy milk")
        self.create_todo("done", "2018-12-25", "buy cheese")


class GetAllTodosTest(BaseViewTest):

    def test_got_all_todos(self):
        """
        This test ensures that all todos added in the setUp method
        exist when we make a GET request to the todos/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("todos-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Todos.objects.all()
        serialized = TodosSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
