#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


# mypy: disable-error-code="var-annotated,index,attr-defined"

from cmk.base.check_api import LegacyCheckDefinition
from cmk.base.check_legacy_includes.dhcp_pools import check_dhcp_pools_levels
from cmk.base.config import check_info

isc_dhcpd_default_levels = (15.0, 5.0)

# Example output from agent:
# <<<isc_dhcpd>>>
# [general]
# PID: 3670
# [pools]
# 10.0.1.1 10.0.1.254
# [leases]
# 10.0.1.16
# 10.0.1.24
# 10.0.1.26
# 10.0.1.27
# 10.0.1.34
# 10.0.1.36
# 10.0.1.45
# 10.0.1.50
# 10.0.1.53
# 10.0.1.57


def parse_isc_dhcpd(string_table):
    def ip_to_number(ip):
        number = 0
        factor = 1
        for part in ip.split(".")[::-1]:
            number += factor * int(part)
            factor *= 256
        return number

    parsed = {
        "pids": [],
        "pools": {},
        "leases": [],
    }

    mode = None
    for line in string_table:
        if line[0] == "[general]":
            mode = "general"
        elif line[0] == "[pools]":
            mode = "pools"
        elif line[0] == "[leases]":
            mode = "leases"

        elif mode == "general":
            if line[0] == "PID:":
                parsed["pids"] = list(map(int, line[1:]))

        elif mode == "pools":
            if "bootp" in line[0]:
                line = line[1:]
            start, end = line[0], line[1]
            item = "%s-%s" % (start, end)
            parsed["pools"][item] = (ip_to_number(start), ip_to_number(end))

        elif mode == "leases":
            parsed["leases"].append(ip_to_number(line[0]))

    return parsed


def inventory_isc_dhcpd(parsed):
    return [(item, isc_dhcpd_default_levels) for item in parsed["pools"]]


def check_isc_dhcpd(item, params, parsed):
    if len(parsed["pids"]) == 0:
        yield 2, "DHCP Daemon not running"
    elif len(parsed["pids"]) > 1:
        yield 1, "DHCP Daemon running %d times (PIDs: %s)" % (
            len(parsed["pids"]),
            ", ".join(map(str, parsed["pids"])),
        )

    if item not in parsed["pools"]:
        return

    range_from, range_to = parsed["pools"][item]
    num_leases = range_to - range_from + 1
    num_used = 0
    for lease_dec in parsed["leases"]:
        if range_from <= lease_dec <= range_to:
            num_used += 1

    for check_result in check_dhcp_pools_levels(
        num_leases - num_used, num_used, None, num_leases, params
    ):
        yield check_result


check_info["isc_dhcpd"] = LegacyCheckDefinition(
    parse_function=parse_isc_dhcpd,
    service_name="DHCP Pool %s",
    discovery_function=inventory_isc_dhcpd,
    check_function=check_isc_dhcpd,
    check_ruleset_name="win_dhcp_pools",
)
