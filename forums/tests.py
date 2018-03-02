from django.test import TestCase
from django.urls import reverse

from .models import Board


class HomePageTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class BoardTopicsTests(TestCase):
    board_name = 'Django'
    board_desc = 'Django board.'

    def setUp(self):
        Board.objects.create(name=self.board_name, description=self.board_desc)

    def test_board_topics_status_code(self):
        response = self.client.get('/boards/1/')
        no_response = self.client.get('/boards/99/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)

    def test_board_topics_view_url_by_name(self):
        response = self.client.get(reverse('board_topics', args=[1]))
        no_response = self.client.get(reverse('board_topics', args=[99]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)

    def test_board_topics_view_uses_correct_template(self):
        response = self.client.get(reverse('board_topics', args=[1]))
        self.assertTemplateUsed(response, 'topics.html')
