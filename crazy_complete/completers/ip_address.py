# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for IP addresses.'''

from .. import bash_versions
from .. import messages as m
from ..bash_complete import BashCompletionCode, BashCompletionFunc
from ..fish_complete import FishCompletionCommand, FishCompletionRawCommand
from ..zsh_complete import ZshComplFunc
from ..errors import CrazySchemaValidationError
from ..scheme_validator import check_type

CATEGORY = 'basic'

SYNOPSIS = r'''
['ip_address', <TYPE>]
'''

SHORT = 'Complete local IP addresses'

LONG = r'''
`TYPE`:
  The type of ip addresses to complete:

  - `ipv4`: IPv4 addresses
  - `ipv6`: IPv6 addresses
  - `all`:  Both IPv4 and IPv6 addresses

  Append `+` to include the unspecified address of the selected family:

  - `ipv4+`: Includes `0.0.0.0`
  - `ipv6+`: Includes `::`
  - `all+`:  Includes both 0.0.0.0 and `::`
'''

ALSO = {
    'net_interface': 'For completing network interfaces',
    'hostname': 'For completing hostnames',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--ip-address']
    complete: ['ip_address']

  - option_strings: ['--ip-address-v4']
    complete: ['ip_address', 'ipv4']

  - option_strings: ['--ip-address-v6']
    complete: ['ip_address', 'ipv6']
'''

OUTPUT = r'''
~ > example --ip-address=<TAB>
::1    10.0.0.71   127.0.0.1   fe80::f567:7a1a:3c98:808d

~ > example --ip-address-v4=<TAB>
10.0.0.71   127.0.0.1

~ > example --ip-address-v6=<TAB>
::1   fe80::f567:7a1a:3c98:808d
'''

_error = CrazySchemaValidationError


def validate(_ctxt, arguments):
    '''Validate YAML for ip_address completer'''
    type_ = arguments.get_optional_arg('all')
    arguments.require_no_more()
    check_type(type_, (str,), "type")

    allowed = ('ipv4', 'ipv6', 'all', 'ipv4+', 'ipv6+', 'all+')

    if type_.value not in allowed:
        allowed =  ', '.join(allowed)
        msg = '%s: %s' % ('type', m.invalid_value_expected_values(allowed))
        raise _error(msg, type_)


def bash(_completer, ctxt, _trace, type_='all'):
    '''Implement ip_address for bash'''
    func = bash_versions.ip_addresses(ctxt)

    if type_ == 'ipv4':
        return BashCompletionFunc(ctxt, [func])

    if type_ == 'ipv6':
        return BashCompletionFunc(ctxt, [func, '-6'])

    if type_ == 'ipv4+':
        code = f'{func}\n'
        code += 'COMPREPLY+=($(compgen -W 0.0.0.0 -- "$cur"))'
        return BashCompletionCode(ctxt, code)

    if type_ == 'ipv6+':
        code = f'{func} -6\n'
        code += 'COMPREPLY+=($(compgen -W :: -- "$cur"))'
        return BashCompletionCode(ctxt, code)

    if type_ == 'all+':
        code = f'{func} -a\n'
        code += 'COMPREPLY+=($(compgen -W "0.0.0.0 ::" -- "$cur"))'
        return BashCompletionCode(ctxt, code)

    return BashCompletionFunc(ctxt, [func, '-a'])


def fish(_completer, ctxt, _trace, type_='all'):
    '''Implement ip_address for fish'''
    func = '__fish_print_addresses'

    if type_ == 'ipv4':
        cmd = f"{func} | string match -e '.'"
        return FishCompletionRawCommand(ctxt, cmd)

    if type_ == 'ipv6':
        cmd = f"{func} | string match -e ':'"
        return FishCompletionRawCommand(ctxt, cmd)

    if type_ == 'ipv4+':
        cmd = f"{func} --all | string match -e '.'"
        return FishCompletionRawCommand(ctxt, cmd)

    if type_ == 'ipv6+':
        cmd = f"{func} --all | string match -e ':'"
        return FishCompletionRawCommand(ctxt, cmd)

    if type_ == 'all+':
        return FishCompletionCommand(ctxt, [func, '--all'])

    return FishCompletionCommand(ctxt, [func])


def zsh(_completer, ctxt, _trace, type_='all'):
    '''Implement ip_address for zsh'''
    if type_ == 'ipv4':
        return ZshComplFunc(ctxt, ['_bind_addresses', '-4'])

    if type_ == 'ipv6':
        return ZshComplFunc(ctxt, ['_bind_addresses', '-6'])

    if type_ == 'ipv4+':
        return ZshComplFunc(ctxt, ['_bind_addresses', '-40'])

    if type_ == 'ipv6+':
        return ZshComplFunc(ctxt, ['_bind_addresses', '-60'])

    if type_ == 'all+':
        return ZshComplFunc(ctxt, ['_bind_addresses', '-0'])

    return ZshComplFunc(ctxt, ['_bind_addresses'])
