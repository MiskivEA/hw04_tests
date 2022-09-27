from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовая слаг',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            text='12345678901234567890',
            author=cls.user
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        self.assertEqual(str(PostModelTest.group), PostModelTest.group.title)
        self.assertEqual(str(PostModelTest.post), PostModelTest.post.text[:15])

    def test_models_verbose_name(self):
        """Проверяем, что у полей отображается нужный лейбл"""
        field_verboses = {
            'text': 'Текст поста',
            'group': 'Группа',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PostModelTest.post._meta.get_field(field).verbose_name,
                    expected_value,
                    'Неверное имя поля'
                )

    def test_models_help_text(self):
        """Проверяем, что у полей отображается нужный хелп-текст"""
        field_help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост'
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PostModelTest.post._meta.get_field(field).help_text, expected_value
                )

