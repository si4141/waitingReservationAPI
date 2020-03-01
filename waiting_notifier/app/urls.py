from django.urls import path
from . import views

urlpatterns = [
    path('linehooks/', views.accept_line_web_hook),
    path('reservationSlot/', views.ReservationSlotList.as_view())
]
