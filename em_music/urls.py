from django.urls import path, include
from .views import PlayListViewSet, SongViewSet
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'songs', SongViewSet)
router.register(r'playlists', PlayListViewSet)


urlpatterns = [
    path('api/', include(router.urls)),


] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

