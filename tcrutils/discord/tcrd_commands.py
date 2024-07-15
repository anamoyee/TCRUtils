from collections.abc import Generator

import arc
import hikari

from .tcrd_string import IFYs


class CommandIDsDict(dict):
  """Mapping of command_name -> command_id for slash commands in Discord."""

  def mentions(self) -> Generator[tuple[int, str], None, None]:
    """Iterate over `tuple[command_id, command_mention]` of commands in this dict where command mention is `f'</{command_name}:{command_id}>'`."""

    for command_name, command_id in self.items():
      yield command_id, IFYs.commandify(command_name, command_id)

def _get_pair_for_command(cmd: arc.SlashCommand | arc.SlashSubCommand | arc.SlashSubGroup, *previous_names):
  if hasattr(cmd, '_instances'):
    id = cmd.instances[None].id if None in cmd.instances else next(iter(cmd.instances.values())).id
    return (' '.join([*previous_names, cmd.name][::-1]), id)

  return _get_pair_for_command(cmd.parent, *previous_names, cmd.name)

def get_slash_command_ids(ACL: arc.Client):
  commands = list(ACL.walk_commands(hikari.CommandType.SLASH, callable_only=True))

  pairs = [_get_pair_for_command(cmd) for cmd in commands]

  return CommandIDsDict(pairs)
