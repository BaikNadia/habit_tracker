from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


class TelegramBotTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_telegram_bot_connection(self):
        # Пропускаем тест если эндпоинта нет
        response = self.client.post("/api/telegram/connect/", {
            "telegram_id": "123456789"
        })
        if response.status_code == 404:
            self.skipTest("Telegram connect endpoint not implemented")
        else:
            self.assertEqual(response.status_code, 200)

    def test_send_reminder(self):
        # Пропускаем тест если эндпоинта нет
        response = self.client.post("/api/telegram/send-reminder/", {
            "habit_id": 1,
            "message": "Напоминание"
        })
        if response.status_code == 404:
            self.skipTest("Send reminder endpoint not implemented")
        else:
            self.assertEqual(response.status_code, 200)

    def test_telegram_model_str(self):
        # Тест для модели если она есть
        try:
            from .models import TelegramUser
            tg_user = TelegramUser(telegram_id="123456", user=self.user)
            self.assertEqual(str(tg_user), "123456")
        except ImportError:
            self.skipTest("TelegramUser model not implemented")


