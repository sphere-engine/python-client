# coding: utf-8

"""
Sphere Engine API

@copyright  Copyright (c) 2015 Sphere Research Labs (http://sphere-research.com)
"""

from __future__ import absolute_import

import re
import sys
import time
import json
from datetime import datetime
from datetime import date
# python 2 and python 3 compatibility library
from six import iteritems
import requests
import sphere_engine
import simplejson
try:
    # for python3
    from urllib.parse import quote
except ImportError:
    # for python2
    from urllib import quote

import logging
logger = logging.getLogger('sphere_engine')


class ApiClient(object):
    """
    Network communication class

    This class base on auto generated class from Swagger client library builds.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    access_token = None
    endpoint = None
    version = None

    host = None
    host_protocol = 'http'

    default_headers = {}

    def __init__(self, access_token, endpoint, version, api_type, request_timeout=5, retry_count=3):
        """
        Constructor of the class.

        :param host: The base path for the server to call.
        :param header_name: a header to pass when making calls to the API.
        :param header_value: a header value to pass when making calls to the API.
        """

        self.access_token = access_token
        self.endpoint = endpoint
        self.version = version
        self.host = self.create_host(api_type, endpoint, version)

        self._request_timeout = request_timeout
        self._retry_count = retry_count

        # Set default User-Agent.
        self.user_agent = 'SphereEngine/ClientPython'

    def create_host(self, api_type, endpoint, version):
        """ Creates complete API link

        :param api_type: api module, problems|compilers
        :type api_type: string
        :param endpoint: api base endpoint
        :type endpoint: string
        :param version: api version (e.g. v3)
        :type version: string
        :returns: complete API endpoint
        :rtype: string
        """
        if '.' not in endpoint:
            host = '%s://%s.%s.sphere-engine.com/api/%s' % (
                self.host_protocol,
                endpoint,
                'compilers' if api_type == 'compilers' else 'problems',
                version
            )
        else:
            endpoint = re.sub('(^https?://)', '', endpoint.lower())
            host = '%s://%s/api/%s' % (
                self.host_protocol,
                endpoint,
                version
            )

        return host

    def call_api(self, resource_path, method, path_params=None, query_params=None,
                 header_params=None, post_params=None, files_params=None, response_type=None):
        """ Call method

        :param resource_path: api method path
        :type resource_path: string
        :param method: HTTP method
        :type method: string
        :param path_params: url parameters
        :type path_params: dict
        :param query_params: query parameters
        :type query_params: dict
        :param header_params: header parameters
        :type header_params: dict
        :param post_params: post data parameters
        :type post_params: dict
        :param files_params: files data parameters
        :type files_params: dict
        :param response_type: response type, file|json
        :type response_type: string
        :returns: api response
        :rtype: json|string
        """

        http_response = self.make_http_call(resource_path, method, path_params,
                                            query_params, header_params, post_params, files_params)
        response = self.process_response(http_response, response_type)
        return response

    def process_response(self, http_response, response_type):
        """ Call method

        :param http_response: response from HTTP call
        :type http_response: dict
        :param response_type: response type, file|json
        :type response_type: string
        :returns: api response
        :rtype: json|string
        """

        try:
            if http_response['http_code'] not in range(200, 206):
                http_body = http_response['http_body'].json()
                if 'message' in http_body:
                    message = http_body['message']
                    error_code = http_body['error_code'] if 'error_code' in http_body else 0
                    raise sphere_engine.exceptions.SphereEngineException(message, http_response['http_code'], error_code)
                else:
                    message = http_response['http_body'].text
                    raise sphere_engine.exceptions.SphereEngineException(message, http_response['http_code'], 0)

            if response_type == 'file':
                data = http_response['http_body'].text
            else:
                data = http_response['http_body'].json()
        except simplejson.scanner.JSONDecodeError:
            message = http_response['http_body'].text
            raise sphere_engine.exceptions.SphereEngineException(message, http_response['http_code'], 0)

        return data

    def _backoff(self, remaining_retries):
        """ Wait time between request in case of retry

        :param remaining_retries: number of remaining retires
        :type remaining_retries: int
        """

        retry_number = max(0, self._retry_count - remaining_retries)

        if retry_number > 0:  # waits only for actual retries
            sleep_time = min(3, retry_number)
            time.sleep(sleep_time)

    def make_http_call(self, resource_path, method, path_params=None, query_params=None,
                       header_params=None, post_params=None, files_params=None):
        """ HTTP call method

        :param resource_path: api method path
        :type resource_path: string
        :param method: HTTP method
        :type method: string
        :param path_params: url parameters
        :type path_params: dict
        :param query_params: query parameters
        :type query_params: dict
        :param header_params: header parameters
        :type header_params: dict
        :param post_params: post data parameters
        :type post_params: dict
        :param files_params: files data parameters
        :type files_params: dict
        :returns: data from http call
        :rtype: dict
        """

        # headers parameters
        header_params = header_params or {}
        header_params.update(self.default_headers)

        if header_params:
            header_params = self.sanitize_for_serialization(header_params)

        # path parameters
        if path_params:
            for k, v in iteritems(path_params):
                replacement = quote(str(self.to_path_value(v)))
                resource_path = resource_path.replace('{' + k + '}', replacement)

        # query parameters
        if not query_params:
            query_params = {}
        if self.access_token:
            query_params['access_token'] = self.access_token

        # post parameters
        if post_params:
            post_params = self.sanitize_for_serialization(post_params)

        if not files_params:
            files_params = {}

        # request url
        url = self.host + resource_path

        retry_count = self._retry_count
        while retry_count > 0:
            self._backoff(retry_count)
            retry_count = retry_count - 1
            try:

                # perform request and return response
                response_data = self.request(method, url,
                                             query_params=query_params,
                                             headers=header_params,
                                             post_params=post_params,
                                             files_params=files_params)

                if 500 <= response_data.status_code < 600:
                    continue

                break
            except requests.exceptions.ConnectionError as e:
                if retry_count > 0:
                    continue
                else:
                    raise e
            except requests.exceptions.Timeout as e:
                if retry_count > 0:
                    continue
                else:
                    raise e
            except Exception as e:
                raise e

        return {
            'http_code': response_data.status_code,
            'http_body': response_data,
            'conn_errno': 0,
            'conn_error': '',
        }

    def request(self, method, url, query_params=None, headers=None,
                post_params=None, files_params=None):
        """
        Makes the HTTP request using requests library.

        :raise requests.exceptions.RequestException
        :raise sphere_engine.exceptions.SphereEngineException
        """

        response = None

        if method == "GET":
            response = requests.get(url, params=query_params, headers=headers, timeout=self._request_timeout)

        elif method == "HEAD":
            response = requests.head(url, params=query_params, headers=headers, timeout=self._request_timeout)

        elif method == "POST":
            response = requests.post(url, params=query_params, headers=headers, data=post_params, files=files_params, timeout=self._request_timeout)

        elif method == "PUT":
            response = requests.put(url, params=query_params, headers=headers, data=post_params, files=files_params, timeout=self._request_timeout)

        elif method == "DELETE":
            response = requests.delete(url, params=query_params, headers=headers, timeout=self._request_timeout)

        else:
            raise ValueError(
                "http method must be `GET`, `HEAD`,"
                " `POST`, `PATCH`, `PUT` or `DELETE`."
            )

        return response

    @property
    def user_agent(self):
        """
        Gets user agent.
        """
        return self.default_headers['User-Agent']

    @user_agent.setter
    def user_agent(self, value):
        """
        Sets user agent.
        """
        self.default_headers['User-Agent'] = value

    def set_default_header(self, header_name, header_value):
        """
        Set default header
        """
        self.default_headers[header_name] = header_value

    def to_path_value(self, obj):
        """
        Takes value and turn it into a string suitable for inclusion in
        the path, by url-encoding.

        :param obj: object or string value.

        :return string: quoted value.
        """
        if isinstance(obj, list):
            return ','.join(obj)
        else:
            return str(obj)

    def sanitize_for_serialization(self, obj):
        """
        Builds a JSON POST object.

        If obj is None, return None.
        If obj is str, int, float, bool, return directly.
        If obj is datetime.datetime, datetime.date
            convert to string in iso8601 format.
        If obj is list, sanitize each element in the list.
        If obj is dict, return the dict.
        If obj is swagger model, return the properties dict.

        :param obj: The data to serialize.
        :return: The serialized form of data.
        """
        types = (str, int, float, bool, tuple)
        if sys.version_info < (3, 0):
            types = types + (unicode,)
        if isinstance(obj, type(None)):
            return None
        elif isinstance(obj, types):
            return obj
        elif isinstance(obj, list):
            return [self.sanitize_for_serialization(sub_obj)
                    for sub_obj in obj]
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        else:
            if isinstance(obj, dict):
                obj_dict = obj
            else:
                # Convert model obj to dict except
                # attributes `swagger_types`, `attribute_map`
                # and attributes which value is not None.
                # Convert attribute name to json key in
                # model definition for request.
                obj_dict = {obj.attribute_map[attr]: getattr(obj, attr)
                            for attr, _ in iteritems(obj.swagger_types)
                            if getattr(obj, attr) is not None}

            return {key: self.sanitize_for_serialization(val)
                    for key, val in iteritems(obj_dict)}

    # def deserialize(self, response, response_type):
    #     """
    #     Deserializes response into an object.

    #     :param response: RESTResponse object to be deserialized.
    #     :param response_type: class literal for
    #         deserialzied object, or string of class name.

    #     :return: deserialized object.
    #     """
    #     # handle file downloading
    #     # save response body into a tmp file and return the instance
    #     if response_type == 'file':
    #         return self.__deserialize_file(response)

    #     # fetch data from response object
    #     try:
    #         data = json.loads(response.data)
    #     except ValueError:
    #         data = response.data

    #     return data
