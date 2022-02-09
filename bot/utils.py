from typing import Protocol

import hikari


class HasUserID(Protocol):
    @property
    def user_id(self) -> int:
        ...


def is_self(bot: hikari.GatewayBot, event: HasUserID) -> bool:
    me = bot.get_me()
    assert me is not None
    return me.id == event.user_id
