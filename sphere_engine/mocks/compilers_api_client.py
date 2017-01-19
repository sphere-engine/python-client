# coding: utf-8

"""
Copyright 2015 SmartBear Software

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   ref: https://github.com/swagger-api/swagger-codegen
"""
import json

from sphere_engine.api_client import ApiClient
from .mocks_commons import MockCommons
from .mocks_commons import MockResponse

class CompilersApiClient(ApiClient, MockCommons):

    def make_http_call(self, resource_path, method,
                   path_params=None, query_params=None, header_params=None,
                   post_params=None):
        """
        Call method

            @param resource_path: sdfasdf
            :param resource_path dfawef
            :param method GET|POST
            :param path_params
            :param query_params
        """
        return self.get_mock_data('compilers/test')