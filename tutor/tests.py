from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model

# Testing the user model


# class UserModelTest(TestCase):
#     def test_user_is_tutor(self):
#         user = get_user_model()
#         user.is_tutor = True
#         self.assertTrue(user.is_tutor)

#     def test_user_is_student(self):
#         user = get_user_model()
#         user.is_tutor = False
#         self.assertFalse(user.is_tutor)

# # Testing the views


# class ViewsTest(TestCase):
#     def test_dashboard(self):
#         response = self.client.get('/search/')
#         self.assertEqual(response.status_code, 200)
#     # def test_tutor_dashboard(self):
#     #     response = self.client.get('/tutoring/')
#     #     self.assertEqual(response.status_code, 200)

# # Testing the forms


# class FormsTest(TestCase):
#     def test_custom_signup_form(self):
#         response = self.client.get('/signup/')
#         self.assertEqual(response.status_code, 200)
