from django.test import TestCase
from django.urls import reverse

class RegisterTest(TestCase):
    def setUp(self):
        self.url = reverse('signup')
        # All correct
        self.register1 = {
            'username': 'demo12',
            'password1': 'admin123456',
            'password2': 'admin123456',
            'email': 'admin@mail.com'
        }
        
        self.register1 = {
            'username': 'demo123',
            'password1': '',
            
        }
        return super().setUp()

    def test_register_page_correctly(self):
        response = self.client.get(self.url)  # option -> response = self.client.get('/users/signup/')
        # To check Http response.
        self.assertEqual(response.status_code, 200)
        # To check template that url used.
        self.assertTemplateUsed(response, 'registration/register.html')
        
    def test_correct_register(self):
        response = self.client.post(self.url, self.register1)
        self.assertEqual(response.status_code, 302)
        
    def test_incorrect_register(self):
        pass