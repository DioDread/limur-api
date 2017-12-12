from django.test import TestCase, RequestFactory
from tastypie.test import ResourceTestCaseMixin

import json
import urllib


API_BASE = '/api/v1'


class ResponseWrapper(object):
    def get_response_data(self):
        content = json.loads(self.content)
        if self.res.request.get('REQUEST_METHOD') == 'PATCH':
            return content
        if 'data' in content:
            return content['data']
        else:
            return content

    def __init__(self, res):
        self.res = res
        self.status_code = res.status_code
        self.content = res.content
        self._data_memo = None

    @property
    def data(self):
        """
        Contains response data.
        Lazy data getter.
        """
        # Memoization
        if not self._data_memo:
            self._data_memo = self.get_response_data()
        return self._data_memo

    def __getitem__(self, idx):
        return self.res[idx]

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return self.res


class ResourceTestUtil(object):
    """
    CRUD mapping mixin
    Each of CRUD methods returns wrapped by ResponseWrapper
    which provides transparent access to response object and
    adds 'data' pseudo-property, which contains response body dict
    """

    def _list_endpoint(self):
        # Force initaliztion
        if not hasattr(self, '_RESOURCE'):
            self._RESOURCE = self.RESOURCE._meta.resource_name
        return API_BASE + '/' + self._RESOURCE + '/'

    def _uri(self, id=None, params=None):
        return self._list_endpoint() + ("%s%s" % (str(id) + '/' if id else "",
            self._generate_params(params)))

    def _generate_params(self, params=None):
        if params:
            return '?' + urllib.urlencode(params)
        return ''

    def set_context(self, context=None):
        self._RESOURCE = context if context else self.RESOURCE

    def get_response_data(self, res):
        """
        Returns dict containing the response data.
        Deprecated. Use `self.read().data` instead.
        Needed for backward compatibility.
        """
        response = res.res if isinstance(res, ResponseWrapper) else res
        if response is None:
            return {}
        content = json.loads(response.content)
        if response.request.get('REQUEST_METHOD') == 'PATCH':
            return content
        if 'data' in content:
            return content['data']
        else:
            return content

    def create(self, data=None, id=None, params=None, bare=False):
        """
        Sends POST request
        :param data: payload data. (default None)
        :param id: resource endpoint (default None)
        :param params: GET params
        :param bare: when True, the payload data will
        not be put into {'data': data} wrapper (default False)
        :type data: dict
        :type id: string
        :type params: dict
        :type bare: boolean
        :rtype: ResponseWrapper instance
        """
        if data is None:
            data = {}
        return ResponseWrapper(
            self.client.post(
                self._uri(id, params),
                json.dumps({'data': data} if not bare else data),
                content_type='application/json')
        )

    def post(self, *args, **kwargs):
        """
        An alias for `create` function
        """
        return self.create(*args, **kwargs)

    def read(self, id=None, params=None):
        return ResponseWrapper(
            self.client.get(
                self._uri(id),
                data=params,
                content_type='application/json')
        )

    def update(self, id=None, data=None, params=None):
        if data is None:
            data = {}
        return ResponseWrapper(
            self.client.put(
                self._uri(id, params),
                json.dumps({'data': data}),
                content_type='application/json')
        )

    def patch(self, id=None, data=None, params=None):
        if data is None:
            data = {}
        return ResponseWrapper(
            self.client.patch(
                self._uri(id, params),
                json.dumps(data),
                content_type='application/json')
        )

    def delete(self, id=None, params=None):
        return ResponseWrapper(
            self.client.delete(
                self._uri(id, params),
                content_type='application/json')
        )


class BaseResourceTest(ResourceTestUtil, ResourceTestCaseMixin, TestCase):
    pass
