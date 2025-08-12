from fastapi_csrf_protect.load_config import LoadConfig as BaseLoadConfig

class LoadConfig(BaseLoadConfig):
    """Same as the base LoadConfig, but no token_location & token_key validations."""

    def validate_token_location(self):
        """Ignore token location validation since we will be checking both locations.

            Header/Form body.
        """
