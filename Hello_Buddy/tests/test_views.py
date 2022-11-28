from django.test import TestCase
from django.urls import reverse


class Baseset(TestCase):

    def setUp(self):
        self.redirect_home_url = reverse('')
        self.home_url = reverse('home')
        self.about_us_url = reverse('aboutus')
        self.create_url = reverse('create')


class HomeViewTest(Baseset):

    def test_home_page_response(self):
        """ To test success response of home page"""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Hello_Buddy/home.html')


class AboutUsViewTest(Baseset):

    def test_about_us_page_response(self):
        """ To test success response of about us page"""
        response = self.client.get(self.about_us_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Hello_Buddy/aboutus.html')


class RedirectToHomeViewTest(Baseset):

    def test_redirect_home_response(self):
        """ To test first page that will redirect to home"""
        response = self.client.get(self.redirect_home_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home')


class CategoryViewTest(Baseset):

    def test_category_sport_page_response(self):
        """ test success response of sport page"""
        category_url = reverse('event_category', args=['sport'])
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Hello_Buddy/event_by_category.html')

    def test_category_eating_page_response(self):
        """ test success response of eating page"""
        category_url = reverse('event_category', args=['eating'])
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Hello_Buddy/event_by_category.html')

    def test_category_movie_page_response(self):
        """ test success response of movie page"""
        category_url = reverse('event_category', args=['movie'])
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Hello_Buddy/event_by_category.html')

    def test_category_party_page_response(self):
        """ test success response of party page"""
        category_url = reverse('event_category', args=['party'])
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Hello_Buddy/event_by_category.html')

    def test_category_education_page_response(self):
        """ test success response of education page"""
        category_url = reverse('event_category', args=['education'])
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Hello_Buddy/event_by_category.html')
    

        
