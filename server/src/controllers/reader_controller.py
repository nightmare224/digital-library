
from flask import Blueprint, jsonify, request
from datetime import datetime
from sqlalchemy import and_
from lib.db.db_manager import DBManager
from models.api.reader import Reader
from models.api.record import Record
from models.db.reader import Reader_DB
from models.db.record import Record_DB
from lib.api.responses import Create, Update, Read, Delete
from lib.api.exceptions import OtherBadRequest, OtherConflict, OtherNotFound

reader_controller = Blueprint('reader_controller', __name__)

@reader_controller.route('/digitallibrary/server/api/reader', methods=['GET'])
def get_reader():
    """
    Get all readers in server side digital library.
    ---
    tags:
        - Reader APIs
    produces: application/json
    responses:
        200:
            description: ok
            schema:
                type: array
                items:
                    schema:
                        id: Reader
                        type: object
                        properties:
                            rid:
                                type: string
                                example: 2019IN013
                            tle:
                                type: string
                                example: Nicole Tai
                            type:
                                type: string
                                example: basic
    """
    
    readers = []
    with DBManager().session_ctx() as session:
        readers_db = session.query(Reader_DB).all()
        for reader_db in readers_db:
            reader = Reader(
                rid=reader_db.rid,
                tle=reader_db.tle,
                type=reader_db.type
            )
            readers.append(reader)

    resp = Read(payload = readers)
    return jsonify(resp.payload), resp.status_code

@reader_controller.route('/digitallibrary/server/api/reader', methods=['POST'])
def create_reader():
    """
    Create a reader in server side digital library.
    ---
    tags:
        - Reader APIs
    produces: application/json
    responses:
        201:
            description: created
    parameters:
      - in: body
        name: Reader
        schema:
            type: array
            items:
                schema:
                    id: Reader
    """    

    request_data = request.get_json()
    try:
        readers = []
        for reader in request_data:
            reader = Reader(**reader)
            if is_reader_exist(reader.rid):
                raise OtherConflict("Reader with same RID is already existed")
            readers.append(reader)
    except TypeError as e:
        raise OtherBadRequest('Invalid request data: %s'%e)

    with DBManager().session_ctx() as session:
        for reader in readers:
            reader_db = Reader_DB(
                rid = reader.rid,
                tle = reader.tle,
                type = reader.type
            )
            session.add(reader_db)

    resp = Create()
    return jsonify(resp.payload), resp.status_code


@reader_controller.route('/digitallibrary/server/api/reader/<rid>/record', methods=['GET'])
def get_reader_record(rid):
    """
    Get the reader's record in server side digital library.
    ---
    tags:
        - Reader APIs
    produces: application/json
    parameters:
      - in: path
        name: rid
        schema:
            type: string
            example: 7PBC52BAB
        required: true
        description: reader number feature data
      - in: query
        name: bid
        schema:
            type: string
            example: 12
        description: literature number
      - in: query
        name: sta_from
        schema:
            type: string
            example: 201705081205
        description: leanding ocurrence time
      - in: query
        name: sta_to
        schema:
            type: string
            example: 201705081205
        description: leanding ocurrence time
    responses:
        200:
            description: ok
            schema:
                type: array
                items:
                    schema:
                        id: Record
    """
    
    request_data = request.args
    param = request_data.to_dict()

    # query param
    stat = Record_DB.rid == rid
    if "sta_from" in param:
        stat = and_(stat, Record_DB.sta >= datetime.strptime(param["sta_from"], "%Y%m%d%H%M"))
    if "sta_to" in param:
        stat = and_(stat, Record_DB.sta <= datetime.strptime(param["sta_to"], "%Y%m%d%H%M"))
    if "bid" in param:
        stat = and_(stat, Record_DB.bid == param["bid"])



    records = []
    with DBManager().session_ctx() as session:
        records_db = session.query(Record_DB).filter(stat).all()
        for record_db in records_db:
            record = Record(
                tid=record_db.tid,
                bid=record_db.bid,
                rid=record_db.rid,
                rtt=record_db.rtt,
                sta=record_db.sta
            )
            records.append(record)

    resp = Read(payload = records)
    return jsonify(resp.payload), resp.status_code


@reader_controller.route('/digitallibrary/server/api/reader/<rid>/record', methods=['POST'])
def create_reader_record(rid):
    """
    Create the reader's record in server side digital library.
    ---
    tags:
        - Reader APIs
    produces: application/json
    parameters:
      - in: path
        name: rid
        schema:
            type: string
            example: 7PBC52BAB
        required: true
        description: reader number feature data
      - in: body
        name: RecordCreate
        schema:
            type: object
            properties:
                bid:
                    type: string
                    example: "0"
                rtt:
                    type: string
                    example: www
    responses:
        201:
            description: created                     
    """

    request_data = request.get_json()
    try:
        request_data["rid"] = rid
        if "sta" not in request_data:
            request_data["sta"] = datetime.now()
        record = Record(**request_data)
    except TypeError as e:
        raise OtherBadRequest('Invalid request data: %s'%e)
    
    with DBManager().session_ctx() as session:
        record_db = Record_DB(
            bid = record.bid,
            rid = record.rid,
            rtt = record.rtt,
            sta = datetime.strptime(record.sta, "%Y%m%d%H%M")
        )
        session.add(record_db)

    resp = Create()
    return jsonify(resp.payload), resp.status_code

def is_reader_exist(rid):

    existed = False
    with DBManager().session_ctx() as session:
        reader_db = session.query(Reader_DB).filter_by(rid = rid).one()
        existed = reader_db is not None 

    return existed

