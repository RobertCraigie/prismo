import time
import tanjun


component = tanjun.Component()


@component.with_command
@tanjun.as_message_command('ping')
async def ping(ctx: tanjun.abc.Context, /) -> None:
    start_time = time.perf_counter()
    await ctx.respond(content='Hello, there!')

    time_taken = (time.perf_counter() - start_time) * 1_000
    heartbeat_latency = (
        ctx.shards.heartbeat_latency * 1_000 if ctx.shards else float('NAN')
    )
    await ctx.edit_last_response(
        f'PONG\n - REST: {time_taken:.0f}ms\n - Gateway: {heartbeat_latency:.0f}ms'
    )


loader = component.make_loader()
