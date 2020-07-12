from sqlalchemy import (Column, ForeignKey, 
        Integer, String, Boolean, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

# Create an engine that stores data in the local directory's
# telegram_bot_info.db file.
engine = create_engine('sqlite:///telegram_bot_info.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(250))
    first_name = Column(String(250))
    last_name = Column(String(250))
    is_bot = Column(Boolean, nullable=False)
 
class Query(Base):
    __tablename__ = 'Query'
    id = Column(Integer, primary_key=True)
    query = Column(String(250))
    query_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'))
    person = relationship(User)

def AddUser(id, username, firstname, lastname, isbot):
    """Add user if not exists"""
    exists = session.query(User).filter_by(id=id).one_or_none()
    if(exists is not None):
        return False

    new_user = User(id=id, user_name = username, first_name=firstname, last_name=lastname, is_bot = isbot)
    session.add(new_user)
    session.commit()
    return True

def CheckUser(firstname):
    exists = session.query(User).filter_by(first_name=firstname).one_or_none()
    if(exists is None):
        return False, False
    else:
        return True, exists.is_bot

def AddQuery(id, query):
    exists = session.query(User).filter_by(id=id).one_or_none()
    if(exists is None):
        return False
    
    number = session.query(Query).filter_by(user_id=exists.id).count()
    if number > 100:
        return False

    new_query = Query(query = query, query_time=datetime.datetime.now(), user_id=exists.id)
    session.add(new_query)
    session.commit()
    return True

if __name__ == "__main__":
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)
