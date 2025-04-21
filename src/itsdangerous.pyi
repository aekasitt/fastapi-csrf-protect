#!/usr/bin/env python3.9
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/src/itsdangerous.pyi
# VERSION:     1.0.2
# CREATED:     2025-03-21 15:43
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION: https://mypy.readthedocs.io/en/stable/stubs.html
#
# HISTORY:
# *************************************************************
"""Stub file containing a skeleton of the public interface of `itsdangerous` library"""

from abc import ABCMeta
from collections.abc import Iterable
from typing import Any, Generic, Protocol, TYPE_CHECKING, Union
from typing_extensions import TypeVar

class BadData(Exception, metaclass=ABCMeta): ...
class BadSignature(BadData, metaclass=ABCMeta): ...
class BadTimeSignature(BadSignature, metaclass=ABCMeta): ...
class SignatureExpired(BadTimeSignature, metaclass=ABCMeta): ...

if TYPE_CHECKING:
  _TSerialized = TypeVar(
    "_TSerialized", bound=Union[str, bytes], default=Union[str, bytes], covariant=True
  )
else:
  _TSerialized = TypeVar("_TSerialized", bound=Union[str, bytes], covariant=True)

class _PDataSerializer(Protocol[_TSerialized], metaclass=ABCMeta): ...

class Serializer(Generic[_TSerialized], metaclass=ABCMeta):
  def __init__(
    self: Serializer[str],
    secret_key: str | bytes | Iterable[str] | Iterable[bytes],
    salt: str | bytes | None = b"itsdangerous",
    serializer: None | _PDataSerializer[str] = None,
    serializer_kwargs: dict[str, Any] | None = None,
    signer: type[Signer] | None = None,
    signer_kwargs: dict[str, Any] | None = None,
    fallback_signers: list[dict[str, Any] | tuple[type[Signer], dict[str, Any]] | type[Signer]]
    | None = None,
  ): ...
  def dumps(self, obj: Any, salt: str | bytes | None = None) -> _TSerialized: ...
  def loads(self, s: str | bytes, salt: str | bytes | None = None, **kwargs: Any) -> Any: ...

class Signer(metaclass=ABCMeta): ...
class TimedSerializer(Serializer[_TSerialized], metaclass=ABCMeta): ...
class URLSafeSerializerMixin(Serializer[str], metaclass=ABCMeta): ...
class URLSafeTimedSerializer(URLSafeSerializerMixin, TimedSerializer[str], metaclass=ABCMeta): ...
