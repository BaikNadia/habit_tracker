from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Habit

User = get_user_model()


class HabitTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="123"
        )
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
        self.assertEqual(Habit.objects.first().user, self.user)

    def test_get_habits_list(self):
        # Создаем привычку сначала
        Habit.objects.create(
            user=self.user,
            place="дом",
            time="08:00",
            action="выпить стакан воды",
            is_pleasant=False,
            periodicity=1,
            duration=60,
            is_public=False
        )

        response = self.client.get("/api/habits/my/")
        self.assertEqual(response.status_code, 200)
        # Проверяем что в ответе есть данные
        self.assertTrue(len(response.data) >= 1)

    def test_get_public_habits(self):
        # Создаем публичную привычку
        habit = Habit.objects.create(
            user=self.user,
            place="парк",
            time="09:00",
            action="пробежка",
            is_pleasant=True,
            periodicity=1,
            duration=120,
            is_public=True
        )

        response = self.client.get("/api/habits/public/")
        self.assertEqual(response.status_code, 200)
        # Проверяем что привычка есть в ответе
        self.assertTrue(any(item['id'] == habit.id for item in response.data))

    def test_update_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place="дом",
            time="08:00",
            action="выпить стакан воды",
            is_pleasant=False,
            periodicity=1,
            duration=60,
            is_public=False
        )

        response = self.client.patch(
            f"/api/habits/my/{habit.id}/",
            {"action": "выпить два стакана воды"}
        )
        self.assertEqual(response.status_code, 200)
        habit.refresh_from_db()
        self.assertEqual(habit.action, "выпить два стакана воды")

    def test_delete_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place="дом",
            time="08:00",
            action="выпить стакан воды",
            is_pleasant=False,
            periodicity=1,
            duration=60,
            is_public=False
        )

        response = self.client.delete(f"/api/habits/my/{habit.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Habit.objects.count(), 0)

    def test_habit_validation(self):
        # Тест на валидацию (длительность > 120 секунд)
        response = self.client.post(
            "/api/habits/my/",  # Правильный URL
            {
                "place": "дом",
                "time": "08:00",
                "action": "выпить стакан воды",
                "is_pleasant": False,
                "periodicity": 1,
                "duration": 130,  # больше 120 секунд
                "is_public": False,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_pleasant_habit_no_reward(self):
        # Тест на приятную привычку без вознаграждения
        response = self.client.post(
            "/api/habits/my/",
            {
                "place": "дом",
                "time": "08:00",
                "action": "медитация",
                "is_pleasant": True,
                "periodicity": 1,
                "duration": 60,
                "is_public": False,
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_habit_periodicity_validation(self):
        # Тест на периодичность (1-7 дней)
        response = self.client.post(
            "/api/habits/my/",
            {
                "place": "дом",
                "time": "08:00",
                "action": "выпить стакан воды",
                "is_pleasant": False,
                "periodicity": 8,  # больше 7
                "duration": 60,
                "is_public": False,
            },
        )
        self.assertEqual(response.status_code, 400)


class HabitModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="123"
        )

    def test_habit_creation(self):
        habit = Habit.objects.create(
            user=self.user,
            place="дом",
            time="08:00",
            action="выпить стакан воды",
            is_pleasant=False,
            periodicity=1,
            duration=60,
            is_public=False
        )
        self.assertEqual(str(habit), "выпить стакан воды")
        self.assertEqual(habit.user.email, "test@example.com")

    def test_habit_duration_validation(self):
        """Тест на валидацию длительности"""
        from django.core.exceptions import ValidationError

        habit = Habit(
            user=self.user,
            place="дом",
            time="08:00",
            action="тест",
            is_pleasant=False,
            periodicity=1,
            duration=130,  # больше 120 секунд
            is_public=False
        )

        try:
            habit.full_clean()
            self.fail("Should have failed validation")
        except ValidationError:
            pass  # Ожидаемое поведение

    def test_habit_periodicity_validation(self):
        """Тест на валидацию периодичности"""
        from django.core.exceptions import ValidationError

        habit = Habit(
            user=self.user,
            place="дом",
            time="08:00",
            action="тест",
            is_pleasant=False,
            periodicity=8,  # больше 7
            duration=60,
            is_public=False
        )

        try:
            habit.full_clean()
            self.fail("Should have failed validation")
        except ValidationError:
            pass  # Ожидаемое поведение
