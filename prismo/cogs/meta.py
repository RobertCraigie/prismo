from __future__ import annotations

import time
import datetime

from disnake.ext import commands

from bot import PrismoBot


class Meta(commands.Cog):
    @commands.command()
    async def ping(self, ctx: commands.Context[PrismoBot]) -> None:
        start_time = time.perf_counter()
        msg = await ctx.reply("Hello, there!")

        time_taken = (time.perf_counter() - start_time) * 1_000
        heartbeat_latency = (
            ctx.bot.latency * 1_000 if ctx.bot.latency else float("NAN")
        )
        uptime: datetime.timedelta = datetime.datetime.utcnow() - ctx.bot.start_time
        await msg.edit(
            f"PONG\n - REST: {time_taken:.0f}ms\n - Gateway: {heartbeat_latency:.0f}ms\n"
            f"Uptime since {uptime.days} days and {uptime.seconds} seconds"
        )


def setup(bot: PrismoBot):
    bot.add_cog(Meta())
