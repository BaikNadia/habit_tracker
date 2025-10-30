from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class UserTestCase(APITestCase):
    def test_user_registration(self):
        """Тест регистрации пользователя"""
        url = '/api/users/register/'
        data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123'
        }

        response = self.client.post(url, data, format='json')
        # Может возвращать 201 или 200 в зависимости от реализации
        self.assertIn(response.status_code, [200, 201])

        # Проверяем, что пользователь создан
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_user_login(self):
        """Тест входа пользователя"""
        # Сначала создаем пользователя
        user = User.objects.create_user(
            email='login_test@example.com',
            password='testpass123'
        )

        url = '/api/users/token/'
        data = {
            'email': 'login_test@example.com',
            'password': 'testpass123'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        """Тест обновления токена"""
        # Сначала получаем refresh token
        user = User.objects.create_user(
            email='refresh_test@example.com',
            password='testpass123'
        )

        # Получаем токены
        auth_url = '/api/users/token/'
        auth_data = {
            'email': 'refresh_test@example.com',
            'password': 'testpass123'
        }
        auth_response = self.client.post(auth_url, auth_data, format='json')
        refresh_token = auth_response.data['refresh']

        # Обновляем токен
        refresh_url = '/api/users/token/refresh/'
        refresh_data = {
            'refresh': refresh_token
        }
        refresh_response = self.client.post(refresh_url, refresh_data, format='json')
        self.assertEqual(refresh_response.status_code, 200)
        self.assertIn('access', refresh_response.data)

    def test_user_str_method(self):
        """Тест строкового представления пользователя"""
        user = User.objects.create_user(
            email='str_test@example.com',
            password='testpass123'
        )
        self.assertEqual(str(user), 'str_test@example.com')


class UserModelTestCase(APITestCase):
    def test_create_user(self):
        """Тест создания обычного пользователя"""
        user = User.objects.create_user(
            email='user@example.com',
            password='password123'
        )
        self.assertEqual(user.email, 'user@example.com')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password('password123'))

    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='admin123'
        )
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_required_fields(self):
        """Тест обязательных полей пользователя"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='password123')
