from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import NewTopicForm
from .models import Board, Topic, Post


class HomePageTests(TestCase):
    board_name = 'Django'
    board_desc = 'Django board.'

    def setUp(self):
        Board.objects.create(name=self.board_name, description=self.board_desc)

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

    def test_home_view_contains_link_to_topics_page(self):
        response = self.client.get(reverse('home'))
        topics_url = reverse('board_topics', args=[1])
        self.assertContains(response, f'href="{topics_url}"')


class BoardTopicsTests(TestCase):
    board_name = 'Django'
    board_desc = 'Django board.'
    topic_subject = 'New topic'

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret',
        )
        self.board = Board.objects.create(name=self.board_name, description=self.board_desc)
        self.topic = Topic.objects.create(subject=self.topic_subject, board=self.board, starter=self.user)

    def test_board_get_absolute_url(self):
        self.assertEqual(self.board.get_absolute_url(), '/boards/1/')

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
        self.assertTemplateUsed(response, 'board_topics.html')

    def test_board_topics_view_contains_navigation_links(self):
        response = self.client.get(reverse('board_topics', args=[1]))
        home_url = reverse('home')
        new_topic_url = reverse('new_topic', args=[1])
        self.assertContains(response, f'href="{home_url}"')
        self.assertContains(response, f'href="{new_topic_url}"')

    def test_board_topics_view_lists_topics(self):
        response = self.client.get(reverse('board_topics', args=[1]))
        self.assertContains(response, self.topic_subject)


class NewTopicTests(TestCase):
    board_name = 'Django'
    board_desc = 'Django board.'

    def setUp(self):
        self.board = Board.objects.create(name=self.board_name, description=self.board_desc)
        user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret',
        )
        self.client.force_login(user)

    def test_new_topic_status_code(self):
        response = self.client.get('/boards/1/new/')
        no_response = self.client.get('/boards/99/new/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)

    def test_new_topic_view_url_by_name(self):
        response = self.client.get(reverse('new_topic', args=[1]))
        no_response = self.client.get(reverse('new_topic', args=[99]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)

    def test_new_topic_view_uses_correct_template(self):
        response = self.client.get(reverse('new_topic', args=[1]))
        self.assertTemplateUsed(response, 'new_topic.html')

    def test_new_topic_view_contains_link_to_board_topics(self):
        response = self.client.get(reverse('new_topic', args=[1]))
        board_topics_url = reverse('board_topics', args=[1])
        self.assertContains(response, f'href="{board_topics_url}"')

    def test_new_topic_view_contains_form(self):
        response = self.client.get(reverse('new_topic', args=[1]))
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)


class PostUpdateViewTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.username = 'testuser'
        self.email = 'test@example.com'
        self.password = 'secretpassword'
        user = get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )
        self.topic = Topic.objects.create(subject='Test topic', board=self.board, starter=user)
        self.post = Post.objects.create(message='Test message', topic=self.topic, created_by=user)
        self.url = reverse('edit_post', kwargs={
            'pk': self.board.pk,
            'topic_pk': self.topic.pk,
            'post_pk': self.post.pk,
        })


class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class UnauthorizedPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        username = 'user2'
        email = 'user2@example.com'
        get_user_model().objects.create_user(
            username=username,
            email=email,
            password=self.password
        )
        self.client.login(username=username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        # Users should get a 404 response when editing another user's posts
        self.assertEqual(self.response.status_code, 404)
