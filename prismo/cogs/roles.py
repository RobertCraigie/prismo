from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Tuple, List

import disnake
from disnake.ext import commands


if TYPE_CHECKING:
    from bot import PrismoBot

MESSAGE_ID: int = 1086687431945883658
EMOJIS: Dict[str, Tuple[str, str, int]] = {
    "announcements": ("🚀", "Get pinged for server announcements!", 939724049330868274),
    "releases": ("📢", "Get pinged for new releases!", 940841684802105355),
}


class Roles(commands.Cog):
    def __init__(self, bot: PrismoBot) -> None:
        self.bot = bot

    @commands.command()
    async def create_roles_message(self, ctx: commands.Context[PrismoBot], create: bool, channel: disnake.TextChannel) -> None:
        embed = disnake.Embed(
            title='Roles',
            colour=disnake.Colour(0x667EEA),
        )

        buttons: List[disnake.ui.Button[None]] = []
        for key, (emoji, message, _) in EMOJIS.items():
            embed.add_field(name=emoji, value=message)
            buttons.append(disnake.ui.Button(emoji=emoji, custom_id=key))

        if create:
            message = await channel.send(
                embed=embed,
                components=buttons,
            )
        else:
            message = ctx.bot.get_message(MESSAGE_ID) or await channel.fetch_message(MESSAGE_ID)

            await message.edit(
                embed=embed,
                components=buttons
            )

    @commands.Cog.listener(disnake.Event.button_click)
    async def add_roles(self, interaction: disnake.MessageInteraction) -> None:
        if not interaction.component.custom_id in EMOJIS.keys():
            return

        for key, (emoji, _, role_id) in EMOJIS.items():
            # just for type safety
            if not isinstance(interaction.component, disnake.Button):
                return

            if interaction.component.emoji == disnake.PartialEmoji.from_str(emoji):
                # something went wrong and the API returned a User object instead of a Member object
                if not isinstance(interaction.author, disnake.Member):
                    self.bot.logger.debug(
                        "Got a User object when expecting a Member object")
                    return await interaction.response.send_message("Oh no! Something went wrong! Error reported to the dev team. We're sorry :'(", ephemeral=True)

                # the member doesn't have the role, adding it
                if not role_id in [role.id for role in interaction.author.roles]:
                    await interaction.author.add_roles(disnake.Object(role_id), reason=f"Add {key} role as requested")
                    self.bot.logger.info(
                        "Added %s (id: %s) role to %s", key, role_id, interaction.author)
                    return await interaction.response.send_message(f"<@&{role_id}> added!", ephemeral=True)

                # the member already has the role, removing it
                await interaction.author.remove_roles(disnake.Object(role_id), reason=f"Removing {key} role as requested")
                self.bot.logger.info(
                    "Removed %s (id: %s) role to %s", key, role_id, interaction.author)
                # i'm manually mentioning the role to not fetch a completed role object (so no request to the API win win)
                return await interaction.response.send_message(f"<@&{role_id}> removed!", ephemeral=True)


def setup(bot: PrismoBot):
    bot.add_cog(Roles(bot))
