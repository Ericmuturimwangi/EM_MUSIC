from rest_framework import serializers
from .models import Song, Playlist, PlayHistory

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'artist', 'album', 'duration', 'release_date', 'genre', 'media_file', 'is_favorited']

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return user in obj.favorited_by.all() if user.is_authenticated else False

class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'name', 'songs', 'created_at']

class PlayHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayHistory
        fields  = ['id', 'name', 'songs', 'played_at']