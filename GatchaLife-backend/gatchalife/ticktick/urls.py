from django.urls import path
from .views import TickTickViewSet, zapier_webhook

urlpatterns = [
    path('stats/', TickTickViewSet.as_view({'get': 'stats'}), name='ticktick-stats'),
    path('webhook/', zapier_webhook, name='zapier-webhook'),
]
