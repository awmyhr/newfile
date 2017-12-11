#!/bin/sh
#-- NOTE: Default to POSIX shell/mode. Be mindful of your reasons before
#--       switching to Bash, and consider using Python instead...
#==============================================================================
#:"""
#: .. program:: install.sh
#:    :synopsis: Installs newfile and its template directory.
#:
#:    :copyright: 2016 awmyhr
#:    :license: Apache-2.0
#:
#: .. codeauthor:: awmyhr <awmyhr@gmail.com>
#:
#:"""
#==============================================================================
#-- Variables which are meta for the script should be dunders (__varname__)
#-- TODO: UPDATE meta vars
__version__='0.1.0-alpha' #: current version
__revised__='20171210-191357' #: date of most recent revision
__contact__='awmyhr <awmyhr@gmail.com>' #: primary contact for support/?'s
__synopsis__='Installs newfile and its template directory.'
__description__="
This script will install newfile and its template directory. The location of
the install depends on the user running the script:

    * Non-root user:

        * newfile -> \$HOME/bin/newfile
        * templates/ -> \$XDG_DATA_HOME/newfile/ or \$HOME/.local/share/newfile/

    * root user:

        * newfile -> /usr/local/bin/newfile
        * templates/ -> /usr/local/share/newfile/

It will also update the newfile executeable with the proper path.

WARNING: This *WILL* overwrite existing templates in the target path which have
the same name as the included templates.
"
#------------------------------------------------------------------------------
#-- The following few variables should be relatively static over life of script
__require_root__=0                      #: Whether the script requires root (1) or not (0)
__author__='awmyhr <awmyhr@gmail.com>' #: coder(s) of script
__created__='2017-12-10'               #: date script originlly created
__copyright__='2016 awmyhr' #: Copyright short name
__license__='Apache-2.0'
__cononical_name__='install.sh' #: static name, *NOT* os.path.basename(sys.argv[0])
__project_name__='newfile'  #: name of overall project, if needed
__project_home__='https://github.com/awmyhr/newfile'  #: where to find source/documentation
__template_version__='1.4.1'             #: version of template file used
#-- We are not using this variable for now.
# shellcheck disable=2034
__docformat__='reStructuredText en'      #: attempted style for documentation
__basename__="${0}" #: name script run as
#------------------------------------------------------------------------------
#-- The following are string formats (prepended with strfmt_)
#-- NOTE: (you can ignore ShellCheck [SC2059] errors in lines
#         where these are used)
strfmt_error="${__cononical_name__}: %s\\n"
#==============================================================================
_usage_options() {
    #:"""
    #: .. function:: _usage_options()
    #:
    #: Lists options usign format passed to it.
    #:
    #: :param str strfmt_option: The format to use.
    #:"""
    #-- TODO: UPDATE option list.
    strfmt_option="${1}"
    #-- We are using a variable to format data in printf
    # shellcheck disable=2059
    printf "${strfmt_option}" '--help, -h' 'Dislay this help'
    #-- We are using a variable to format data in printf
    # shellcheck disable=2059
    printf "${strfmt_option}" '--version ' 'Display version'
}

#==============================================================================
_usage() {
    #:"""
    #: .. function:: _usage()
    #:
    #: Provides usage information
    #:
    #: .. note::
    #:     GNU does not recommend short options for help/version.
    #:     I do not recommend short option for, nor display of, debug option.
    #:     but I do recommend short option for help.
    #:"""
    printf 'Usage: %s [options]\n\n' "${__basename__}"
    printf '%s\n\n' "${__synopsis__}"
    printf 'Options:\n'
    _usage_options '  %s     %s\n'
    printf '\n%s\n\n' "${__description__}"
    printf 'Created: %s  Contact: %s\n' "${__created__}" "${__contact__}"
    printf 'Revised: %s  Version: %s\n' "${__revised__}" "${__version__}"
    printf '(c) Copyright %s (License: %s)\n'   "${__copyright__}" "${__license__}"
    printf '%s, part of %s. Project home: %s\n' "${__cononical_name__}" \
                                                "${__project_name__}" \
                                                "${__project_home__}"
}

#==============================================================================
_usage_rest() {
    #:"""
    #: .. function:: _usage_rest()
    #:
    #: Provides usage information in Sphinx/ReST format.
    #:
    #:"""
    #
    char="%${#__cononical_name__}s" #
    #-- We are using a variable to format data in printf
    # shellcheck disable=2059
    printf "${char}\\n" | tr " " "="
    printf '%s\n' "${__cononical_name__}"
    #-- We are using a variable to format data in printf
    # shellcheck disable=2059
    printf "${char}\\n" | tr " " "="
    printf '\n'
    printf 'Synopsis\n'
    printf '%s\n\n' '--------'
    printf '**%s** [*options*]\n\n' "${__cononical_name__}" #: TODO: UPDATE usage
    printf 'Description\n'
    printf '%s\n\n' '-----------'
    printf '%s\n\n' "${__description__}"
    printf 'Options\n'
    printf '%s\n\n' '-------'
    _usage_options '.. option:: %s\n\n    %s\n\n'
    printf 'Author\n'
    printf '%s\n\n' '------'
    printf '%s\n\n' "${__author__}"
    printf 'Copyright\n'
    printf '%s\n\n' '------'
    printf '(c) Copyright %s (License: %s)\n\n' "${__copyright__}" "${__license__}"
}

