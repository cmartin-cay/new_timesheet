from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Time, Client


def make_session():
    """
    Generate a SQLAlchemy session
    :return: SQLAlchemy session
    """
    engine = create_engine("sqlite:///timesheet.db")
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


def enter_time(name, total_time):
    """
    Create a Time entry in the Time database
    :param name: Client Name
    :param start: Datetime
    :param end: Datetime
    :return: None
    """
    session = make_session()
    entry = Time(name=name, total_time=total_time)
    session.add(entry)
    session.commit()


def enter_multiple_times(time_dictionary):
    """
    Create multiple Time entries in the Time database
    :param dictionary: Dictionary formatted to match the Time class
    :return: None
    """
    session = make_session()
    for entry in time_dictionary.items():
        name, total_time = entry
        new_entry = Time(name=name, total_time=total_time)
        session.add(new_entry)
    session.commit()


def enter_client(name):
    """
    Add a new client to the Client database
    :param name: Client Name
    :return: None
    """
    session = make_session()
    if session.query(Client).filter(Client.name == name).all():
        return
    entry = Client(name=name)
    session.add(entry)
    session.commit()


def show_clients(active=True):
    """
    Query the Client database for active/inactive clients
    :param active: Boolean
    :return: List
    """
    session = make_session()
    clients = session.query(Client.name).filter(Client.is_active == active).all()
    return [client for client, in clients]


def show_all_clients():
    """
    Query the Client database for all clients
    :return: List
    """
    session = make_session()
    clients = session.query(Client.name).all()
    return [client for client, in clients]


def activate_client(name):
    """
    Change a client status to active
    :param name: Client Name
    :return: None
    """
    session = make_session()
    entry = session.query(Client).filter(Client.name == name).first()
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
    entry = session.query(Client).filter(Client.name == name).first()
    if entry and entry.is_active:
        entry.is_active = False
        session.commit()

def retrieve_time():
    """

    :param start_date:
    :param end_date:
    :return:
    """
    session = make_session()
    time_entries = session.query(Time).all()
    return time_entries

if __name__ == '__main__':
    res = []
    for entry in retrieve_time():
        res.append([entry.name, entry.total_time, entry.day.strftime("%A")])
    print(res)
