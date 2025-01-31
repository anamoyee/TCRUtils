import tempfile
from pathlib import Path


def temp_file(content: str = "", *, suffix: str = None) -> Path:
	temp_file = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8", suffix=suffix)  # noqa: SIM115

	try:
		temp_file.write(content)
		temp_file_path = Path(temp_file.name)
	finally:
		temp_file.close()

	return temp_file_path
