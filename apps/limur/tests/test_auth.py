from django.contrib.auth.models import User

from limur.api.auth_api import AuthResource
from limur.models.auth import UserProfile
from util.test import ResourceTestUtil, BaseResourceTest


# TODO Combine all mixins together
class AuthResourceTest(BaseResourceTest):
    RESOURCE = AuthResource
    EMAIL = 'test@email'
    PASSWORD = 'password'

    def register_user(self, email=EMAIL):
        payload = {
            'email': email,
            'password': self.PASSWORD
        }
        self.assertHttpOK(self.post(payload, 'register', bare=True))

    def test_logout(self):
        self.assertHttpOK(self.read('logout'))

    def test_register_valid(self):
        email = 'test@email'

        self.register_user(email)
        user = User.objects.get(email=email)

        # Check user email is correct
        self.assertEqual(user.email, email)
        # Should not be stored as plain text
        self.assertNotEqual(user.password, 'password')
        # Check user profile exists
        ref = user.userprofile

    def test_user_deleted(self):
        email = 'test@email'
        self.register_user(email)

        User.objects.get(email=email).delete()
        self.assertEqual(User.objects.count(), 0)
        # Userprofile should be removed by DB
        self.assertEqual(UserProfile.objects.count(), 0)

    def test_login_valid(self):
        email = 'test@email'
        payload = {
            'email': email,
            'password': self.PASSWORD
        }

        self.register_user(email)
        self.assertHttpOK(self.post(payload, 'login', bare=True))

    def test_login_invalid(self):
        email = 'test@email'
        payload = {
            'email': email,
            'password': 'totally incorrect'
        }

        self.register_user(email)
        self.assertHttpBadRequest(self.post(payload, 'login', bare=True))
