from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import CustomUserCreationForm as UserCreationForm


class SignupPageTests(TestCase):
    def setUp(self):
        username = 'test'
        email = 'test@example.com'
        password = 'secretpassword'

        self.data = {
            'username': username,
            'email': email,
            'password1': password,
            'password2': password,
        }

    def test_signup_page_status_code(self):
        response = self.client.get('/users/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_view_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_view_contains_form(self):
        response = self.client.get(reverse('signup'))
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, UserCreationForm)

    def test_successful_signup_redirects_to_homepage(self):
        response = self.client.post(reverse('signup'), self.data)
        self.assertRedirects(response, reverse('home'))

    def test_successful_signup_creates_user(self):
        self.client.post(reverse('signup'), self.data)
        user_model = get_user_model()
        self.assertTrue(user_model.objects.exists())

    def test_successful_signup_logs_in_user(self):
        self.client.post(reverse('signup'), self.data)
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)
