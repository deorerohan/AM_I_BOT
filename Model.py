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

class Group(Base):
    __tablename__ = 'Group'
    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    group_type = Column(String(250))

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    user_name = Column(String(250))
    first_name = Column(String(250))
    last_name = Column(String(250))
    is_bot = Column(Boolean, nullable=False)
    group_id = Column(Integer, ForeignKey('Group.id'))
    group = relationship(Group)
 
class Query(Base):
    __tablename__ = 'Query'
    id = Column(Integer, primary_key=True)
    query = Column(String(250))
    query_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'))
    person = relationship(User)

def AddUser(effective_user, effective_chat):
    """Add user if not exists"""
    chatId = effective_chat.id
    chatType = effective_chat.type
    chatTitle = effective_chat.title
    userId = effective_user.id

    if chatId == userId:
        exists = session.query(User).filter_by(user_id=userId, group_id=None).one_or_none()
        group_exists = False
    else:
        exists = session.query(User).filter_by(user_id=userId, group_id=chatId).one_or_none()
        group_exists = session.query(Group).filter_by(id=chatId).one_or_none()

    if(exists is not None):
        return False

    userGroupID = None
    if chatId != userId:
        userGroupID = chatId

    new_user = User(user_id=userId, 
        user_name = effective_user.username, 
        first_name=effective_user.first_name, 
        last_name=effective_user.last_name, 
        is_bot = effective_user.is_bot,
        group_id = userGroupID)

    if chatId != userId and group_exists is None:
        new_group = Group(id = chatId,
        group_type = chatType,
        title = chatTitle)
        session.add(new_group)

    session.add(new_user)
    session.commit()
    return True

def CheckUser(firstname, chatID):
    exists = session.query(User).filter_by(first_name=firstname, group_id=chatID).one_or_none()
    if(exists is None):
        return False, False
    else:
        return True, exists.is_bot

def AddQuery(id, chatId, query):
    if id == chatId:
        chatId = None

    exists = session.query(User).filter_by(user_id=id, group_id=chatId).one_or_none()
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
