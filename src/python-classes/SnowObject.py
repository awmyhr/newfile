#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-
# Author:     awmyhr <awmyhr@gmail.com>
# Contact:    awmyhr <awmyhr@gmail.com>
# Project:    newfile
# Proj Home:  https://github.com/awmyhr/newfile
# Copyright:  2019 awmyhr
# License:    Apache-2.0
# Revised:    20191211-140831
# Created:    2019-12-10
''' Class for working with ServiceNow '''
#==============================================================================
from __future__ import absolute_import  #: Require parens to group imports PEP-0328
from __future__ import division         #: Enable 3.x True Division PEP-0238
from __future__ import with_statement   #: Clean up some uses of try/except PEP--343
from __future__ import print_function   #: Makes print a function, not a statement PEP-3105
from __future__ import unicode_literals #: Introduce bytes type for older strings PEP-3112
import logging
import os
import sys
#------------------------------------------------------------------------------
__cononical_name__ = 'SnowObject'
#------------------------------------------------------------------------------
##--==
#===============================================================================
#-- SnowObject v2.0.0
#==============================================================================
import tempfile
import RestUtil
#==============================================================================
class SnowObject(object): #: pylint: disable=useless-object-inheritance
    ''' Class for interacting with ServiceNow API '''
    __version = '2.0.0'

    def __init__(self, server=None, authkey=None,
                 client_id=None, insecure=False, basepath=None):
        self.logger = logging.getLogger(__cononical_name__)
        self.logger.debug('Initiallizing SnowObject version %s.', self.__version)
        if server is None:
            raise RuntimeError('Must provide ServiceNow API server name.')
        if authkey is None:
            raise RuntimeError('Must provide authkey for access.')
        if client_id is None:
            raise RuntimeError('Must provide API Client ID.')

        self.url = 'https://%s/%s' % (server, basepath)
        self.compinsts = '%s/itsm-compute/compute/instances' % self.url

        tokenurl = '%s/authorization/token' % self.url
        tokenfile = '%s/.%s-%s' % (tempfile.gettempdir(),
                                   os.getenv('USER'),
                                   client_id.split("-")[0])
        self.util = RestUtil(authkey=authkey, client_id=client_id,
                             tokenfile=tokenfile, tokenurl=tokenurl,
                             insecure=insecure)
        self.results = {"success": None, "msg": None, "return": None, "entries": 0, "list": None}

    def get_host(self, hostname, rels=False):
        ''' Return SNOW info on a specific host

        Args:
            hostname (str):  Name of host to find.

        Returns:
            Info for a host (dict). Of particular value may be
            return['certname']
            return['ciFunction']
            return['environment']
            return['lifecycleStatus']

        '''
        self.logger.debug('Entering Function: %s', sys._getframe().f_code.co_name) #: pylint: disable=protected-access
        self.logger.debug('Looking for host: %s', hostname)
        self.results = {"success": None, "msg": None, "return": None, "entries": 0, "list": None}

        if hostname is None:
            self.results['success'] = False
            self.results['msg'] = 'Hostname passed was type None.'
            self.results['return'] = None
            self.logger.debug('Error: %s', self.results['msg'])
        else:
            if self.util.is_valid_ipv4(hostname):
                field = 'ipAddress'
            else:
                hostname = hostname.upper().split(".")[0]
                field = 'name'
            req_results = self.util.rest_call('get', self.compinsts, {field: hostname})
            req_return = req_results['return']
            if req_return['total'] == 0:
                self.results['success'] = False
                self.results['msg'] = 'No host matches for %s.' % hostname
                self.results['entries'] = 0
                self.results['return'] = None
                self.logger.debug('Error: %s', self.results['msg'])
            else:
                if rels:
                    count = 0
                    for item in req_return['items']:
                        req_return['items'][count]['relations'] = self.get_host_relations(item['id'])
                        req_return['items'][count]['costCenter'] = next((entry['parent'] for entry in req_return['items'][count]['relations'] if entry['type'] == "Expensed by::Expensed to"), None)
                        req_return['items'][count]['registeredOn'] = next((entry['child'] for entry in req_return['items'][count]['relations'] if entry['type'] == "Registered on::Has registered"), None)
                        req_return['items'][count]['hostedOn'] = next((entry['child'] for entry in req_return['items'][count]['relations'] if entry['type'] == "Hosted on::Hosts"), None)
                        count += 1
                if req_return['total'] > 1:
                    req_return['items'] = sorted(req_return['items'], key=lambda i: i['id'])
                    self.results['success'] = False
                    self.results['msg'] = 'Too many host matches for %s (%s).' % (hostname, req_return['total'])
                    self.results['entries'] = req_return['total']
                    self.results['list'] = req_return['items']
                    self.results['return'] = None
                    self.logger.debug('Error: %s', self.results['msg'])
                else:
                    self.results['success'] = True
                    self.results['msg'] = 'Found %s.' % hostname
                    self.results['entries'] = 1
                    self.results['list'] = req_return['items']
                    self.results['return'] = req_return['items'][0]
                    self.logger.debug('Success: %s', self.results['msg'])
        return self.results['return']


    def get_host_relations(self, hostid):
        ''' Return SNOW info on a specific host

        Args:
            hostname (str):  Name of host to find.

        Returns:
            Info for a host (dict). Of particular value may be
            return['certname']
            return['ciFunction']
            return['environment']
            return['lifecycleStatus']

        '''
        self.logger.debug('Entering Function: %s', sys._getframe().f_code.co_name) #: pylint: disable=protected-access
        self.logger.debug('Looking for host: %s', hostid)
        self.results = {"success": None, "msg": None, "return": None, "entries": 0, "list": None}

        if hostid is None:
            self.results['success'] = False
            self.results['msg'] = 'Host ID passed was type None.'
            self.results['return'] = None
            self.logger.debug('Error: %s', self.results['msg'])
        else:
            req_results = self.util.rest_call('get', '%s/%s/relationships' % (self.compinsts, hostid))
            req_return = req_results['return']
            self.results['return'] = req_return['items']
            self.results['entries'] = req_return['total']
            if self.results['return'] is None:
                self.results['success'] = False
            else:
                self.results['success'] = True
        return self.results['return']


##==---
#==============================================================================
