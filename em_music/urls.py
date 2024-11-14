from django.urls import path, include
from .views import PlayListViewSet, SongViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'songs', SongViewSet)
router.register(r'playlists', PlayListViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]

