from typing import Dict, Optional, Tuple, Union

import hikari
import tanjun

from .. import checks
from ..utils import is_self


component = tanjun.Component()

MESSAGE_ID: int = 940855218533441556
EMOJIS: Dict[str, Tuple[str, int]] = {
    '🚀': ('Get pinged for server announcements!', 940841684802105355),
    '📢': ('Get pinged for new releases!', 939724049330868274),
}


def _resolve_emoji_role(
    event: Union[hikari.GuildReactionAddEvent, hikari.GuildReactionDeleteEvent]
) -> Optional[int]:
    for emoji, (_, role_id) in EMOJIS.items():
        if event.is_for_emoji(emoji):
            return role_id


@component.with_command
@tanjun.with_guild_check
@tanjun.with_check(checks.is_moderator)
@tanjun.with_option(
    'create',
    '--create',
    '-c',
    converters=(bool,),
    default=False,
    empty_value=True,
)
@tanjun.with_argument('channel_id', converters=(int,))
@tanjun.as_message_command('role-message')
async def role_message(
    ctx: tanjun.abc.Context,
    /,
    create: bool,
    channel_id: int,
    bot: hikari.GatewayBot = tanjun.inject(type=hikari.GatewayBot),
) -> None:
    guild = ctx.get_guild()
    assert guild is not None

    embed = hikari.Embed(
        title='Roles',
        colour=hikari.Colour(0x667EEA),
    )
    for emoji, (message, _) in EMOJIS.items():
        embed.add_field(name=emoji, value=message)

    channel = guild.get_channel(channel_id)
    if channel is None:
        await ctx.respond(
            content=f'Could not find channel with ID: {channel_id}'
        )
        return

    if channel.type != hikari.ChannelType.GUILD_TEXT:
        await ctx.respond(content='Given channel is not a text channel')
        return

    if create:
        message = await bot.rest.create_message(
            channel=channel.id,
            embed=embed,
        )
    else:
        message = await bot.rest.edit_message(
            message=MESSAGE_ID,
            channel=channel.id,
            embed=embed,
        )

    # NOTE: we should really be doing an asyncio.gather() here but this hits a rate limit :/
    for emoji in EMOJIS:
        await message.add_reaction(emoji)


@component.with_listener(hikari.GuildReactionAddEvent)
async def reaction_add_callback(
    event: hikari.GuildReactionAddEvent,
    /,
    bot: hikari.GatewayBot = tanjun.inject(type=hikari.GatewayBot),
) -> None:
    if is_self(bot, event) or event.message_id != MESSAGE_ID:
        return

    role_id = _resolve_emoji_role(event)
    if role_id is not None:
        await event.member.add_role(
            role_id, reason=f'User reacted with {event.emoji_name}'
        )


@component.with_listener(hikari.GuildReactionDeleteEvent)
async def reaction_delete_callback(
    event: hikari.GuildReactionDeleteEvent,
    /,
    bot: hikari.GatewayBot = tanjun.inject(type=hikari.GatewayBot),
) -> None:
    if is_self(bot, event) or event.message_id != MESSAGE_ID:
        return

    role_id = _resolve_emoji_role(event)
    if role_id is not None:
        await bot.rest.remove_role_from_member(
            role=role_id,
            user=event.user_id,
            guild=event.guild_id,
            reason=f'The {event.emoji_name} reaction was removed',
        )


loader = component.make_loader()
