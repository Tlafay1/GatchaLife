from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, PlayerQuestViewSet, CollectionViewSet, GatchaViewSet

router = DefaultRouter()
router.register(r'player', PlayerViewSet, basename='player')
router.register(r'quests', PlayerQuestViewSet, basename='quests')
router.register(r'collection', CollectionViewSet, basename='collection')
router.register(r'gatcha', GatchaViewSet, basename='gatcha')

urlpatterns = [
    path('', include(router.urls)),
]
