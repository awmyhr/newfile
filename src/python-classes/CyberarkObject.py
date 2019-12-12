#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-
# Author:     awmyhr <awmyhr@gmail.com>
# Contact:    awmyhr <awmyhr@gmail.com>
# Project:    newfile
# Proj Home:  https://github.com/awmyhr/newfile
# Copyright:  2019 awmyhr
# License:    Apache-2.0
# Revised:    20191212-093309
# Created:    2019-12-12
''' My base class for dealing with CyberArk's APIs '''
#===============================================================================
from __future__ import absolute_import  #: Require parens to group imports PEP-0328
from __future__ import division         #: Enable 3.x True Division PEP-0238
from __future__ import with_statement   #: Clean up some uses of try/except PEP--343
from __future__ import print_function   #: Makes print a function, not a statement PEP-3105
from __future__ import unicode_literals #: Introduce bytes type for older strings PEP-3112
import logging
import sys
import RestUtil
#------------------------------------------------------------------------------
__cononical_name__ = 'CyberarkObject'
#------------------------------------------------------------------------------
##--==
#===============================================================================
#-- CyberarkObject v0.1.0
#==============================================================================
class CyberarkObject(object): #: pylint: disable=useless-object-inheritance
    ''' Class for interacting with CyberArk API '''
    __version = '0.1.0'


##==---
#==============================================================================
