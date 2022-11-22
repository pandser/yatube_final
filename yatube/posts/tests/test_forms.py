import shutil

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Comment, Post, User
from .constants import TEMP_MEDIA_ROOT, SMALL_GIF


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.author,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.client.force_login(self.author)

    def test_create_valid_post(self):
        posts_count = Post.objects.count()
        uploaded_image = SimpleUploadedFile(
            name='small.gif',
            content=SMALL_GIF,
            content_type='image/gif',
        )
        form_data = {
            'text': 'Валидный тестовый пост',
            'image': uploaded_image,
        }
        response = self.client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(
            Post.objects.count(),
            posts_count + 1,
            'Пост не был создан'
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': 'author'})
        )
        self.assertTrue(
            Post.objects.filter(
                text='Валидный тестовый пост',
                image='posts/small.gif'
            ).exists()
        )

    def test_edit_valid_post(self):
        post_before = Post.objects.get(pk=1).text
        form_data = {
            'text': 'Измененный валидный тестовый пост',
        }
        self.client.post(
            reverse('posts:post_edit', kwargs={'post_id': 1}),
            data=form_data,
            follow=True,
        )
        post_after = Post.objects.get(pk=1).text
        self.assertNotEqual(Post.objects.get(pk=1).text, post_before)
        self.assertEqual(Post.objects.get(pk=1).text, post_after)


class CommentCreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.post = Post.objects.create(
            text='Тестовый пост для коментария',
            author=cls.author,
        )
        cls.comment = Comment.objects.create(
            text='Первый комментарий',
            post_id=1,
            author=cls.author,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_create_comment(self):
        comments = Comment.objects.filter(post_id=1).count()
        form_data = {
            'text': 'Второй комментарий',
        }
        self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': 1}),
            data=form_data,
            follow=True,
        )
        self.assertEqual(
            Comment.objects.filter(post_id=1).count(),
            comments + 1,
            'Коментарий не был создан'
        )

    def test_create_comment_not_authorized_client(self):
        comments = Comment.objects.filter(post_id=1).count()
        form_data = {
            'text': 'Коментарий не авторизованного пользователя'
        }
        self.client.post(
            reverse('posts:add_comment', kwargs={'post_id': 1}),
            data=form_data,
            follow=True,
        )
        self.assertNotEqual(
            Comment.objects.filter(post_id=1).count(),
            comments + 1,
            'Коментарий был создан'
        )
