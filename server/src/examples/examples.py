import json
from datetime import datetime
from lib.db.db_manager import DBManager
from models.db.reader import Reader_DB
from models.db.literature import Literature_DB
from models.db.record import Record_DB
from models.api.reader import Reader
from models.api.literature import Literature
from models.api.record import Record

def create_example_data():
    # readers
    with open('examples/data/readers.json') as f:
        readers = json.load(f)
        with DBManager().session_ctx() as session:
            readers_db = session.query(Reader_DB).first()
            if readers_db is None:
                for reader in readers:
                    reader = Reader(**reader)
                    reader_db = Reader_DB(
                        rid = reader.rid,
                        tle = reader.tle,
                        type = reader.type
                    )
                    session.add(reader_db)

    # literature
    with open('examples/data/literatures.json') as f:
        literatures = json.load(f)
        with DBManager().session_ctx() as session:
            literatures_db = session.query(Literature_DB).first()
            if literatures_db is None:
                for literature in literatures:
                    literature = Literature(**literature)
                    literature_db = Literature_DB(
                        tle = literature.tle,
                        type = literature.type
                    )
                    session.add(literature_db)

    # record
    with open('examples/data/records.json') as f:
        records = json.load(f)
        with DBManager().session_ctx() as session:
            records_db = session.query(Record_DB).first()
            if records_db is None:
                for record in records:
                    record = Record(**record)
                    record_db = Record_DB(
                        bid = record.bid,
                        rid = record.rid,
                        rtt = record.rtt,
                        sta = datetime.strptime(record.sta, "%Y%m%d%H%M")
                    )
                    session.add(record_db)