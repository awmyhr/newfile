#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-
# Author:     awmyhr <awmyhr@gmail.com>
# Contact:    awmyhr <awmyhr@gmail.com>
# Project:    newfile
# Proj Home:  https://github.com/awmyhr/newfile
# Copyright:  2019 awmyhr
# License:    Apache-2.0
# Revised:    20191210
# Created:    2019-12-10
##--==
#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-
# ^^-- use utf-8 strings by default
#-- NOTE: Tabs and spaces do NOT mix!! '-tt' will flag violations as an error.{#
# pylint: disable=line-too-long
#-- line-too-long is inevitable with the Jinga2 strings #}
#===============================================================================
#-- Preamble v2.0.0
#===============================================================================
'''{#
    .. py:module:: python_script
    #}
    :program:`{{ script_name|default("TODO: CHANGEME", true) }}`
    ============================================================

    In addition to the options listed in help output, :program:`{{ script_name|default("TODO: CHANGEME", true) }}` includes
    the following 'hidden' options:

    .. option:: --help-rest

        Output usage information in Sphinx/reST-style markup.

    .. option:: --debug

        Output debug-level information.

    :synopsis: {{ script_synopsis|default("TODO: CHANGEME", true) }}

    :copyright: {{ software_copyright|default("TODO: CHANGEME", true) }}
    :license: {{ software_license|default("TODO: CHANGEME", true) }}

    .. codeauthor:: {{ full_name|default("TODO: CHANGEME", true) }} <{{ email|default("TODO: CHANGEME", true) }}>
'''
#===============================================================================
#-- Standard Imports
#-- NOTE: See __future__ documentation at https://docs.python.org/2/library/__future__.html
#--       This allows us to write Python 3 code for older version.
from __future__ import absolute_import  #: Require parens to group imports PEP-0328
from __future__ import division         #: Enable 3.x True Division PEP-0238
from __future__ import with_statement   #: Clean up some uses of try/except PEP--343
#-- These may break 2.5 compatibility
from __future__ import print_function   #: Makes print a function, not a statement PEP-3105
from __future__ import unicode_literals #: Introduce bytes type for older strings PEP-3112
try:
    import ConfigParser #: 'Easy' configuration parsing
except ImportError:
    import configparser as ConfigParser#: At some point this was required...
#-- NOTE: We use optparse for compatibility with python < 2.7 as
#--       argparse wasn't standard until 2.7 (2.7 deprecates optparse)
#--       As of 20161212 the template is coded for optparse only
import optparse     #: pylint: disable=deprecated-module
import logging      #: Python's standard logging facilities
import os           #: Misc. OS interfaces
import sys          #: System-specific parameters & functions
# import traceback    #: Print/retrieve a stack traceback
#==============================================================================
#-- Third Party Imports
#==============================================================================
#-- Require a minimum Python version
if sys.version_info <= (2, 6):
    sys.exit("Minimum Python version: 2.6")
#-- NOTE: default Python versions:
#--       RHEL4    2.3.4
#--       RHEL5    2.4.3
#--       RHEL6.0  2.6.5
#--       RHEL6.1+ 2.6.6
#--       RHEL7    2.7.5
#--       RHEL8    3.6.7 *(not confirmed)
#-- Recent Fedora versions (24/25) stay current on 2.7 (2.7.12 as of 20161212)
#==============================================================================
#==============================================================================
#-- Application Library Imports
#==============================================================================
#-- Variables which are meta for the script should be dunders (__varname__)
#-- TODO: Update meta vars
__version__ = '{{ version|default("TODO: CHANGEME", true) }}' #: current version
__revised__ = '20190705-153700' #: date of most recent revision
__contact__ = '{{ contact_name|default("TODO: CHANGEME", true) }} <{{ contact_email|default("TODO: CHANGEME", true) }}>' #: primary contact for support/?'s
__synopsis__ = '{{ script_synopsis|default("TODO: CHANGEME", true) }}'
__description__ = '''{{ script_description|default("TODO: CHANGEME", true) }}
'''
#------------------------------------------------------------------------------
#-- The following few variables should be relatively static over life of script
__author__ = ['{{ full_name|default("TODO: CHANGEME", true) }} <{{ email|default("TODO: CHANGEME", true) }}>'] #: coder(s) of script
__created__ = '{{ date|default("TODO: CHANGEME", true) }}'               #: date script originlly created
__copyright__ = '{{ software_copyright|default("TODO: CHANGEME", true) }}' #: Copyright short name
__license__ = '{{ software_license|default("TODO: CHANGEME", true) }}'
__cononical_name__ = '{{ script_name|default("TODO: CHANGEME", true) }}' #: static name, *NOT* os.path.basename(sys.argv[0])
__project_name__ = '{{ project_name|default("TODO: CHANGEME", true) }}'  #: name of overall project, if needed
__project_home__ = '{{ project_home|default("TODO: CHANGEME", true) }}'  #: where to find source/documentation
__template_version__ = '3.0.0'  #: version of template file used
#-- We are not using this variable for now.
__docformat__ = 'reStructuredText en'       #: attempted style for documentation
__basename__ = os.path.basename(sys.argv[0]) #: name script run as
#------------------------------------------------------------------------------
#-- Flags
__gnu_version__ = False #: If True print GNU version string (which includes copyright/license)
__require_root__ = False    #: Does script require root
#------------------------------------------------------------------------------
#-- Load in environment variables, or set defaults
__default_dsf__ = os.getenv('DEFAULT_TIMESTAMP') if 'DEFAULT_TIMESTAMP' in os.environ else "%Y%m%d-%H%M%S"
__logger_dsf__ = os.getenv('LOGGER_DSF') if 'LOGGER_DSF' in os.environ else __default_dsf__
__backup_dsf__ = os.getenv('BACKUP_DSF') if 'BACKUP_DSF' in os.environ else __default_dsf__
__logger_file__ = os.getenv('LOGGER_FILE') if 'LOGGER_FILE' in os.environ else None
__logger_lvl__ = os.getenv('LOGGER_LVL') if 'LOGGER_LVL' in os.environ else 'info'

EXIT_STATUS = None
#------------------------------------------------------------------------------
METAVARS = {
    'name': __cononical_name__,
    'basename': __basename__,
    'script': {
        'version': __version__,
        'revised': __revised__,
        'contact': __contact__,
        'synopsis': __synopsis__,
        'description': __description__,
        'author': __author__,
        'created': __created__,
        'copyright': __copyright__,
        'license': __license__,
        'cononical_name': __cononical_name__,
        'project_name': __project_name__,
        'project_home': __project_home__,
        'template_version': __template_version__,
        'docformat': __docformat__,
        'basename': __basename__
    },
    'flags': {
        'gnu_version': __gnu_version__,
        'require_root': __require_root__
    },
    'env': {
        'default_dsf': __default_dsf__,
        'logger_dsf': __logger_dsf__,
        'backup_dsf': __backup_dsf__,
        'logger_file': __logger_file__,
        'logger_lvl': __logger_lvl__
    }
}


##==---
#==============================================================================