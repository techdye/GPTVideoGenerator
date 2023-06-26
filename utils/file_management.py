import logging
from pathlib import Path


def create_files(files: list[str], folders: list[str], main_path: Path = Path(__file__).parents[1]) -> tuple[list[str], list[str]]:
    created_files = []
    created_folders = []

    if files:
        for file in files:
            path = main_path / file

            if not path.exists():
                path.touch()
                created_files.append(str(path))

            logging.debug(f"{path} created!")

    if folders:
        for folder in folders:
            path = main_path / folder

            if not path.exists():
                path.mkdir(parents=True)
                created_folders.append(str(path))

            logging.debug(f"{path} created!")

    return created_files, created_folders
