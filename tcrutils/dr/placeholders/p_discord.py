from __future__ import annotations as __future_annotations

from ...discord.tcrd_snowflake import is_snowflake as __is_snowflake
from ...discord.tcrd_string import IFYs
from ...src.tcr_console import console as c
from .. import util as __

if True:  # Author

  @__.REQUIRE('ctx', 'event')
  @__.REQUIRE('user_mentions')
  @__.SWITCH('noping')
  def mention(
    name,
    user: str | None = None,
    *args: str,
    ctx: __.arc.Context | None,
    event: __.hikari.MessageCreateEvent | None,
    user_mentions: list,
    noping: bool,
    **ctxs,
  ) -> str:
    """### Return user's mention.

    ### Example:
    ```txt
    Hello {@}!
    ```

    ### Result:
    ```txt
    Hello <@507642999992352779>!
    ```

    ### Dependencies
    (SlashContext || MessageCreateEvent) && user_mentions
    """

    if user is None:
      author_id = ctx.author.id if ctx else event.author.id
    else:
      if __is_snowflake(user):
        author_id = int(user)
      else:
        return __.rebuild_yourself(name, user, *args, **ctxs)

    if not noping and author_id not in user_mentions:
      user_mentions.append(author_id)

    return IFYs.userify(author_id)

  @__.REQUIRE_AUTHOR
  def username(
    *args,
    author: __.hikari.User,
    **ctxs,
  ) -> str:
    """### Return user's username.

    Example:
    ```txt
    Hello {username}!
    ```

    Result:
    ```txt
    Hello anamoyee!
    ```

    ### Dependencies
    (SlashContext || MessageCreateEvent) && user_mentions
    """
    return author.username

  @__.REQUIRE_AUTHOR
  def globalname(
    *args,
    author: __.hikari.User,
    **ctxs,
  ):
    """### Return user's global name.

    Example:
    ```txt
    Hello {globalname}
    ```

    Result:
    ```txt
    Hello anamoyee :3
    ```

    ### Dependencies
    SlashContext || MessageCreateEvent
    """
    return author.global_name

  @__.REQUIRE_MEMBER_AUTHOR(lambda *_, author, **__: author.global_name or author.username)
  def nickname(
    *args,
    author: __.hikari.User,
    member: __.hikari.Member,
    **ctxs,
  ) -> str:
    """### Return user's nickname, then global name, then username if any are not available.

    Return various user's names in that order
     - `nickname` if they have one, otherwise:
     - `globalname` if they have one, otherwise:
     - `username`

    Example:
    ```txt
    Hello {nickname}
    ```

    Result:
    ```txt
    Hello anamoyee [🦊🎴]
    ```

    ### Dependencies
    (SlashContext && InGuild) || GuildMessageCreateEvent
    """
    return member.nickname or author.global_name or author.username

  @__.STRINGIFY
  @__.REQUIRE_AUTHOR
  def discriminator(
    *args,
    author: __.hikari.User,
    **ctxs,
  ) -> str:
    """### Return user's discriminator.

    Example:
    ```txt
    Hello {discriminator}!
    ```

    Result:
    ```txt
    Hello 0009!
    ```

    ### Dependencies
    SlashContext || MessageCreateEvent
    """

    if hasattr(author, 'discrim'):
      return author.discriminator
    else:
      return 0

  @__.REQUIRE_AUTHOR
  def tag(
    *args,
    author: __.hikari.User,
    **ctxs,
  ) -> str:
    """### Return user's tag.

    Example:
    ```txt
    Hello {tag}!
    ```

    Result:
    ```txt
    Hello anamoyee#0009! // Whenever user's discriminator != 0
    ```
    OR
    ```txt
    Hello @anamoyee // Whenever user's discriminator == 0
    ```

    ### Dependencies
    SlashContext || MessageCreateEvent
    """
    discrim = author.discriminator if hasattr(author, 'discrim') else '0'

    if discrim == '0':
      return f'@{author.username}'
    else:
      return f'{author.username}#{discrim}'

  @__.REQUIRE_AUTHOR
  def id(
    *args,
    author: __.hikari.User,
    **ctxs,
  ) -> str:
    """### Return user's id.

    Example:
    ```txt
    Hello {id}!
    ```

    Result:
    ```txt
    Hello 507642999992352779!
    ```

    ### Dependencies
    SlashContext || MessageCreateEvent
    """
    return str(author.id)

  @__.REQUIRE_AUTHOR
  def bot(
    *args,
    author: __.hikari.User,
    **ctxs,
  ):
    """### Return whether user is bot or not.

    Example:
    ```txt
    It is {bot} that you are a bot!
    ```

    Result:
    ```txt
    It is false that you are a bot!
    ```

    ### Dependencies
    SlashContext || MessageCreateEvent
    """
    return __.jsbool(author.is_bot)

  @__.REQUIRE('event', 'ctx')
  def human(
    *args,
    ctx: __.arc.Context | None = None,
    event: __.hikari.MessageCreateEvent | None = None,
    **ctxs,
  ):
    """### Return whether user is the system user or not.

    Example:
    ```txt
    It is {system} that you are the system user!
    ```

    Result:
    ```txt
    It is false that you are the system user!
    ```

    ### Dependencies
    SlashContext || MessageCreateEvent
    """
    if ctx:
      return 'true'
    else:
      return __.jsbool(event.is_human)

  @__.REQUIRE('event', 'ctx')
  def in_dms(
    *args,
    ctx: __.arc.Context | None = None,
    event: __.hikari.MessageCreateEvent | None = None,
    **ctxs,
  ):
    """### Return whether user is in DMs or not.

    Example:
    ```txt
    It is {indms} that you are running this command in DMs!
    ```

    Result:
    ```txt
    It is true that you are running this command in DMs!
    ```

    ### Dependencies
    SlashContext || MessageCreateEvent
    """
    return __.jsbool(not hasattr(ctx or event, 'guild_id'))

  @__.REQUIRE_AUTHOR
  def avatar(
    *args,
    author: __.hikari.User,
    **ctxs,
  ) -> str:
    """### Return user's avatar url.

    Example:
    ```txt
    Hello {avatar}
    ```

    Result:
    ```txt
    Here's your avatar url https://cdn.discordapp.com/avatars/507642999992352779/cef9fec7c8afce0635c24dff93ff6010.png?size=4096
    ```

    ### Dependencies
    SlashContext || MessageCreateEvent
    """
    return str(author.display_avatar_url)

  @__.REQUIRE_MEMBER_AUTHOR('0')
  def roles(
    *args,
    member: __.hikari.Member,
    **ctxs,
  ) -> str:
    """### Return user's roles.

    Example:
    ```txt
    You have {roles} roles!
    ```

    Result:
    ```txt
    You have 6 roles!
    ```

    ### Dependencies
    (SlashContext && InGuild) || GuildMessageCreateEvent
    """
    return str(len(member.role_ids) - 1)  # -1 to compensate for the @everyone role

  @__.REQUIRE('attachments')
  @__.REQUIRE_POSITIONAL(1, None)
  def attach(
    _,
    url: str,
    *args,
    attachments: list[__.hikari.Attachment],
    **ctxs,
  ):
    """### Attach a file to the message from a given url.

    This will wieve out the url if it's not a valid url,
    however, this may cause a BadRequestError if the url is invalid.

    Example:
    ```txt
    {attach|{avatar}}
    ```

    Result:
    ```txt
    <no content but the avatar will be attached as file>
    ```

    ### Dependencies
    attachments
    """
    url = url.strip()
    if not __.regex.match(__.RegexPreset.URL, url):
      return f"Something went wrong while attaching a file, here's a link instead: <{url}>"

    attachments.append(url)

  @__.SWITCH('nohash')
  @__.REQUIRE_MEMBER_AUTHOR(lambda *_, nohash, **__: f'{"" if nohash else "#"}000000')
  def color(
    *args,
    member: __.hikari.Member,
    nohash: bool = False,
    **ctxs,
  ) -> str:
    """### Return user's topmost role's color (skipping non-colored roles).

    Example:
    ```txt
    Your color is {color}
    ```

    Result:
    ```txt
    Your color is #ff8000
    ```

    ### Dependencies
    (SlashContext && InGuild) || GuildMessageCreateEvent
    """
    top_color = 0x0
    for role in member.get_roles():
      if str(role.color) != '#000000':
        top_color = int(role.color)
        break

    return f'{__.tcrhex(top_color, leading_zeroes=6, prefix=("" if nohash else "#"))}'


