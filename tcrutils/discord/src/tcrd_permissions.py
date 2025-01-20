from collections.abc import Callable, Iterable

import hikari

Permission = hikari.Permissions

PERMISSIONS_DICT = {x: int(y) for x, y in hikari.Permissions.__dict__.items() if not x.startswith("_") and x == x.upper() and x not in ["MANAGE_EMOJIS_AND_STICKERS"]}


class _Permissions:
	"""### Contains useful utilities related to checking discord permissions.

	This is tested with the [Hikari](https://pypi.org/project/hikari/) module and most likely will not work with any module that uses a different object structure to Hikari, although `has()` function will work with any module since it takes solely the permission ints.

	use `has*` (`has`, `has_by_GMCE`, etc.) functions to return bool based on whether the user matches the selected permissions.
	use `perms.devlist = (1234,)` to set a list of devs. This step is entirely optional although you will not be able to use `allow_devs=True` option in some functions
	pass in any method you want to use for comparing permissions for example `method=perms.ANY` or `method=perms.ALL`

	It's recommended to import the permissions object as follows:
	```py
	from tcrutils.discord import permissions as perms
	# or any other short name you wish to use, although that's the name that will be used in many explainations and examples
	```
	"""

	_devs: tuple | None = None

	@property
	def devlist(self) -> list:
		return list(self._devs)  # type: ignore

	@devlist.setter
	def devlist(self, x: Iterable[int]) -> None:
		if isinstance(x, list | tuple | set) and all(isinstance(item, int) for item in x):
			self._devs = tuple(x)

	@devlist.deleter
	def devlist(self) -> None:
		self._devs = None

	@staticmethod
	def ALL(possessed: int, required: int, /) -> bool:
		"""Used in `has*()` functions (`has()`, `has_by_GMCE()`, etc.) as the method=ALL argument.

		You may, although it's not recommended to use it by itself.

		Equivalent to:
		```py
		return (possessed & required) == required # Checks if all bits of required are contained in possessed.
		```
		"""
		return (possessed & required) == required

	@staticmethod
	def ANY(possessed: int, required: int, /) -> bool:
		"""Used in `has*()` functions (`has()`, `has_by_GMCE()`, etc.) as the method=ANY argument.

		You may, although it's not recommended to use it by itself.

		Equivalent to:
		```py
		return bool(possessed & required) # Checks if any of the bits of required are set in possessed.
		```
		"""
		return bool(possessed & required)

	def has(
		self,
		possessed: int,
		required: int,
		method: Callable[[int, int], bool] = ALL,
		*,
		allow_administrator=False,
	) -> bool:
		"""Return bool whether `possessed` shares `ALL` (or `ANY` if that method is selected) bits or more with `required`.

		`allow_administrator`: Will ignore method and required permissions and return True if possessed permissions have the admininistrator bit set.
		"""
		if allow_administrator and (possessed & Permission.ADMINISTRATOR):
			return True

		return method(possessed, required)

	def has_by_GMCE(
		self,
		event: hikari.GuildMessageCreateEvent,
		required: int,
		*,
		method: Callable[[int, int], bool] = ALL,
		allow_administrator=False,
		allow_owner=False,
		allow_dev=False,
	) -> bool:
		if allow_dev:
			if self._devs is not None:
				if event.author.id in self._devs:
					return True
			else:
				raise ValueError("You can't use allow_dev=True without setting up devs first with `perms.devlist = [1337, 1234] # A list of ints (discord user ids)`")

		if allow_owner and event.author.id == event.get_guild().owner_id:  # type: ignore
			return True

		roles = event.message.member.get_roles()  # type: ignore

		if allow_administrator and any(role.permissions & hikari.Permissions.ADMINISTRATOR for role in roles):  # fmt: skip
			return True

		return any(method(role.permissions, required) for role in roles)

	def to_str(self, permissions: int) -> str:
		if not permissions:
			return f"`No permissions`"

		return ", ".join([f"`{name.replace('_', ' ').title()}`" for name, value in PERMISSIONS_DICT.items() if value & permissions])


permissions = _Permissions()
