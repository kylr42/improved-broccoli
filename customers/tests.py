from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):

    def test_create_user(self):
        user = get_user_model()
        test_user = user.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(test_user.email, 'normal@user.com')
        self.assertTrue(test_user.is_active)
        self.assertFalse(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)
        try:
            self.assertIsNone(test_user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            user.objects.create_user()
        with self.assertRaises(TypeError):
            user.objects.create_user(email='')
        with self.assertRaises(ValueError):
            user.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        user = get_user_model()
        admin_user = user.objects.create_superuser(email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            user.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False
            )
