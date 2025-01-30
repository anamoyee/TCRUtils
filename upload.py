import pathlib as p
import string
import subprocess
import sys

from bump_version import main as _bump_version

ALLOWED_CHARS = string.ascii_letters + string.digits + "-_/\\.: "


def print_error(msg: str, *, and_exit: bool = True):
	print(f"\nUPLOAD FAILED: {msg}\n")
	if and_exit:
		sys.exit(1)


def bump_version() -> str:
	version_after_bump = _bump_version()
	return "".join(filter(lambda x: x in ALLOWED_CHARS, version_after_bump))


def rm_r_dist_directory():
	dist_folder = p.Path("./dist")

	if not dist_folder.is_dir():
		print_error("./dist/ folder not found, are you in the correct directory?")
		sys.exit(1)

	for file in dist_folder.iterdir():
		file.unlink()


def run_shell_commands(*, version_after_bump: str):
	cmds = f"""
git add .
git commit -m "commit files not committed before upload and bump version to {version_after_bump}"
git push
py -m build
py -m twine upload dist/*
""".strip().split("\n")

	for cmd in cmds:
		# input(f'RUNNING: {cmd!r}\n>>> ')
		subprocess.run(cmd, shell=True)


def main():
	version_after_bump = bump_version()
	rm_r_dist_directory()
	run_shell_commands(
		version_after_bump=version_after_bump,
	)


if __name__ == "__main__":
	main()
