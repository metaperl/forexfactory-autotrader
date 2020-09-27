from sqlalchemy import Column, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

import os
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
engine = create_engine(f'sqlite:///{dir_path}/placed_trades.db', echo=True)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class PlacedTrades(Base):
    __tablename__ = "placed_trades"

    id = Column(String, primary_key=True)
    symbol = Column(String)
    price = Column(String)
    trade_id = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())




# Base.metadata.create_all(engine)
