from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from http import HTTPStatus


User = get_user_model()


class UsersURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create_user(username='author')

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_author)

    def test_url_auth_exists_at_desired_location(self):
        url_name_users = [
            '/auth/login/',
            '/auth/logout/',
            '/auth/signup/',
            '/auth/password_reset_form/',
            '/auth/password_reset/done/',
            '/auth/reset/NA/65c-72f002bdd5072dba9130/',
            '/auth/reset/done/',
        ]
        for url in url_name_users:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK, (
                    f'URL {url} не доступен'
                ))

    def test_url_autheticated_users(self):
        urls_name_users = [
            '/auth/password_change/',
            '/auth/password_change/done/',
        ]
        for url in urls_name_users:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK, (
                    f'URL {url} не доступен'
                ))

    def test_urls_uses_correct_template(self):
        template_urls_name = {
            '/auth/login/': 'users/login.html',
            '/auth/signup/': 'users/signup.html',
            '/auth/password_reset_form/': 'users/password_reset_form.html',
            '/auth/password_reset/done/': 'users/password_reset_done.html',
            '/auth/reset/NA/65c-72f002bdd5072dba9130/':
                'users/password_reset_confirm.html',
            '/auth/reset/done/': 'users/password_reset_complete.html',
            '/auth/password_change/': 'users/password_change_form.html',
            '/auth/password_change/done/': 'users/password_change_done.html',
            '/auth/logout/': 'users/logged_out.html',
        }
        for url, template in template_urls_name.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template, (
                    f'В {url} используется не корректный шаблон'
                ))
