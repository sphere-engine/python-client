#
# Copyright 2015 Sphere Research Sp z o.o.
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from .apis.compilers import CompilersApi
from .apis.problems import ProblemsApi
from .api_client import ApiClient

class CompilersClientV3(CompilersApi):
    """
    Client for Sphere Engine Compilers - version 3
    """
    
    _version = 'v3'
    _access_token = None
    _endpoint = None
    
    def __init__(self, access_token, endpoint, **options):
        """
        :param access_token: string
        :param endpoint: string
        """
        
        self._access_token = access_token
        self._endpoint = endpoint
        api_client = ApiClient(self._access_token, self._endpoint, self._version, 'compilers')
        
        CompilersApi.__init__(self, api_client)

class ProblemsClientV3(ProblemsApi):
    """
    Client for Sphere Engine Problems - version 3
    """
    
    _version = 'v3'
    _access_token = None
    _endpoint = None
    
    def __init__(self, access_token, endpoint, **options):
        """
        :param access_token: string
        :param endpoint: string
        """
        
        self._access_token = access_token
        self._endpoint = endpoint
        api_client = ApiClient(self._access_token, self._endpoint, self._version, 'problems')
                
        ProblemsApi.__init__(self, api_client)
