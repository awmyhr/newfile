#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-
''' Tail end of most my Python scripts '''
# Author:     awmyhr <awmyhr@gmail.com>
# Contact:    awmyhr <awmyhr@gmail.com>
# Project:    newfile
# Proj Home:  https://github.com/awmyhr/newfile
# Copyright:  2019 awmyhr
# License:    Apache-2.0
# Revised:    20191218-113351
# Created:    2019-12-10
from __future__ import absolute_import  #: Require parens to group imports PEP-0328
from __future__ import division         #: Enable 3.x True Division PEP-0238
from __future__ import with_statement   #: Clean up some uses of try/except PEP--343
from __future__ import print_function   #: Makes print a function, not a statement PEP-3105
from __future__ import unicode_literals #: Introduce bytes type for older strings PEP-3112
import logging      #: Python's standard logging facilities
import os           #: Misc. OS interfaces
import sys          #: System-specific parameters & functions
#------------------------------------------------------------------------------
__cononical_name__ = 'Postscript'
EXIT_STATUS = None
METAVARS = {
    'name': __cononical_name__,
    'basename': 'postscript.py',
    'flags': {'require_root': False}
}
class Setup(object): #: pylint: disable=useless-object-inheritance,too-few-public-methods
    ''' dummy class for testing '''
    _logger = logging.getLogger(__cononical_name__)
    args = None
    mvars = None
    debug = False
    _is_init_done = False

    def __init__(self, args=None, mvars=None):
        if Setup._is_init_done:
            pass
        else:
            Setup._logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            console.setFormatter(formatter)
            Setup._logger.addHandler(console)
            if Setup.args is None:
                Setup.args = args
            if Setup.mvars is None:
                Setup.mvars = mvars
            Setup._is_init_done = True

##--==
#==============================================================================
#-- Postscript v2.1.0
#==============================================================================
def main():
    ''' This is where the magic takes place '''
    options = Setup()
    logger = logging.getLogger(options.mvars['name'])
    logger.debug('Starting main()')
    #-- TODO: Do something more interesting here...{#
    logger.debug('This is a debug message.')
    logger.info('This is a info message.')
    logger.warning('This is a warn message.')
    logger.error('This is a error message.')
    logger.critical('This is a critical message.')

    print('This is normal text.')
    # Leave the next line, it is part of the Jinja templating
    #}


#==============================================================================
if __name__ == '__main__':
    #-- Parse configs/envs/options and set up logging
    OPTS = Setup(args=sys.argv[1:], mvars=METAVARS)
    LOGGER = logging.getLogger(OPTS.mvars['name'])
    if OPTS.mvars['flags']['require_root'] and os.getegid() != 0:
        LOGGER.error('Must be run as root.')
        sys.exit(77)

    #-- NOTE: "except Exception as variable:" syntax was added in 2.6, previously
    #         one would use "except Exception, variable:", but that is not
    #         compatible with 3.x. In order to be compatible with 2.5 (for RHEL 5)
    #         and forward, we use "execpt Exception:", then on the first line of
    #         the exception use "_, error, _ = sys.exc_info()". HOWEVER, pylint
    #         will no longer be able to warn on object members...
    #         type, value, traceback = sys.exc_info()
    try:
        main()
    except SystemExit as error: # Catches sys.exit()
        #_, error, _ = sys.exc_info()
        LOGGER.debug('Caught SystemExit')
        LOGGER.warning('%s: [SystemExit] %s', OPTS.mvars['basename'], error)
    except KeyboardInterrupt: # Catches Ctrl-C
        LOGGER.debug('Caught Ctrl-C')
        EXIT_STATUS = 130
    except (OSError, IOError) as error:
        #_, error, _ = sys.exc_info()
        LOGGER.debug('Caught OSError')
        if error.errno is None:
            LOGGER.critical('%s: [OSError]: %s', OPTS.mvars['basename'], error)
            EXIT_STATUS = 10
        elif error.errno == 2:                #: No such file/directory
            LOGGER.critical('%s: [OSError] %s: %s', OPTS.mvars['basename'],
                            error, error.filename
                           )
            EXIT_STATUS = os.EX_UNAVAILABLE
        elif error.errno == 13:                #: Permission Denied
            LOGGER.critical('%s: [OSError] %s: %s', OPTS.mvars['basename'],
                            error, error.filename
                           )
            EXIT_STATUS = os.EX_NOPERM
        else:
            LOGGER.critical('%s: [OSError] %s', OPTS.mvars['basename'], error)
            EXIT_STATUS = error.errno
    except Exception as error:                   #: pylint: disable=broad-except
        #_, error, _ = sys.exc_info()
        LOGGER.debug('Caught Exception: %s', sys.exc_info())
        LOGGER.critical('%s: %s', OPTS.mvars['basename'], error)
        EXIT_STATUS = 10
    else:
        LOGGER.debug('main() exited cleanly.')
        if EXIT_STATUS is None:
            EXIT_STATUS = os.EX_OK
    #-- NOTE: "try..except..finally" does not work pre 2.5
    finally:
        LOGGER.debug('Mandatory clean-up.')
        if EXIT_STATUS is None:
            LOGGER.debug('EXIT_STATUS is still None.')
            EXIT_STATUS = 20
        if OPTS.debug:
            print('\n------ end ------\n')
        logging.shutdown()
        sys.exit(EXIT_STATUS)
    #-- NOTE: more exit codes here:
    #--   https://docs.python.org/2/library/os.html#process-management
##==---
#==============================================================================
