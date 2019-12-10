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
''' My base class for dealing with options and configurations '''
#===============================================================================
from __future__ import absolute_import  #: Require parens to group imports PEP-0328
from __future__ import division         #: Enable 3.x True Division PEP-0238
from __future__ import with_statement   #: Clean up some uses of try/except PEP--343
from __future__ import print_function   #: Makes print a function, not a statement PEP-3105
from __future__ import unicode_literals #: Introduce bytes type for older strings PEP-3112
import logging      #: Python's standard logging facilities
import ConfigParser
#-- NOTE: We use optparse for compatibility with python < 2.7 as
#--       argparse wasn't standard until 2.7 (2.7 deprecates optparse)
#--       As of 20161212 the template is coded for optparse only
import optparse #: pylint: disable=deprecated-module
import os
import sys
#==============================================================================
#-- These are only here to support the class
__version__ = '0.1.0-alpha'
__revised__ = '20191210-114118'
__contact__ = 'awmyhr <awmyhr@gmail.com>'
__synopsis__ = 'Experiments with the CyberArk API'
__description__ = '''Functionality to be added.
'''
__author__ = ['awmyhr <awmyhr@gmail.com>']
__created__ = '2019-12-10'
__copyright__ = '2019, awmyhr'
__license__ = 'TODO: CHANGEME'
__gnu_version__ = False #: If True print GNU version string (which includes copyright/license)
__cononical_name__ = 'RunOptions'
__project_name__ = 'nixTools from *NIXLand'
__project_home__ = 'https://github.com/awmyhr/nixTools'
__basename__ = os.path.basename(sys.argv[0]) #: name script run as
##--==
#==============================================================================
class _ModOptionParser(optparse.OptionParser):
    ''' By default format_epilog() strips newlines, we don't want that,
        so we override.
    '''

    def format_epilog(self, formatter):
        ''' We'll preformat the epilog in the decleration, just pass it through '''
        return self.epilog


#==============================================================================
class _ReSTHelpFormatter(optparse.HelpFormatter):
    ''' Format help for Sphinx/ReST output.

    NOTE: All over-ridden methods started life as copy'n'paste from original's
          source code.

    '''

    def __init__(self, indent_increment=0, max_help_position=4, width=80, short_first=0):
        optparse.HelpFormatter.__init__(self, indent_increment,
                                        max_help_position, width, short_first
                                       )

    def format_usage(self, usage):
        retval = ['%s\n' % ('=-'[self.level] * len(__cononical_name__))]
        retval.append('%s\n' % (__cononical_name__))
        retval.append('%s\n\n' % ('=-'[self.level] * len(__cononical_name__)))
        retval.append('%s' % self.format_heading('Synopsis'))
        retval.append('**%s** %s\n\n' % (__cononical_name__, usage))
        return ''.join(retval)

    def format_heading(self, heading):
        return '%s\n%s\n\n' % (heading, '--'[self.level] * len(heading))

    def format_description(self, description):
        if description:
            retval = ['%s' % self.format_heading('Description')]
            retval.append('%s\n' % self._format_text(description))
            return ''.join(retval)
        return ''

    def format_option(self, option):
        opts = self.option_strings[option]
        retval = ['.. option:: %s\n\n' % opts]
        if option.help:
            # help_text = self.expand_default(option)
            # help_lines = textwrap.wrap(help_text, self.help_width)
            retval.append('%4s%s\n\n' % ('', self.expand_default(option)))
            # retval.extend(['%4s%s\n' % ('', line)
            #                for line in help_lines[1:]])
        elif opts[-1] != '\n':
            retval.append('\n')
        return ''.join(retval)

    def format_option_strings(self, option):
        ''' Return a comma-separated list of option strings & metavariables. '''
        if option.takes_value():
            metavar = option.metavar or option.dest.upper()
            short_opts = ['%s <%s>' % (sopt, metavar)
                          for sopt in option._short_opts] #: pylint: disable=protected-access
                                                          #: We're over-riding the default
                                                          #:    method, keeping most the code.
                                                          #:    Not sure how else we'd do this.
            long_opts = ['%s=<%s>' % (lopt, metavar)
                         for lopt in option._long_opts]   #: pylint: disable=protected-access
        else:
            short_opts = option._short_opts               #: pylint: disable=protected-access
            long_opts = option._long_opts                 #: pylint: disable=protected-access

        if self.short_first:
            opts = short_opts + long_opts
        else:
            opts = long_opts + short_opts

        return ', '.join(opts)


