from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User



class BaseSet(TestCase):
    def setUp(self):
        """ Set attribute """
        self.url_register = reverse('account_signup')
        self.url_login = reverse('account_login')
        self.url_resetpassword = reverse('account_reset_password')
        User.objects.create_user(username='jack',
                                 email='j@mail.com',
                                 password='jack123456')

        self.register1 = {
            'username': 'demo12',
            'password1': 'admin123456',
            'password2': 'admin123456',
            'email': 'admin@mail.com'
        }

        self.register2 = {
            'username': 'demo12',
            'password1': 'admin54343',
            'password2': 'admin54343',
            'email': 'admin1@mail.com'
        }

        self.register3 = {
            'username': 'demo123',
            'password1': 'admin54343',
            'password2': 'admin54343',
            'email': 'admin1@mail.com'
        }

        self.register4 = {
            'username': 'demo123',
            'password1': 'admin54343',
            'password2': 'admin54341',
            'email': 'admin1@mail.com'
        }

        self.register5 = {
            'username': 'demo123',
            'password1': 'admin54343',
            'password2': 'admin54341',
            'email': 'admin1'
        }

        self.register6 = {
            'username': 'demo123',
            'password1': 'a54',
            'password2': 'a54',
            'email': 'admin1@mail.com'
        }

        self.login1 = {
            'username': 'demo12',
            'password': 'admin123456',
        }

        self.login2 = {
            'username': 'demo1234',
            'password': 'admin54343',
        }
        return super().setUp()


class RegisterTest(BaseSet):

    def test_register_page_correctly(self):
        """ Test register page"""
        response = self.client.get(self.url_register)  # option -> response = self.client.get('/accounts/signup/')
        # To check Http response.
        self.assertEqual(response.status_code, 200)
        # To check template that url used.
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_correct_register(self):
        """ Correctly information to register"""
        response = self.client.post(self.url_register, self.register1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home')

    def test_taken_username(self):
        """ Username already taken"""
        self.client.post(self.url_register, self.register1)
        self.client.logout()
        response = self.client.post(self.url_register, self.register2)
        # Cilent should not error and should render the register page to fix information.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_taken_email(self):
        """ Email already taken"""
        self.client.post(self.url_register, self.register2)
        self.client.logout()
        response = self.client.post(self.url_register, self.register3)
        # Cilent should not error and should render the register page to fix information.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_unmatch_password(self):
        """ Password are not matching"""
        response = self.client.post(self.url_register, self.register4)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_invalid_email(self):
        """ Invalid email"""
        response = self.client.post(self.url_register, self.register5)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')


    def test_short_password(self):
        """ Short password"""
        response = self.client.post(self.url_register, self.register6)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')


class LoginTest(BaseSet):


    def test_login_page_correctly(self):
        """ Test login page"""
        response = self.client.get(self.url_login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_login_successful(self):
        """ User login successful"""
        self.client.post(self.url_register, self.register1)
        response = self.client.post(self.url_login, self.login1)
        self.assertEqual(response.status_code, 302)
        # Check url that redirect to
        self.assertEqual(response.url, '/home')

    def test_incorrect_password(self):
        """ User enter incorrect password"""
        self.client.post(self.url_register, self.register2)
        self.client.logout()
        response = self.client.post(self.url_login, self.login1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_incorrect_username(self):
        """ User enter incorrect username"""
        self.client.post(self.url_register, self.register2)
        self.client.logout()
        response = self.client.post(self.url_login, self.login2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_with_no_username(self):
        """ User can not login with no username"""
        response = self.client.post(self.url_login, {'password':'admin1234567'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_with_no_password(self):
        """ User can not login with no password"""
        response = self.client.post(self.url_login, {'username':'demo123'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')


class LogoutTest(BaseSet):
        

    def test_logout_successful(self):
        """ Test user can logout without error"""
        self.client.post(self.url_register, self.register1)
        self.client.login(username='demo12', password='admin123456')
        self.client.logout()
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        
class ResetPasswordTest(BaseSet):
    
    
    def test_reset_password_page(self):
        """ Test reset password page"""
        response = self.client.get(self.url_resetpassword)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/password_reset.html')
        
    def test_reset_password_email_sent(self):
        """ test reset password email sent"""
        response = self.client.post(self.url_resetpassword,{'email':'admin@mail.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, '[example.com] Password Reset E-mail')
        self.assertEqual(response.url, "/accounts/password/reset/done/")

    def test_password_reset_from_key_page(self):
        """ test reset password from key page"""
        self.client.post(self.url_resetpassword,{'email':'j@mail.com'})
        body = mail.outbox[0].body
        url = body[body.find("/accounts/password/reset/") :].split()[0]
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/password/reset/key/1-set-password/')
        
    def test_change_password_successful(self):
        """ test reset password is successful"""
        
        # check password before reset
        user = User.objects.filter(id=1).first()
        self.assertTrue(user.check_password("jack123456"))
        
        # reset password
        self.client.post(self.url_resetpassword,{'email':'j@mail.com'})
        body = mail.outbox[0].body
        url = body[body.find("/accounts/password/reset/") :].split()[0]
        resp = self.client.get(url)
        url = resp.url
        response = self.client.post(url, {'password1':'demo123456', 'password2': 'demo123456'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/password/reset/key/done/')
        
        # check password after reset
        user = User.objects.filter(id=1).first()
        self.assertTrue(user.check_password("demo123456"))
        
        
        

        