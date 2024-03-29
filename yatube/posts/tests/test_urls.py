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
        self.post_id = str(PostURLTest.post.pk)
        self.username = PostURLTest.user.username
        self.slug = str(PostURLTest.group.slug)

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
            f'/group/{self.slug}/': 'posts/group_list.html',
            f'/profile/{self.username}/': 'posts/profile.html',
            f'/posts/{self.post_id}/edit/': 'posts/create_post.html',
            f'/posts/{self.post_id}/': 'posts/post_detail.html',
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
            f'/group/{self.slug}/': 200,
            f'/posts/{self.post_id}/': 200,
            '/unexisting_page/': 404
        }
        for url, status_code in check_urls.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(
                    response.status_code,
                    status_code,
                    'Ответ на запрос не соответствует ожидаомому'
                )

    def test_exists_edit(self):
        """Проверка доступности редактирования поста для
        авторизованого пользователя"""

        response = self.authorized_client.get(
            f'/posts/{self.post_id}/edit/')
        self.assertEqual(
            response.status_code,
            200,
            'Доступ к редактированию поста должен быть только у его автора'
        )

    def test_create_edit_not_authorized_user_redirects(self):
        """Проверка редиректов неавторизованого пользователя
        при попытке создания и редактирования постов"""

        response = self.guest_client.get('/create/')
        self.assertRedirects(
            response,
            '/auth/login/?next=/create/'
        )
        response = self.guest_client.get(f'/posts/{self.post_id}/edit/')
        self.assertRedirects(
            response,
            f'/auth/login/?next=/posts/{self.post_id}/edit/'
        )

    def test_edit_not_author_redirects(self):
        """Не автор поста, при попытке редактирования
        будет редиректиться на просмотр, во всяком случае,
        пока я не узнаю куда надо =) Это мы и проверим"""

        response = self.authorized_client_not_author.get(
            f'/posts/{self.post_id}/edit/')
        self.assertRedirects(
            response,
            f'/posts/{self.post_id}/'
        )
