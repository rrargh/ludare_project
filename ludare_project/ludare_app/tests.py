import json
from datetime import date
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from urllib.parse import urlencode
from .models import Todos
from .serializers import TodosSerializer

date_today = date(2018, 12, 25)
date_yesterday= date(2018, 12, 24)
date_tomorrow = date(2018, 12, 26)

# Create your tests here.

# encode URL with a query string
def url_with_querystring(path, **kwargs):
    return path + "?" + urlencode(kwargs)

# tests for models


class TodosModelTest(APITestCase):
    def setUp(self):
        self.my_todo = Todos.objects.create(
            state="T",
            due_date=date_today,
            text="Call Mom"
        )

    def test_todo(self):
        """"
        This test ensures that the todo created in the setup
        exists
        """
        self.assertEqual(self.my_todo.state, "T")
        self.assertEqual(self.my_todo.due_date, date_today)
        self.assertEqual(self.my_todo.text, "Call Mom")
        self.assertEqual(str(self.my_todo), "Call Mom")

# tests for views

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

    def make_a_request(self, kind="post", **kwargs):
        """
        Make a post request to create a todo
        :param kind: HTTP VERB
        :return:
        """
        if kind == "post":
            return self.client.post(
                reverse(
                    "todos-list-create",
                    kwargs={
                        "version": kwargs["version"]
                    }
                ),
                data=json.dumps(
                    kwargs["data"],
                    cls=DjangoJSONEncoder
                ),
                content_type='application/json'
            )
        elif kind == "put":
            return self.client.put(
                reverse(
                    "todos-detail",
                    kwargs={
                        "version": kwargs["version"],
                        "pk": kwargs["id"]
                    }
                ),
                data=json.dumps(
                    kwargs["data"],
                    cls=DjangoJSONEncoder
                ),
                content_type='application/json'
            )
        else:
            return None

    def fetch_a_todo(self, pk=0):
        return self.client.get(
            reverse(
                "todos-detail",
                kwargs={
                    "version": "v1",
                    "pk": pk
                }
            )
        )

    def delete_a_todo(self, pk=0):
        return self.client.delete(
            reverse(
                "todos-detail",
                kwargs={
                    "version": "v1",
                    "pk": pk
                }
            )
        )

    def setUp(self):
        # add test data
        self.create_todo("T", date_tomorrow, "buy eggs")
        self.create_todo("I", date_today, "buy milk")
        self.create_todo("D", date_yesterday, "buy cheese")
        self.create_todo("T", date_tomorrow, "eat breakfast")
        self.create_todo("I", date_today, "eat dinner")
        self.create_todo("D", date_yesterday, "eat lunch")
        self.valid_data = {
            "state": "T",
            "due_date": "2018-12-25",
            "text": "test text"
        }
        self.invalid_data = {
            "state": "",
            "due_date": "",
            "text": ""
        }
        self.valid_todo_id = 1
        self.invalid_todo_id = 100


class GetAllTodosTest(BaseViewTest):

    def test_get_all_todos(self):
        """
        This test ensures that all todos added in the setUp method
        exist when we make a GET request to the todos/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("todos-list-create", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Todos.objects.all()
        serialized = TodosSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test filtering by state "to do"
        url_with_filtering = url_with_querystring(
            reverse("todos-list-create", kwargs={"version": "v1"}),
            state="T"
        )
        response = self.client.get(url_with_filtering)
        expected = Todos.objects.filter(state="T")
        serialized = TodosSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test filtering by state "in progress"
        url_with_filtering = url_with_querystring(
            reverse("todos-list-create", kwargs={"version": "v1"}),
            state="I"
        )
        response = self.client.get(url_with_filtering)
        expected = Todos.objects.filter(state="I")
        serialized = TodosSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test filtering by state "done"
        url_with_filtering = url_with_querystring(
            reverse("todos-list-create", kwargs={"version": "v1"}),
            state="D"
        )
        response = self.client.get(url_with_filtering)
        expected = Todos.objects.filter(state="D")
        serialized = TodosSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test ordering by ascending due date
        url_with_filtering = url_with_querystring(
            reverse("todos-list-create", kwargs={"version": "v1"}),
            ordering="due_date"
        )
        response = self.client.get(url_with_filtering)
        expected = Todos.objects.order_by("due_date")
        serialized = TodosSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test ordering by descending due date
        url_with_filtering = url_with_querystring(
            reverse("todos-list-create", kwargs={"version": "v1"}),
            ordering="-due_date"
        )
        response = self.client.get(url_with_filtering)
        expected = Todos.objects.order_by("-due_date")
        serialized = TodosSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetASingleTodosTest(BaseViewTest):

    def test_get_a_todo(self):
        """
        This test ensures that a single todo of a given id is
        returned
        """
        # hit the API endpoint
        response = self.fetch_a_todo(self.valid_todo_id)
        # fetch the data from db
        expected = Todos.objects.get(pk=self.valid_todo_id)
        serialized = TodosSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with a todo that does not exist
        response = self.fetch_a_todo(self.invalid_todo_id)
        self.assertEqual(
            response.data["message"],
            "TODO with ID: 100 does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AddTodosTest(BaseViewTest):

    def test_create_a_todo(self):
        """
        This test ensures that a single todo can be added
        """
        # hit the API endpoint
        response = self.make_a_request(
            kind="post",
            version="v1",
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test with invalid data
        response = self.make_a_request(
            kind="post",
            version="v1",
            data=self.invalid_data
        )
        self.assertEqual(
            response.data["message"],
            "TODO item requires state, due_date and text"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateTodosTest(BaseViewTest):

    def test_update_a_todo(self):
        """
        This test ensures that a single todo can be updated. In this
        test we update the second todo in the db with valid data and
        the third todo with invalid data and make assertions
        """
        # hit the API endpoint
        response = self.make_a_request(
            kind="put",
            version="v1",
            id=2,
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with invalid data
        response = self.make_a_request(
            kind="put",
            version="v1",
            id=3,
            data=self.invalid_data
        )
        self.assertEqual(
            response.data["message"],
            "TODO item requires state, due_date and text"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteTodosTest(BaseViewTest):

    def test_delete_a_todo(self):
        """
        This test ensures that a todo of given id can be deleted
        """
        # hit the API endpoint
        response = self.delete_a_todo(1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # test with invalid data
        response = self.delete_a_todo(100)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
