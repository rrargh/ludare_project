from rest_framework.serializers import ModelSerializer
from .models import Todos


class TodosSerializer(ModelSerializer):
    class Meta:
        model = Todos
        fields = ("state", "due_date", "text")

    def update(self, instance, validated_data):
        instance.state = validated_data.get("state", instance.state)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance
