from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Song, Playlist
from datetime import timedelta

# creating sample data for testing
class MusicAppTests(APITestCase):

    def setUp(self):
        # sample user
        self.user = User.objects.create_user(username='testuser', password='password')

        # sample song
        self.song = Song.objects.create(
            title="Song Title",
            artist="Artist Name",
            album="Album Name",
            release_date="2024-01-01",
            duration=timedelta(minutes=3, seconds=45)  
        )

        # create a smple playlist

        self.playlist = Playlist.objects.create(
            user = self.user,
            name ="My playlist"
        )
        self.playlist.songs.add(self.song)

        # url for testing

        self.song_url = reverse('song-list')
        self.playlist_url = reverse('playlist-list')

    def test_create_song(self):
        """ TESTING THE CREATING OF A SONG """
        data = {
            "title": "New Song",
            "artist": "New Artist",
            "album": "New ALbum",
            "genre": "ROck",
            "duration": "00:04:00",
            "release_date":"2024-01-01"
        }
        response =self.client.post(self.song_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Song.objects.count(), 2)


    def test_list_song(self):
        response = self.client.get(self.song_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_playlist(self):
        data ={
            "name": "New PLaylist",
            "songs":[self.song.id]

        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.playlist_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Playlist.objects.count(), 2)

    def test_list_playlist(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.playlist_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_song_by_title(self):
        # Make the request with authorization
        url = '/api/songs/search/'
        response = self.client.get(url, {'title': 'Song Title'}, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Assert that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ordering_songs(self):
        # Make the request with the authorization token
        url = '/api/songs/order/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Assert the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_ordering_playlist(self):
        response = self.client.get(self.playlist_url, {'ordering': '-created_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)