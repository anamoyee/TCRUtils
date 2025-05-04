import subprocess
import sys

from .console import console as c


class Dependency:
	import_name: str
	pip_name: str

	def __init__(self, *, import_as: str, pip_install_as: str = None) -> None:
		self.import_name = import_as
		self.pip_name = pip_install_as or import_as

	def install(self) -> bool:
		"""Returns bool if the installation succeeded or not."""
		try:
			subprocess.run([sys.executable, "-m", "pip", "install", self.pip_name], check=True)
		except subprocess.CalledProcessError:
			return False
		except Exception:
			return False
		else:
			return True


class DependencyEnsurer:
	deps: tuple[Dependency]
	auto_install: bool

	def __init__(self, *deps: Dependency, auto_install: bool = False) -> None:
		"""Allows libraries to have optional dependencies (I KNOW OF `lib[extra]` syntax..! - you should probably use that thing instead).

		Requires at least 1 dependency to work. (will do nothing if `deps=()`)

		auto_install: If true, will install any missing dependencies automatically, if False, a RuntimeError will be raised and a message will be displayed. Warning: This may heavily slow down the program and may crash if no internet connection is present to fetch the missing dependencies.
		"""
		self.deps = deps
		self.auto_install = auto_install

	def __call__(self, auto_install_override: bool | None = None) -> bool:
		"""Verify if this package's dependencies are installed."""

		auto_install = auto_install_override if auto_install_override is not None else self.auto_install

		missing_deps: list[Dependency] = []

		for dep in self.deps:
			try:
				__import__(dep.import_name)
			except ImportError:
				missing_deps.append(dep)

		def errored():
			c.error("The following dependencies are missing:")
			for dep in missing_deps:
				c.error(f"{dep.import_name!r} (pip install {dep.pip_name})")
			raise RuntimeError("Missing dependencies (see errors above for tips!!).")

		if missing_deps:
			if auto_install:
				for dep in missing_deps.copy():
					if not dep.install():
						errored()
					else:
						missing_deps.remove(dep)
			else:
				errored()
