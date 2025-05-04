from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
	import arc


def userify(user_id: int | str) -> str:
	"""### User mentions.

	```py
	>>> IFYs.userify(1234)
	'<@1234>'
	```
	"""

	return f"<@{user_id}>"


def userbangify(user_id: int | str) -> str:
	"""### User mentions (Old discord system).

	```py
	>>> IFYs.userbangify(1234)
	'<@!1234>'
	```
	"""

	return f"<@!{user_id}>"


def channelify(channel_id: int | str) -> str:
	"""### Channel mentions.

	```py
	>>> IFYs.channelify(1234)
	'<#1234>'
	```
	"""

	return f"<#{channel_id}>"


def roleify(role_id: int | str) -> str:
	"""### Role mentions.

	```py
	>>> IFYs.roleify(1234)
	'<@&1234>'
	```
	"""

	return f"<@&{role_id}>"


def commandify(command_name: str, command_id: int | str) -> str:
	"""### Command mentions.

	I'm not sure how to validate `command_name` other than the type (python regex apparently doesn't support whatever discord wrote [here](https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-naming))

	```py
	>>> IFYs.commandify('settings', 1234)
	'</settings:1234>'
	```
	"""
	return f"</{command_name}:{command_id}>"


def emojify(emoji_name: str, emoji_id: int | str, *, animated: bool = False) -> str:
	"""### Emojis (animated and non-animated).

	I'm not sure how to validate `emoji_name` other than the type (i'm not aware of discord's emoji naming scheme unlime command_name where they at least published some regex? maybe they did somewhere but if they did as i said im not aware of it).

	```py
	>>> IFYs.emojify('mmLol', 1234)
	'<:mmLol:1234>'
	>>> IFYs.emojify('b1nzy', 1234, animated=True)
	'<a:b1nzy:1234>'
	```
	"""
	return f"<{'a' if animated else ''}:{emoji_name}:{emoji_id}>"


def timeify(timestamp: int, style: None | Literal["t", "T", "d", "D", "f", "F", "R"] = None) -> str:
	return f"<t:{timestamp}{':' if style is not None else ''}{style if style is not None else ''}>"


def specialify(option: Literal["customize", "browse", "guide"] = "customize") -> str:
	if option not in ("customize", "browse", "guide"):
		raise ValueError(f"Expected option in ('customize', 'browse', 'guide'), got {option} instead.")

	return f"<id:{option}>"


def ctx_commandify(ctx: "arc.Context") -> str:
	return f"<{ctx.command.display_name}:{ctx.interaction.command_id}>"
