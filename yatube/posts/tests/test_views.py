import shutil

from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Comment, Follow, Post, Group, User
from .constants import TEMP_MEDIA_ROOT, SMALL_GIF


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create_user(username='author')
        cls.user_follower = User.objects.create_user(username='follower')
        cls.group_1 = Group.objects.create(
            title='test',
            slug='test_slug',
            description='description_test_group',
        )
        cls.group_2 = Group.objects.create(
            title='test_group',
            slug='slug_for_test_group',
            description='description_test_group',
        )
        cls.uploaded_image = SimpleUploadedFile(
            name='small.gif',
            content=SMALL_GIF,
            content_type='image/gif'
        )
        cls.post = Post.objects.bulk_create([
            Post(
                author=cls.user_author,
                text=f'Текст # {post_number} тестового поста автора author',
                group=cls.group_1,
            )
            if post_number != 14
            else
            Post(
                author=cls.user_author,
                text=f'Текст # {post_number} тестового поста автора author',
                image=cls.uploaded_image,
                group=cls.group_1,
            )
            for post_number in range(1, 15)
        ])
        cls.template_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': 'test_slug'}): 'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username': 'author'}): 'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': '14'}): 'posts/post_detail.html',
            reverse('posts:post_edit',
                    kwargs={'post_id': '14'}): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        cls.reverse_names_context = {
            reverse('posts:index'): 'page_obj',
            reverse('posts:group_list',
                    kwargs={'slug': 'test_slug'}): 'page_obj',
            reverse('posts:profile',
                    kwargs={'username': 'author'}): 'page_obj',
            reverse('posts:post_detail', kwargs={'post_id': 14}): 'post',
        }
        cls.reverse_names_pages_contains = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'test_slug'}),
            reverse('posts:profile', kwargs={'username': 'author'}),
        ]

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_author)
        self.authorized_follower = Client()
        self.authorized_follower.force_login(self.user_follower)

    def test_pages_uses_correct_template(self):
        for reverse_name, template in self.template_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_list_page_show_correct_context(self):
        for reverse_name, context in self.reverse_names_context.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                if context == 'post':
                    first_object = response.context[context]
                else:
                    first_object = response.context[context][0]
                post_author = first_object.author.username
                post_text = first_object.text
                post_image = first_object.image
                self.assertEqual(post_author,
                                 'author',
                                 'Некорректное значение поля author')
                self.assertEqual(post_text,
                                 'Текст # 14 тестового поста автора author',
                                 'Некоррректное значение поля text')
                self.assertEqual(post_image,
                                 'posts/small.gif',
                                 'Не верное значение прикрепленного файла')

    def test_first_page_contains_ten_records(self):
        for reverse_name in self.reverse_names_pages_contains:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_last_page_contains_four_records(self):
        for reverse_name in self.reverse_names_pages_contains:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(
                    reverse_name + '?page=2'
                )
                self.assertEqual(len(response.context['page_obj']), 4)

    def test_pages_forms_correct_context(self):
        reverse_names = [
            reverse('posts:post_create'),
            reverse('posts:post_edit', kwargs={'post_id': '1'})
        ]
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for reverse_name in reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                for value, expected in form_fields.items():
                    with self.subTest(value=value):
                        form_field = response.context.get('form').fields.get(
                            value
                        )
                        self.assertIsInstance(form_field, expected, (
                            f'Поле {value} использует не верный тип'))

    def test_post_in_correct_group(self):
        reverse_names = [
            reverse('posts:index'),
            reverse('posts:group_list',
                    kwargs={'slug': 'slug_for_test_group'}),
            reverse('posts:group_list',
                    kwargs={'slug': 'test_slug'}),
            reverse('posts:profile', kwargs={'username': 'author'}),
        ]
        for reverse_name in reverse_names:
            Post.objects.create(
                author=PostPagesTest.user_author,
                text='Этот пост должен быть в группе test_group',
                group=PostPagesTest.group_2
            )
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                first_object = response.context['page_obj'][0]
                post_author = first_object.author.username
                post_text = first_object.text
                self.assertEqual(post_author, 'author')
                if 'test_slug' in reverse_name:
                    self.assertNotEqual(post_text,
                                        'Этот пост должен быть в группе'
                                        ' test_group')
                else:
                    self.assertEqual(post_text,
                                     'Этот пост должен быть в группе'
                                     ' test_group')

    def test_comments_post_details(self):
        Comment.objects.create(
            post_id=5,
            author=PostPagesTest.user_author,
            text='Тестовый коментарий 5 поста'
        )
        response = self.client.get(
            reverse('posts:post_detail', kwargs={'post_id': 5})
        )
        self.assertEqual(
            response.context['comments'][0].text,
            'Тестовый коментарий 5 поста',
            'Не отображается коментарий'
        )

    def test_cache_index_page(self):
        response_before = self.client.get(
            reverse('posts:index')
        )
        Post.objects.filter(id=13).delete()
        response_after = self.client.get(
            reverse('posts:index')
        )
        self.assertEqual(response_before.content, response_after.content,
                         'Кэш не отработал')

    def test_follow(self):
        self.authorized_follower.get(
            reverse('posts:profile_follow', kwargs={'username': 'author'})
        )
        self.assertTrue(
            Follow.objects.filter(
                author=self.user_author,
                user=self.user_follower,
            ).exists()
        )

    def test_follow_index(self):
        self.authorized_follower.get(
            reverse('posts:profile_follow', kwargs={'username': 'author'})
        )
        self.authorized_client.get(
            reverse('posts:profile_follow', kwargs={'username': 'follower'})
        )
        Post.objects.create(
            author=self.user_follower,
            text='Пост для любимых подписчиков!!!',
        )
        follower = self.authorized_follower.get(
            reverse('posts:follow_index')
        )
        unfollower = self.authorized_client.get(
            reverse('posts:follow_index')
        )
        first_object_follow = follower.context['page_obj'][0].text
        first_object_unfollow = unfollower.context['page_obj'][0].text
        self.assertEqual(
            first_object_follow,
            'Текст # 14 тестового поста автора author',
        )
        self.assertEqual(
            first_object_unfollow,
            'Пост для любимых подписчиков!!!',
        )

    def test_unfollow(self):
        self.authorized_follower.get(
            reverse('posts:profile_unfollow', kwargs={'username': 'author'})
        )
        self.assertFalse(
            Follow.objects.filter(
                author=self.user_author,
                user=self.user_follower,
            ).exists()
        )
