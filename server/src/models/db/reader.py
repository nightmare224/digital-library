from sqlalchemy import Column, String
from lib.db.db_util import Base


class Reader_DB(Base):
    __tablename__ = 'readers'
    __table_args__ = ()
    # reader number
    rid = Column(
        String(length = 64),
        unique = True, primary_key = True, nullable = False
    )
    # reader name
    tle = Column(
        String(length = 64), 
        nullable = False
    )
    # reader type
    type = Column(
        String(length = 64), 
        nullable = False
    )