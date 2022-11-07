from os import getenv

CONFIG_FILE_NAME = "pymod.json"
DEFAULT_DEST_FOLDER = "_models"


class Config:
    database_url: str | None
    dest_folder: str | None

    def __init__(
        self, *, database_url: str | None = None, dest_folder: str | None = None
    ) -> None:
        self.database_url = database_url
        self.dest_folder = dest_folder or DEFAULT_DEST_FOLDER


def init_config() -> Config:
    database_url = getenv("DATABASE_URL")

    return Config(database_url=database_url)


config = init_config()
