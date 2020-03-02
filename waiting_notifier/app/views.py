from rest_framework import status

from .models import User, ReservationSlot, Reservation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer, ReservationSlotSerializer, ReservationSerializer
from django.conf import settings
from django.http import Http404
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
        reservation_slots = ReservationSlot.objects.all()
        serializer = ReservationSlotSerializer(reservation_slots, many=True)
        return Response(serializer.data)


class ReservationSlotDetail(APIView):

    def get_slot(self, start_time):
        try:
            import datetime
            start_time = datetime.datetime.strptime(start_time, '%Y%m%d%H%M').astimezone(
                datetime.timezone(datetime.timedelta(hours=9), 'JST')
            )
            return ReservationSlot.objects.get(start_time=start_time)
        except ReservationSlot.DoesNotExist:
            raise Http404
        except ValueError:
            raise Http404

    def get_user(self, user_id):
        try:
            return User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, start_time, format=None):
        slot = self.get_slot(start_time)
        serializer = ReservationSlotSerializer(slot)
        return Response(serializer.data)

    def post(self, request, start_time, format=None):
        user_id = request.data.get('userId')
        user = self.get_user(user_id)

        slot = self.get_slot(start_time)

        serializer = ReservationSerializer(
            data={'user': user.user_id, 'reservation_slot': slot.start_time}
        )
        if serializer.is_valid():
            if ReservationSlotSerializer(slot).data['remaining'] and UserSerializer(user).data['user_id']:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data={'message': 'No available slot', 'start_time': slot.start_time}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
