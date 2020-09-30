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

    trade_explorer_url = 'https://www.forexfactory.com/belleblue#acct.94-tab.overview-explorer'
    trade_explorer_url = 'https://www.forexfactory.com/ratmach#acct.05-tab.overview-explorer.192759'
    lot_size = 0.01
    

settings = Settings()

