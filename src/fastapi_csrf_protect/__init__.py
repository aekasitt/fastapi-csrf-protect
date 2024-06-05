#!/usr/bin/env python3
# Copyright (C) 2020-2024 All rights reserved.
# FILENAME:    ~~/src/fastapi_csrf_protect/__init__.py
# VERSION:     0.3.4
# CREATED:     2020-11-25 14:35
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
FastAPI extension that provides Csrf Protection Token support
"""

__version__ = "0.3.4"

from .core import CsrfProtect

__all__ = ("CsrfProtect",)
