from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Habit

User = get_user_model()


class HabitTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        response = self.client.post(
            "/api/habits/my/",
            {
                "place": "дом",
                "time": "08:00",
                "action": "выпить стакан воды",
                "is_pleasant": False,
                "periodicity": 1,
                "duration": 60,
                "is_public": False,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 1)
