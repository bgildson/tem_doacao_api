from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Category


class CategoriesTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='category name')

    def test_anon_user_can_get_categories(self):
        url = reverse('categories-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anon_user_can_get_categories_by_id(self):
        category_id = str(CategoriesTest.category.id)
        url = reverse('categories-detail', args=[category_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
