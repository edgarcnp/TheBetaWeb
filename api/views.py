from base.models import Room
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import RoomSerializer

# Create your views here.


@api_view(["GET"])
def get_route(request):
    routes = [
        "GET /api",
        "GET /api/rooms",
        "GET /api/rooms/:id",
    ]

    return Response(routes)


@api_view(["GET"])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_room(request, room_id):
    room = Room.objects.get(id=room_id)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)
