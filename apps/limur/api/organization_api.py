from limur.models import Organization
from util.resources import ResourceUtil

from tastypie.resources import ModelResource
from tastypie.authentication import SessionAuthentication


# TODO Base class for authentication and authorization
class OrganizationResource(ResourceUtil, ModelResource):
    class Meta:
        queryset = Organization.objects.all()
        resource_name = 'organization'
        authentication = SessionAuthentication()
        # TODO Authorization
