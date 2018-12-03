from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):
        state = args[0].request.data.get("state", "")
        due_date = args[0].request.data.get("due_date", None)
        text = args[0].request.data.get("text", "")
        if not state and not due_date and not text:
            return Response(
                data={
                    "message": "TODO item requires state, due_date and text"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated
