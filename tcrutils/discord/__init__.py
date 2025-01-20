"""TCRUtils Discord. Contains various features related to bot development on discord and other stuff maybe."""

from .src import tcrd_types as types
from .src.tcrd_alias import get_guild_count
from .src.tcrd_cached_fetch import AsyncCachedFetch, AsyncCachedFetchWithConverter
from .src.tcrd_commands import get_slash_command_ids
from .src.tcrd_constants import DISCORD_EPOCH
from .src.tcrd_dpy import escape_markdown, escape_mentions, remove_markdown
from .src.tcrd_embeds import embed, modal
from .src.tcrd_limits import DiscordLimits
from .src.tcrd_markdown import codeblock, codeblocks, discord_error, uncodeblock
from .src.tcrd_permissions import PERMISSIONS_DICT, Permission, permissions
from .src.tcrd_permissions import Permission as DiscordPermission
from .src.tcrd_permissions import permissions as discord_permissions
from .src.tcrd_shorts import confirm
from .src.tcrd_snowflake import is_snowflake
from .src.tcrd_string import IFYs, backtick_comma_str_list_join
