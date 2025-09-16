#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/src/fastapi_csrf_protect/__init__.py
# VERSION:     1.0.7
# CREATED:     2020-11-25 14:35
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************
"""
FastAPI extension that provides Csrf Protection Token support
"""

### Local modules ###
from fastapi_csrf_protect.core import CsrfProtect

__all__: tuple[str, ...] = ("CsrfProtect",)
__name__ = "fastapi-csrf-protect"
__package__ = "fastapi-csrf-protect"
__version__ = "1.0.7"
