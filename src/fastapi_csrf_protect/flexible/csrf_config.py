#!/usr/bin/env python3
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/src/fastapi_csrf_protect/flexible/csrf_config.py
# VERSION:     1.0.3
# CREATED:     2025-08-11 16:02:06+02:00
# AUTHOR:      Elliam Lotonga <e.m.lotonga@gmail.com>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Any, Callable, Sequence, Tuple, Union

### Third-party packages ###
from pydantic import ValidationError
from pydantic_settings import BaseSettings

### Local modules ###
from fastapi_csrf_protect.csrf_config import CsrfConfig as BaseCsrfConfig
from fastapi_csrf_protect.flexible.load_config import LoadConfig


class CsrfConfig(BaseCsrfConfig):
  """Same as the base CsrfConfig, except that it uses `flexible.load_config.LoadConfig`."""

  @classmethod
  def load_config(
    cls, settings: Callable[..., Union[Sequence[Tuple[str, Any]], BaseSettings]]
  ) -> None:
    try:
      config = LoadConfig(**{key.lower(): value for key, value in settings()})
      cls._load_config(config)
    except ValidationError:
      raise
    except Exception as err:
      print(err)
      raise TypeError('CsrfConfig must be pydantic "BaseSettings" or list of tuple')


__all__: Tuple[str, ...] = ("CsrfConfig",)
