from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Series, Character, CharacterVariant

class CharacterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.series = Series.objects.create(name="Test Series", description="Desc")
        self.character = Character.objects.create(name="Char 1", series=self.series)
        self.variant = CharacterVariant.objects.create(name="Base", character=self.character)

    def test_list_series(self):
        response = self.client.get('/series/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Test Series")

    def test_create_character(self):
        payload = {
            "name": "Char 2",
            "series": self.series.id,
            "description": "New Char"
        }
        response = self.client.post('/characters/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Character.objects.count(), 2)

    def test_filter_characters_by_series(self):
        series2 = Series.objects.create(name="Series 2")
        Character.objects.create(name="Char 3", series=series2)
        
        response = self.client.get(f'/characters/?series={self.series.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Char 1")

    def test_create_variant(self):
        payload = {
            "name": "Alt Outfit",
            "character": self.character.id
        }
        response = self.client.post('/variants/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CharacterVariant.objects.count(), 2)
