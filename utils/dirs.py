import pathlib
import shutil

from config import settings


def get_media_path(prefix: str) -> pathlib.Path:
    if not isinstance(prefix, str):
        prefix = str(prefix)
    return settings.ROOT_DIR.joinpath(settings.MEDIA, prefix)


def create_dir(prefix: str):
    dir_path = get_media_path(prefix)
    if not dir_path.exists():
        dir_path.mkdir(parents=True)


def remove_dir(prefix: str):
    dir_path = get_media_path(prefix)
    if dir_path.exists():
        shutil.rmtree(dir_path)
