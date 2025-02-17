#!/usr/bin/env python3
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2020             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Checkmk.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

# Example SNMP Walk
# .1.3.6.1.4.1.318.1.1.10.4.3.2.1.3.1.6 Leckagekontrolle-RZ4
# .1.3.6.1.4.1.318.1.1.10.4.3.2.1.3.2.5 Pumpe 1 RZ4
# .1.3.6.1.4.1.318.1.1.10.4.3.2.1.3.2.6 Pumpe 2 RZ4
# .1.3.6.1.4.1.318.1.1.10.4.3.2.1.4.1.6 Kaeltepark RZ4
# .1.3.6.1.4.1.318.1.1.10.4.3.2.1.4.2.5 Kaeltepark RZ4
# .1.3.6.1.4.1.318.1.1.10.4.3.2.1.4.2.6 Kaeltepark RZ4
# .1.3.6.1.4.1.318.1.1.10.4.3.2.1.5.1.6 2
# .1.3.6.1.4.1.318.1.1.10.4.3.2.1.5.2.5 2
# .1.3.6.1.4.1.318.1.1.10.4.3.2.1.5.2.6 2
# .1.3.6.1.4.1.318.1.1.10.4.3.2.1.7.1.6 1
# .1.3.6.1.4.1.318.1.1.10.4.3.2.1.7.2.5 1
# .1.3.6.1.4.1.318.1.1.10.4.3.2.1.7.2.6 1
# .1.3.6.1.4.1.318.1.1.10.4.3.2.1.8.1.6 2
# .1.3.6.1.4.1.318.1.1.10.4.3.2.1.8.2.5 2
# .1.3.6.1.4.1.318.1.1.10.4.3.2.1.8.2.6 2


from cmk.base.check_api import LegacyCheckDefinition
from cmk.base.config import check_info
from cmk.base.plugins.agent_based.agent_based_api.v1 import OIDEnd, SNMPTree
from cmk.base.plugins.agent_based.utils.apc import DETECT


def parse_apc_netbotz_drycontact(string_table):
    parsed = {}

    state_map = {
        "1": ("Closed high mem", 2),
        "2": ("Open low mem", 0),
        "3": ("Disabled", 1),
        "4": ("Not applicable", 3),
    }

    for idx, inst, loc, state in string_table:
        parsed[inst + " " + idx] = {
            "location": loc,
            "state": state_map.get(state, ("unknown[%s]" % state, 3)),
        }

    return parsed


def check_apc_netbotz_drycontact(item, params, parsed):
    if not (data := parsed.get(item)):
        return
    state_readable, state = data["state"]
    loc = data["location"]
    if loc:
        loc_info = "[%s] " % loc
    else:
        loc_info = ""
    yield state, "%sState: %s" % (loc_info, state_readable)


def discover_apc_netbotz_drycontact(section):
    yield from ((item, {}) for item in section)


check_info["apc_netbotz_drycontact"] = LegacyCheckDefinition(
    detect=DETECT,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.318.1.1.10.4.3.2.1",
        oids=[OIDEnd(), "3", "4", "5"],
    ),
    parse_function=parse_apc_netbotz_drycontact,
    service_name="DryContact %s",
    discovery_function=discover_apc_netbotz_drycontact,
    check_function=check_apc_netbotz_drycontact,
)
