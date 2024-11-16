from rest_framework import serializers
from .models import Song, Playlist

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'artist', 'album', 'duration', 'release_date', 'genre', 'media_file']

class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'name', 'songs', 'created_at']

