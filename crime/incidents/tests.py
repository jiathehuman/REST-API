import unittest

from django.test import TestCase

class MyTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Perform initialization here (e.g., create common fixtures)
        pass

    def setUp(self):
        # Minimal setup for each test method (optional)
        pass

    def test_something(self):
        # Your test logic here
        pass


# class MyUnitTest(unittest.TestCase):

#     def test_something(self):
#         # Your test logic here (without Django's test framework)
#         self.assertEqual(1,1)


# from django.test import TransactionTestCase

# class MyTransactionTestCase(TransactionTestCase):

#     def test_something(self):
#         # Your test logic here
#         self.assertEqual(1,1)

# from django.test import TestCase, Client
# from django.test.utils import tag
# from django.test import override_settings
# from .models import *

# # @override_settings(MIDDLEWARE=[])
# # @override_settings(INSTALLED_APPS=[])

# class FormTests(TestCase):
# #     # @tag('slow')
# #     def setUp(self):
# #         pass
# #     def test_one(self):
# #         self.assertEqual(1,1)

# #     def test_two(self):
# #         self.assertEqual(1,1)

#     @classmethod
#     def setUpTestData(cls):
#         # Perform initialization here (e.g., create common fixtures)
#         pass

#     def setUp(self):
#         # Minimal setup for each test method (optional)
#         pass

#     def test_one(self):
#         self.assertEqual(1,1)

#     def test_two(self):
#         self.assertEqual(1,1)
