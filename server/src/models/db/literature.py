from sqlalchemy import Column, String, Integer
from lib.db.db_util import Base


class Literature_DB(Base):
    __tablename__ = 'literatures'
    __table_args__ = ()
    # literature number
    bid = Column(
        Integer, primary_key=True, autoincrement=True,
        nullable = False
    )
    # literature name
    tle = Column(
        String(length = 64), 
        nullable = False
    )
    # literature type
    type = Column(
        String(length = 64), 
        nullable = False
    )