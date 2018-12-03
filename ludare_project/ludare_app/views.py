from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status

from .decorators import validate_request_data
from .models import Todos
from .serializers import TodosSerializer


# Create your views here.

class ListCreateTodosView(generics.ListCreateAPIView):
    """
    Provides GET and POST method handlers
    """
    serializer_class = TodosSerializer

    def get_queryset(self):
        queryset = Todos.objects.all()
        state = self.request.query_params.get("state", None)
        due_date = self.request.query_params.get("due_date", None)
        # Narrow results to chosen state
        if state in ["T", "I", "D"]:
            queryset = queryset.filter(state=state)
        # Sort results by due date
        if due_date == "asc":
            queryset = queryset.order_by("due_date")
        elif due_date == "desc":
            queryset = queryset.order_by("-due_date")
        return queryset


    @validate_request_data
    def post(self, request, *args, **kwargs):
        new_todo = Todos.objects.create(
            state=request.data["state"],
            due_date=request.data["due_date"],
            text=request.data["text"]
        )
        return Response(
            data=TodosSerializer(new_todo).data,
            status=status.HTTP_201_CREATED
        )


class TodosDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Provides GET, PUT and DELETE methods given todo ID/PK
    """
    queryset = Todos.objects.all()
    serializer_class = TodosSerializer

    def get(self, request, *args, **kwargs):
        try:
            my_todo = self.queryset.get(pk=kwargs["pk"])
            return Response(TodosSerializer(my_todo).data)
        except Todos.DoesNotExist:
            return Response(
                data={
                    "message": "TODO with ID: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            my_todo = self.queryset.get(pk=kwargs["pk"])
            serializer = TodosSerializer()
            updated_todo = serializer.update(my_todo, request.data)
            return Response(TodosSerializer(updated_todo).data)
        except Todos.DoesNotExist:
            return Response(
                data={
                    "message": "TODO with ID: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            my_todo = self.queryset.get(pk=kwargs["pk"])
            my_todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Todos.DoesNotExist:
            return Response(
                data={
                    "message": "TODO with ID: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
