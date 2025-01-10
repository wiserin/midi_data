from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///app.db')

Base = declarative_base()

class Link(Base):
    __tablename__ = 'link'

    id = Column(Integer, primary_key=True)
    link = Column(String)


class Mid(Base):
    __tablename__ = 'mid'

    id = Column(Integer, primary_key=True)
    note = Column(String)
    previous_note = Column(String)

start_db = Base.metadata.create_all(engine)