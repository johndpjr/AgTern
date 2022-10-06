from pathlib import Path
from os import makedirs
from os.path import isfile
from typing import Union


class DataFile:
    def __init__(
        self,
        filename: str,
        is_temp: bool = False,
        default_data: Union[str, None] = None,
    ):
        self.filename = filename
        self.is_temp = is_temp
        if is_temp:
            self.path = Path.cwd().joinpath("data", "temp", filename)
        else:
            self.path = Path.cwd().joinpath("data", filename)

        # Makes sure file exists after initialization
        assert self.exists() or self.create(default_data)

    def exists(self):
        return isfile(self.path)

    def create(self, default_data: str):
        """Creates a data file if it doesn't exist. Returns true if successful."""
        # Will only create new file if default data given
        assert not self.exists() and default_data
        try:
            if self.is_temp:
                makedirs(Path.cwd().joinpath("data", "temp"), exist_ok=True)
            else:
                makedirs(Path.cwd().joinpath("data"), exist_ok=True)

            with open(self.path, "w") as f:
                f.write(default_data)
        except OSError:
            pass
        return self.exists()
