import tempfile
from pathlib import Path


def temp_file(filename: str, content: str) -> Path:
  temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix=filename)

  try:
    temp_file.write(content)
    temp_file_path = Path(temp_file.name)
  finally:
    temp_file.close()

  return temp_file_path
