from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import Play, Performance, TheatreHall, Genre, Actor
from theatre.serializers import PlayListSerializer

PLAY_URL = reverse("theatre:play-list")
PERFORMANCE_URL = reverse("theatre:performance-list")


def sample_play(**params):
    defaults = {
        "title": "Sample movie",
        "description": "Sample description",
    }
    defaults.update(params)

    return Play.objects.create(**defaults)


def sample_genre(**params):
    defaults = {
        "name": "Drama",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


def sample_actor(**params):
    defaults = {"first_name": "George", "last_name": "Clooney"}
    defaults.update(params)

    return Actor.objects.create(**defaults)


def sample_movie_session(**params):
    theatre_hall = TheatreHall.objects.create(
        name="Blue", rows=20, seats_in_row=20
    )

    defaults = {
        "showtime": "2022-06-02 14:00:00",
        "play": None,
        "theatre_hall": theatre_hall,
    }
    defaults.update(params)

    return Performance.objects.create(**defaults)


def detail_url(play_id):
    return reverse("theatre:play-detail", args=[play_id])


class UnauthenticatedPlayApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLAY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlayApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.play1 = sample_play(title="test_play1")
        self.play2 = sample_play(title="test_play2")
        self.genre1 = Genre.objects.create(name="test_genre1")
        self.genre2 = Genre.objects.create(name="test_genre2")
        self.client.force_authenticate(self.user)

    def test_list_plays(self):
        sample_play()
        movie_with_genre = sample_play()

        movie_with_genre.genres.add(self.genre1, self.genre2)

        response = self.client.get(PLAY_URL)
        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_plays_by_title(self):
        response = self.client.get(PLAY_URL, {"title": "test_play1"})

        serializer1 = PlayListSerializer(self.play1)
        serializer2 = PlayListSerializer(self.play1)

        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    def test_filter_plays_by_genres(self):
        self.play1.genres.add(self.genre1)
        self.play2.genres.add(self.genre2)

        response = self.client.get(PLAY_URL, {"genres": f"{self.genre1.id}"})

        serializer1 = PlayListSerializer(self.play1)
        serializer2 = PlayListSerializer(self.play2)

        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    def test_filter_plays_by_actors(self):
        actor1 = Actor.objects.create(first_name="test_name1", last_name="test_surname1")
        actor2 = Actor.objects.create(first_name="test_name2", last_name="test_surname2")

        self.play1.actors.add(actor1)
        self.play2.actors.add(actor2)

        response = self.client.get(PLAY_URL, {"actors": f"{actor1.id}"})

        serializer1 = PlayListSerializer(self.play1)
        serializer2 = PlayListSerializer(self.play2)

        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    def test_create_play_forbidden(self):
        payload = {
            "title": "Movie",
            "description": "description",
        }

        response = self.client.post(PLAY_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminPlayApi(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
            is_staff=True
        )
        self.play = sample_play()
        self.url = detail_url(self.play.id)
        self.client.force_authenticate(self.user)

    def test_create_play_with_genres_and_actors_allowed(self):
        genre = Genre.objects.create(name="test_genre")
        actor = Actor.objects.create(
            first_name="test_first_name",
            last_name="test_last_name"
        )
        payload = {
            "title": "title",
            "description": "description",
            "genres": [genre.id],
            "actors": [actor.id],
        }
        response = self.client.post(PLAY_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_play_without_genres_and_actors_not_allowed(self):
        payload = {
            "title": "title",
            "description": "description",
        }
        response = self.client.post(PLAY_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_play_not_allowed(self):
        response = self.client.put(self.url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_partial_update_play_not_allowed(self):
        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_play_not_allowed(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
