#!/usr/bin/env python3
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/src/fastapi_csrf_protect/flexible/load_config.py
# VERSION:     1.0.3
# CREATED:     2025-08-11 16:02:06+02:00
# AUTHOR:      Eliam Lotonga <e.m.lotonga@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Tuple

### Local modules ###
from fastapi_csrf_protect.load_config import LoadConfig as BaseLoadConfig


class LoadConfig(BaseLoadConfig):
  """Same as the base LoadConfig, but no token_location & token_key validations."""

  def validate_token_location(self):
    """Ignore token location validation since we will be checking both locations.

    Header/Form body.
    """


__all__: Tuple[str, ...] = ("LoadConfig",)
