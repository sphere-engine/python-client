#
# Sphere Engine API
#
# LICENSE
#
#
# Tu tresc licencji
#
#
# @copyright  Copyright (c) 2015 Sphere Research Labs (http://sphere-research.com)
# @license    link do licencji
# @version    0.5
#
import urllib
import urllib2

class SphereEngineAPI:
    """Opis klasy"""

    def __init__(self, params):
        self.type = params['type'] if 'type' in params else 'SC'
        self.version = params['version'] if 'version' in params else '3'
        self.access_token = params['access_token'] if 'access_token' in params else ''
        self.default_language_id = 11 # hardcoded C language
        self.use_timeouts = int(params['use_timeouts']) if 'use_timeouts' in params else 1

        self.timeout = {
            'test': 5,
            'languages': 5,
            'getSubmission': 5,
            'sendSubmission': 10,
            'problems': 15,
            'getProblem': 5
        }

        if self.type == 'SC':
            self.baseurl = 'http://api.compilers.sphere-engine.com/api/' + self.version + '/'
        elif self.type == 'SP':
            self.baseurl = 'http://problems.sphere-engine.com/api/v' + self.version + '/'
        else:
            self.baseurl = ''


    #
    # API settings
    #

    #
    # Set default language
    #
    # @param  integer      language       id of the language
    #
    def setDefaultLanguage(self, language):
        self.default_language_id = int(language)

    #
    # Enable or disable timeouts for connections
    #
    # @param  bool      t       true to enable timeouts, false to disable timeouts
    #
    def setTimeouts(self, t):
        self.use_timeouts = int(t)


    def getTimeout(self, method):
        if self.use_timeouts == 1:
            return self.timeout[method];
        else:
            return 120

    #
    # API functions
    #

    #
    # Test API
    #
    # @return test message or error
    #

    def test(self):
        data = {}
        data['method'] = 'test'
        url = self.baseurl + 'test?access_token=' + self.access_token
        return self.get_content(url, data)

    #
    # Get available languages
    #
    # @return list of languages or error
    #

    def languages(self):
        data = {}
        data['method'] = 'languages'
        url = self.baseurl + 'languages?access_token=' + self.access_token
        return self.get_content(url, data)

    #
    # SUBMISSIONS
    #

    #
    # Get submission by ID
    #
    # @param  integer  id         id of the submission
    # @param  array    params     SphereCompilers: 
    #                                  'withSource' => bool,
    #                                  'withInput' => bool,
    #                                  'withOutput' => bool,
    #                                  'withStderr' => bool,
    #                                  'withCmpinfo' => bool
    #                              SphereProblems: 
    #                                  not applicable
    # @return submission info as dictionary or error
    # 
    def getSubmission(self, id, params={}):
        data = {}
        if self.type == 'SC':
            data = {
                'withSource': int(params['withSource']) if 'withSource' in params else 0,
                'withInput': int(params['withInput']) if 'withInput' in params else 0,
                'withOutput': int(params['withOutput']) if 'withOutput' in params else 0,
                'withStderr': int(params['withStderr']) if 'withStderr' in params else 0,
                'withCmpinfo': int(params['withCmpinfo']) if 'withCmpinfo' in params else 0
                }
        data['access_token'] = self.access_token
        data['method'] = 'getSubmission'
        url = self.baseurl + 'submissions/' + str(id)
        return self.get_content(url, 'GET', data)   


    #
    # Send submission
    #
    # @param  array    params     SphereCompilers: 
    #                                  'source' => string,
    #                                  'language' => integer,
    #                                  'input' => string,
    #                              SphereProblems: 
    #                                  'problemCode' => string, (required)
    #                                  'language' => integer, (required)
    #                                  'source' => string, (required)
    #                                  'contestCode' => string,
    #                                  'userId' => integer,
    #                                  'private' => bool,
    # @return submission id or error
    # 
    def sendSubmission(self, params={}):
        if self.type == 'SC':
            data = {
                'sourceCode': params['source'] if 'source' in params else '',
                'language': int(params['language']) if 'language' in params else self.default_language_id,
                'input': params['input'] if 'input' in params else ''
                }
        elif self.type == 'SP':
            data = {
                'problemCode': params['problemCode'] if 'problemCode' in params else 'TEST',
                'languageId': int(params['language']) if 'language' in params else self.default_language_id,
                'source': params['source'] if 'source' in params else '',
                'contestCode': params['contestCode'] if 'contestCode' in params else '',
                'userId': int(params['userId']) if 'userId' in params else 0,
                'private': int(params['private']) if 'private' in params else 0
                }
        data['method'] = 'sendSubmission'
        url = self.baseurl + 'submissions?access_token=' + self.access_token
        return self.get_content(url, 'POST', data)

    #
    # PROBLEMS
    #

    #
    # Get problems (SphereProblems only)                       CHYBA TU JEST PAGINACJA??
    #
    # @return problem list or error
    # 
    def problems(self):
        data = {}
        data['method'] = 'problems'
        if self.type == 'SP':
            url = self.baseurl + 'problems?access_token=' + self.access_token
            return self.get_content(url, 'GET', data)
        else:
            return 'Error: action available only for Sphere Problem service'

    #
    # Get problem info (SphereProblems only)
    #
    # @param  string    problemCode    Code of the problem
    # @return problem info as dictionary or error
    # 
    def getProblem(self, problemCode):
        data = {}
        data['method'] = 'getProblem'
        data['access_token'] = self.access_token
        if self.type == 'SP':
            url = self.baseurl + 'problems/' + problemCode
            return self.get_content(url, 'GET', data);
        else:
            return 'Error: action available only for Sphere Problem service';

    #
    # API connection
    #

    def get_content(self, url, type='GET', data={}):
        method = data['method'] if 'method' in data else 'test'
        data.pop('method', None)
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
            response = urllib2.urlopen(req, timeout=self.getTimeout(method))
            return response.read()
        except urllib2.URLError, e:
            return 'ERROR: timeout or other exception'


