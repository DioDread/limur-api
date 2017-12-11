from limur.api.auth_api import AuthResource
from util.test import ResourceTestUtil, BaseResourceTest


# TODO Combine all mixins together
class AuthResourceTest(BaseResourceTest):
    RESOURCE = AuthResource

    def test_logout(self):
        self.assertHttpOK(self.read('logout'))
