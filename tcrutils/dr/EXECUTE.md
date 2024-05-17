# Execute (aka Dynamic Responses)

A feature from **[RoboTop](https://robotop.xyz)**, a now shutdown bot made by [Colon](https://gdcolon.com)<img style="width: 15px; height: 15px;" src="https://cdn.discordapp.com/emojis/1132968267963715634.webp?size=64&name=fluff&quality=lossless"></img>
I only recreated said feature in python, i am not the original idea provider of it.

#### This subpackage implements **contexed-placeholder-transformation** of a string:

#### For a full list of built in (choosable by default) placeholders see [PLACEHOLDERS.md](./PLACEHOLDERS.md)

Let's start with an example (top line: before, bottom line: after):
```md
Hello **{nickname}**! Welcome to **{server|name}**!{attach|https://gdcolon.com/assets/colon.png}
Hello **anamoyee :3**! Welcome to **TCRUtils Testing Server**!
```

\[If sent on Discord, to the bottom text an image would be attached due to `{attach|<url>}`]

Currently for discord only the [Hikari](https://pypi.org/project/hikari/) ([Github](https://github.com/hikari-py/hikari)) library is pre-written, however it supports custom {placeholders} if only you're willing to write them for your library.
Placeholders not depentant on Discord should work everywhere ({var}, {add})

Let's explain this step by step:
- **Contexted**: Placeholders get context like, your discord's library current event/ctx, the state that may be changed by other (previously evaluated) placeholders, or any other state you might want to introduce.
- **Placeholder**: A placeholder is a substring bounded by chosen parenthesis (default `{}`), which is replaced by a value on evaluation time, evaluated from left-right, innermost first. For example you can nest placeholders: `{add|1|{div|4|2}}` -> `{add|1|2}` -> `3`
- **Transformation**: String is slowly transformed from leftmost, innermost placeholder to the rightmost outermost one, slowly changing the placeholder's values or arguments

Placeholder arguments are split by a splitter (default: `|`), for example: `{add|1|2}`
- First argument is the placeholder identifier, it will be the chosen key of the placeholders dictionary you have to provide.
- Any subsequent arguments are passed to placeholder as text (the name of the placeholder itself is passed as well as the first argument, if it was invoked by an alias, the alias will be passed) (simillar to `sys.argv`)

## Setup / usage
```py
# Define an EXECUTE instance. You can reuse it to reuse the below settings.
EXECUTE = tcr.dynamic_responses.DynamicResponseBuilder(
  tcr.dr.placeholder_set.ALL, # Choose the placeholder sets you wish to include, either built in or your own.
  {"myplaceholder": myplaceholder_callable}, # You may choose multiple sets of placeholders or add/or mix them with your custom placeholder sets (in this case a placeholderset containing one placeholder) - not to be confused with builtins.set, this is a dict!
  # parens=('{{', '}}'), # You may change parens
  # splitter='!', # or the splitter
  # Many other instance settings may be provided. Read the `DynamicResponseBuilder`'s docstring for more details.
)

result = await EXECUTE("Hello {username}", **{
  'ctx': ctx, # Any contexts you might want to provide to the placeholders you use
  # make sure to always provide all required contexts by the placeholders you use or narrow your placeholder sets.
})

print(result) # May be interpreted as a str, although it loses track of the contexts (unless kept somewhere else), or...
await ctx.respond(**result.resp) # ...may be converted into a hikari ctx.respond() dict with .resp property
```

## Placeholder signatures & examples (read if you're willing to code your own placeholders.):
```py
def placeholder(name: str, *args: str, **ctxs) -> str | None:
  ... # Transform values by taking args, name and/or contexts into account
  return 'hai' # Example: this placeholder automatically voids anything and everything passed into it and gets always replaced with the string 'hai'. {#} works simillarly
```
```py
def literal_text_example(*_, **__) -> str:
  return '{placeholder}' # This will NOT invoke the {placeholder} placeholder. This will return the literal text, to evaluate placeholders see util.build_placeholder_rich_return_value()
```
```py
@util.STRINGIFY
def stringify_example(*_, **__) -> Any:
  return 123+456 # Will not error due to the @STRINGIFY decorator converting the type into a str.
```
```py
@util.STRINGIFY
@util.REQUIRE('event', 'ctx') # This ensure that EITHER of 'event' or 'ctx' contexts is present
def contexed_placeholder_example(*_, event: hikari.MessageCreateEvent, ctx: arc.Context, **__):
  if ctx:
    return ctx.author.id
  else: # At least one of 'event' or 'ctx' is guaranteed to be present, if it's not, DynamicResponsePlaceholderMissingContextError will be raised.
    return event.author.id
```
```py
@util.STRINGIFY
@util.REQUIRE('event')
@util.REQUIRE('ctx') # This would mean: BOTH 'event' and 'ctx' must be present
...
```
```py
@util.STRINGIFY
@util.REQUIRE_AUTHOR # This ensures an author is present, simillar to REQUIRE('event', 'ctx') but extracts the author from the available event/ctx and passes it as the `author` context
def author_placeholder_example(*_, author: hikari.User, **__):
  ...
```
```py
@util.REQUIRE('user_mentions') # Any mutable objects will be correctly mutated and their states will be changed throughout this dynamic response.S
@util.REQUIRE_AUTHOR
def mention(*_, user_mentions: list[hikari.User], author: hikari.User, **__):
  user_mentions.append(author) # You can then use `**EXECUTE('{mention}').resp` property to convert the execute response to a hikari ctx.respond() response.
  return f'<@{author.id}>'
```
