import tanjun
import hikari


async def is_guild(ctx: tanjun.abc.Context) -> bool:
    if ctx.guild_id is None:
        await ctx.respond('Command can only be used within a server')
        return False

    return True


async def is_moderator(ctx: tanjun.abc.Context) -> bool:
    member = ctx.member
    if member is None:
        return False

    permissions = await tanjun.utilities.fetch_permissions(ctx.client, member)
    return permissions.any(hikari.Permissions.MANAGE_GUILD)
