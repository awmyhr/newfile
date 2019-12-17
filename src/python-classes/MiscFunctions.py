#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-
# Author:     awmyhr <awmyhr@gmail.com>
# Contact:    awmyhr <awmyhr@gmail.com>
# Project:    newfile
# Proj Home:  https://github.com/awmyhr/newfile
# Copyright:  2019 awmyhr
# License:    Apache-2.0
# Revised:    20191217-152829
# Created:    2019-12-10
''' My misc, generally useful Python functions '''
#===============================================================================
from __future__ import absolute_import  #: Require parens to group imports PEP-0328
from __future__ import division         #: Enable 3.x True Division PEP-0238
from __future__ import with_statement   #: Clean up some uses of try/except PEP--343
from __future__ import print_function   #: Makes print a function, not a statement PEP-3105
from __future__ import unicode_literals #: Introduce bytes type for older strings PEP-3112
import logging
import os
#------------------------------------------------------------------------------
__cononical_name__ = 'MiscFunctions'
#------------------------------------------------------------------------------
##--==
#==============================================================================
#-- MiscFunctions v2.0.0
#==============================================================================
def get_temp(directory=None, stem=None):
    '''Creates a temporary file (or directory), returning the path.
    Defaults to file.

    Args:
        program (str): Name of program to find.

    Returns:
        For directory: absolute path to directory as a string.
        For a file: a tuple with OS-level handle to an open file.
    '''
    logger = logging.getLogger(__cononical_name__)
    logger.debug('Called: get_temp(stem=%s, directory: %s)', stem, directory)

    if stem is None:
        try:
            stem = __cononical_name__
        except NameError:
            stem = __name__

    import tempfile
    if directory is not None and directory.lower() in 'directory':
        return tempfile.mkdtemp(prefix='%s-d.' % stem)
    return tempfile.mkstemp(prefix='%s.' % stem)

#==============================================================================
def get_timestamp(time_format=None):
    '''Return date in specified format

    Args:
        time_format (str): Format string for timestamp. Compatible w/'date'.

    Returns:
        The formatted timestamp as a string.
    '''
    logger = logging.getLogger(__cononical_name__)
    logger.debug('Called: get_timestamp(%s)', time_format)

    import time
    if time_format is None:
        try:
            time_format = __default_dsf__
        except NameError:
            time_format = "%Y%m%d-%H%M%S"
    return time.strftime(time_format.strip('+'))

#==============================================================================
def is_valid_ipv4(ipaddr):
    '''Checks if passed paramater is a valid IPv4 address'''
    logger = logging.getLogger(__cononical_name__)
    logger.debug('Called: is_valid_ipv4(%s)', ipaddr)

    parts = ipaddr.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(p) < 256 for p in parts)
    except ValueError:
        return False

#==============================================================================
def set_value(filename, key, value):
    '''Add or change a KEY to a VALUE in a FILE, creating FILE if necessary.

    Args:
        filename (str): File to create/modify
        key (str) :     Key to create/modify
        value (str):    Value to set key to

    Returns:
        Success/failure as a Boolean.
    '''
    logger = logging.getLogger(__cononical_name__)
    logger.debug('Called: set_value(file=%s, key=%s, value=%s)', filename, key, value)

    raise NotImplementedError('TODO: implement set_value().')

#==============================================================================
def which(program):
    '''Test if a program exists in $PATH.

    Args:
        program (str): Name of program to find.

    Returns:
        String to use for program execution.

    Note:
        Originally found this here:
        http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    '''
    logger = logging.getLogger(__cononical_name__)
    logger.debug('Called: which(%s)', program)

    def _is_exe(fpath):
        ''' Private test for executeable '''
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, _ = os.path.split(program)
    if fpath:
        if _is_exe(program):
            logger.debug('Found %s here.', program)
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if _is_exe(exe_file):
                logger.debug('Found %s here: %s', program, exe_file)
                return exe_file

    logger.debug('Could not find %s.', program)
    return None


##==---
#==============================================================================
if __name__ == '__main__':
    # from pprint import pprint
    print('testing 1, 2, 3...')

    print('=============================')
    print('get_temp()            : ' + str(get_temp()))
    print('get_temp("dir", "stuff"): ' + get_temp("dir", "stuff"))

    print('=============================')
    print('is_valid_ipv4("123.123.123.123"): %s' % is_valid_ipv4("123.123.123.123"))
    print('is_valid_ipv4("nopenotatall")   : %s' % is_valid_ipv4("nopenotatall"))

    print('=============================')
