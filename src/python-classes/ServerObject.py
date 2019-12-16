#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-
# Author:     awmyhr <awmyhr@gmail.com>
# Contact:    awmyhr <awmyhr@gmail.com>
# Project:    newfile
# Proj Home:  https://github.com/awmyhr/newfile
# Copyright:  2019 awmyhr
# License:    Apache-2.0
# Revised:    20191216-141510
# Created:    2019-12-13
''' Hold server access data '''
#==============================================================================
from __future__ import absolute_import  #: Require parens to group imports PEP-0328
from __future__ import division         #: Enable 3.x True Division PEP-0238
from __future__ import with_statement   #: Clean up some uses of try/except PEP--343
from __future__ import print_function   #: Makes print a function, not a statement PEP-3105
from __future__ import unicode_literals #: Introduce bytes type for older strings PEP-3112
#------------------------------------------------------------------------------
__cononical_name__ = 'ServerObject'
#------------------------------------------------------------------------------
##--==
#===============================================================================
#-- UserObject
#==============================================================================
class ServerObject(object): #: pylint: disable=useless-object-inheritance
    '''Hold server/API access data

        Args:
            name          (str): Required. Server name as a string.
            base_url      (str): Over-ride default base url. Default: http://name
            insecure     (bool): Ignore SSL verification?    Default: False
            api           (str): Relative path or full URL.
            api          (dict): API specific information.
                api['path']: (str): Path of API relative to base url.
                api['url']:  (str): Over-ride full URL for API.
            cookies       (str): Path to cookie file. Default: None
            token         (str): Relative path or full URL. Default: None
            token        (dict): Information about token. Default: None
                token['file'] (str): Path to token file. Default: $TMP/.$USER-__cononical_name__
                token['path'] (str): Path of Token auth relative to base url.
                token['url']  (str): Full URL for Token authentication.

        A value for api is required. If it's a string, an attempt will be made
            to identify if its a valid URL or not. If not, it is assumed to be
            a relative path. If no value is passed, a dict without a path
            or url key is passed, or an unuseable value is passed, a ValueError
            will be raised.
        If token is None (the default), then token authentication is not used.
            Otherwise, if a string is passed then it will be processed like api
            above and the default value will be used for the file key. Path is
            relative to the API url. If a dict is passed, either a path or a
            url key is required. If an unuseable value is passed, a ValueError
            will be raised.
        If cookies is None, then cookies will not be used. Otherwise, should be
            valid filesystem path to a writeable file.

        Returns:
            A ServerObject.'''
    __version = '0.2.0'

    _defaults = {
        'api': {'path': None, 'url': None},
        'token': {'file': None, 'path': None, 'url': None}
    }

    def __init__(self, name=None, base_url=None, insecure=False, api=None,
                 cookies=None, token=None):
        import logging
        self._logger = logging.getLogger(__cononical_name__)
        self._logger.debug('Initiallizing ServerObject version %s.', self.__version)
        if name is None:
            raise ValueError('name is a required paramater.')
        if api is None:
            raise ValueError('api is a required paramater.')
        self._name = name
        self._insecure = insecure
        self._base_url = base_url
        self._cookies = cookies
        self._api = self._defaults['api']
        self._token = self._defaults['token']

        self.api = api
        self.token = token

    def __str__(self):
        return 'Data for server %s' % self.name

    def __repr__(self):
        params = []
        if self._name is not None:
            params.append('name="%s"' % self.name)
        if self._insecure is not False:
            params.append('insecure="%s"' % self.insecure)
        if self._base_url is not None:
            params.append('base_url="%s"' % self.base_url)
        if self._cookies is not None:
            params.append('cookies="%s"' % self.cookies)
        if self._api is not None:
            params.append('api="%s"' % self.api)
        if self._token is not None:
            params.append('token="%s"' % self.token)
        return 'ServerObject(%s)' % ', '.join(params)

    @property
    def name(self):
        ''' instance property '''
        return self._name

    @name.setter
    def name(self, value):
        ''' property setter '''
        self._name = value

    @property
    def base_url(self):
        ''' instance property '''
        if self._base_url is None:
            return 'https://%s' % self.name
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        ''' property setter '''
        self._base_url = value

    @property
    def insecure(self):
        ''' instance property '''
        return self._insecure

    @insecure.setter
    def insecure(self, value):
        ''' property setter '''
        if not isinstance(value, bool):
            raise ValueError('insecure requires bool')
        self._insecure = value

    @property
    def cookies(self):
        ''' instance property '''
        return self._cookies

    @cookies.setter
    def cookies(self, value):
        ''' property setter '''
        self._cookies = value

    @property
    def api(self):
        ''' instance property '''
        return self._api

    @api.setter
    def api(self, value):
        ''' property setter '''
        if isinstance(value, dict):
            if 'path' in value:
                self._api['path'] = value['path']
                self._api['url'] = '%s/%s' % (self.base_url, self._api['path'])
            if 'url' in value:
                self._api['url'] = value['url']
            if 'url' not in value and 'path' not in value:
                raise ValueError('api dict does not include url or path (%s)' % value)
        elif isinstance(value, basestring):
            if self._is_url(value):
                self._api['url'] = value
            else:
                self._api['path'] = value
                self._api['url'] = '%s/%s' % (self.base_url, self._api['path'])
        else:
            raise ValueError('unuseable type for api (%s)' % type(value))

    @property
    def token(self):
        ''' instance property '''
        return self._token

    @token.setter
    def token(self, value):
        ''' property setter '''
        self._token = value

    @classmethod
    def _is_url(cls, value):
        ''' Check if a string looks like a web URL '''
        from urlparse import urlparse
        check = urlparse(value)
        if check.scheme in ['http', 'https']:
            return True
        return False


##==---
#==============================================================================
if __name__ == '__main__':
    from pprint import pprint
    print('testing 1, 2, 3...')
    print('=============================')

    test1 = ServerObject(name='test1', api='api/v1')
    print(test1.api)
    print('-----------------------------')
    pprint(vars(test1))
    print(test1)
    print(repr(test1))

    print('=============================')

    test2 = ServerObject(name='test2', api='http://otherserver/v1/api', cookies='/path/to/cooks')
    print(test2.api)
    print('-----------------------------')
    pprint(vars(test2))
    print(test2)
    print(repr(test2))

    # print('=============================')
    # print('type: %s ; is ServerObject? %s' % (type(test1), isinstance(test1, ServerObject)))
    # print(test1.__doc__)
    # print('=============================')
