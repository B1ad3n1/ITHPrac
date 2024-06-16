from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

db_url = f"mysql+mysqlconnector://{config['DEFAULT']['db_user']}:{config['DEFAULT']['db_password']}@{config['DEFAULT']['db_host']}/{config['DEFAULT']['db_name']}"

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class LogEntry(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    ip = Column(String(15))
    timestamp = Column(DateTime)
    request = Column(String(255))
    status = Column(Integer)
    size = Column(Integer)

Base.metadata.create_all(engine)