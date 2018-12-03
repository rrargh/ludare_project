from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
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
    queryset = Todos.objects.all()
    serializer_class = TodosSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ("state",)
    ordering_fields = ("due_date",)

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
