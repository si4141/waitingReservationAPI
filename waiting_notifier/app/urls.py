from django.urls import path
from . import views

urlpatterns = [
    path('linehooks/', views.accept_line_web_hook),
    path('reservationSlot/', views.ReservationSlotList.as_view()),
    path('reservationSlot/<str:start_time>/', views.ReservationSlotDetail.as_view())
]
