#!/usr/bin/env python3

import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path


def pause(message):
	input(f"{message} Press enter to continue or Ctrl+C to abort...")


def get_version_from_hatch_config(pyproject_path: Path) -> str:
	with pyproject_path.open("rb") as f:
		data = tomllib.load(f)

	try:
		hatch_config = data["tool"]["hatch"]["version"]
		version_file = hatch_config["path"]
		pattern = hatch_config["pattern"]
	except KeyError as e:
		print(f"Missing or invalid hatch dynamic version config in pyproject.toml: {e}")
		sys.exit(1)

	version_path = pyproject_path.parent / version_file
	if not version_path.exists():
		print(f"Version file not found: {version_path}")
		sys.exit(1)

	version_text = version_path.read_text(encoding="utf-8")
	match = re.search(pattern, version_text)
	if not match:
		print(f"Version pattern not found in {version_path}")
		sys.exit(1)

	return match.group("version")


def main():
	script_dir = Path(__file__).resolve().parent
	os.chdir(script_dir)

	pause("Have you bumped the version?")

	pyproject_path = script_dir / "pyproject.toml"
	if not pyproject_path.exists():
		print("pyproject.toml not found.")
		sys.exit(1)

	version = get_version_from_hatch_config(pyproject_path)

	try:
		subprocess.run(["git", "add", "."], check=True)
		subprocess.run(["git", "commit", "-m", f"Release {version}"], check=True)
		subprocess.run(["git", "push"], check=True)
	except subprocess.CalledProcessError:
		print("Git command(s) failed. Aborting.")
		sys.exit(1)

	dist_dir = script_dir / "dist"
	dist_dir.mkdir(exist_ok=True)

	# Clear contents of dist/
	for file in dist_dir.glob("*"):
		if file.is_file():
			file.unlink()

	try:
		subprocess.run(["uv", "build"], check=True)

		token_path = script_dir / "PYPI_TOKEN.txt"
		if not token_path.exists():
			print("Error: PYPI_TOKEN.txt not found.")
			sys.exit(1)

		token = token_path.read_text(encoding="utf-8").strip()
		subprocess.run(["uv", "publish", "--token", token], check=True)

	except subprocess.CalledProcessError:
		print("Build or publish failed.")
		sys.exit(1)


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\nAborted by user.")
		sys.exit(1)
