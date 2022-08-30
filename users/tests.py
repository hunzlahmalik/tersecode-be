from django.contrib.auth import get_user_model
from django.test import TestCase, Client


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@users.com", password="foo")
        self.assertEqual(user.email, "normal@users.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@users.com", password="foo"
        )
        self.assertEqual(admin_user.email, "super@users.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@users.com", password="foo", is_superuser=False
            )


class TestUserModel(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        User.objects.create(username="test", password="test", email="test@email.com")
        User.objects.create(username="test1", password="test2", email="test1@email.com")
        User.objects.create(username="test2", password="test2", email="test2@email.com")

    def test_user_count(self):
        self.assertEqual(User.objects.count(), 3)

    def test_user_get(self):
        User = get_user_model()

        user = User.objects.get(username="test")
        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "test@email.com")
        user = User.objects.get(email="test1@email.com")
        self.assertEqual(user.username, "test1")
        self.assertEqual(user.email, "test1@email.com")

    def test_user_filter(self):
        User = get_user_model()

        users = User.objects.filter(username="test")
        self.assertEqual(users.count(), 1)
        self.assertEqual(users[0].username, "test")
        self.assertEqual(users[0].email, "test@email.com")
        users = User.objects.filter(email="test1@email.com")
        self.assertEqual(users.count(), 1)
        self.assertEqual(users[0].username, "test1")
        self.assertEqual(users[0].email, "test1@email.com")

    def test_user_exists(self):
        User = get_user_model()

        self.assertTrue(User.objects.filter(username="test").exists())
        self.assertTrue(User.objects.filter(username="test1").exists())
        self.assertTrue(User.objects.filter(username="test2").exists())
        self.assertFalse(User.objects.filter(username="test3").exists())

    def test_try_to_create_duplicate_user(self):
        User = get_user_model()

        with self.assertRaises(Exception):
            User.objects.create(username="test", password="test")
        with self.assertRaises(Exception):
            User.objects.create(
                username="test", password="test", email="random@email.com"
            )
        with self.assertRaises(Exception):
            User.objects.create(
                username="random", password="test", email="test@email.com"
            )


class TestAccountViews(TestCase):
    c = Client()

    def setUp(self) -> None:
        User = get_user_model()

        # create 3 users
        User.objects.create(username="test", password="test")
        User.objects.create(username="test1", password="test1")
        User.objects.create(username="test2", password="test2")

    def test_login_view(self):
        User = get_user_model()

        response = self.c.get("/users/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")
