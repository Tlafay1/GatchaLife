from django.contrib import admin
from django.urls import include, path
from rest_framework import routers, permissions
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from gatchalife.character.views import (
    CharacterViewSet,
    CharacterVariantViewSet,
    VariantReferenceImageViewSet,
    SeriesViewSet,
)

from gatchalife.generated_image.views import GeneratedImageViewSet

from gatchalife.style.views import StyleViewSet, RarityViewSet, ThemeViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'series', SeriesViewSet)             # /api/series/
router.register(r'characters', CharacterViewSet)      # /api/characters/
router.register(r'variants', CharacterVariantViewSet) # /api/variants/
router.register(r'variant-images', VariantReferenceImageViewSet) # /api/variant-images/
router.register(r'generated-images', GeneratedImageViewSet) # /api/generated-images/
router.register(r'styles', StyleViewSet)               # /api/styles/
router.register(r'rarities', RarityViewSet)           # /api/rarities/
router.register(r'themes', ThemeViewSet)               # /api/themes/

urlpatterns = [
    path("admin/", admin.site.urls),
    path("gamification/", include("gatchalife.gamification.urls")),
    path("", include(router.urls)),
    path(
        "apidocs.<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "apidocs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
