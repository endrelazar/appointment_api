from rest_framework import generics, permissions, status
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.response import Response
import logging

logger = logging.getLogger('appointments')

class BookingListCreateAPI(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    def get_queryset(self):
        return Booking.objects.filter(client=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
           
            slot_id = request.data.get('timeslot')
            if not slot_id:
                logger.warning(f"API: User {request.user.username} tried to book without timeslot.")
                return Response({'error': 'Missing time identifier'}, status=status.HTTP_400_BAD_REQUEST)
            logger.info(f"API:User {request.user.username} is attempting to create a booking for slot {slot_id}.")
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"API: Error creating booking: {str(e)}")
            return Response({'error': f'An error occured: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)