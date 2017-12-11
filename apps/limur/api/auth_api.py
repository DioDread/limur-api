from limur.models.auth import UserProfile

from util.resources import api_method, ResourceUtil
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from tastypie.resources import Resource

import json


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

        # TODO Throttle

        users = User.objects.filter(
            email=payload.get('email')
        ).prefetch_related('userprofile')

        matches = len(users)

        if matches == 0:
            # TODO Create HttpResponseUnauthorized
            return self.create_response(
                request,
                'Ivalid User/Password pair',
                response_class=HttpResponse,
                status=401,
            )
        elif matches == 1:
            user = users[0]
            # TODO Check user.userprofile exists
        else:
            pass
            # TODO probably an error

        # TODO max attempts

        user = authenticate(username=user.username, password=payload.get('password'))
        if user is not None:
            # TODO Check expired
            # TODO Check is active
            login(request, user)
            # TODO Reset invalid attempts
            # TODO Return session
            return self.create_response(request, {'msg': 'Logged in'})
        else:
            # TODO incr invalid attemts
            raise Error

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
