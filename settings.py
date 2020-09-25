from typing import Set

from pydantic import (
    BaseModel,
    BaseSettings,
    PyObject,
    RedisDsn,
    PostgresDsn,
    Field,
)

class Settings(BaseSettings):

    # trader = 'ratmach'
    trader = 'Belleblue'

    lot_size = 0.01
    

settings = Settings()

