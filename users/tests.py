from django.test import TestCase
from django.contrib.auth import get_user_model

class UsersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='Steve', email='hkk@mail.ru')
        self.assertEqual(user.username, 'Steve')
        self.assertEqual(user.email, 'hkk@mail.ru')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
            
    def test_create_superuser(self):
        User = get_user_model()
        admin = User.objects.create_superuser(username='New mike', email='hkk@mail.ru', password='123')
        self.assertEqual(admin.username, 'New mike')
        self.assertEqual(admin.email, 'hkk@mail.ru')
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        