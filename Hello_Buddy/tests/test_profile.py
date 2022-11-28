from django.test import TestCase
from django.urls import reverse
from Hello_Buddy.models import Profile

class ProfileUserViewTest(TestCase):
    
    def setUp(self):
        self.register = reverse('account_signup')
        self.profile_url = reverse('profile-user')
        
        self.register1 = {
            'username': 'demo12',
            'password1': 'admin123456',
            'password2': 'admin123456',
            'email': 'admin@mail.com'
        }
        
    def test_profile_user_page_response_after_login(self):
        """ profile user page success response after login"""
        # automatic login after signup
        self.client.post(self.register, self.register1)

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Hello_Buddy/profile_user.html')
    
    def test_profile_user_page_response_before_login(self):
        """ profile user page will redirect you to login"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/profile-user')
        
    def test_change_information(self):
        """ test change information """
        self.client.post(self.register, self.register1)
        self.client.get(self.profile_url)
        response = self.client.post(self.profile_url, {'username': 'test123','email':'b@mail.com', 'bio':'Hello', 'save':''})
        self.assertEqual(response.status_code, 302)
        profile = Profile.objects.all().first()
        self.assertEqual(profile.bio, 'Hello')
        self.assertEqual(profile.user.email, 'b@mail.com')
