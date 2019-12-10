#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-
''' Tail end of most my Python scripts '''
# Author:     awmyhr <awmyhr@gmail.com>
# Contact:    awmyhr <awmyhr@gmail.com>
# Project:    newfile
# Proj Home:  https://github.com/awmyhr/newfile
# Copyright:  2019 awmyhr
# License:    Apache-2.0
# Revised:    20191210
# Created:    2019-12-10
from __future__ import absolute_import  #: Require parens to group imports PEP-0328
from __future__ import division         #: Enable 3.x True Division PEP-0238
from __future__ import with_statement   #: Clean up some uses of try/except PEP--343
from __future__ import print_function   #: Makes print a function, not a statement PEP-3105
from __future__ import unicode_literals #: Introduce bytes type for older strings PEP-3112
import logging      #: Python's standard logging facilities
import os           #: Misc. OS interfaces
import sys          #: System-specific parameters & functions
##--==
#==============================================================================
#-- Postscript v2.0.0
#==============================================================================
def main(options):
    ''' This is where the action takes place
    '''
    logger = logging.getLogger(options.mvars['name'])
    logger.debug('Starting main()')
    #-- TODO: Do something more interesting here...{#
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')

    # print('%sAnsible Called: %s' % (colors._colors['cf_white'], options.ansible_called))
    # c = colors()
    # print('%sAnsible Called: %s%s' % (c.white, c.reset, options.ansible_called))
    # print('%sAnsible Called: %s' % (colors.white, options.ansible_called))
    # from pprint import pprint
    # print('%sAnsible Called: %s' % (colors._colors['cf_white'], options.ansible_called))
    # print (options._options)
    # print(timestamp())
    # print('FILE')
    # tempfile = get_temp()
    # print(tempfile)
    # os.remove(tempfile[1])
    # print('DIR')
    # tempdir = get_temp('dir')
    # print(tempdir)
    # os.rmdir(tempdir)
    # print('THING')
    # tempthing = get_temp('dat')
    # print(tempthing)
    # os.remove(tempthing[1])
    # print(__logger_file_set__)
    # raise OSError('Testing 1 2 3')
    # set_value('file', 'key', 'value')
    #}


#==============================================================================
if __name__ == '__main__':
    #-- Parse configs/envs/options and set up logging
    OPTS = Initilize(args=sys.argv[1:], mvars=METAVARS)
    # logger = logging.getLogger(OPTS.mvars['name'])
    if OPTS.mvars['flags']['require_root'] and os.getegid() != 0:
        OPTS.logger.error('Must be run as root.')
        sys.exit(77)

    #-- NOTE: "except Exception as variable:" syntax was added in 2.6, previously
    #         one would use "except Exception, variable:", but that is not
    #         compatible with 3.x. In order to be compatible with 2.5 (for RHEL 5)
    #         and forward, we use "execpt Exception:", then on the first line of
    #         the exception use "_, error, _ = sys.exc_info()". HOWEVER, pylint
    #         will no longer be able to warn on object members...
    #         type, value, traceback = sys.exc_info()
    try:
        main(OPTS)
    except SystemExit as error: # Catches sys.exit()
        #_, error, _ = sys.exc_info()
        OPTS.logger.debug('Caught SystemExit')
        OPTS.logger.warning('%s: [SystemExit] %s', OPTS.mvars['basename'], error)
    except KeyboardInterrupt: # Catches Ctrl-C
        OPTS.logger.debug('Caught Ctrl-C')
        EXIT_STATUS = 130
    except (OSError, IOError) as error:
        #_, error, _ = sys.exc_info()
        OPTS.logger.debug('Caught OSError')
        if error.errno is None:
            OPTS.logger.critical('%s: [OSError]: %s', OPTS.mvars['basename'], error)
            EXIT_STATUS = 10
        elif error.errno == 2:                #: No such file/directory
            OPTS.logger.critical('%s: [OSError] %s: %s', OPTS.mvars['basename'],
                                 error, error.filename
                                )
            EXIT_STATUS = os.EX_UNAVAILABLE
        elif error.errno == 13:                #: Permission Denied
            OPTS.logger.critical('%s: [OSError] %s: %s', OPTS.mvars['basename'],
                                 error, error.filename
                                )
            EXIT_STATUS = os.EX_NOPERM
        else:
            OPTS.logger.critical('%s: [OSError] %s', OPTS.mvars['basename'], error)
            EXIT_STATUS = error.errno
    except Exception as error:                   #: pylint: disable=broad-except
        #_, error, _ = sys.exc_info()
        OPTS.logger.debug('Caught Exception: %s', sys.exc_info())
        OPTS.logger.critical('%s: %s', OPTS.mvars['basename'], error)
        EXIT_STATUS = 10
    else:
        OPTS.logger.debug('main() exited cleanly.')
        if EXIT_STATUS is None:
            EXIT_STATUS = os.EX_OK
    #-- NOTE: "try..except..finally" does not work pre 2.5
    finally:
        OPTS.logger.debug('Mandatory clean-up.')
        if EXIT_STATUS is None:
            OPTS.logger.debug('EXIT_STATUS is still None.')
            EXIT_STATUS = 20
        if OPTS.debug:
            print('\n------ end ------\n')
        logging.shutdown()
        sys.exit(EXIT_STATUS)
    #-- NOTE: more exit codes here:
    #--   https://docs.python.org/2/library/os.html#process-management
##==---
#==============================================================================
