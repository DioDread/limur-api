import json
import pytz

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone
from tastypie.resources import Resource

from limur.models.auth import UserProfile
from util.resources import api_method, ResourceUtil


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
        # FIXME JSONDecodeError
        except ValueError as e:
            self.raise_error('Invalid POST request body: %s' % e.message)

        def invalid_passowrd_resp(request):
            return self.create_response(
                request,
                'Invalid login/password pair',
                response_class=HttpResponseBadRequest,
            )

        users = User.objects.filter(
            email=payload.get('email')
        ).prefetch_related('userprofile')

        matches = len(users)

        if matches == 0:
            return invalid_passowrd_resp(request)
        elif matches == 1:
            user = users[0]
            # Check user.userprofile exists
            if not hasattr(user, 'userprofile'):
                # TODO Log an error
                # Throw an error
                return self.create_response(
                    request,
                    'Error! User profile is damaged. Contact us please!',
                    response_class=HttpResponseBadRequest,
                )
            userprofile = user.userprofile
        else:
            # probably an error
            # TODO log
            return self.create_response(
                request,
                'error! user profile is damaged. contact us please!',
                response_class=httpresponsebadrequest,
            )

        # Check if login is locked
        if userprofile.lock_out_end is not None:
            now = timezone.now()
            if now > userprofile.lock_out_end:
                userprofile.lock_out_end = None
            else:
                return self.create_response(
                    request,
                    'Too many attemts. Try again at {}'.format(
                        timezone.localtime(userprofile.lock_out_end, pytz.timezone(settings.LOCAL_TIME_ZONE))
                    ),
                    response_class=HttpResponseBadRequest,
                )

        auth_user = authenticate(username=user.username, password=payload.get('password'))
        if auth_user is not None:
            # TODO Check expired
            # Check is active
            if not user.is_active:
                return self.create_response(
                    request,
                    'Error! The account is inactivated. Please, contact us.',
                    response_class=HttpResponseBadRequest,
                )

            login(request, auth_user)

            # Reset invalid attempts
            if userprofile.invalid_attemps_count > 0:
                userprofile.invalid_attemps_count = 0
                userprofile.save()
            # TODO Return session
            return self.create_response(request, {'msg': 'Logged in'})
        else:
            # incr invalid attemts
            userprofile.invalid_attemps_count += 1
            # Lock account if max attempts reached
            if userprofile.invalid_attemps_count > settings.MAX_LOGIN_ATTEMPTS:
                userprofile.lock_out_end = timezone.now() + settings.LOGIN_LOCK_DURATION
            userprofile.save()
            return invalid_passowrd_resp(request)

    @api_method(allowed_methods=['get'])
    def logout(self, request, **kwargs):
        logout(request)
        return self.create_response(request, {})

    @api_method(allowed_methods=['post'])
    def register(self, request, **kwargs):
        payload = json.loads(request.body)

        email = payload['email']

        # Check exists
        if User.objects.filter(email=email).exists():
            return self.create_response(
                request,
                'Requested email already in use!',
                response_class=HttpResponseBadRequest,
            )

        username = email

        user = User.objects.create_user(username, email)

        password = payload['password']

        # TODO Validate password
        user.set_password(password)
        user.is_active=True
        user.save()

        # TODO Send mail

        return self.create_response(request, 'User ID %s created' % user.id)

    @api_method(allowed_methods=['get'])
    def session(self, request, **kwargs):
        return self.create_response(request, {})
