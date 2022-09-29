from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group

User = get_user_model()


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_admin')
        cls.group = Group.objects.create(
            title='Test group-2433245',
            slug='test-slug-24353',
            description='test group description-242343q54'
        )
        cls.post = Post.objects.create(
            text='тестовый пост три четыре пять',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTest.user)

    def test_form_create(self):
        """Тестирование создания форм.
        1. Проверка создания поста по факту уведичения их количества в БД
        2. Проверка редиректа после создания поста
        3. Проверка данных после создания поста
        """
        posts_count_1 = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст из формы',
            'group': PostFormTest.group.pk
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        posts_count_2 = Post.objects.count()
        self.assertEqual(posts_count_1 + 1, posts_count_2)
        self.assertRedirects(
            response,
            reverse('posts:profile',
                    kwargs={'username': PostFormTest.user.username})
        )
        self.assertEqual(
            response.context['page_obj'][0].text,
            Post.objects.first().text
        )
        self.assertEqual(
            response.context['page_obj'][0].author.username,
            Post.objects.first().author.username
        )
        self.assertEqual(
            response.context['page_obj'][0].group.pk,
            Post.objects.first().group.pk
        )

    def test_form_edit(self):
        """Тестирование формы редактирования поста.
        Сравнение данных поста после редактирования
        с данными, переданными в форму
        """
        post_id = PostFormTest.post.pk
        form_data = {
            'text': 'Текст поста после редактирования',
            'group': PostFormTest.group.pk
        }
        self.authorized_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': post_id}
            ),
            data=form_data
        )
        self.assertEqual(
            Post.objects.get(pk=post_id).text,
            form_data['text']
        )
        self.assertEqual(
            Post.objects.get(pk=post_id).group.pk,
            form_data['group']
        )
