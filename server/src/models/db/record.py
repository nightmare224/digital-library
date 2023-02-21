from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from lib.db.db_util import Base
from models.db.literature import Literature_DB

class Record_DB(Base):
    __tablename__ = 'records'
    __table_args__ = ()
    
    # record number
    tid = Column(
        Integer, primary_key=True, autoincrement=True,
        nullable = False
    )
    # literature number
    bid = Column(
        Integer,
        ForeignKey("literatures.bid", ondelete="CASCADE"),
        nullable = False
    )
    # feature data
    rid = Column(
        String(length = 64),
        nullable = False
    )
    # ciphertext data
    rtt = Column(
        String(length = 64),
        nullable = False
    )
    # lending time (leanding ocurrence time)
    sta = Column(
        DateTime,
        nullable = False
    )