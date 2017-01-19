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

from sphere_engine import CompilersClientV3 as CCV3
from compilers_api_client import CompilersApiClient

class CompilersClientV3(CCV3):
    """
    Mock for client for Sphere Engine Compilers - version 3
    """

    def __init__(self, access_token, endpoint, **options):
        api_client = CompilersApiClient(access_token, endpoint, 'v3', 'compilers')
        
        CCV3.__init__(self, access_token, endpoint, api_client)

