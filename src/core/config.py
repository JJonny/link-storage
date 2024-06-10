from environs import Env
from pathlib import Path
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parents[1].absolute()


Env.read_env()


class Config(BaseSettings):
    """Base config"""

    JWT_SECRET: str


config = Config()
