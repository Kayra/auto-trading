from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy import create_engine
import datetime

engine = create_engine("postgresql://autotrader:pa55word@localhost:5432/autotrader", echo=False)

Base = declarative_base()


class Car(Base):

    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)
    milage = Column(Integer)
    transmission = Column(String)
    year = Column(DateTime)
    price = Column(Integer)
    size = Column(Float)
    first_scraped = Column(DateTime, default=datetime.datetime.utcnow)
    last_scraped = Column(DateTime)


# To create the tables, uncomment the next line and run this script
# Base.metadata.create_all(engine)
