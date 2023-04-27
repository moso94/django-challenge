from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.permissions import AllowAny
from .models import Listing, Room, Reservation
from .serializers import ListingsSerializer, RoomsSerializer, ReservationsSerializer
from .helper import getEmptyRooms
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi

# # Create your views here.


class ListingsRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ListingsSerializer
    queryset = Listing.objects.all()


class ListingsView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Listing.objects.all()
    serializer_class = ListingsSerializer
    ordering_fields = ('pk',)
    ordering = ('-pk',)


class RoomsRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RoomsSerializer
    queryset = Room.objects.all()


class RoomsView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Room.objects.all()
    serializer_class = RoomsSerializer
    ordering_fields = ('pk',)
    ordering = ('-pk',)


class ReservationsView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Reservation.objects.all()
    serializer_class = ReservationsSerializer
    ordering_fields = ('pk',)
    ordering = ('-pk',)


class ReservationsRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ReservationsSerializer
    queryset = Reservation.objects.all()


class ProfileList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'room_list.html'

    def get(self, request, pk):
        queryset = Reservation.objects.filter(room__listing_id=pk).all()
        return Response({'reservations': queryset})


start_at_param = openapi.Parameter('start_at', openapi.IN_QUERY,
                                   type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME)
end_at_param = openapi.Parameter('end_at', openapi.IN_QUERY,
                                 type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME)


@swagger_auto_schema(method='get', manual_parameters=[start_at_param, end_at_param],
                     responses={200: RoomsSerializer(many=True)})
@api_view(['GET'])
def check_rooms(request):
    result, rooms = getEmptyRooms(request.query_params)
    if result:
        return Response(RoomsSerializer(rooms, many=True).data)
    raise ValidationError("message: add start and end time")
