from http import HTTPStatus

from django.core import mail

from authapp.models import CustomUser as User
from django.test import TestCase, Client
from django.urls import reverse

from mainapp import tasks
from mainapp.models import News


class StaticPagesSmokeTest(TestCase):

    def test_base_pages_open(self):

        pages = (
            'mainapp:main_page',
            'mainapp:contacts',
            'mainapp:courses',
            'mainapp:news',
            'authapp:login',
        )

        for page in pages:
            url = reverse(page)
            result = self.client.get(url)

            self.assertEqual(result.status_code, HTTPStatus.OK)


class NewsTestCase(TestCase):

    # метод выполнения каких-либо команд перед каждым тестом
    # например наполнение базы

    def setUp(self) -> None:
        for i in range(10):
            News.objects.create(
                title=f'Новость {i}',
                preambule=f'Описание {i}',
                body=f'Содержание {i}'
            )

        User.objects.create_superuser(username='django', password='geekbrains')
        self.client_with_auth = Client() # не авторизованный пользователь

        # генерация авторизованного пользователя, например админа
        auth_url = reverse('authapp:login')
        self.client_with_auth.post(
            auth_url,
            {'username': 'django', 'password': 'geekbrains'}
        )

    def test_failed_open_add_by_anon(self):

        url = reverse('mainapp:news_create')
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_create_news_by_admin(self):
        news_count = News.objects.count()

        url = reverse('mainapp:news_create')
        result = self.client_with_auth.post(
            url,
            data={
                'title': 'title123',
                'preambule': 'intro123',
                'body': 'body123',
            }
        )

        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        self.assertEqual(News.objects.count(), news_count+1)

    def test_news_detail_open(self):
        news_obj = News.objects.first()
        url = reverse('mainapp:news_detail', args=[news_obj.pk])
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_update_news_open_by_admin(self):
        news_obj = News.objects.first()
        url = reverse('mainapp:news_update', args=[news_obj.pk])
        result = self.client_with_auth.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_fail_update_news_open_by_anon(self):
        news_obj = News.objects.first()
        url = reverse('mainapp:news_update', args=[news_obj.pk])
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_update_news_by_admin(self):
        new_data = 'Updated data'
        news_obj = News.objects.first()

        self.assertNotEqual(news_obj.title, new_data)

        url = reverse('mainapp:news_update', args=[news_obj.pk])
        result = self.client_with_auth.post(
            url,
            data={
                'title': new_data,
                'preambule': news_obj.preambule,
                'body': news_obj.body,
            }
        )

        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        news_obj.refresh_from_db()
        self.assertEqual(news_obj.title, new_data)

    def test_fail_news_delete_by_anon(self):
        news_obj = News.objects.first()
        url = reverse('mainapp:news_delete', args=[news_obj.pk])
        result = self.client.post(url)

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_news_delete_by_admin(self):
        news_obj = News.objects.first()
        url = reverse('mainapp:news_delete', args=[news_obj.pk])
        self.client_with_auth.post(url)
        news_obj.refresh_from_db()

        self.assertTrue(news_obj.deleted)

class MailSendTest(TestCase):

    def setUp(self) -> None:
        auth_url = reverse('authapp:login')
        User.objects.create_user(username='django1', password='123')
        self.client = Client()
        self.client.post(
            auth_url,
            {'username': 'django1', 'password': '123'}
        )

    def test_mail_send(self):
        message_text = 'test_message'
        user_id = User.objects.first()
        tasks.send_feedback_to_email(message_from=user_id.id, message_body=message_text)

        self.assertEqual(mail.outbox[0].body, message_text)

