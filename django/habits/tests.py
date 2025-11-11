from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        """Создание тестового пользователя и аутентификация"""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

        # Получаем JWT токен для аутентификации
        auth_url = '/api/users/token/'
        auth_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        auth_response = self.client.post(auth_url, auth_data, format='json')
        token = auth_response.data['access']

        # Устанавливаем заголовок авторизации
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Создаем тестовую привычку
        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="читать книгу",
            duration=120,
            periodicity=1
        )

    def test_create_habit(self):
        """Тест создания привычки"""
        url = '/api/habits/my/'  # Используем endpoint для моих привычек
        data = {
            'place': 'Дом',
            'time': '20:00:00',
            'action': 'медитация',
            'duration': 60,
            'periodicity': 1
        }

        # POST запрос на создание привычки
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 2)

    def test_get_user_habits(self):
        """Тест получения привычек пользователя"""
        url = '/api/habits/my/'  # Endpoint для моих привычек
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Проверяем пагинацию
        if 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['action'], 'читать книгу')

    def test_update_habit(self):
        """Тест обновления привычки"""
        url = f'/api/habits/{self.habit.id}/'  # Endpoint для деталей привычки
        data = {
            'action': 'обновленная привычка',
            'place': 'Офис',
            'time': '15:00:00',
            'duration': 90,
            'periodicity': 2
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        # Обновляем объект из базы
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, 'обновленная привычка')

    def test_delete_habit(self):
        """Тест удаления привычки"""
        url = f'/api/habits/{self.habit.id}/'  # Endpoint для деталей привычки
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())

    def test_get_public_habits(self):
        """Тест получения публичных привычек"""
        # Создаем публичную привычку
        public_habit = Habit.objects.create(
            user=self.user,
            place="Парк",
            time="08:00:00",
            action="утренняя пробежка",
            duration=120,
            periodicity=1,
            is_public=True
        )

        # URL для публичных привычек
        url = '/api/habits/public/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Обрабатываем пагинацию
        if 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data

        # Проверяем, что привычка есть в ответе
        habit_ids = [item['id'] for item in results]
        self.assertIn(public_habit.id, habit_ids)


class HabitModelTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='model_test@example.com',
            password='testpass123'
        )

    def test_habit_creation(self):
        """Тест создания модели привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place="Кухня",
            time="09:00:00",
            action="выпить стакан воды",
            duration=30,
            periodicity=1
        )

        self.assertEqual(str(habit), "выпить стакан воды")

    def test_habit_validators_success(self):
        """Тест успешной валидации привычки"""
        habit = Habit(
            user=self.user,
            place="Дом",
            time="10:00:00",
            action="тестовая привычка",
            duration=120,  # максимально допустимое время
            periodicity=1
        )

        # Должно пройти без ошибок
        try:
            habit.full_clean()
        except Exception as e:
            self.fail(f"Валидация провалилась неожиданно: {e}")

    def test_habit_validators_duration_exceeded(self):
        """Тест валидации превышения времени выполнения"""
        habit = Habit(
            user=self.user,
            place="Дом",
            time="10:00:00",
            action="тест",
            duration=121,  # > 120 секунд
            periodicity=1
        )

        with self.assertRaises(Exception):
            habit.full_clean()

    def test_habit_validators_periodicity_range(self):
        """Тест валидации периодичности"""
        # Слишком маленькая периодичность
        habit_low = Habit(
            user=self.user,
            place="Дом",
            time="10:00:00",
            action="тест",
            duration=60,
            periodicity=0
        )

        with self.assertRaises(Exception):
            habit_low.full_clean()

        # Слишком большая периодичность
        habit_high = Habit(
            user=self.user,
            place="Дом",
            time="10:00:00",
            action="тест",
            duration=60,
            periodicity=8
        )

        with self.assertRaises(Exception):
            habit_high.full_clean()

    def test_pleasant_habit_constraints(self):
        """Тест ограничений для приятной привычки"""
        # Приятная привычка не должна иметь вознаграждения
        habit = Habit(
            user=self.user,
            place="Дом",
            time="10:00:00",
            action="приятная привычка",
            duration=60,
            periodicity=1,
            is_pleasant=True,
            reward="вознаграждение"
        )

        with self.assertRaises(Exception):
            habit.full_clean()

    def test_reward_and_related_habit_constraint(self):
        """Тест ограничения на одновременное указание вознаграждения и связанной привычки"""
        # Создаем приятную привычку для связи
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="10:00:00",
            action="приятная привычка",
            duration=60,
            periodicity=1,
            is_pleasant=True
        )

        # Нельзя одновременно иметь и вознаграждение, и связанную привычку
        habit = Habit(
            user=self.user,
            place="Дом",
            time="10:00:00",
            action="тест",
            duration=60,
            periodicity=1,
            reward="вознаграждение",
            related_habit=pleasant_habit
        )

        with self.assertRaises(Exception):
            habit.full_clean()
