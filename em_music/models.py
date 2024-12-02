from django.db import models
from django.contrib.auth.models import User


class Song (models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255, blank=True)
    duration = models.DurationField()
    release_date = models.DateField()
    genre = models.CharField(max_length=255, blank=True)
    media_file = models.FileField(upload_to='songs/media', blank=True, null=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_songs', blank=True)

    def __str__(self):
        return f"{self.title} {self.artist}"
    
class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    name = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song, related_name="playlists")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username}'s Playlist - {self.name}"


class PlayHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    played_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} played {self.song.title} at {self.played_at}"
    
class Track(models.Model):
    song = models.OneToOneField(Song, related_name="track", on_delete=models.CASCADE)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    file_url = models.URLField()
    plays = models.PositiveIntegerField(default=0)
    duration = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    lyrics = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.title} by {self.artist}"
    
    def increment_play_count(self):
        self.plays +=1
        self.save()
        