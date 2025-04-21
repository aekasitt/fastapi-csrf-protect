#!/usr/bin/env python3.9
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/src/starlette/requests.pyi
# VERSION:     1.0.2
# CREATED:     2025-03-21 15:43
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION: https://mypy.readthedocs.io/en/stable/stubs.html
#
# HISTORY:
# *************************************************************
"""Stub file containing a skeleton of the public interface of `starlette.requests` module"""

from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Mapping

from starlette.datastructures import MutableHeaders

class Request(Mapping[str, Any], metaclass=ABCMeta):
  @abstractmethod
  async def body(self) -> bytes: ...
  @property
  @abstractmethod
  def cookies(self) -> Dict[str, str]: ...
  @property
  @abstractmethod
  def headers(self) -> MutableHeaders: ...
