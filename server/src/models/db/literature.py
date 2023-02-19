from sqlalchemy import Column, String
from lib.db.db_util import Base


class Literature_DB(Base):
    __tablename__ = 'literatures'
    __table_args__ = ()
    # literature number
    bid = Column(
        String(length = 64),
        unique = True, primary_key = True, nullable = False
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