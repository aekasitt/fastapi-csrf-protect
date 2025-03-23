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
from typing import (
  Any,
  Callable,
  Literal,
  Generator,
  Mapping,
  Protocol,
  Set,
  Tuple,
  TypeAlias,
  TypeVar,
  Union,
)
from typing_extensions import Annotated, Generic, Self

_ModelType = TypeVar("_ModelType")
IncEx: TypeAlias = Union[
  Set[int], Set[str], Mapping[int, Union["IncEx", bool]], Mapping[str, Union["IncEx", bool]]
]
ModelAfterValidator = Callable[[_ModelType, ValidationInfo], _ModelType]
ModelAfterValidatorWithoutInfo = Callable[[_ModelType], _ModelType]
StrictBool = Annotated[bool, ...]
StrictInt = Annotated[int, ...]
StrictStr = Annotated[str, ...]
ReturnType = TypeVar("ReturnType")
TupleGenerator: TypeAlias = Generator[Tuple[str, Any], None, None]

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

class ModelValidatorDecoratorInfo(metaclass=ABCMeta): ...
class PydanticDescriptorProxy(Generic[ReturnType], metaclass=ABCMeta): ...
class ValidationError(ValueError, metaclass=ABCMeta): ...
class ValidationInfo(Protocol, metaclass=ABCMeta): ...

_AnyModelAfterValidator = Union[
  ModelAfterValidator[_ModelType], ModelAfterValidatorWithoutInfo[_ModelType]
]

def create_model(model_name: str) -> type[BaseModel]: ...
def model_validator(
  *, mode: Literal["after"]
) -> Callable[
  [_AnyModelAfterValidator[_ModelType]], PydanticDescriptorProxy[ModelValidatorDecoratorInfo]
]: ...
