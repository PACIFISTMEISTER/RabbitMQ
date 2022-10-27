from django.urls import path
from .views import URLView

urlpatterns = [
    path('', URLView.as_view())
]
