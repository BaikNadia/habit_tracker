from django.test import TestCase
from habits.models import Habit
from users.models import User


class TelegramBotTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='telegram_test@example.com',
            password='testpass123',
            telegram_chat_id='123456'
        )

        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="тестовая привычка",
            duration=60,
            periodicity=1
        )

    def test_user_with_telegram_chat_id(self):
        """Тест пользователя с Telegram chat_id"""
        self.assertEqual(self.user.telegram_chat_id, '123456')
        self.assertEqual(self.user.email, 'telegram_test@example.com')

    def test_habit_creation_for_telegram(self):
        """Тест создания привычки для Telegram напоминаний"""
        self.assertEqual(str(self.habit), 'тестовая привычка')
        self.assertEqual(self.habit.user.telegram_chat_id, '123456')
