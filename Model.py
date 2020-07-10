from sqlalchemy import (Column, ForeignKey, 
        Integer, String, Boolean, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
 
Base = declarative_base()

# Create an engine that stores data in the local directory's
# telegram_bot_info.db file.
engine = create_engine('sqlite:///telegram_bot_info.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(250), unique=True, nullable=False)
    is_bot = Column(Boolean, nullable=False)
 
class Query(Base):
    __tablename__ = 'Query'
    id = Column(Integer, primary_key=True)
    query = Column(String(250))
    query_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'))
    person = relationship(User)

def AddUser(username, isbot):
    """Add user if not exists"""
    exists = session.query(User).filter_by(user_name=username).one_or_none()
    if(exists is not None):
        return False

    new_user = User(user_name = username, is_bot = isbot)
    session.add(new_user)
    session.commit()
    return True

def CheckUser(username):
    exists = session.query(User).filter_by(user_name=username).one_or_none()
    if(exists is None):
        return False, False
    else:
        return True, exists.is_bot

if __name__ == "__main__":
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)
