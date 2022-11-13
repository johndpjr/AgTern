from os import makedirs, remove
from os.path import isdir, isfile
from pathlib import Path
from shutil import rmtree
from typing import Union


class DataFile:
    def __init__(
        self,
        *path: str,
        is_temp: bool = False,
        default_data: Union[str, None] = None,
        create_on_init: bool = True
    ):
        self.name = path[-1]
        self.is_temp = is_temp
        if is_temp:
            self.path = Path.cwd().joinpath("data", "temp", *path)
        else:
            self.path = Path.cwd().joinpath("data", *path)
        self.folder = DataFolder(
            *(path[:-1]), is_temp=is_temp, create_on_init=create_on_init
        )

        if create_on_init:
            assert self.create(default_data)

    def exists(self):
        return isfile(self.path)

    def create(self, default_data: Union[str, None] = None):
        """Creates a data file if it doesn't exist. Returns true if successful."""
        if self.exists():
            return True
        success = False
        try:
            self.folder.create()
            with open(self.path, "w") as f:
                f.write(default_data if default_data else "")
            success = True
        except OSError:
            pass
        return success

    def delete(self):
        if not self.exists():
            return True
        success = False
        try:
            remove(self.path)
            success = True
        except OSError:
            pass
        return success


class DataFolder:
    def __init__(self, *path: str, is_temp: bool = False, create_on_init: bool = True):
        self.is_temp = is_temp
        if is_temp:
            self.path = Path.cwd().joinpath("data", "temp", *path)
        else:
            self.path = Path.cwd().joinpath("data", *path)

        if create_on_init:
            assert self.create()

    def exists(self):
        return isdir(self.path)

    def clean(self):
        if not self.exists():
            return True
        success = False
        try:
            self.delete()
            self.create()
            success = True
        except OSError:
            pass
        return success

    def create(self):
        if self.exists():
            return True
        success = False
        try:
            makedirs(self.path, exist_ok=True)
            success = True
        except OSError:
            pass
        return success

    def delete(self):
        if not self.exists():
            return True
        success = False
        try:
            rmtree(self.path)
            success = True
        except OSError:
            pass
        return success
