from django.urls import path
from .views import ListCreateTodosView, TodosDetailView


urlpatterns = [
    path("todos/", ListCreateTodosView.as_view(), name="todos-list-create"),
    path("todos/<int:pk>/", TodosDetailView.as_view(), name="todos-detail")
]
