import arc as __arc
import hikari as __hikari

from ...discord.tcrd_snowflake import is_snowflake as __is_snowflake
from .. import util as __

if True:  # User

  @__.REQUIRE('ctx', 'event')
  @__.REQUIRE('user_mentions')
  @__.SWITCH('noping')
  def mention(
    name,
    user: str | None = None,
    *args: str,
    ctx: __arc.Context | None,
    event: __hikari.MessageCreateEvent | None,
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

    if not noping:
      user_mentions.append(author_id)

    return f'<@{author_id}>'

  @__.REQUIRE('ctx', 'event')
  def username(
    *args,
    ctx: __arc.Context | None,
    event: __hikari.MessageCreateEvent | None,
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

    if ctx:
      return ctx.author.username
    else:
      return event.author.username
