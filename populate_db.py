from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Time, Client

def make_session():
    """
    Generate a SQLAlchemy session
    :return: SQLAlchemy session
    """
    engine = create_engine('sqlite:///timesheet.db')
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

def enter_time(name, start, end):
    """
    Create a Time entry in the Time database
    :param name: Client Name
    :param start: Datetime
    :param end: Datetime
    :return: None
    """
    session = make_session()
    entry = Time(name=name, start_time=start, end_time=end)
    session.add(entry)
    session.commit()

def enter_client(name):
    """
    Add a new client to the Client database
    :param name: Client Name
    :return: None
    """
    session = make_session()
    if session.query(Client).filter(Client.name==name).all():
        return
    entry = Client(name=name)
    session.add(entry)
    session.commit()

def show_clients(active=True):
    """
    Query the Client database for all clients
    :param active: Boolean
    :return: List
    """
    session = make_session()
    clients = session.query(Client.name).filter(Client.is_active==active).all()
    return [client for client, in clients]


def activate_client(name):
    """
    Change a client status to active
    :param name: Client Name
    :return: None
    """
    session = make_session()
    entry = session.query(Client).filter(Client.name==name).first()
    if entry and not entry.is_active:
        entry.is_active = True
        session.commit()


def inactivate_client(name):
    """
    Change a client status to not active
    :param name: Client Name
    :return: None
    """
    session = make_session()
    entry = session.query(Client).filter(Client.name==name).first()
    if entry and entry.is_active:
        entry.is_active = False
        session.commit()
