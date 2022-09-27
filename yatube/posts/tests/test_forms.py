from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post

User = get_user_model()


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_admin')
        Post.objects.create(
            text='тестовый пост три четыре пять',
            author=cls.user,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTest.user)

    def test_create_post(self):
        self.posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст нового поста из формы',
            'author': PostFormTest.user
        }
        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(
            Post.objects.count(),
            self.posts_count + 1,
            'Новый пост не создан'
        )

    def test_edit_post(self):
        form_data = {
            'text': 'Текст нового поста из формы',
            'author': PostFormTest.user
        }
        self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': 1}),
            data=form_data,
            follow=True
        )
        cur_post = Post.objects.get(pk=1)
        cur_data = {
            'text': cur_post.text,
            'author': cur_post.author
        }
        print('Надеюсь я не забуду это убрать')
        print(cur_data, form_data)
        self.assertEqual(cur_data, form_data)
