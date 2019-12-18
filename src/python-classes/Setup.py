#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-
# Author:     awmyhr <awmyhr@gmail.com>
# Contact:    awmyhr <awmyhr@gmail.com>
# Project:    newfile
# Proj Home:  https://github.com/awmyhr/newfile
# Copyright:  2019 awmyhr
# License:    Apache-2.0
# Revised:    20191218-113351
# Created:    2019-12-10
''' My base class for dealing with options and configurations '''
#===============================================================================
from __future__ import absolute_import  #: Require parens to group imports PEP-0328
from __future__ import division         #: Enable 3.x True Division PEP-0238
from __future__ import with_statement   #: Clean up some uses of try/except PEP--343
from __future__ import print_function   #: Makes print a function, not a statement PEP-3105
from __future__ import unicode_literals #: Introduce bytes type for older strings PEP-3112
import os
import sys
#------------------------------------------------------------------------------
__cononical_name__ = 'Setup'
METAVARS = {
    u'name': u'Setup',
    u'basename': 'setup.py',
    u'env': {
        u'backup_dsf': '+%Y%m%d-%H%M%S',
        u'default_dsf': '+%Y%m%d-%H%M%S',
        u'logger_dsf': '+%Y%m%d-%H%M%S',
        u'logger_file': None,
        u'logger_lvl': u'info'
    },
    u'flags': {u'gnu_version': False, u'require_root': False},
    u'script': {
        u'author': [u'Test Author <test.author@test.com>'],
        u'basename': 'setup.py',
        u'cononical_name': u'Setup',
        u'contact': u' <Test Contact <test.contact@test.com>>',
        u'copyright': u'Test CR',
        u'created': u'2019-12-17',
        u'description': u'Test data for METAVARS\n',
        u'docformat': u'reStructuredText en',
        u'license': u'Test Lic',
        u'project_home': u'Project Home',
        u'project_name': u'Project Name',
        u'revised': u'20191217-125940',
        u'synopsis': u'dummy data for METAVARS for testing.',
        u'template_version': u'3.0.0',
        u'version': u'2.0.0'
    }
}
#------------------------------------------------------------------------------
##--==
#==============================================================================
#-- Setup v2.0.0
#==============================================================================
#-- NOTE: We use optparse for compatibility with python < 2.7 as
#--       argparse wasn't standard until 2.7 (2.7 deprecates optparse)
#--       As of 20161212 the template is coded for optparse only
import optparse #: pylint: disable=deprecated-module,wrong-import-position
import logging #: pylint: disable=wrong-import-position
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

    def __init__(self, name=None):
        optparse.HelpFormatter.__init__(self, indent_increment=0, max_help_position=4,
                                        width=80, short_first=0
                                       )
        self.name = name

    def format_usage(self, usage):
        retval = ['%s\n' % ('=-'[self.level] * len(self.name))]
        retval.append('%s\n' % (self.name))
        retval.append('%s\n\n' % ('=-'[self.level] * len(self.name)))
        retval.append('%s' % self.format_heading('Synopsis'))
        retval.append('**%s** %s\n\n' % (self.name, usage))
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
class Setup(object): #: pylint: disable=useless-object-inheritance
    '''Parse the configuration and options; set up logging

    Args:
        args  (list): sys.argv[1:]
        mvars (dict): The METAVARS dict from Preamble

    Returns:
        An object containing settings.'''
    __version = '2.2.0'

    _defaults = {
        'debug': False
    }

    _arguments = None
    _configs = None
    _init_done = False
    _logger = logging.getLogger(__cononical_name__)
    _logger_file_set = False
    _mvars = None
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
    def mvars(self):
        ''' Class property '''
        return self._mvars

    @property
    def ansible_called(self):
        ''' Class property '''
        return bool(self.mvars['basename'].startswith('ansible_module'))

    def __init__(self, args=None, mvars=None):
        if Setup._mvars is None:
            if not isinstance(mvars, dict):
                raise ValueError('A metavars dict is required on first call!')
            Setup._mvars = mvars
        if Setup._configs is None:
            Setup._configs = self._load_configs(self.mvars['name'])
        if Setup._options is None:
            (Setup._options, Setup._arguments) = self._parse_args(args, self.mvars['script'])

        if self._init_done:
            self._logger.debug('Additional instnace of Setup ready.')
        else:
            self._logger.setLevel(logging.DEBUG)
            self._init_logger(self.mvars['env'])
            self._logger.debug('Initialized Setup version %s.', self.__version)
            if self.debug or self._logger_file_set:
                self._debug_info(self.mvars['script'])
            Setup._init_done = True

    def __str__(self):
        return 'Configuration data for %s.' % self.mvars['name']

    def __repr__(self):
        return 'Setup(args=sys.argv[1:], mvars=METAVARS)'

    def _load_configs(self, name):
        try:
            import ConfigParser #: 'Easy' configuration parsing
        except ImportError:
            import configparser as ConfigParser#: At some point this was required...
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
        if self.mvars['flags']['gnu_version']:
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
            parser.formatter = _ReSTHelpFormatter(name=script['cononical_name'])
            parser.usage = '[*options*]'         #: pylint: disable=attribute-defined-outside-init
                                                 #: Not yet sure of a better way to do this...
            parser.description = script['description'] #: pylint: disable=attribute-defined-outside-init
            parser.epilog = '\nAuthor\n------\n\n%s\n' % ('; '.join(script['author']))
            parser.print_help()
            sys.exit(os.EX_OK)
        #-- Put any option validation here...

        return parsed_opts, parsed_args

    def _init_logger(self, env):
        ''' Initilze logger '''
        if self.debug:
            level = logging.DEBUG
            formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s',
                                          env['logger_dsf']
                                         )
        else:
            if env['logger_lvl'].isdigit():
                if int(env['logger_lvl']) > 49:
                    level = logging.CRITICAL
                elif int(env['logger_lvl']) < 10:
                    level = logging.NOTSET
                else:
                    level = (int(env['logger_lvl'])) //10 * 10
            else:
                level = logging.getLevelName(env['logger_lvl'].upper())
            #-- Yes, we are going to ignore unknown values by setting to INFO
            if isinstance(level, str) and level.startswith('Level'):
                level = logging.INFO
            formatter = logging.Formatter('%(message)s')

        #-- Console output
        console = logging.StreamHandler()
        console.setLevel(level)
        console.setFormatter(formatter)
        self._logger.addHandler(console)

        #-- File output
        if env['logger_file']:
            import time
            if os.path.isfile(env['logger_file']):
                os.rename(env['logger_file'], '%s.%s' % (env['logger_file'],
                                                         time.strftime(env['backup_dsf']).strip('+')))
            #: NOTE: In Python >= 2.6 normally I give FileHandler 'delay="true"'
            logfile = logging.FileHandler(env['logger_file'])
            logfile.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s.%(msecs)d:%(levelno)s:%(name)s.%(funcName)s:%(lineno)d:%(message)s',
                env['logger_dsf']
                )
            logfile.setFormatter(formatter)
            self._logger.addHandler(logfile)
            self._logger_file_set = True

    def _debug_info(self, script):
        import platform #: Easily get platforms identifying info
        self._logger.debug('Version:   %s (%s) %s', script['cononical_name'],
                           script['project_name'], script['version'])
        self._logger.debug('Created:   %s / Revised: %s', script['created'], script['revised'])
        self._logger.debug('Abs Path:  %s', os.path.abspath(sys.argv[0]))
        self._logger.debug('Full Args: %s', ' '.join(sys.argv[:]))
        self._logger.debug('Python:    %s (%s)', sys.executable, platform.python_version())
        self._logger.debug('Coder(s):  %s', script['author'])
        self._logger.debug('Contact:   %s', script['contact'])
        self._logger.debug('Project Home: %s', ['project_home'])
        self._logger.debug('Template Version: %s', script['template_version'])
        self._logger.debug('System:    %s', platform.system_alias(platform.system(),
                                                                  platform.release(),
                                                                  platform.version()
                                                                 )
                          )
        self._logger.debug('Platform:  %s', platform.platform())
        self._logger.debug('Hostname:  %s', platform.node())
        self._logger.debug('Logname:   %s', os.getlogin())
        self._logger.debug('[re]uid:  %s/%s', os.getuid(), os.geteuid())
        self._logger.debug('PID/PPID:  %s/%s', os.getpid(), os.getppid())
        if self._options is not None:
            self._logger.debug('Parsed Options: %s', self._options)
        if self.debug:
            print('\n----- start -----\n')


##==---
#==============================================================================
if __name__ == '__main__':
    from pprint import pprint
    print('testing 1, 2, 3...')

    print('=============================')
    test1 = Setup(args=sys.argv[1:], mvars=METAVARS)
    print('-----------------------------')
    pprint(vars(test1))
    pprint(test1.mvars)

    print('=============================')
    test2 = Setup()
    print('-----------------------------')
    pprint(vars(test2))
    pprint(test2.mvars)

    print('=============================')
    print(test1)
    print(repr(test1))
    print('type: %s ; is Setup? %s' % (type(test1), isinstance(test1, Setup)))
    print('-----------------------------')
    print(test1.__doc__)
    print('=============================')
