import pathlib as p
import re as regex

from setup import PACKAGE_NAME, VERSION_REGEX

version_file = p.Path(f"./{PACKAGE_NAME}/_version.py")


def main() -> str:
	content = version_file.read_text()

	# Search for the version string and extract it
	match = regex.search(VERSION_REGEX, content)
	if match:
		version_parts = match.group(1).split(".")
		version_parts = [int(x) for x in version_parts]
		version_parts[-1] += 1  # Increment the patch version
		version_parts = [str(x) for x in version_parts]

		version_after_bump = ".".join(version_parts)

		# Replace the old version with the new version, but leave the rest of the content intact
		updated_content = regex.sub(
			regex.escape(match.group(0)),  # Match the whole version line
			f"__version__ = '{version_after_bump}'",  # Replace with the new version
			content,
		)

		# Write the updated content back to the file
		version_file.write_text(updated_content)

		return version_after_bump
	else:
		raise ValueError("Version not found in file")


if __name__ == "__main__":
	main()
