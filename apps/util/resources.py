from django.conf.urls import url
from tastypie.utils import trailing_slash

def api_method(allowed_methods=['get']):
    """
    Wraps tastypie api method with basic tastypie checks
    Args:
        allowed_methods (list): List with allowed methods.
    """
    def decorator(fn):
        def wrapped(self, request, **kwargs):
            self.is_authenticated(request)
            self.method_check(request, allowed=allowed_methods)
            self.throttle_check(request)

            response = fn(self, request, **kwargs)

            self.log_throttled_access(request)
            return response
        return wrapped
    return decorator

# TODO Make resource mixin
def make_url(self, name, view=None):
    if not view:
        view = name

    return url(
        r"^(?P<resource_name>{resource_name})/{api_name}{trailing_slash}".format(**{
            'resource_name': self._meta.resource_name,
            'api_name': name,
            'trailing_slash': trailing_slash()
        }),
        self.wrap_view(view),
        name="api_%s" % name
    )
