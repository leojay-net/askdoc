from django.urls import path
from .views import Chat


urlpatterns = [
    path('diagnosis/', Chat.as_view(), name="diagnose-patient"),
]