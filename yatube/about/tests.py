from django.test import TestCase
from http import HTTPStatus


class AboutURLTest(TestCase):
    def test_url_abut(self):
        about_url = [
            '/about/author/',
            '/about/tech/',
        ]
        for url in about_url:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_uses_correct_template(self):
        template_about_url = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for url, template in template_about_url.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertTemplateUsed(response, template)
