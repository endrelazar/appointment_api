from rest_framework import serializers
from .models import Booking,TimeSlot

class BookingSerializer(serializers.ModelSerializer):
    def validate_timeslot(self, value):
        # Csak akkor engedjük, ha nincs aktív Booking ehhez a timeslot-hoz
        if Booking.objects.filter(timeslot=value, status='active').exists():
            raise serializers.ValidationError("Ez az időpont már foglalt!")
        return value

    class Meta:
        model = Booking
        fields = ['id', 'timeslot', 'client', 'status']
        read_only_fields = ['client', 'status']

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'