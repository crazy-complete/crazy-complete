# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for SSIDs (service set identifiers).'''

from ..helpers import ShellFunction
from ..zsh_complete import ZshComplFunc
from ..zsh_helpers import ZshHelpers

CATEGORY = 'basic'

SHORT = 'Complete SSIDs of visible Wi-Fi networks'

ALSO = {
    'net_bssid': 'For completing BSSIDs',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--ssid']
    complete: ['net_ssid']
'''

OUTPUT = r'''
~ > example --ssid=<TAB>
Siddhartha  (C0:5C:47:57:7B:04)
WLAN        (CE:9A:04:A7:79:31)
'''

_COMMAND_BASH = 'nmcli --terse --fields ssid --escape no device wifi list'

_COMMAND_FISH = r"nmcli --terse --escape no --fields bssid,ssid device wifi list | string replace -r -- '^(.{17}):(.+)' '$2\t$1'"

_NET_SSID_ZSH = ShellFunction('net_ssid_complete', r'''
local line='' bssid='' ssid='' esc='\:' ssids=()

while IFS= read -r line; do
  bssid=${line:0:17}
  ssid=${line:18}
  [[ -n $ssid ]] && ssids+=("${ssid//:/$esc}:$bssid")
done < <(nmcli --terse --fields bssid,ssid device wifi list)

_describe 'SSID' ssids
''')

ZshHelpers.add_function(_NET_SSID_ZSH)


def validate(_ctxt, arguments):
    '''Validate YAML for net_ssid completer'''
    arguments.require_no_more()


def bash(completer, ctxt, trace):
    '''Implement net_ssid for bash'''
    return completer.complete(ctxt, trace, 'exec', _COMMAND_BASH)


def fish(completer, ctxt, trace):
    '''Implement net_ssid for fish'''
    return completer.complete(ctxt, trace, 'exec', _COMMAND_FISH)


def zsh(_completer, ctxt, _trace):
    '''Implement net_ssid for zsh'''
    func = ctxt.helpers.use_function('net_ssid_complete')
    return ZshComplFunc(ctxt, [func], needs_braces=True)
