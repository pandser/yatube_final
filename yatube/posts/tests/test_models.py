from django.test import TestCase
from mixer.backend.django import mixer

from ..models import Post, Group
from ..constants import SLICE_POST_TEXT


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = mixer.blend(Post)

    def test_models_have_correct_object_name(self):
        post = self.post
        expected_post_object_name = post.text[:SLICE_POST_TEXT]
        self.assertEqual(expected_post_object_name, str(post), (
            'Не корректно работает __str__ классв Post'
        ))

    def test_verbose_name(self):
        post = self.post
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
        post = self.post
        field_help_text = {
            'text': 'Текст нового поста',
            'author': 'Автор поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        for field, expected_help_text in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(expected_help_text,
                                 post._meta.get_field(field).help_text)


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = mixer.blend(Group)

    def test_model_group_have_correct_object_name(self):
        group = self.group
        expected_group_object_name = group.title
        self.assertEqual(expected_group_object_name, str(group), (
            'Не корректно работает __str__ класса Group'
        ))
