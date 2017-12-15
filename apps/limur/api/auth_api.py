import json

from util.resources import api_method, ResourceUtil
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from tastypie.resources import Resource

from limur.models.auth import UserProfile


class AuthResource(ResourceUtil, Resource):

    class Meta:
        allowed_methods = []
        resource_name = 'auth'

    def prepend_urls(self):
        return [
            self.make_url('login'),
            self.make_url('logout'),
            self.make_url('register'),
            self.make_url('session'),
        ]

    @api_method(allowed_methods=['post'])
    def login(self, request, **kwargs):
        try:
            payload = json.loads(request.body)
        except ValueError as e:
            self.raise_error('Invalid POST request body: %s' % e.message)

        def invalid_passowrd_resp(request):
            return self.create_response(
                request,
                'Invalid login/password pair',
                response_class=HttpResponseBadRequest,
            )

        # TODO Throttle

        users = User.objects.filter(
            email=payload.get('email')
        ).prefetch_related('userprofile')

        matches = len(users)

        if matches == 0:
            return invalid_passowrd_resp(request)
        elif matches == 1:
            user = users[0]
            # TODO Check user.userprofile exists
        else:
            pass
            # TODO probably an error

        # TODO max attempts

        auth_user = authenticate(username=user.username, password=payload.get('password'))
        if auth_user is not None:
            # TODO Check expired
            # TODO Check is active
            login(request, auth_user)
            # Reset invalid attempts
            user.userprofile.invalid_attemps_count = 0
            user.userprofile.save()
            # TODO Return session
            return self.create_response(request, {'msg': 'Logged in'})
        else:
            # incr invalid attemts
            user.userprofile.invalid_attemps_count += 1
            user.userprofile.save()
            return invalid_passowrd_resp(request)

    @api_method(allowed_methods=['get'])
    def logout(self, request, **kwargs):
        logout(request)
        return self.create_response(request, {})

    @api_method(allowed_methods=['post'])
    def register(self, request, **kwargs):
        payload = json.loads(request.body)

        # TODO Check exists
        email = payload['email']
        username = email

        user = User.objects.create_user(username, email)

        password = payload['password']

        # TODO Validate password
        user.set_password(password)
        user.is_active=True
        user.save()

        userprofile = UserProfile.objects.create(
            user=user,
        )

        userprofile.save()

        # TODO Send mail

        return self.create_response(request, 'User ID %s created' % user.id)

    @api_method(allowed_methods=['get'])
    def session(self, request, **kwargs):
        return self.create_response(request, {})
