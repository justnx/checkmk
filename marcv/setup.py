#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from setuptools import find_packages, setup

setup(
    name="marcv",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["fastapi==0.68", "python-multipart==0.0.*"],
    entry_points={
        "console_scripts": ["create_server_certificate=marcv.create_certificate:main"]
    },
)
