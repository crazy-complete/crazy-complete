# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for BSSIDs (base station service set identifiers).'''

from ..helpers import ShellFunction
from ..zsh_complete import ZshComplFunc
from ..zsh_helpers import ZshHelpers

CATEGORY = 'basic'

SHORT = 'Complete BSSIDs of visible Wi-Fi networks'

ALSO = {
    'net_ssid': 'For completing SSIDs',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--bssid']
    complete: ['net_bssid']
'''

OUTPUT = r'''
~ > example --bssid=<TAB>
C0:5C:47:57:7B:04  (Siddhartha)
CE:9A:04:A7:79:31  (WLAN)
'''

_COMMAND_BASH = 'nmcli --terse --fields bssid --escape no device wifi list'

_COMMAND_FISH = r'nmcli --terse --escape no --fields bssid,ssid device wifi list | string replace -r -- "^(.{17}):" "\$1\t"'

_NET_BSSID_ZSH = ShellFunction('net_bssid_complete', r'''
local line='' bssid='' ssid='' esc='\:' bssids=()

while IFS= read -r line; do
  bssid=${line:0:17}
  ssid=${line:18}
  [[ -n $bssid ]] && bssids+=("${bssid//:/$esc}:$ssid")
done < <(nmcli --terse --fields bssid,ssid device wifi list)

_describe 'BSSID' bssids
''')

ZshHelpers.add_function(_NET_BSSID_ZSH)


def validate(_ctxt, arguments):
    '''Validate YAML for net_bssid completer'''
    arguments.require_no_more()


def bash(completer, ctxt, trace):
    '''Implement net_bssid for bash'''
    return completer.complete(ctxt, trace, 'exec', _COMMAND_BASH)


def fish(completer, ctxt, trace):
    '''Implement net_bssid for fish'''
    return completer.complete(ctxt, trace, 'exec', _COMMAND_FISH)


def zsh(_completer, ctxt, _trace):
    '''Implement net_bssid for zsh'''
    func = ctxt.helpers.use_function('net_bssid_complete')
    return ZshComplFunc(ctxt, [func], needs_braces=True)
