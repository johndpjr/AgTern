import json
from os import fsdecode, listdir, makedirs, remove
from os.path import isdir, isfile
from pathlib import Path
from shutil import rmtree
from typing import IO, AnyStr, Self, Union


class DataFile:
    def __init__(
        self,
        *path: str,
        is_temp: bool = False,
        default_data: Union[str, None] = None,
        create_on_init: bool = True,
    ):
        self._full_name = fsdecode(path[-1])
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

    @property
    def name(self) -> str:
        """Returns the name of this data file including its extension."""
        return self._full_name

    @property
    def name_without_extension(self) -> Union[str, None]:
        """Returns the name of this data file without its file extension."""
        dot_location = self._full_name.find(".")
        return self._full_name[:dot_location] if dot_location != -1 else None

    @property
    def extension(self) -> Union[str, None]:
        """Returns the file extension of this data file (ex: .json, .tar.gz, None). Always lowercase."""
        dot_location = self._full_name.find(".")
        return self._full_name[dot_location:].lower() if dot_location != -1 else None

    @property
    def exists(self) -> bool:
        """Returns true if this data file exists."""
        return isfile(self.path)

    def create(self, default_data: Union[str, None] = None) -> bool:
        """Creates a data file if it doesn't exist. Returns true if successful."""
        if self.exists:
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

    def delete(self) -> bool:
        """Deletes a data file if it exists. Returns true if successful."""
        if not self.exists:
            return True
        success = False
        try:
            remove(self.path)
            success = True
        except OSError:
            pass
        return success

    def open(self, *args, **kwargs) -> IO:
        """Attempts to open a data file. Raises OSError on failure."""
        return open(self.path, *args, **kwargs)

    def contents(self, binary: bool = False) -> AnyStr:
        """Attempts to read a data file and return the result as a string. Raises OSError on failure."""
        mode = "rb" if binary else "r"
        with self.open(mode) as f:
            return f.read()

    def lines(self) -> list[AnyStr]:
        """Attempts to read a data file and return its lines as a list of strings. Raises OSError on failure."""
        with self.open("r") as f:
            return f.readlines()

    def overwrite_contents(self, data: AnyStr, binary: bool = False):
        """Attempts to write to a data file. Raises OSError on failure."""
        mode = "wb" if binary else "w"
        with self.open(mode) as f:
            f.write(data)

    def load_json(self, *args, **kwargs) -> Union[dict, list]:
        """Attempts to read a data file as JSON and returns the parsed object. Raises OSError or JSONDecodeError on failure."""
        return json.loads(self.contents(), *args, **kwargs)

    def __repr__(self) -> str:
        """Returns a string representation of this data file. Used in Python interactive sessions."""
        return f"DataFile({str(self.path.relative_to(Path.cwd()))})"

    def __str__(self) -> str:
        """Returns the absolute path of this data file as a string."""
        return str(self.path)


class DataFolder:
    def __init__(self, *path: str, is_temp: bool = False, create_on_init: bool = True):
        self.path_segments = path
        self.is_temp = is_temp
        if is_temp:
            self.path = Path.cwd().joinpath("data", "temp", *path)
        else:
            self.path = Path.cwd().joinpath("data", *path)

        if create_on_init:
            assert self.create()

    @property
    def name(self) -> str:
        """Returns the name of this data folder."""
        return self.path_segments[-1]

    @property
    def exists(self) -> bool:
        """Returns true if this data folder exists."""
        return isdir(self.path)

    def clean(self) -> bool:
        """Deletes all data files in this data folder if the data folder exists. Returns true if successful."""
        if not self.exists:
            return True
        success = False
        try:
            self.delete()
            self.create()
            success = True
        except OSError:
            pass
        return success

    def create(self) -> bool:
        """Creates a data folder if it doesn't exist. Returns true if successful."""
        if self.exists:
            return True
        success = False
        try:
            makedirs(self.path, exist_ok=True)
            success = True
        except OSError:
            pass
        return success

    def delete(self) -> bool:
        """Deletes a data folder if it exists. Returns true if successful."""
        if not self.exists:
            return True
        success = False
        try:
            rmtree(self.path)
            success = True
        except OSError:
            pass
        return success

    def file(self, filename: str, create_on_init: bool = True) -> DataFile:
        """Returns a data file in this data folder by name."""
        return DataFile(
            *self.path_segments,
            filename,
            is_temp=self.is_temp,
            create_on_init=create_on_init,
        )

    def folder(self, foldername: str, create_on_init: bool = True) -> Self:
        """Returns a data folder in this data folder by name."""
        return DataFolder(
            *self.path_segments,
            foldername,
            is_temp=self.is_temp,
            create_on_init=create_on_init,
        )

    def files(self) -> list[DataFile]:
        """Returns a list of all of the data files in this data folder."""
        if not self.exists:
            return []
        return [
            DataFile(
                *self.path_segments,
                fsdecode(filename),
                is_temp=self.is_temp,
                create_on_init=False,
            )
            for filename in listdir(self.path)
            if isfile(self.path.joinpath(filename))
        ]

    def folders(self) -> list[Self]:
        """Returns a list of all of the data folders in this data folder."""
        if not self.exists:
            return []
        return [
            DataFolder(
                *self.path_segments,
                fsdecode(foldername),
                is_temp=self.is_temp,
                create_on_init=False,
            )
            for foldername in listdir(self.path)
            if isdir(self.path.joinpath(foldername))
        ]

    def items(self) -> list[Union[DataFile, Self]]:
        """Returns a list of all of the data files and data folders in this data folder."""
        return sorted([*self.files(), *self.folders()], key=lambda i: str(i.path))

    def __repr__(self) -> str:
        """Returns a string representation of this data folder. Used in Python interactive sessions."""
        return f"DataFolder({str(self.path.relative_to(Path.cwd()))})"

    def __str__(self) -> str:
        """Returns the absolute path of this data folder as a string."""
        return str(self.path)
