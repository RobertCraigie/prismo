from typing import Any
from pydantic import BaseSettings


class Config(BaseSettings):
    bot_token: str
    prefix: str = 'p.'

    @classmethod
    def load(cls, **kwargs: Any) -> 'Config':
        """Load the Config.

        Useful as type checkers would otherwise report an error
        if not all options are passed as init arguments.
        """
        return cls.parse_obj(kwargs)
