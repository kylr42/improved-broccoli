from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.transaction import TransactionManagementError
from django.test import TestCase

from transaction.models import TransactionAccount


class TransactionAccountTests(TestCase):

    def test_create_personal_account(self):
        user = get_user_model()
        test_user = user.objects.create_user(email='normal@user.com', password='foo')
        test_account = TransactionAccount.objects.create(customer=test_user, balance=42.21, is_active=True)

        self.assertEqual(test_account.balance, 42.21)
        self.assertEqual(test_account.customer.id, test_user.id)
        self.assertTrue(test_account.is_active)
        self.assertIsNotNone(test_account.id)

        with self.assertRaises(IntegrityError):
            TransactionAccount.objects.create()
        with self.assertRaises(ValueError):
            TransactionAccount.objects.create(customer=42)
        with self.assertRaises(TransactionManagementError):
            TransactionAccount.objects.create(balance=42.21)
        with self.assertRaises(TransactionManagementError):
            TransactionAccount.objects.create(customer=test_user, balance=-42.21)