#==============================================================================
class Initilize(object):
    ''' Parse the configuration and options; set up logging

        Returns:
            An object containing settings.

    '''
    __version = '2.0.0'

    _defaults = {
        'debug': False,
    }

    _arguments = None
    _configs = None
    _options = None

    @property
    def args(self):
        ''' Class property '''
        if self._arguments is not None:
            return self._arguments
        return None

    @property
    def debug(self):
        ''' Class property '''
        if self._options is not None:
            return self._options.debug
        return self._defaults['debug']

    @property
    def ansible_called(self):
        ''' Class property '''
        return bool(__basename__.startswith('ansible_module'))

    def __init__(self, args=None, vars=None):
        if vars is None:
            raise ValueError('A metavars dict is required!')
        self.logger = logging.getLogger(vars['name'])
        self.logger.setLevel(logging.DEBUG)
        if self._configs is not None:
            raise ValueError('Configs already initialized.')
        self._configs = self._load_configs(vars['name'])
        if self._options is not None:
            raise ValueError('Arguments already initialized.')
        (self._options, self._arguments) = self._parse_args(args, vars['script'])
        self._init_logger()

    def _load_configs(self, name):
        parser = ConfigParser.SafeConfigParser(defaults=self._defaults)
        parser.read([os.path.expanduser('~/.%s' % name),
                     '%s.cfg' % name])
        #-- TODO: Define possible sections
        if not parser.has_section('debug'):
            parser.add_section('debug')
        return parser

    def _parse_args(self, args, script):
        #-- Parse Options (rely on OptionsParser's exception handling)
        description_string = script['synopsis']
        epilog_string = ('\n%s\n\n'
                         'Created: %s  Contact: %s\n'
                         'Revised: %s  Version: %s\n'
                         '%s, part of %s. Project home: %s\n'
                        ) % (script['description'], script['created'],
                             script['contact'], script['revised'],
                             script['version'], script['cononical_name'],
                             script['project_name'], script['project_home']
                            )
        usage_string = '%s [options]' % (script['basename'])
        version_string = '%s (%s) %s' % (script['cononical_name'],
                                         script['project_name'], script['version'])
        if __gnu_version__:
            version_string += '\nCopyright %s\nLicense %s\n' % (script['copyright'],
                                                                script['license'])
        parser = _ModOptionParser(version=version_string, usage=usage_string,
                                  description=description_string, epilog=epilog_string)
        #-- TODO: Add options, also set _default and @property (if needed).
        #-- Visible Options
        #   These can *not* be set in a config file
        #   These could be set in a config file

        #-- Hidden Options
        #   These can *not* be set in a config file
        parser.add_option('--help-rest', dest='helprest', action='store_true',
                          help=optparse.SUPPRESS_HELP, default=None)
        #   These could be set in a config file
        parser.add_option('--debug', dest='debug', action='store_true',
                          help=optparse.SUPPRESS_HELP,
                          default=self._configs.get('debug', 'debug'))

        parsed_opts, parsed_args = parser.parse_args(args)
        if parsed_opts.helprest:
            parser.formatter = _ReSTHelpFormatter()
            parser.usage = '[*options*]'         #: pylint: disable=attribute-defined-outside-init
                                                 #: Not yet sure of a better way to do this...
            parser.description = script['description'] #: pylint: disable=attribute-defined-outside-init
            parser.epilog = '\nAuthor\n------\n\n%s\n' % ('; '.join(script['author']))
            parser.print_help()
            sys.exit(os.EX_OK)
        #-- Put any option validation here...

        return parsed_opts, parsed_args

    def _init_logger(self):
        ''' Initilze logger '''
        if self.debug:
            level = logging.DEBUG
            formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s',
                                          __logger_dsf__
                                         )
        else:
            if __logger_lvl__.isdigit():
                if int(__logger_lvl__) > 49:
                    level = logging.CRITICAL
                elif int(__logger_lvl__) < 10:
                    level = logging.NOTSET
                else:
                    level = (int(__logger_lvl__)) //10 * 10
            else:
                level = logging.getLevelName(__logger_lvl__.upper())
            #-- Yes, we are going to ignore unknown values by setting to INFO
            if isinstance(level, str) and level.startswith('Level'):
                level = logging.INFO
            formatter = logging.Formatter('%(message)s')

        #-- Console output
        console = logging.StreamHandler()
        console.setLevel(level)
        console.setFormatter(formatter)
        self.logger.addHandler(console)

        #-- File output
        if __logger_file__:
            if os.path.isfile(__logger_file__):
                os.rename(__logger_file__, '%s.%s' % (__logger_file__, timestamp(__backup_dsf__)))
            #: NOTE: In Python >= 2.6 normally I give FileHandler 'delay="true"'
            logfile = logging.FileHandler(__logger_file__)
            logfile.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s.%(msecs)d:%(levelno)s:%(name)s.%(funcName)s:%(lineno)d:%(message)s',
                __logger_dsf__
                )
            logfile.setFormatter(formatter)
            self.logger.addHandler(logfile)
            global __logger_file_set__               #: pylint: disable=global-statement
            __logger_file_set__ = True

        import platform #: Easily get platforms identifying info
        self.logger.debug('Version:   %s (%s) %s', __cononical_name__, __project_name__, __version__)
        self.logger.debug('Created:   %s / Revised: %s', __created__, __revised__)
        self.logger.debug('Abs Path:  %s', os.path.abspath(sys.argv[0]))
        self.logger.debug('Full Args: %s', ' '.join(sys.argv[:]))
        self.logger.debug('Python:    %s (%s)', sys.executable, platform.python_version())
        self.logger.debug('Coder(s):  %s', __author__)
        self.logger.debug('Contact:   %s', __contact__)
        self.logger.debug('Project Home: %s', __project_home__)
        self.logger.debug('Template Version: %s', __template_version__)
        self.logger.debug('System:    %s', platform.system_alias(platform.system(),
                                                                platform.release(),
                                                                platform.version()
                                                               )
                        )
        self.logger.debug('Platform:  %s', platform.platform())
        self.logger.debug('Hostname:  %s', platform.node())
        self.logger.debug('Logname:   %s', os.getlogin())
        self.logger.debug('[re]uid:  %s/%s', os.getuid(), os.geteuid())
        self.logger.debug('PID/PPID:  %s/%s', os.getpid(), os.getppid())
        if self.options._options is not None:             #: pylint: disable=protected-access
            self.logger.debug('Parsed Options: %s', self.options._options) #: pylint: disable=protected-access
        if self.debug:
            print('\n----- start -----\n')
        return


##==---
#==============================================================================
