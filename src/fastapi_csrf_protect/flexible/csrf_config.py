from typing import Any, Callable, Sequence, Tuple, Union

from pydantic import ValidationError
from pydantic_settings import BaseSettings

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
