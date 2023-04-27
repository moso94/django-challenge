from rest_framework import serializers
from .models import Listing, Room, Reservation
from .helper import checkReservationData


class ListingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ('pk',
                  'created_at',
                  'name')
        read_only_fields = ('created_at',)


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('pk',
                  'name',
                  'created_at',
                  'listing',)

        read_only_fields = ('created_at',)


class ReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('pk',
                  'name',
                  'created_at',
                  'room',
                  'start_at',
                  'end_at',)

        read_only_fields = ('created_at',)

    def create(self, validated_data):
        result, message = checkReservationData(validated_data)
        if result:
            return Reservation.objects.create(**validated_data)
        else:
            raise serializers.ValidationError(f"message: {message}")
