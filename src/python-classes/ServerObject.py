#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-
# Author:     awmyhr <awmyhr@gmail.com>
# Contact:    awmyhr <awmyhr@gmail.com>
# Project:    newfile
# Proj Home:  https://github.com/awmyhr/newfile
# Copyright:  2019 awmyhr
# License:    Apache-2.0
# Revised:    20191213-150515
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
#-- UserObject v0.1.0
#==============================================================================
class ServerObject(object): #: pylint: disable=useless-object-inheritance
    ''' Hold server access data '''
    __version = '0.1.0'

    _api_path = None
    _api_url = None
    _base_url = None
    _cookies_used = False
    _insecure = False
    _name = None
    _token_needed = False
    _token_url = None

    def __init__(self, name=None, api_path=None, base_url=None, cookies_used=False,
                 insecure=False, api_url=None, token_needed=False, token_url=None):
        import logging
        self.logger = logging.getLogger(__cononical_name__)
        self.logger.debug('Initiallizing ServerObject version %s.', self.__version)
        if name is None:
            raise ValueError('name is a required paramater.')
        if api_path is None and api_url is None:
            raise ValueError('either api_path or api_url is required.')
        self.name = name
        self.insecure = insecure
        self.base_url = base_url
        self.cookies_used = cookies_used
        self.api_path = api_path
        self.api_url = api_url
        self.token_needed = token_needed
        self.token_url = token_url

    def __str__(self):
        return 'Data for authkey %s' % self.name

    def __repr__(self):
        params = []
        if self._name is not None:
            params.append('name="%s"' % self.name)
        if self._insecure is not False:
            params.append('insecure="%s"' % self.insecure)
        if self._base_url is not None:
            params.append('base_url="%s"' % self.base_url)
        if self._cookies_used is not False:
            params.append('cookies_used="%s"' % self.cookies_used)
        if self._api_path is not None:
            params.append('api_path="%s"' % self.api_path)
        if self._api_url is not None:
            params.append('api_url="%s"' % self.api_url)
        if self._token_needed is not False:
            params.append('token_needed="%s"' % self.token_needed)
        if self._token_url is not None:
            params.append('token_url="%s"' % self.token_url)
        return 'ServerObject(%s)' % ', '.join(params)

    @property
    def api_path(self):
        ''' instance property '''
        return self._api_path

    @api_path.setter
    def api_path(self, value):
        ''' property setter '''
        self._api_path = value

    @property
    def api_url(self):
        ''' instance property '''
        if self._api_url is None:
            return '%s/%s' % (self.base_url, self.api_path)
        return self._api_url

    @api_url.setter
    def api_url(self, value):
        ''' property setter '''
        self._api_url = value

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
    def cookies_used(self):
        ''' instance property '''
        return self._cookies_used

    @cookies_used.setter
    def cookies_used(self, value):
        ''' property setter '''
        if not isinstance(value, bool):
            raise ValueError('cookies_used requires bool')
        self._cookies_used = value

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
    def name(self):
        ''' instance property '''
        return self._name

    @name.setter
    def name(self, value):
        ''' property setter '''
        self._name = value

    @property
    def token_needed(self):
        ''' instance property '''
        return self._token_needed

    @token_needed.setter
    def token_needed(self, value):
        ''' property setter '''
        if not isinstance(value, bool):
            raise ValueError('token_needed requires bool')
        self._token_needed = value

    @property
    def token_url(self):
        ''' instance property '''
        return self._token_url

    @token_url.setter
    def token_url(self, value):
        ''' property setter '''
        self._token_url = value


##==---
#==============================================================================
if __name__ == '__main__':
    from pprint import pprint
    print('testing 1, 2, 3...')
    print('=============================')

    test1 = ServerObject(name='test1', api_path='api/v1')
    print(test1.api_url)
    print('-----------------------------')
    print('type: %s ; is ServerObject? %s' % (type(test1), isinstance(test1, ServerObject)))
    pprint(vars(test1))
    print(test1)
    print(repr(test1))

    print('=============================')
