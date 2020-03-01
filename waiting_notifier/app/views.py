from rest_framework import status

from .models import User, ReservationSlot
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer, ReservationSlotSerializer
from django.conf import settings
import requests
from logging import getLogger
logger = getLogger(__name__)


@api_view(['POST'])
def accept_line_web_hook(request):
    logger.info('Call view')
    if request.method == 'POST':
        logger.debug(f'{request.data}')
        data = request.data.get('events')
        if data:
            data = data[0]
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        event_source = data.get('source')
        if event_source is None:
            return Response(status.HTTP_400_BAD_REQUEST)

        event_type = data.get('type')
        logger.debug(f'event_type: {event_type}')
        if event_type == 'follow':
            logger.debug('follow event')

            source_type = event_source.get('type')
            logger.debug(f'source_type: {source_type}')
            if source_type != 'user':
                return Response(status.HTTP_400_BAD_REQUEST)
            user_id = event_source.get('userId')
            response = requests.get(
                f'https://api.line.me/v2/bot/profile/{user_id}',
                headers={'Authorization': f'Bearer {settings.LINE_ACCESS_TOKEN}'}
            )
            user_data = response.json()
            display_name = user_data.get('displayName')
            serializer = UserSerializer(
                data={'user_id': user_id, 'display_name': display_name}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                try:
                    user = User.objects.get(pk=user_id)
                    return Response(
                        {'message': f'Passed User already created at {user.created_at:%Y-%m-%d %H:%M:%S}'},
                        status=status.HTTP_200_OK
                    )
                except User.DoesNotExist:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReservationSlotList(APIView):

    def get(self, request, format=None):
        reservation_slots = ReservationSlot.objects.filter(available_slot__gt=0)
        serializer = ReservationSlotSerializer(reservation_slots, many=True)
        return Response(serializer.data)
