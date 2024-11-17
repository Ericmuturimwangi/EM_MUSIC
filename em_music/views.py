from django.shortcuts import render
from .serializers import PlayListSerializer, SongSerializer
from .models import Song, Playlist
from rest_framework import viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]
    # search features
    search_fields =['title', 'artist', 'album', 'genre']
    ordering_fileds = ['release_date', 'title', 'artist']

class PlayListViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlayListSerializer
    permission_classes = [permissions.IsAuthenticated]
    # search features
    search_fileds = ['name','songs__title' ]
    ordering_fields = ['created_at', 'name']


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SongReccomendationView(APIView):
    def get(self, request):
        user = request.user
        favorite_songs = Song.objects.filter(favorited_by=user)
        recommendations = Song.objects.exclude(id__in=favorite_songs).order_by('?')[:10]
        serializer = SongSerializer(recommendations, many=True, context={'request':request})
        return Response(serializer.data)