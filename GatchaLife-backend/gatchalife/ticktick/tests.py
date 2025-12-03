import json
from unittest.mock import patch
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from gatchalife.gamification.models import Player
from gatchalife.ticktick.models import ProcessedTask

class ZapierWebhookTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/ticktick/webhook/'
        self.user = User.objects.create(username='Player1')
        self.player = Player.objects.create(user=self.user)

    def test_missing_id(self):
        """Test that missing ID returns 400"""
        payload = {'data': json.dumps({'task_name': 'No ID Task'})}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_task(self):
        """Test that duplicate tasks are handled gracefully"""
        task_id = 'duplicate_task_1'
        ProcessedTask.objects.create(task_id=task_id, task_title='Old Task')
        
        payload = {'data': json.dumps({'id': task_id, 'task_name': 'New Task'})}
        response = self.client.post(self.url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'already_processed')
        # Ensure player stats didn't change
        self.player.refresh_from_db()
        self.assertEqual(self.player.xp, 0)

    @patch('random.randint')
    @patch('random.random')
    def test_basic_task_processing(self, mock_random, mock_randint):
        """Test processing a basic task (First ever task)"""
        # Mock randoms for deterministic results
        mock_randint.return_value = 20 # Base currency
        mock_random.return_value = 0.5 # No crit (> 0.1)

        # Ensure player is fresh
        self.player.last_activity_date = None
        self.player.current_streak = 0
        self.player.save()

        task_id = 'basic_task_1'
        payload = {'data': json.dumps({'id': task_id, 'task_name': 'Basic Task'})}
        
        response = self.client.post(self.url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify Player Stats
        self.player.refresh_from_db()
        # Calculation:
        # Base: 20
        # Difficulty: 1.0 (Easy)
        # Streak: 1.05 (1 * 0.05 + 1) -> The view sets streak=1 for first task
        # Crit: 1.0
        # Daily Bonus: 100 (First ever task)
        # Total: (20 * 1.0 * 1.05 * 1.0) + 100 = 21 + 100 = 121
        
        self.assertEqual(self.player.gatcha_coins, 121)
        self.assertEqual(self.player.xp, 60)
        self.assertEqual(self.player.current_streak, 1)
        
        # Verify ProcessedTask
        pt = ProcessedTask.objects.get(task_id=task_id)
        self.assertEqual(pt.coin_gain, 121)
        self.assertEqual(pt.xp_gain, 60)
        self.assertEqual(pt.difficulty, 'easy')
        self.assertFalse(pt.is_crit)

    @patch('random.randint')
    @patch('random.random')
    def test_difficulty_multipliers(self, mock_random, mock_randint):
        """Test different difficulty tags"""
        mock_randint.return_value = 20
        mock_random.return_value = 0.5 # No crit
        
        # Set streak to 1 so multiplier is 1.05
        self.player.current_streak = 1
        self.player.last_activity_date = timezone.now()
        self.player.save()

        difficulties = [
            ('difficulty/medium', 'medium', 1.5),
            ('difficulty/hard', 'hard', 2.0),
            ('difficulty/extreme', 'extreme', 3.0),
        ]

        for i, (tag, expected_diff, mult) in enumerate(difficulties):
            task_id = f'diff_task_{i}'
            payload = {'data': json.dumps({
                'id': task_id, 
                'task_name': f'Task {expected_diff}',
                'tags': [tag]
            })}
            
            # Reset player coins for easier assertion
            self.player.gatcha_coins = 0
            self.player.save()
            
            self.client.post(self.url, payload, format='json')
            
            pt = ProcessedTask.objects.get(task_id=task_id)
            self.assertEqual(pt.difficulty, expected_diff)
            
            # Calc: (20 * mult * 1.05 * 1.0) + 0 (no daily bonus)
            expected_coins = int(20 * mult * 1.05)
            self.assertEqual(pt.coin_gain, expected_coins)

    @patch('random.randint')
    @patch('random.random')
    def test_crit_mechanic(self, mock_random, mock_randint):
        """Test critical success (10% chance -> 2x multiplier)"""
        mock_randint.return_value = 20
        mock_random.return_value = 0.05 # Crit! (< 0.1)
        
        # Set streak to 1 so multiplier is 1.05
        self.player.current_streak = 1
        self.player.last_activity_date = timezone.now()
        self.player.save()
        
        task_id = 'crit_task'
        payload = {'data': json.dumps({'id': task_id, 'task_name': 'Crit Task'})}
        
        self.client.post(self.url, payload, format='json')
        
        pt = ProcessedTask.objects.get(task_id=task_id)
        self.assertTrue(pt.is_crit)
        self.assertEqual(pt.crit_multiplier, 2.0)
        
        # Calc: (20 * 1.0 * 1.05 * 2.0) = 42
        self.assertEqual(pt.coin_gain, 42)

    def test_streak_logic(self):
        """Test streak increment and reset"""
        from datetime import datetime, timezone as dt_timezone
        
        # 1. Day 1
        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = datetime(2023, 1, 1, 12, 0, 0, tzinfo=dt_timezone.utc)
            self.player.last_activity_date = None
            self.player.current_streak = 0
            self.player.save()
            
            # Process task
            self.client.post(self.url, {'data': json.dumps({'id': 'day1', 'task_name': 'T1'})}, format='json')
            self.player.refresh_from_db()
            self.assertEqual(self.player.current_streak, 1)

        # 2. Day 2 (Consecutive)
        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = datetime(2023, 1, 2, 12, 0, 0, tzinfo=dt_timezone.utc)
            
            self.client.post(self.url, {'data': json.dumps({'id': 'day2', 'task_name': 'T2'})}, format='json')
            self.player.refresh_from_db()
            self.assertEqual(self.player.current_streak, 2)

        # 3. Day 4 (Gap of 1 day) -> Reset
        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = datetime(2023, 1, 4, 12, 0, 0, tzinfo=dt_timezone.utc)
            
            self.client.post(self.url, {'data': json.dumps({'id': 'day4', 'task_name': 'T4'})}, format='json')
            self.player.refresh_from_db()
            self.assertEqual(self.player.current_streak, 1)

    @patch('random.randint')
    @patch('random.random')
    def test_level_up(self, mock_random, mock_randint):
        """Test leveling up when XP threshold is reached"""
        mock_randint.return_value = 1000 # Massive base reward to force level up
        mock_random.return_value = 0.5
        
        self.player.level = 1
        self.player.xp = 0
        self.player.save()
        
        # XP needed for lvl 1 is 100
        # Reward will be huge
        
        self.client.post(self.url, {'data': json.dumps({'id': 'lvl_task', 'task_name': 'Big Task'})}, format='json')
        
        self.player.refresh_from_db()
        self.assertGreater(self.player.level, 1)
        # Check if bonus coins were added (50 per level)
        # We can't easily check exact coins without calculating the loop, but we can check it's high
        self.assertGreater(self.player.gatcha_coins, 1000)


class TickTickStatsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='Player1')
        self.player = Player.objects.create(user=self.user)
        
        # Create some processed tasks
        now = timezone.now()
        ProcessedTask.objects.create(task_id='t1', task_title='T1', xp_gain=10, coin_gain=20)
        
        t2 = ProcessedTask.objects.create(task_id='t2', task_title='T2', xp_gain=10, coin_gain=20)
        t2.processed_at = now - timedelta(days=1)
        t2.save()
        
        t3 = ProcessedTask.objects.create(task_id='t3', task_title='T3', xp_gain=10, coin_gain=20)
        t3.processed_at = now - timedelta(days=2)
        t3.save()

    def test_stats_endpoint(self):
        response = self.client.get('/ticktick/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_completed_all_time'], 3)
        self.assertEqual(response.data['rewarded_today'], 1)
        self.assertEqual(len(response.data['recent_activity']), 3)
        
        # Check detailed fields in recent activity
        activity = response.data['recent_activity'][0]
        self.assertIn('xp_gain', activity)
        self.assertIn('coin_gain', activity)
        self.assertIn('difficulty', activity)

    def test_history_endpoint(self):
        response = self.client.get('/ticktick/history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], 3)
        self.assertEqual(len(response.data['results']), 3)
        
        # Test pagination
        response = self.client.get('/ticktick/history/?page=1&page_size=1')
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['pages'], 3)

    def test_progression_endpoint(self):
        response = self.client.get('/ticktick/progression/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return list of daily stats
        self.assertTrue(len(response.data) > 0)
        
        first_entry = response.data[0]
        self.assertIn('date', first_entry)
        self.assertIn('total_xp', first_entry)
        self.assertIn('total_coins', first_entry)

    def test_stats_endpoint_streak(self):
        # Set streak
        self.player.current_streak = 5
        self.player.last_activity_date = timezone.now()
        self.player.save()
        
        response = self.client.get('/ticktick/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_streak'], 5)
        
        # Test broken streak (visually)
        self.player.last_activity_date = timezone.now() - timedelta(days=2)
        self.player.save()
        
        response = self.client.get('/ticktick/stats/')
        self.assertEqual(response.data['current_streak'], 0)
