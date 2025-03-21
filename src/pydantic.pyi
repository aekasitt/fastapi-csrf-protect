#!/usr/bin/env python3.9
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/src/pydantic.pyi
# VERSION:     1.0.2
# CREATED:     2025-03-21 15:43
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION: https://mypy.readthedocs.io/en/stable/stubs.html
#
# HISTORY:
# *************************************************************
"""Stub file containing a skeleton of the public interface of `pydantic` library"""

from abc import ABCMeta
from typing import Any, Literal, Generator, Mapping, Set, Tuple, TypeAlias, Union
from typing_extensions import Annotated, Self

class BaseModel(metaclass=ABCMeta):
  def __iter__(self) -> TupleGenerator: ...
  def model_dump(
    self,
    *,
    mode: Literal["json", "python"] | str = "python",
    include: IncEx | None = None,
    exclude: IncEx | None = None,
    context: Any | None = None,
    by_alias: bool = False,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    round_trip: bool = False,
    warnings: bool | Literal["none", "warn", "error"] = True,
    serialize_as_any: bool = False,
  ) -> dict[str, Any]: ...
  @classmethod
  def model_validate_json(
    cls,
    json_data: str | bytes | bytearray,
    *,
    strict: bool | None = None,
    context: Any | None = None,
  ) -> Self: ...

IncEx: TypeAlias = Union[
  Set[int], Set[str], Mapping[int, Union["IncEx", bool]], Mapping[str, Union["IncEx", bool]]
]
StrictBool = Annotated[bool, ...]
StrictInt = Annotated[int, ...]
StrictStr = Annotated[str, ...]
TupleGenerator: TypeAlias = Generator[Tuple[str, Any], None, None]

class ValidationError(ValueError, metaclass=ABCMeta): ...

def create_model(model_name: str) -> type[BaseModel]: ...
def model_validator(*, mode: Literal["wrap", "before", "after"]) -> Any: ...
