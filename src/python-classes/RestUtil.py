#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-
# Author:     awmyhr <awmyhr@gmail.com>
# Contact:    awmyhr <awmyhr@gmail.com>
# Project:    newfile
# Proj Home:  https://github.com/awmyhr/newfile
# Copyright:  2019 awmyhr
# License:    Apache-2.0
# Revised:    20191211-140742
# Created:    2019-12-10
''' My base class for dealing with REST APIs '''
#===============================================================================
from __future__ import absolute_import  #: Require parens to group imports PEP-0328
from __future__ import division         #: Enable 3.x True Division PEP-0238
from __future__ import with_statement   #: Clean up some uses of try/except PEP--343
from __future__ import print_function   #: Makes print a function, not a statement PEP-3105
from __future__ import unicode_literals #: Introduce bytes type for older strings PEP-3112
import logging
import sys
#------------------------------------------------------------------------------
__cononical_name__ = 'RestUtil'
#------------------------------------------------------------------------------
##--==
#===============================================================================
#-- RestUtil v2.0.0
#==============================================================================
from cookielib import LWPCookieJar
from urllib import urlencode
import base64
import json
import time
try:
    import requests
except ImportError:
    raise ImportError('The python-requests module is required.')
#==============================================================================
class RestUtil(object): #: pylint: disable=useless-object-inheritance
    ''' Class for interacting with Satellite 6 API '''
    __version = '2.0.0'

    per_page = 100
    verbose = False

    def __init__(self, authkey=None, client_id=None, insecure=False,
                 cookiefile=None, tokenfile=None, tokenurl=None):
        self.logger = logging.getLogger(__cononical_name__)
        self.logger.debug('Initiallizing RestUtil version %s.', self.__version)
        self.logger.debug(locals())
        self.token_file = tokenfile
        self.cookie_file = cookiefile

        self.connection = self._new_connection(authkey=authkey, client_id=client_id, insecure=insecure)
        if client_id is not None:
            self.token = self._get_token(tokenfile=self.token_file, tokenurl=tokenurl)
            self.connection = self._new_connection(authkey=authkey, client_id=client_id, token=self.token, insecure=insecure)
        if self.cookie_file is not None:
            self.connection.cookies = LWPCookieJar(self.cookie_file)
            try:
                self.connection.cookies.load(ignore_discard=True)
            except IOError:
                pass
        self.results = {"success": None, "msg": None, "return": None}

    def __del__(self):
        self.logger.debug('Entering Function: %s', sys._getframe().f_code.co_name) #: pylint: disable=protected-access
        if self.token_file is not None:
            self.logger.debug('Saving token file: %s.', self.token_file)
            with open(self.token_file, 'w') as file_:
                json.dump(self.token, file_)
        if self.cookie_file is not None:
            self.logger.debug('Saving cookie file: %s.', self.cookie_file)
            try:
                self.connection.cookies.save(ignore_discard=True)
            except IOError:
                pass

    #===============================================================================
    #-- The following originates from a  StackOverflow thread titled
    #   "Check if a string matches an IP address pattern in Python".
    #   We are only interested in valid IPv4 addresses.
    #===============================================================================
    # https://stackoverflow.com/questions/3462784/check-if-a-string-matches-an-ip-address-pattern-in-python
    #===============================================================================
    @classmethod
    def is_valid_ipv4(cls, ipaddr):
        '''Checks if passed paramater is a valid IPv4 address'''
        parts = ipaddr.split('.')
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(p) < 256 for p in parts)
        except ValueError:
            return False

    @classmethod
    def get_authkey(cls, username, password):
        '''Return base64 encoded username/password'''
        return  base64.b64encode('%s:%s' % (username, password)).strip()

    # def _get_cookies(self):
    #     ''' Handle session cookie '''
    #     logger.debug('Entering Function: %s', sys._getframe().f_code.co_name) #: pylint: disable=protected-access
    #     self.cookies = LWPCookieJar(os.getenv("HOME") + "/.sat6_api_session")
    #     try:
    #         self.cookies.load(ignore_discard=True)
    #     except IOError:
    #         pass
    #     return self.cookies

    def _get_token(self, tokenfile=None, tokenurl=None):
        ''' Retrive a Bearer token

        Returns:
            Token as a dict

        '''
        self.logger.debug('Entering Function: %s', sys._getframe().f_code.co_name) #: pylint: disable=protected-access
        try:
            self.logger.debug('Attempting to load token file: %s.', tokenfile)
            with open(tokenfile, 'r') as file_:
                token = json.load(file_)
            if 'expires' not in token or int(time.time()) > int(token['expires']):
                self.logger.debug('Token file invalid or expired, getting new token.')
                self.logger.debug('Time: %s ; Token Exp: %s', int(time.time()), int(token['expires']))
                self.logger.debug('Token: %s', token)
                token = self.rest_call('get', tokenurl)
        except (IOError, AttributeError, TypeError, ValueError):
            self.logger.debug('Error with token file, requesting new token.')
            token = self.rest_call('get', tokenurl)
        if 'access_token' not in token:
            raise RuntimeError('Error: No access token. Only found: %s' % token)
        return token

    def _new_connection(self, authkey=None, client_id=None, token=None, insecure=False):
        ''' Create a Request session object

        Args:
            authkey (str):   User authorization key
            insecure (bool): If True do not validate SSL
            token (dict):    User token as a dict, need 'access_token'
            client_id (str): User client ID for controlled API access

        Returns:
            Requests session object.

        '''
        self.logger.debug('Entering Function: %s', sys._getframe().f_code.co_name) #: pylint: disable=protected-access

        connection = requests.Session()
        connection.headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
            'cache-control': 'no-cache'
        }
        if token is None:
            if authkey is not None:
                connection.headers['authorization'] = 'Basic %s' % authkey
        else:
            connection.headers['authorization'] = 'Bearer %s' % token['access_token']
        if client_id is not None:
            connection.headers['x-ibm-client-id'] = client_id
        self.logger.debug('Headers set: %s', connection.headers)
        connection.verify = not bool(insecure)

        return connection

    def rest_call(self, method, url, params=None, data=None, jsonin=None):
        ''' Call a REST API URL using method.

        Args:
            session_obj (obj): Session object
            method (str):      One of: get, put, post
            url (str):         URL of API
            params (dict):     Dict of params to pass to Requests.get

        Returns:
            Results of API call in a dict

        '''
        self.logger.debug('Entering Function: %s', sys._getframe().f_code.co_name) #: pylint: disable=protected-access
        results = {"success": None, "msg": None, "return": None}

        self.logger.debug('Calling URL: %s', url)
        self.logger.debug('Using method: %s', method)
        self.logger.debug('With Headers: %s', self.connection.headers)
        if params is not None:
            self.logger.debug('With params: %s', params)
        if jsonin is not None:
            self.logger.debug('With json: %s', jsonin)
        if data is not None:
            self.logger.debug('With data: %s', data)
            data = json.dumps(data)

        try:
            req_results = self.connection.request(method, url, params=params, data=data, json=jsonin)
            self.logger.debug('Final URL: %s', req_results.url)
            self.logger.debug('Return Headers: %s', req_results.headers)
            self.logger.debug('Status Code: %s', req_results.status_code)
            self.logger.debug('Results: %s', req_results.content)
            rjson = req_results.json()
            if not req_results.ok:
                if self.verbose:
                    self.logger.debug('Results: %s', rjson)
                if 'error' in rjson:
                    self.logger.debug('Requests API call returned error.')
                    if 'full_messages' in rjson['error']:
                        self.logger.error('\n'.join(rjson['error']['full_messages']))
                    else:
                        self.logger.error('Sorry, no further info, try --debug.')
                elif 'displayMessage' in rjson:
                    self.logger.debug(rjson['displayMessage'])
                    self.logger.error('Sorry, no useful info, try --debug.')
                else:
                    self.logger.error('Sorry, no error info, try --debug.')
            req_results.raise_for_status()
            results['success'] = True
            results['return'] = rjson
        except requests.exceptions.HTTPError as error:
            self.logger.debug('Caught Requests HTTP Error.')
            results['msg'] = '[HTTPError]: %s' % (error.message) #: pylint: disable=no-member
        except requests.exceptions.ConnectionError as error:
            self.logger.debug('Caught Requests Connection Error.')
            results['msg'] = '[ConnectionError]: %s' % (error.message) #: pylint: disable=no-member
        except requests.exceptions.Timeout as error:
            self.logger.debug('Caught Requests Timeout.')
            results['msg'] = '[Timeout]: %s' % (error.message) #: pylint: disable=no-member
        except requests.exceptions.RequestException as error:
            self.logger.debug('Caught Requests Exception.')
            results['msg'] = '[Requests]: REST call failed: %s' % (error.message) #: pylint: disable=no-member

        self.logger.debug('rest_call: %s', results['msg'])
        return results

    def find_item(self, url, search=None, field='name'):
        ''' Searches for and returns info for a Satellite 6 host.

        Args:
            hostname (str):        Name of host to find.

        Returns:

        '''
        self.logger.debug('Entering Function: %s', sys._getframe().f_code.co_name) #: pylint: disable=protected-access
        results = {"success": False, "msg": None, "return": None}

        if url is None:
            results['msg'] = 'Error: No url passed.'
        else:
            search_str = '%s~"%s"' % (field, search)

            results = self.rest_call('get', url,
                                     urlencode([('search', '' + str(search_str))]))
            if self.logger['return']['subtotal'] == 0:
                results['success'] = False
                results['msg'] = 'Warning: No matches for %s.' % search
            elif results['return']['subtotal'] > 1:
                results['success'] = False
                results['msg'] = 'Warning: Too many matches for %s (%s).' % (search, results['total'])
            else:
                results['success'] = True
                results['msg'] = 'Success: %s found.' % search
                results['return'] = results['return']['results'][0]

        self.logger.debug('find_item: %s', results['msg'])
        return results

    def get_item(self, url, label):
        ''' Searches for and returns info for a Satellite 6 host.

        Args:
            url (str):        url to hit.

        Returns:

        '''
        self.logger.debug('Entering Function: %s', sys._getframe().f_code.co_name) #: pylint: disable=protected-access
        results = {"success": False, "msg": None, "return": None}

        if url is None:
            results['msg'] = 'Error: No url passed.'
        else:
            results = self.rest_call('get', url)
            if 'error' in results['return']:
                #-- This is not likely to execute, as if the host ID is not
                #   found a 404 is thrown, which is caught by the exception
                #   handling mechanism, and the program will bomb out.
                #   Not sure I want to change that...
                results['success'] = False
                results['msg'] = 'Warning: %s not found.' % label
            else:
                results['success'] = True
                results['msg'] = 'Success: %s found.' % label

        self.logger.debug('get_item: %s', results['msg'])
        return results

    def get_list(self, url, search=None, field='name', per_page=None, params=None):
        ''' This returns a list of Satellite 6 Hosts.

        Returns:
            List of Hosts (dict). Of particular value will be

        '''
        self.logger.debug('Entering Function: %s', sys._getframe().f_code.co_name) #: pylint: disable=protected-access
        if per_page is None:
            per_page = self.per_page
        if params is None:
            params = {'page': 1, 'per_page': per_page}
        else:
            params['page'] = 1
            params['per_page'] = per_page
        if search is not None:
            if any(symbol in search for symbol in '=~!^'):
                params['search'] = search
            else:
                params['search'] = '%s~"%s"' % (field, search)
        item = 0
        page_item = 0

        results = self.rest_call('get', url, params)
        while item < results['return']['subtotal']:
            if page_item == per_page:
                params['page'] += 1
                page_item = 0
                results = self.rest_call('get', url, params)
            yield results['return']['results'][page_item]
            item += 1
            page_item += 1


##==---
#==============================================================================
