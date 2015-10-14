#
# Sphere Engine API
#
# LICENSE
#
#
# @copyright  Copyright (c) 2015 Sphere Research Labs (http://sphere-research.com)
# @license    link do licencji
# @version    0.6

from base import AbstractApi

class CompilersApiSubmissions(AbstractApi):
    
    def create(self, sourceCode, compilerId=None, _input=''):
        """ Send submission
            @param  string    source        source code
            @param  integer   language      language ID   
            @param  string    input         input for the program
            @return submission id or error
        """
    
        resource_path = '/submissions'
        method = 'POST'
        post_params = {
                       'sourceCode': sourceCode,
                       'compilerId': compilerId,
                       'input': _input
        }
    
        response = self.api_client.call_api(resource_path, 
                                            method,
                                            {},
                                            {},
                                            {},
                                            post_params=post_params,
        )
        return response
    
    def get(self, _id, withSource=False, withInput=False, withOutput=False, withStderr=False, withCmpinfo=False):
        
        resource_path = '/submissions/{id}'
        method = 'GET'
        query_data = {
            'withSource': int(withSource),
            'withInput': int(withInput),
            'withOutput': int(withOutput),
            'withStderr': int(withStderr),
            'withCmpinfo': int(withCmpinfo),
        }
    
        response = self.api_client.call_api(resource_path, 
                                            method,
                                            {'id': _id},
                                            query_data,
        )
        return response

class CompilersApi(AbstractApi):
    
    submissions = None
    
    def __init__(self, api_client):
        super(CompilersApi, self).__init__(api_client)
        self.submissions = CompilersApiSubmissions(api_client)
    
    def test(self):
        
        resource_path = '/test'
        method = 'GET'
        
        response = self.api_client.call_api(resource_path, method, )
        return response
    
    def compilers(self):
        """
        Get available languages
        :return list of languages or error
        """
        
        resource_path = '/languages'
        method = 'GET'
        
        response = self.api_client.call_api(resource_path, 
                                            method,
        )
        return response
        