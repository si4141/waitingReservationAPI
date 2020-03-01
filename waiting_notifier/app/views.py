from rest_framework import status

from .models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import UserSerializer
from django.conf import settings
import requests
from logging import getLogger
logger = getLogger(__name__)


@api_view(['POST'])
def accept_line_web_hook(request):
    logger.info('Call view')
    if request.method == 'POST':
        logger.debug(f'{request.data}')
        data = request.data
        event_source = data.get('source')
        if event_source is None:
            return Response(status.HTTP_400_BAD_REQUEST)

        event_type = data.get('type')
        if event_type == 'follow':
            source_type = event_source.get('type')
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
