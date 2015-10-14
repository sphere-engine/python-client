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

from apis.compilers import CompilersApi
from apis.problems import ProblemsApi
from api_client import ApiClient

class SphereEngine:
    """SphereEngineAPI"""

    __access_token = None
    __endpoint = None
    __version = None
    __compilers_client = None
    __problems_client = None

    def __init__(self, access_token, version, endpoint=None, config=None):
        self.__access_token = access_token
        self.__endpoint = endpoint
        self.__version = version

    def execution_client(self):
        
        if self.__version not in ('v3', '3'):
            raise ValueError('Invalid API version')
        
        if self.__compilers_client is None:
            api_client = ApiClient(self.__access_token, self.__endpoint, self.__version, 'compilers')
            self.__compilers_client = CompilersApi(api_client)
            
        return self.__compilers_client

    def problems_client(self):
        
        if self.__version not in ('v3', '3'):
            raise ValueError('Invalid API version')
        
        if self.__problems_client is None:
            api_client = ApiClient(self.__access_token, self.__endpoint, self.__version, 'problems')
            self.__problems_client = ProblemsApi(api_client)
    
        return self.__problems_client
"""
class SphereEngineAbstractAPI:

    def test(self):
        url = self.baseurl + 'test?access_token=' + self.access_token
        return self.get_content(url, 'GET', self.getTimeout('test'))

    def get_content(self, url, type='GET', timeout=10, data={}):
        if type == 'GET':
            if data != {}:
                url_values = urllib.urlencode(data)
                url += '?' + url_values
                data = {}

        if data != {}:
            content = urllib.urlencode(data)
            req = urllib2.Request(url, content)
        else:
            req = urllib2.Request(url)
        try:
            response = urllib2.urlopen(req, timeout=timeout)
            return response.read()
        except urllib2.URLError, e:
            return 'ERROR: timeout or other exception'
"""
