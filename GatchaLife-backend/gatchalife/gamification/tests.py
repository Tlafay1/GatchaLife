from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from .models import Player, Card, UserCard
from gatchalife.character.models import Series, Character, CharacterVariant
from gatchalife.style.models import Rarity, Style, Theme

class GatchaRollTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='Player1')
        self.player = Player.objects.create(user=self.user)
        self.player.gatcha_coins = 1000 # Give plenty of coins
        self.player.save()

        # Setup Game Data
        self.rarity_common, _ = Rarity.objects.get_or_create(name="Common", defaults={'min_roll_threshold': 0})
        self.rarity_rare, _ = Rarity.objects.get_or_create(name="Rare", defaults={'min_roll_threshold': 80})
        
        self.series = Series.objects.create(name="Series 1")
        self.character = Character.objects.create(name="Char 1", series=self.series)
        self.variant = CharacterVariant.objects.create(name="Base", character=self.character)
        
        self.style = Style.objects.create(name="Anime", rarity=self.rarity_common)
        self.theme = Theme.objects.create(name="Forest")

    @patch('gatchalife.gamification.views.generate_image')
    def test_roll_success(self, mock_generate):
        """Test a successful roll"""
        response = self.client.post('/gamification/gatcha/roll/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('drop', response.data)
        self.assertIn('roll_info', response.data)
        
        # Check coins deducted
        self.player.refresh_from_db()
        self.assertEqual(self.player.gatcha_coins, 900) # 1000 - 100
        
        # Check card created
        self.assertEqual(UserCard.objects.count(), 1)
        self.assertEqual(Card.objects.count(), 1)

    def test_roll_insufficient_funds(self):
        self.player.gatcha_coins = 50
        self.player.save()
        
        response = self.client.post('/gamification/gatcha/roll/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Not enough coins')

    @patch('gatchalife.gamification.views.generate_image')
    @patch('random.randint')
    def test_roll_rarity_selection(self, mock_randint, mock_generate):
        """Test that high roll selects Rare"""
        mock_randint.return_value = 90 # Above Rare threshold (80)
        
        # Need a style for Rare otherwise fallback logic kicks in
        Style.objects.create(name="Rare Style", rarity=self.rarity_rare)
        
        response = self.client.post('/gamification/gatcha/roll/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['roll_info']['rarity'], 'Rare')

    @patch('gatchalife.gamification.views.generate_image')
    @patch('random.choice')
    @patch('random.randint')
    def test_duplicate_card_stacking(self, mock_randint, mock_choice, mock_generate):
        """Test that getting the same card increases count"""
        mock_randint.return_value = 1 # Force Common Rarity
        mock_choice.side_effect = lambda x: x[0] # Always pick first item
        
        # First Roll
        self.client.post('/gamification/gatcha/roll/')
        self.assertEqual(UserCard.objects.first().count, 1)
        
        # Second Roll
        self.client.post('/gamification/gatcha/roll/')
        self.assertEqual(UserCard.objects.first().count, 2)
        self.assertEqual(UserCard.objects.count(), 1) # Still only 1 entry

class PlayerCollectionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='Player1')
        self.player = Player.objects.create(user=self.user)
        
        # Create some cards
        self.rarity, _ = Rarity.objects.get_or_create(name="Common", defaults={'min_roll_threshold': 0})
        self.series = Series.objects.create(name="S1")
        self.char = Character.objects.create(name="C1", series=self.series)
        self.var = CharacterVariant.objects.create(name="V1", character=self.char)
        self.style = Style.objects.create(name="St1", rarity=self.rarity)
        self.theme = Theme.objects.create(name="Th1")
        
        self.card = Card.objects.create(
            character_variant=self.var, rarity=self.rarity, style=self.style, theme=self.theme
        )
        UserCard.objects.create(player=self.player, card=self.card, count=5)

    def test_collection_list(self):
        response = self.client.get('/gamification/collection/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['count'], 5)
        self.assertEqual(response.data[0]['card']['character_name'], "C1")
