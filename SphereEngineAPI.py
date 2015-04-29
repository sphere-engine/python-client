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
# @version    0.6
#
import urllib
import urllib2



class SphereEngineAPI:
    """SphereEngineAPI"""

    def __init__(self, access_token, url_compilers=None, url_problems=None):
        self.compilers = SphereEngineCompilersAPI(access_token, url_compilers)
        self.problems = SphereEngineProblemsAPI(access_token, url_problems)

    #
    # Set default language
    #
    # @param  integer      language       id of the language
    #
    def setDefaultLanguage(self, language):
        self.compilers.setDefaultLanguage(language)
        self.problems.setDefaultLanguage(language)

    #
    # Enable or disable timeouts for connections
    #
    # @param  bool      t       true to enable timeouts, false to disable timeouts
    #
    def setTimeouts(self, t):
        self.compilers.setTimeouts(t)
        self.problems.setTimeouts(t)


class SphereEngineCompilersAPI:
    """SphereEngineCompilersAPI"""

    def __init__(self, access_token, url=None):
        self.version = 3
        self.access_token = access_token
        self.default_language_id = 11 # hardcoded C language
        self.use_timeouts = 1

        self.timeout = {
            'test': 5,
            'languages': 5,
            'getSubmission': 5,
            'sendSubmission': 10,
        }

        if url == None:
            self.baseurl = 'http://api.compilers.sphere-engine.com/api/' + str(self.version) + '/'
        else:
            self.baseurl = url

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
    # Test API
    #
    # @return test message or error
    #

    def test(self):
        url = self.baseurl + 'test?access_token=' + self.access_token
        return SphereEngineREST.get_content(url, 'GET', self.getTimeout('test'))

    #
    # Get available languages
    #
    # @return list of languages or error
    #

    def languages(self):
        url = self.baseurl + 'languages?access_token=' + self.access_token
        return SphereEngineREST.get_content(url, 'GET', self.getTimeout('languages'))

    #
    # Get submission by ID
    #
    # @param  integer   id                    id of the submission
    # @param  bool      withSource            include source in response
    # @param  bool      withInput             include input in response
    # @param  bool      withOutput            include output in response
    # @param  bool      withStderr            include stderr info in response
    # @param  bool      withCmpinfo           include cmpinfo in response
    #
    # @return submission info as dictionary or error
    # 
    def getSubmission(self, id, withSource=False, withInput=False, withOutput=False, withStderr=False, withCmpinfo=False):
        data = {
            'withSource': int(withSource),
            'withInput': int(withInput),
            'withOutput': int(withOutput),
            'withStderr': int(withStderr),
            'withCmpinfo': int(withCmpinfo),
            'access_token': self.access_token,
            }
        url = self.baseurl + 'submissions/' + str(id)
        return SphereEngineREST.get_content(url, 'GET', self.getTimeout('getSubmission'), data)   


    #
    # Send submission
    #
    # @param  string    source        source code
    # @param  integer   language      language ID
    # @param  string    input         input for the program
    #
    # @return submission id or error
    # 
    def sendSubmission(self, source, language=None, input=''):
        data = {
            'sourceCode': source,
            'language': int(language) if language != None else self.default_language_id,
            'input': input,
            }
        url = self.baseurl + 'submissions?access_token=' + self.access_token
        return SphereEngineREST.get_content(url, 'POST', self.getTimeout('sendSubmission'), data)


class SphereEngineProblemsAPI:
    """SphereEngineProblemsAPI"""

    def __init__(self, access_token, url=None):
        self.version = 3
        self.access_token = access_token
        self.default_language_id = 11 # hardcoded C language
        self.use_timeouts = 1

        self.timeout = {
            'test': 5,
            'languages': 5,
            'getSubmission': 5,
            'sendSubmission': 10,
            'problemsList': 5,
            'getProblem': 5,
        }

        if url == None:
            self.baseurl = 'http://problems.sphere-engine.com/api/v' + str(self.version) + '/'
        else:
            self.baseurl = url

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
    # Test API
    #
    # @return test message or error
    #

    def test(self):
        url = self.baseurl + 'test?access_token=' + self.access_token
        return SphereEngineREST.get_content(url, 'GET', self.getTimeout('test'))

    #
    # Get available languages
    #
    # @return list of languages or error
    #

    def languages(self):
        url = self.baseurl + 'languages?access_token=' + self.access_token
        return SphereEngineREST.get_content(url, 'GET', self.getTimeout('languages'))

    #
    # Get submission by ID
    #
    # @param  integer   id                    id of the submission
    #
    # @return submission info as dictionary or error
    # 
    def getSubmission(self, id):
        url = self.baseurl + 'submissions/' + str(id) + '?access_token=' + self.access_token
        return SphereEngineREST.get_content(url, 'GET', self.getTimeout('getSubmission'))   


    #
    # Send submission
    #
    # @param  string       problemCode       code of the problem
    # @param  string       source            source code
    # @param  integer      language          language id
    # @param  string       contestCode       code of the contest
    # @param  integer      userId            user ID
    # @param  bool         private           flag for private submissions
    #
    # @return submission id or error
    # 
    def sendSubmission(self, problemCode, source, language=None, contestCode='', userId=0, private=False):
        data = {
            'problemCode': problemCode,
            'source': source,
            'languageId': int(language) if language != None else self.default_language_id,
            'contestCode': contestCode,
            'userId': int(userId),
            'private': int(private),
            }
        url = self.baseurl + 'submissions?access_token=' + self.access_token
        return SphereEngineREST.get_content(url, 'POST', self.getTimeout('sendSubmission'), data)

    #
    # Get problems                       CHYBA TU JEST PAGINACJA??
    #
    # @return problem list or error
    # 
    def problemsList(self):
        url = self.baseurl + 'problems?access_token=' + self.access_token
        return SphereEngineREST.get_content(url, 'GET', self.getTimeout('problemsList'))

    #
    # Get problem info
    #
    # @param  string    problemCode    Code of the problem
    # @return problem info as dictionary or error
    # 
    def getProblem(self, problemCode):
        url = self.baseurl + 'problems/' + problemCode + '?access_token=' + self.access_token
        return SphereEngineREST.get_content(url, 'GET', self.getTimeout('problemsList'))
        
    
class SphereEngineREST:
    """SphereEngineREST"""
    @staticmethod
    def get_content(url, type='GET', timeout=10, data={}):
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