if True:  # Server

  async def server(
    name: str,
    subname: str,
    *args: str,
    **ctxs,
  ) -> str:
    """### Dispatcher for all server-related subplaceholders.

    Example:
    ```txt
    Server name: {server|name}{#|You have to specify the subplaceholder 'name'}
    ```

    Result:
    ```txt
    Server name: Mt. Celeste Paceping Association
    ```

    ### Dependencies
    Technically None but all subplaceholders require (SlashContext && InGuild) || GuildMessageCreateEvent
    """
    LOOKUP = {
      'name': _server_name,
      'id': _server_id,
    }

    if subname in LOOKUP:
      return await __.run_sac(LOOKUP[subname], name, subname, *args, **ctxs)
    else:
      return __.rebuild_yourself(name, subname, *args, **ctxs)

  @__.REQUIRE_GUILD()
  def _server_name(
    *args,
    guild: __.hikari.Guild,
    **ctxs,
  ):
    """### Get the name of the server.

    Example:
    ```txt
    Server name: {server|name}{#|You have to specify the subplaceholder 'name'}
    ```

    Result:
    ```txt
    Server name: Mt. Celeste Paceping Association
    ```

    ### Dependencies
    (SlashContext && InGuild) || GuildMessageCreateEvent
    """
    return guild.name

  @__.REQUIRE_GUILD()
  def _server_id(
    *args,
    guild: __.hikari.Guild,
    **ctxs,
  ):
    return str(guild.id)
