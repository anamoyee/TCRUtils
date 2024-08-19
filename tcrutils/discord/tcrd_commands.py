import arc
import hikari

from .tcrd_types import CommandIDsDict


def _get_pair_for_command(cmd: arc.SlashCommand | arc.SlashSubCommand | arc.SlashSubGroup, *previous_names):
  if hasattr(cmd, '_instances'):
    id = cmd.instances[None].id if None in cmd.instances else next(iter(cmd.instances.values())).id  # type: ignore
    return (' '.join([*previous_names, cmd.name][::-1]), id)

  return _get_pair_for_command(cmd.parent, *previous_names, cmd.name) # type: ignore

def get_slash_command_ids(arc_client: arc.GatewayClient):
  commands = list(arc_client.walk_commands(hikari.CommandType.SLASH, callable_only=True))

  pairs = [_get_pair_for_command(cmd) for cmd in commands]

  return CommandIDsDict(pairs)
