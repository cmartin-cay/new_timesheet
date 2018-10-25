from sqlalchemy import Column, String, Integer, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()

class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    name =Column(String(250), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"Client {self.name} is shown: {self.is_active}"


class Time(Base):
    __tablename__ = 'time'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    def time_spent(self):
        return (self.end_time - self.start_time).seconds


    def __repr__(self):
        return f"Client {self.name} for {self.time_spent()/60:.0f} minutes"

if __name__=="__main__":
    engine = create_engine('sqlite:///timesheet.db')
    Base.metadata.create_all(engine)