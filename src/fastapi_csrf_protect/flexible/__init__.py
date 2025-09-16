#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/src/fastapi_csrf_protect/flexible/__init__.py
# VERSION:     1.0.7
# CREATED:     2025-08-11 16:02:06+02:00
# AUTHOR:      Eliam Lotonga <e.m.lotonga@gmail.com>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************

### Local modules ###
from fastapi_csrf_protect.flexible.core import CsrfProtect

__all__: tuple[str, ...] = ("CsrfProtect",)
