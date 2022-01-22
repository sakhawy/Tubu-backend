from django.urls import include, path
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

from api import views

router = routers.DefaultRouter()
router.register(r'playlists', views.PlaylistViewSet)
router.register(r'videos', views.VideoViewSet)

urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)