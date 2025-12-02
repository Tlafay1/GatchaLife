from django.urls import path
from .views import TickTickViewSet, zapier_webhook

urlpatterns = [
    path('stats/', TickTickViewSet.as_view({'get': 'stats'}), name='ticktick-stats'),
    path('history/', TickTickViewSet.as_view({'get': 'history'}), name='ticktick-history'),
    path('progression/', TickTickViewSet.as_view({'get': 'progression'}), name='ticktick-progression'),
    path('webhook/', zapier_webhook, name='zapier-webhook'),
]
