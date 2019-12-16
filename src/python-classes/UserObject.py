#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-
# Author:     awmyhr <awmyhr@gmail.com>
# Contact:    awmyhr <awmyhr@gmail.com>
# Project:    newfile
# Proj Home:  https://github.com/awmyhr/newfile
# Copyright:  2019 awmyhr
# License:    Apache-2.0
# Revised:    20191213-150457
# Created:    2019-12-13
''' Hold user login and related data '''
#==============================================================================
from __future__ import absolute_import  #: Require parens to group imports PEP-0328
from __future__ import division         #: Enable 3.x True Division PEP-0238
from __future__ import with_statement   #: Clean up some uses of try/except PEP--343
from __future__ import print_function   #: Makes print a function, not a statement PEP-3105
from __future__ import unicode_literals #: Introduce bytes type for older strings PEP-3112
#------------------------------------------------------------------------------
__cononical_name__ = 'UserObject'
#------------------------------------------------------------------------------
##--==
#===============================================================================
#-- UserObject
#==============================================================================
class UserObject(object): #: pylint: disable=useless-object-inheritance
    '''Hold user login and related data

        Args:
            username    (str): User string for login.
            password    (str): Password string for login.
            authkey     (str): Base64 string for login.
            client_id   (str): String required by some forms of login.
            cookie_file (str): Path to file for holding cookie data.
            token_file  (str): Path to file for holding token data.

        If authkey is not passed, then username/password are reqrired.
        If either of those are not passed, they will be asked for.

        Returns:
            An UserObject.'''
    __version = '0.2.0'

    _authkey = None
    _client_id = None
    _cookie_file = None
    _password = None
    _token_file = None
    _username = None

    def __init__(self, username=None, password=None, authkey=None, client_id=None,
                 cookie_file=None, token_file=None):
        import logging
        self.logger = logging.getLogger(__cononical_name__)
        self.logger.debug('Initiallizing UserObject version %s.', self.__version)
        if authkey is None:
            if username is None:
                username = raw_input('Username: ')
            if password is None:
                import getpass
                password = getpass.getpass('Password: ')
        self.username = username
        self.password = password
        self.client_id = client_id
        self.token_file = token_file
        self.cookie_file = cookie_file
        if authkey is not None:
            self.authkey = authkey

    def __str__(self):
        if self.username is not None:
            return 'Data for user %s' % self.username
        return 'Data for authkey %s' % self.authkey

    def __repr__(self):
        params = []
        if self._username is not None:
            params.append('username="%s"' % self.username)
        if self._password is not None:
            params.append('password="%s"' % self.password)
        if self._authkey is not None:
            params.append('authkey="%s"' % self.authkey)
        if self._client_id is not None:
            params.append('client_id="%s"' % self.client_id)
        if self._cookie_file is not None:
            params.append('cookie_file="%s"' % self.cookie_file)
        if self._token_file is not None:
            params.append('token_file="%s"' % self.token_file)
        return 'UserObject(%s)' % ', '.join(params)

    @property
    def client_id(self):
        ''' instance property '''
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        ''' property setter '''
        self._client_id = value

    @property
    def cookie_file(self):
        ''' instance property '''
        if self._cookie_file is None:
            import os
            return '%s/.%s-%s' % (os.getenv("HOME"), os.getenv('USER'), 'cookie')
        return self._cookie_file

    @cookie_file.setter
    def cookie_file(self, value):
        ''' property setter '''
        self._cookie_file = value

    @property
    def token_file(self):
        ''' instance property '''
        if self._token_file is None:
            import os
            import tempfile
            return '%s/.%s-%s' % (tempfile.gettempdir(), os.getenv('USER'), 'token')
        return self._token_file

    @token_file.setter
    def token_file(self, value):
        ''' property setter '''
        self._token_file = value

    @property
    def username(self):
        ''' instance property '''
        return self._username

    @username.setter
    def username(self, value):
        ''' property setter '''
        self._username = value
        self._gen_authkey()

    @property
    def password(self):
        ''' instance property '''
        return self._password

    @password.setter
    def password(self, value):
        ''' property setter '''
        self._password = value
        self._gen_authkey()

    @property
    def authkey(self):
        ''' instance property '''
        return self._authkey

    @authkey.setter
    def authkey(self, value):
        ''' property setter '''
        if self._authkey is None:
            self._authkey = value
        else:
            self._gen_authkey()
            if self._authkey != value:
                raise ValueError('Username/Password authkey do not match passed authkey (%s / %s).'
                                 % (self._authkey, value))

    def _gen_authkey(self):
        ''' instance function to generate base64 authkey '''
        if self.username is None or self.password is None:
            self._authkey = None
        else:
            import base64
            self._authkey = base64.b64encode('%s:%s' % (self.username, self.password)).strip()


##==---
#==============================================================================
if __name__ == '__main__':
    from pprint import pprint
    print('testing 1, 2, 3...')
    print('=============================')

    test1 = UserObject('test1', '1test')
    print('test 1a:    %s / %s / %s / %s' % (test1.username, test1.password,
                                             test1.authkey, test1.client_id))
    test1.username = 'TEST1'
    test1.password = '1TEST'
    print('test 1b:    %s / %s / %s / %s' % (test1.username, test1.password,
                                             test1.authkey, test1.client_id))
    print('cookie_file: %s' % (test1.cookie_file))
    print('token_file:  %s' % (test1.token_file))
    test1.cookie_file = '/path/to/cookie/file'
    test1.token_file = '/path/to/token/file'
    print('cookie_file: %s' % (test1.cookie_file))
    print('token_file:  %s' % (test1.token_file))
    print('-----------------------------')
    pprint(vars(test1))
    print(test1)
    print(repr(test1))

    print('=============================')

    test2 = UserObject('test2', '2test', 'dGVzdDI6MnRlc3Q=')
    print('test 2a:    %s / %s / %s / %s' % (test2.username, test2.password,
                                             test2.authkey, test2.client_id))
    test2.username = 'TEST2'
    test2.password = '2TEST'
    print('test 2b:    %s / %s / %s / %s' % (test2.username, test2.password,
                                             test2.authkey, test2.client_id))
    print('-----------------------------')
    pprint(vars(test2))
    print(test2)
    print(repr(test2))

    print('=============================')

    if isinstance(test2, UserObject):
        print('We got a UserObject')
    else:
        print('UserObject requried! We got a %s (%s)' % (type(test2), test2.__class__.__name__))
    print(test2.__doc__)
    print('=============================')
