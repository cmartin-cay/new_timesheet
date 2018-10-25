from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Time, Client

def make_session():
    """SQLAlchemy requires a session connection, so this just makes one"""
    engine = create_engine('sqlite:///timesheet.db')
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

def enter_time(name, start, end):
    session = make_session()
    entry = Time(name=name, start_time=start, end_time=end)
    session.add(entry)
    session.commit()

def enter_client(name):
    session = make_session()
    if session.query(Client).filter(Client.name==name).all():
        return
    entry = Client(name=name)
    session.add(entry)
    session.commit()

def show_client():
    session = make_session()
    clients = session.query(Client.name).all()
    return [client for client, in clients]

def activate_client(name):
    session = make_session()
    entry = session.query(Client).filter(Client.name==name).first()
    if entry and not entry.is_active:
        entry.is_active = True
        session.commit()


def inactivate_client(name):
    session = make_session()
    entry = session.query(Client).filter(Client.name==name).first()
    if entry and entry.is_active:
        entry.is_active = False
        session.commit()

