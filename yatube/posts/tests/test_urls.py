from django.test import TestCase, Client, override_settings
from http import HTTPStatus

from ..models import Post, Group, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create_user(username='author')
        cls.user_not_author = User.objects.create_user(username='not_author')
        cls.group = Group.objects.create(
            title='test',
            slug='test_slug',
            description='description_test_group',
        )
        cls.post = Post.objects.create(
            author=cls.user_author,
            text='Текст тестового поста автора author',
        )

    def setUp(self):
        self.authorized_client_author = Client()
        self.authorized_client_not_author = Client()
        self.authorized_client_author.force_login(self.user_author)
        self.authorized_client_not_author.force_login(self.user_not_author)

    def test_url_exists_at_desired_location(self):
        url_name = [
            '/',
            f'/group/{self.group.slug}/',
            f'/profile/{self.user_author}/',
            f'/posts/{self.post.pk}/',
            f'/posts/{self.post.pk}/edit/',
            '/create/',
        ]
        for url in url_name:
            with self.subTest(url=url):
                response = self.authorized_client_author.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK,
                                 f'URL {url} не доступен')

    def test_url_redirect_anonymous(self):
        url_name = [
            f'/posts/{self.post.pk}/edit/',
            '/create/',
        ]
        for url in url_name:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_url_redirect_not_author(self):
        response = self.authorized_client_not_author.get(
            f'/posts/{self.post.pk}/edit/'
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_not_found_url(self):
        response = self.client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_uses_correct_template(self):
        template_urls_name = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user_author}/': 'posts/profile.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
            f'/posts/{self.post.pk}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for url, template in template_urls_name.items():
            with self.subTest(url=url):
                response = self.authorized_client_author.get(url)
                self.assertTemplateUsed(response, template)

    @override_settings(DEBUG=False)
    def test_custom_404_page(self):
        response = self.client.get('/tratata/')
        self.assertTemplateUsed(response, 'core/404.html')
