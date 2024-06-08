from environs import Env
from pathlib import Path
from pydantic import BaseConfig


BASE_DIR = Path(__file__).parents[1].absolute()


Env.read_env()


class Config(BaseConfig):
    """Base config"""

    JWT_SECRET: str


config = Config()
