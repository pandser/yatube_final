from django.test import TestCase

from ..models import Post, Group, User
from ..constants import SLICE_POST_TEXT


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='тест_группа',
            slug='test_slug',
            description='тестовая группа'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Здесь написан тестовый пост длинной более 15 символов'
        )

    def test_models_have_correct_object_name(self):
        post = PostModelTest.post
        group = PostModelTest.group
        expected_post_object_name = post.text[:SLICE_POST_TEXT]
        expected_group_object_name = group.title
        self.assertEqual(expected_post_object_name, str(post), (
            'Не корректно работает __str__ классв Post'
        ))
        self.assertEqual(expected_group_object_name, str(group), (
            'Не корректно работает __str__ класса Group'
        ))

    def test_verbose_name(self):
        post = PostModelTest.post
        field_verbose = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(expected_value,
                                 post._meta.get_field(field).verbose_name)

    def test_help_text(self):
        post = PostModelTest.post
        field_help_text = {
            'text': 'Текст нового поста',
            'author': 'Автор поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        for field, expected_help_text in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(expected_help_text,
                                 post._meta.get_field(field).help_text)
