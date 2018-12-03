from django.db.models import Model, CharField, DateField, TextField

# Create your models here.


class Todos(Model):
    TODO_STATES = (
        ("T", "to do"),
        ("I", "in progress"),
        ("D", "done"),
    )
    state = CharField(max_length=1, choices=TODO_STATES)
    due_date = DateField()
    text = TextField()

    def __str__(self):
        return "{}".format(self.text)
