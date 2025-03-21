#!/usr/bin/env python3.9
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/src/starlette/datastructures.pyi
# VERSION:     1.0.2
# CREATED:     2025-03-21 15:43
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION: https://mypy.readthedocs.io/en/stable/stubs.html
#
# HISTORY:
# *************************************************************
"""Stub file containing a skeleton of the public interface of `starlette.datastructures` module"""

from abc import ABCMeta
from typing import Mapping

class Headers(Mapping[str, str], metaclass=ABCMeta): ...
class MutableHeaders(Headers, metaclass=ABCMeta): ...
class UploadFile(metaclass=ABCMeta): ...
