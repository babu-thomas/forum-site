from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.core import mail
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
        response = self.client.get('/signup/')
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

    def test_signup_form_inputs(self):
        # The form must contain 5 input fields: username, email, password1, password2 and csrf
        response = self.client.get(reverse('signup'))
        self.assertContains(response, '<input', 5)
        self.assertContains(response, 'type="text"', 1)
        self.assertContains(response, 'type="email"', 1)
        self.assertContains(response, 'type="password"', 2)
        self.assertContains(response, '<button', 1)

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


class UserCreationFormTests(TestCase):
    def test_form_has_fields(self):
        form = UserCreationForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(actual, expected)


class PasswordResetPageTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('password_reset'))

    def test_password_reset_page_status_code(self):
        response = self.client.get('/password_reset/')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_view_url_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_password_reset_view_uses_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'password_reset.html')

    def test_password_reset_page_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_password_reset_page_form_inputs(self):
        # The form must contain 2 input fields: email and csrf
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, '<button', 1)


class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        username = 'test'
        email = 'test@example.com'
        password = 'secretpassword'
        user_model = get_user_model()
        user_model.objects.create_user(username=username, email=email, password=password)
        url = reverse('password_reset')
        data = {'email': email}
        self.response = self.client.post(url, data)

    def test_redirection(self):
        # A valid form submission must redirect user to 'password_reset_done' view
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        self.assertEqual(len(mail.outbox), 1)


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        data = {'email': 'invalid@example.com'}
        self.response = self.client.post(url, data)

    def test_redirection(self):
        # Even invalid email must redirect user to 'password_reset_done' view
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_reset_email_sent(self):
        self.assertEqual(len(mail.outbox), 0)


class PasswordResetMailTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.email_id = 'test@example.com'
        password = 'secretpassword'
        user_model = get_user_model()
        user_model.objects.create_user(username=self.username, email=self.email_id, password=password)
        url = reverse('password_reset')
        data = {'email': self.email_id}
        self.response = self.client.post(url, data)
        self.email_text = mail.outbox[0]

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email_text.body)
        self.assertIn(self.username, self.email_text.body)
        self.assertIn(self.email_id, self.email_text.body)

    def test_email_to(self):
        self.assertEqual([self.email_id, ], self.email_text.to)
