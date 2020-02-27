from django.http import JsonResponse
import django_filters
from rest_framework import viewsets, filters
from rest_framework.parsers import JSONParser

from .models import Reservation
from .serializer import UserSerializer
from django.conf import settings
import requests


def accept_line_web_hook(request):
    if request.mothod == 'POST':
        data = JSONParser().parse(request)
        event_source = data.get('source')
        if event_source is None:
            raise NotImplementedError()

        event_type = data.get('type')
        if event_type == 'follow':
            source_type = event_source.get('type')
            if source_type != 'user':
                raise ValueError()
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
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        raise NotImplementedError()