from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, PlayerQuestViewSet, CollectionViewSet, GatchaViewSet
from .views_companion import CompanionViewSet, set_companion_state

router = DefaultRouter()
router.register(r'player', PlayerViewSet, basename='player')
router.register(r'quests', PlayerQuestViewSet, basename='quests')
router.register(r'collection', CollectionViewSet, basename='collection')
router.register(r'gatcha', GatchaViewSet, basename='gatcha')
router.register(r"companion", CompanionViewSet, basename="companion")

urlpatterns = [
    path("", include(router.urls)),
    path("admin/companion/set_state/", set_companion_state, name="set_companion_state"),
]
