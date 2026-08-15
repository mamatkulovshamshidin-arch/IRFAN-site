from django.test import TestCase
from django.urls import reverse
from .models import Registration, Teacher


class PublicPagesTests(TestCase):
    def test_public_pages_open(self):
        for name in ('home', 'about', 'program', 'teachers', 'news', 'faq', 'register', 'contact', 'robots', 'sitemap'):
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_register_creates_record(self):
        response = self.client.post(reverse('register'), {
            'full_name': 'Тест Колдонуучу',
            'phone': '+996 700 000 000',
            'email': 'test@example.com',
            'age': 25,
            'city': 'Бишкек',
            'education_level': 'beginner',
            'learning_format': 'either',
            'notes': '',
            'consent': 'on',
        })
        self.assertRedirects(response, reverse('registration_success'))
        self.assertEqual(Registration.objects.count(), 1)

    def test_register_rejects_missing_consent(self):
        response = self.client.post(reverse('register'), {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Registration.objects.count(), 0)

    def test_teacher_detail_opens(self):
        teacher = Teacher.objects.create(
            name='Демо мугалим',
            title='Маалымат жакында жарыяланат',
            biography='Бул демо маалымат. Администратор панелинен өзгөртүлөт.',
        )
        response = self.client.get(reverse('teacher_detail', args=[teacher.slug]))
        self.assertEqual(response.status_code, 200)

    def test_unknown_url_returns_404(self):
        response = self.client.get('/жок-барак/')
        self.assertEqual(response.status_code, 404)

    def test_openapi_schema_and_swagger_open(self):
        self.assertEqual(self.client.get('/api/schema/').status_code, 200)
        self.assertEqual(self.client.get('/api/docs/').status_code, 200)
