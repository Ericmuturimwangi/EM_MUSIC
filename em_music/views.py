from django.shortcuts import render
from .serializers import PlayListSerializer, SongSerializer, PlayHistorySerializer
from .models import Song, Playlist, PlayHistory, Track
from rest_framework import viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework import status
class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]
    # search features
    search_fields =['title', 'artist', 'album', 'genre']
    ordering_fileds = ['release_date', 'title', 'artist']


    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        song = self.get_object()
        user = request.user
        if user in song.favorited_by.all():
            song.favorited_by.remove(user)
            return Response({'status': 'removed from favorites'})
        else:
            song.favorited_by.add(user)
            return Response({'status': 'added to favorites'})

class PlayListViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlayListSerializer
    permission_classes = [permissions.IsAuthenticated]
    # search features
    search_fileds = ['name','songs__title' ]
    ordering_fields = ['created_at', 'name']


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PlayHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = PlayHistorySerializer


    def get_queryset(self):
        return PlayHistory.objects.filter(user=self.request.user)


class SongReccomendationView(APIView):
    def get(self, request):
        user = request.user
        favorite_songs = Song.objects.filter(favorited_by=user)
        recommendations = Song.objects.exclude(id__in=favorite_songs).order_by('?')[:10]
        serializer = SongSerializer(recommendations, many=True, context={'request':request})
        return Response(serializer.data)
    

class TrackPlayView(APIView):
    def get(self, request, track_id):
        try:
            track = Track.objects.get(id=track_id)
            track.increment_play_count()
            return JsonResponse({
                'track_id': track.id,
                'title': track.title,
                'artist': track.artist,
                'album': track.album,
                'plays': track.plays,
                'release_date': track.release_date,
                'duration': track.duration,
                'genre': track.genre,
            })
        except Track.DoesNotExist:
            return JsonResponse({'error': 'Track not found'})
        
class TopTracksView(APIView):
    def get(self, request):

        top_track = Track.objects.order_by('-plays')[:10]
        data= [{
            'track_id': track.id,
            'title': track.title,
            'artist': track.artist,
            'album': track.album,
            'plays': track.plays,
            'release_date': track.release_date,
            'duration': track.duration,
            'genre': track.genre
        }for track in top_track]

        return JsonResponse({'top_track': data})
    

class TrackDetailView(APIView):
    def get(self, request, track_id):
        try:
            track = Track.objects.get(id=track_id)
            return JsonResponse({
                'track_id': track.id,
                'title': track.title,
                'artist': track.artist,
                'album': track.album,
                'plays': track.plays,
                'release_date': track.release_date,
                'duration': track.duration,
                'genre': track.genre,
                'cover_art_url': track.cover_art.url if track.cover_art else None,
                'description': track.description,
                'lyrics': track.lyrics
            })
        except Track.DoesNotExist:
            return Response({'error': 'Track Not Found'}, sstatus=status.HTTP_404_NOT_FOUND)
        