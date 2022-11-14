from django.test import TestCase
from django.urls import reverse


class BaseSet(TestCase):
    def setUp(self):
        """ Set attribute """
        self.url_register = reverse('account_signup')
        self.url_login = reverse('account_login')

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
        response = self.client.post(self.url_register, self.register2)
        # Cilent should not error and should render the register page to fix information.
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'registration/register.html')

#     def test_taken_email(self):
#         """ Email already taken"""
#         self.client.post(self.url_register, self.register2)
#         response1 = self.client.post(self.url_register, self.register3)
#         # Cilent should not error and should render the register page to fix information.
#         self.assertEqual(response1.status_code, 200)
#         self.assertTemplateUsed(response1, 'registration/register.html')

#     def test_unmatch_password(self):
#         """ Password are not matching"""
#         response = self.client.post(self.url_register, self.register4)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'registration/register.html')

#     def test_invalid_email(self):
#         """ Invalid email"""
#         response = self.client.post(self.url_register, self.register5)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'registration/register.html')


#     def test_short_password(self):
#         """ Short password"""
#         response = self.client.post(self.url_register, self.register6)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'registration/register.html')


# class LoginTest(BaseSet):


#     def test_login_page_correctly(self):
#         """ Test login page"""
#         response = self.client.get(self.url_login)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'registration/login.html')

#     def test_login_successful(self):
#         """ User login successful"""
#         self.client.post(self.url_register, self.register1)
#         response = self.client.post(self.url_login, self.login1)
#         self.assertEqual(response.status_code, 302)
#         # Check url that redirect to
#         self.assertEqual(response.url, '/home')

#     def test_incorrect_password(self):
#         """ User enter incorrect password"""
#         self.client.post(self.url_register, self.register2)
#         response = self.client.post(self.url_login, self.login1)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'registration/login.html')

#     def test_incorrect_username(self):
#         """ User enter incorrect username"""
#         self.client.post(self.url_register, self.register2)
#         response = self.client.post(self.url_login, self.login2)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'registration/login.html')

#     def test_with_no_username(self):
#         """ User can not login with no username"""
#         response = self.client.post(self.url_login, {'password':'admin1234567'})
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'registration/login.html')

#     def test_with_no_password(self):
#         """ User can not login with no password"""
#         response = self.client.post(self.url_login, {'username':'demo123'})
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'registration/login.html')


# class LogoutTest(BaseSet):

#     def test_logout_successful(self):
#         """ Test user can logout without error"""
#         self.client.post(self.url_register, self.register1)
#         self.client.login(username='demo12', password='admin123456')
#         self.client.logout()
#         response = self.client.get('/home')
#         self.assertEqual(response.status_code, 200)

