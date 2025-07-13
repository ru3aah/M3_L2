from rest_framework.request import Request
from rest_framework.response import Response


def simpleAPIView(request: Request) -> Response:
    return Response({'status': 'ok'})
