#
# Sphere Engine API
#
# LICENSE
#
#
# @copyright  Copyright (c) 2015 Sphere Research Labs (http://sphere-research.com)
# @license    link do licencji
# @version    0.6

from .base import AbstractApi

class CompilersApiSubmissions(AbstractApi):
    
    def create(self, sourceCode, compilerId=None, _input=''):
        """ Create submission
            @param  string    source        source code
            @param  integer   language      language ID   
            @param  string    input         input for the program
            @return submission id or error
        """
        
        if not sourceCode:
            raise ValueError('empty source code')
        
        try:
            _cId = int(compilerId)
        except:
            raise ValueError('compilerId should be int')
    
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
        """ Get submission details
            @param _id: 
            @param withSource:
            @param withInput:
            @param withOutput:
            @param withStderr:
            @param withCmpinfo:
            
            @return: array
        """
        
        if not _id:
            raise ValueError('empty _id value')
        
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
    
    @property
    def submissions(self):
        """
        :return: CompilersApiSubmissions """
        return self._submissions
    
    def __init__(self, api_client):
        super(CompilersApi, self).__init__(api_client)
        self._submissions = CompilersApiSubmissions(api_client)
    
    def test(self):
        """ Test request """
        
        resource_path = '/test'
        method = 'GET'
        
        response = self.api_client.call_api(resource_path, method, )
        return response
    
    def compilers(self):
        """
        Get list of available compilers
        :return array
        """
        
        resource_path = '/languages'
        method = 'GET'
        
        response = self.api_client.call_api(resource_path, method)
        return response
        