#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-
# Author:     awmyhr <awmyhr@gmail.com>
# Contact:    awmyhr <awmyhr@gmail.com>
# Project:    newfile
# Proj Home:  https://github.com/awmyhr/newfile
# Copyright:  2019 awmyhr
# License:    Apache-2.0
# Revised:    20191216-141452
# Created:    2019-12-13
''' Hold user login and related data '''
#==============================================================================
from __future__ import absolute_import  #: Require parens to group imports PEP-0328
from __future__ import division         #: Enable 3.x True Division PEP-0238
from __future__ import with_statement   #: Clean up some uses of try/except PEP--343
from __future__ import print_function   #: Makes print a function, not a statement PEP-3105
from __future__ import unicode_literals #: Introduce bytes type for older strings PEP-3112
# import logging
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
        paths      (dict): Holds filesystem paths for user data.
            paths['cache']  (str): User cache path.
            paths['config'] (str): User configuration path.
            paths['temp']   (str): User temp path.

    If authkey is not passed, then username/password are reqrired.
    If either of those are not passed, they will be asked for.

    Returns:
        An UserObject.'''
    import logging
    __version = '0.3.0'

    _defaults = {
        'paths': {'cache': None, 'config': None, 'temp': None}
    }
    _logger = logging.getLogger(__cononical_name__)

    @classmethod
    def _is_tty(cls):
        ''' class method to check if console is a tty '''
        from sys import stdout
        if stdout.isatty():
            return True
        return False

    @property
    def client_id(self):
        ''' instance property '''
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        ''' property setter '''
        self._client_id = value

    @property
    def paths(self):
        ''' instance property '''
        return self._paths

    @paths.setter
    def paths(self, value):
        ''' property setter '''
        if value is None:
            self._paths = self._defaults['paths'].copy()
        elif not isinstance(value, dict):
            ValueError('Argument paths excpects a dict with one or more keys: cache, config, temp')
        else:
            for key in value:
                if key not in ['cache', 'config', 'temp']:
                    self._logger.debug('Unknown path key: %s', key)
                self._paths[key] = value[key]

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
        if value is None:
            return
        if self._authkey is None:
            self._authkey = value
        else:
            self._gen_authkey()
            if self._authkey != value:
                raise ValueError('Username/Password authkey do not match passed authkey (%s / %s).'
                                 % (self._authkey, value))

    def __init__(self, username=None, password=None, authkey=None, client_id=None,
                 paths=None):
        self._logger.debug('Initiallizing UserObject version %s.', self.__version)
        if authkey is None:
            if username is None:
                if self._is_tty():
                    username = raw_input('Username: ')
                else:
                    raise ValueError('Username/password or authkey is required.')
            if password is None:
                if self._is_tty():
                    import getpass
                    password = getpass.getpass('Password: ')
                else:
                    raise ValueError('Username/password or authkey is required.')
        self._username = username
        self._password = password
        self._authkey = authkey
        self._client_id = client_id
        #-- Initilize the paths dict before setting from args
        self._paths = self._defaults['paths'].copy()
        self.paths = paths

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
        if self._paths is not None:
            params.append('paths="%s"' % self.paths)
        return 'UserObject(%s)' % ', '.join(params)

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
    test1 = UserObject('test1', authkey='1test', paths={'temp': '/h/e/l/o'})
    print('test 1a:    %s / %s / %s / %s' % (test1.username, test1.password,
                                             test1.authkey, test1.client_id))
    test1.username = 'TEST1'
    test1.password = '1TEST'
    print('test 1b:    %s / %s / %s / %s' % (test1.username, test1.password,
                                             test1.authkey, test1.client_id))
    print('-----------------------------')
    print('test 1c:    %s - %s - %s' % (test1.paths['cache'], test1.paths['config'], test1.paths['temp']))
    test1.paths = {'cache': '/path/to/cache', 'config': '/config/path', 'temp': '/path/for/temp'}
    print('test 1d:    %s - %s - %s' % (test1.paths['cache'], test1.paths['config'], test1.paths['temp']))
    test1.paths['cache'] = '/a/diff/path'
    print('test 1e:    %s - %s - %s' % (test1.paths['cache'], test1.paths['config'], test1.paths['temp']))
    print('-----------------------------')
    pprint(vars(test1))

    # print('=============================')
    # test2 = UserObject('test2', '2test', 'dGVzdDI6MnRlc3Q=')
    # print('test 2a:    %s / %s / %s / %s' % (test2.username, test2.password,
    #                                          test2.authkey, test2.client_id))
    # test2.username = 'TEST2'
    # test2.password = '2TEST'
    # print('test 2b:    %s / %s / %s / %s' % (test2.username, test2.password,
    #                                          test2.authkey, test2.client_id))
    # print('-----------------------------')
    # pprint(vars(test2))

    print('=============================')
    print(test1)
    print(repr(test1))
    print('type: %s ; is UserObject? %s' % (type(test1), isinstance(test1, UserObject)))
    print('-----------------------------')
    print(test1.__doc__)
    print('=============================')
