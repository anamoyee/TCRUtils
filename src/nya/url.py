import json

import arc


def make_loopback_link(ctx: arc.GatewayContext, text: str, *, tip: str | None = None):
	guild_id = ctx.guild_id or "@me"
	channel_id = ctx.channel_id

	if tip is not None:
		return f"[{text}](https://discord.com/channels/{guild_id}/{channel_id} {json.dumps(tip)})"
	else:
		return f"[{text}](https://discord.com/channels/{guild_id}/{channel_id})"