#==============================================================================
_version() {
    #:"""
    #: .. function:: _version()
    #:
    #: Provides version information
    #:
    #: .. note::
    #:     GNU guidelines dictate adding copyright and license info
    #:     (see commented code.)
    #:
    #: .. warning::
    #:     HOWEVER, this may not always be desierable.
    #:     If not, REMOVE these lines -- do NOT leave them commented!
    #:"""
    printf '%s (%s) %s\n' "${__cononical_name__}" "${__project_name__}" "${__version__}"
    #-- TODO: UPDATE license - a boilerplate notice should go here as well
    # printf '%s\n' "${__copyright__}"
    # printf '%s\n' "${__license__}"
}

#==============================================================================
_debug_info() {
    #:"""
    #: .. function:: _debug_info()
    #:
    #: Provides meta info for debug-level output
    #:
    #: .. note::
    #:     We set script_path here to avoid calling cd/dirname/pwd when not really needed
    #:"""
    # shellcheck disable=SC1007
    script_path="$(CDPATH= cd -- "$(dirname -- "${0}")" && pwd )"

    printf 'DEBUG    Cononical: %s\n' "${__cononical_name__}"
    printf 'DEBUG    Abs Path:  %s\n' "${script_path}/${__basename__}"
    printf 'DEBUG    Args List: %s\n' "$@"
    printf 'DEBUG    Version:   %s\n' "${__version__}"
    printf 'DEBUG    Created:   %s\n' "${__created__}"
    printf 'DEBUG    Revised:   %s\n' "${__revised__}"
    printf 'DEBUG    Coder(s):  %s\n' "${__author__}"
    printf 'DEBUG    Contact:   %s\n' "${__contact__}"
    printf 'DEBUG    Project:   %s\n' "${__project_name__}"
    printf 'DEBUG    Project Home: %s\n' "${__project_home__}"
    printf 'DEBUG    Template Version: %s\n' "${__template_version__}"
    printf 'DEBUG    System:    %s\n' "$(uname -orv)"
    printf 'DEBUG    Hostname:  %s\n' "$(hostname)"
    printf 'DEBUG    [re]uid:   %s/%s\n' "$(id -ur)", "$(id -u)"
    printf 'DEBUG    PID/PPID:  %s/%s\n' "", "${PPID}"
    printf '\n%s\n' '----- start -----'
}

#==============================================================================
exit_error() {
    #:"""
    #: .. function:: exit_error()
    #:
    #: Report error and exit
    #:
    #: :param int error_number:  Number to use for Exit Code
    #: :param str error_string:  Short description of error
    #: .. note::
    #:     You may want to use ${LINENO} in the string this is called with.
    #: .. warning::
    #:     This function exits the script
    #:"""
    # shellcheck disable=SC2059
    printf "${strfmt_error}" "${2}" 1>&2
    exit "${1}"
}

#==============================================================================
_exit_trap() {
    #:"""
    #: .. function:: exit_trap()
    #:
    #: On terminal traps, run this before exit_error
    #:
    #: :param int trap_line: Line number trap caught on
    #: :param str trap_name: Short name of trap
    #:"""
    exit_error "${?}" "caught trap ${2} at line ${1}; exiting"
}

#==============================================================================
exit_clean() {
    #:"""
    #: .. function:: exit_clean()
    #:
    #: Clean up everything and exit gracefully
    #:"""
    [ "${script_debug}" = true ] && {
        set +o xtrace
        script_debug=false
        printf '%s\n' '------ end ------'
    }

    trap - INT TERM HUP
    exit 0
}

#==============================================================================
_init() {
    #:"""
    #: .. function:: init()
    #:
    #: Check for requirements, other set-up stuff
    #:"""
    #-- TODO: 'Initilize', check for requirements, etc...
    #--------------------------------------------------------------------------
    #-- Check if effectively root
    #--------------------------------------------------------------------------
    if [ "${__require_root__}" -eq 1 ] && [ "$(id -u)" -ne 0 ] ; then
      exit_error 77 'Must be run as root.'
    elif [ "$(id -u)" -eq 0 ] ; then
        BIN_PATH='/usr/local/bin'
        SHARE_PATH='/usr/local/share/newfile/'
    else
        BIN_PATH="${HOME}/bin"
        if [ "${XDG_DATA_HOME}+z" = 'z' ] ; then
            SHARE_PATH="${HOME}/.local/share/newfile/"
        else
            SHARE_PATH="${XDG_DATA_HOME}/newfile/"
        fi

    fi
    #--------------------------------------------------------------------------
}

#==============================================================================
#-- Check for debug flag & process
if [ "${*#*--debug}" != "${*}" ]; then
    _debug_info "$@"
    script_debug=true
    set -o xtrace
else
    script_debug=false
fi

#-- Some default settings
set -o errexit  # Exit if any statement returns non-true value
set -o nounset  # Exit if attempt to use an uninitialised variable

#:"""
#: .. note::
#:     Setting traps seprately for 2 reasons:
#:
#:         - Avoid calling "$(kill -l $((trap_num - 128)))" in exti_trap
#:         - Incase we want to handle them differently in the future
#:
#: .. describe:: Bug
#:     Passing LINENO may not be working as expected, need more real-world tests
#:"""
trap '_exit_trap ${LINENO} INT'  INT
trap '_exit_trap ${LINENO} TERM' TERM
trap '_exit_trap ${LINENO} HUP'  HUP

#-- Process options (ignore --debug, as we already checked)
#
# [ "${#}" -gt 0 ] && while :; do
while [ "${#}" -gt 0 ]; do  #
    case "${1}" in
        --debug)     ;;
        -h|--help)   _usage   && exit 0 ;;
        --help-rest) _usage_rest   && exit 0 ;;
        --version)   _version && exit 0 ;;
        --)          shift && break ;;
        -?*)         exit_error 64 "invalid option: ${1}" ;;
        *)           ;;
    esac

    shift
done

_init

#==============================================================================
#-- TODO: Do something more interesting here...

#==============================================================================
exit_clean
