from django.contrib.auth.models import User

from limur.api.auth_api import AuthResource
from limur.models.auth import UserProfile
from util.test import ResourceTestUtil, BaseResourceTest


# TODO Combine all mixins together
class AuthResourceTest(BaseResourceTest):
    RESOURCE = AuthResource

    def register_user(self, email=None):
        if email is None:
            email = self.DEFAULT_EMAIL
        payload = {
            'email': email,
            'password': self.DEFAULT_PASSWORD
        }
        return self.post(payload, 'register', bare=True)

    def get_user(self, email=None):
        if email is None:
            email = self.DEFAULT_EMAIL
        return User.objects.get(email=email)

    def test_logout(self):
        self.assertHttpOK(self.read('logout'))

    def test_register_valid(self):
        email = 'test@email'

        self.assertHttpOK(self.register_user(email))
        user = User.objects.get(email=email)

        # Check user email is correct
        self.assertEqual(user.email, email)
        # Should not be stored as plain text
        self.assertNotEqual(user.password, 'password')
        # Check user profile exists
        ref = user.userprofile

    def test_register_invlid_duplicate(self):
        self.register_user()
        self.assertHttpBadRequest(self.register_user())

    def test_user_deleted(self):
        email = 'test@email'
        self.register_user(email)

        User.objects.get(email=email).delete()
        self.assertEqual(User.objects.count(), 0)
        # Userprofile should be removed by DB
        self.assertEqual(UserProfile.objects.count(), 0)

    def test_login_valid(self):
        self.register_user()
        self.assertHttpOK(self.login_user())
        # Check inner state
        self.assertEqual(
            str(self.get_user().pk),
            self.client.session['_auth_user_id']
        )

    def test_login_invalid(self):
        self.register_user()
        self.assertHttpBadRequest(self.login_user(password='wrong'))
        # Check inner state
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_login_not_exists(self):
        self.assertHttpBadRequest(self.login_user())

    def test_login_invalid_attempt(self):
        self.register_user()

        up = self.get_user().userprofile
        self.assertEqual(up.invalid_attemps_count, 0)

        self.login_user(password='wrong')

        up.refresh_from_db()
        self.assertEqual(up.invalid_attemps_count, 1)

    def test_login_invalid_attempt_restore(self):
        self.register_user()

        self.login_user(password='wrong')
        self.assertHttpOK(self.login_user())
        up = self.get_user().userprofile
        self.assertEqual(up.invalid_attemps_count, 0)

    def test_login_invalid_inactive(self):
        self.register_user()
        user = self.get_user()
        user.is_active = False
        user.save()
        self.assertHttpBadRequest(self.login_user())

    def test_login_invalid_lock_out(self):
        self.register_user()

        for i in range(3):
            self.login_user(password='wrong')
        self.assertHttpBadRequest(self.login_user())
        up = self.get_user().userprofile
        self.assertEqual(up.invalid_attemps_count, 4)
