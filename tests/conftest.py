#!/usr/bin/env python3.11
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/conftest.py
# VERSION:     1.0.7
# CREATED:     2025-09-09 13:17
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module defining fixtures auto-imported by `pytest` command when running tests"""

### Third-party packages ###
from pytest import Config, Item, Parser, UsageError, mark


def pytest_addoption(parser: Parser) -> None:
  """Add option to Pytest CLI parser

  ---
  :param parser: Pytest Parser instance passed when running via pytest command line interface
  :type parser: pytest.Parser
  """
  parser.addoption(
    "--flexible",
    action="store_true",
    default=False,
    help="When flagged, only run Flexible mode tests.",
  )
  parser.addoption(
    "--normal",
    action="store_true",
    default=False,
    help="when flagged, only run Normal mode tests.",
  )


def pytest_collection_modifyitems(config: Config, items: list[Item]) -> None:
  for item in items:
    posix_path, _, _ = item.reportinfo()
    if config.getoption("--flexible") and "tests/flexible" not in str(posix_path):
      item.add_marker(mark.skip(reason="Tests manually skipped in Flexible Mode"))
    elif config.getoption("--normal") and "tests/flexible" in str(posix_path):
      item.add_marker(mark.skip(reason="Tests manually skipped in Normal mode"))


def pytest_configure(config: Config) -> None:
  flexible_mode: bool = config.getoption("flexible")  # type: ignore[assignment]
  normal_mode: bool = config.getoption("normal")  # type: ignore[assignment]
  if flexible_mode is True and normal_mode is True:
    raise UsageError("--flexible and --normal are mutually exclusive flags.")


__all__: tuple[str, ...] = ("pytest_addoption", "pytest_collection_modifyitems", "pytest_configure")
