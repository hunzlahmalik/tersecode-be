from django.test import TestCase, Client
from .models import User
from .constants import AVATAR_STORAGE_PATH


class TestAccountModel(TestCase):
    def setUp(self) -> None:
        User.objects.create(username='test', password='test',
                            email='test@email.com')
        User.objects.create(username='test1', password='test2',
                            email='test1@email.com')
        User.objects.create(username='test2', password='test2',
                            email='test2@email.com')

    def test_user_count(self):
        self.assertEqual(User.objects.count(), 3)

    def test_user_get(self):
        user = User.objects.get(username='test')
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@email.com')
        user = User.objects.get(email='test1@email.com')
        self.assertEqual(user.username, 'test1')
        self.assertEqual(user.email, 'test1@email.com')

    def test_user_filter(self):
        users = User.objects.filter(username='test')
        self.assertEqual(users.count(), 1)
        self.assertEqual(users[0].username, 'test')
        self.assertEqual(users[0].email, 'test@email.com')
        users = User.objects.filter(email='test1@email.com')
        self.assertEqual(users.count(), 1)
        self.assertEqual(users[0].username, 'test1')
        self.assertEqual(users[0].email, 'test1@email.com')

    def test_user_exists(self):
        self.assertTrue(User.objects.filter(username='test').exists())
        self.assertTrue(User.objects.filter(username='test1').exists())
        self.assertTrue(User.objects.filter(username='test2').exists())
        self.assertFalse(User.objects.filter(username='test3').exists())

    def test_try_to_create_duplicate_user(self):
        with self.assertRaises(Exception):
            User.objects.create(username='test', password='test')
        with self.assertRaises(Exception):
            User.objects.create(
                username='test', password='test', email='random@email.com')
        with self.assertRaises(Exception):
            User.objects.create(username='random',
                                password='test', email='test@email.com')


class TestAccountViews(TestCase):
    c = Client()

    def setUp(self) -> None:
        # create 3 users
        User.objects.create(username='test', password='test')
        User.objects.create(username='test1', password='test1')
        User.objects.create(username='test2', password='test2')

    def test_login_view(self):
        response = self.c.get('/account/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')
