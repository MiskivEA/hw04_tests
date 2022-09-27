from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.user_not_author = User.objects.create_user(username='not_author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            text='12345678901234567890',
            author=cls.user
        )

    def setUp(self):
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTest.user)

        self.authorized_client_not_author = Client()
        self.authorized_client_not_author.force_login(
            PostURLTest.user_not_author)

    def test_urls_uses_correct_template(self):
        """Проверка соответствия шаблонов URL-адресам"""
        url_template_names = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/author/': 'posts/profile.html',
            '/posts/1/edit/': 'posts/create_post.html',
            '/posts/1/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
        }
        for url, template in url_template_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(
                    response,
                    template,
                    'Вызываемый шаблон не соответствует ожидаемому'
                )

    def test_exists_urls_for_everyone(self):
        """Проверка доступности страниц для
        неавторизованого пользователя"""
        check_urls = {
            '/': 200,
            '/group/test-slug/': 200,
            '/posts/1/': 200,
            '/unexisting_page/': 404
        }
        for url, status_code in check_urls.items():
            with self.subTest(field=url):
                response = self.guest_client.get(url)
                self.assertEqual(
                    response.status_code,
                    status_code,
                    'Ответ на запрос не соответствует ожидаомому'
                )

    def test_exist_edit(self):
        """Проверка доступности редактирования поста для
        авторизованого пользователя"""
        response = self.authorized_client.get('/posts/1/edit/')
        self.assertEqual(
            response.status_code,
            200,
            'Доступ к редактированию поста должен быть только у его автора'
        )
