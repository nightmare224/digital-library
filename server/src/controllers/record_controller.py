
from flask import Blueprint, jsonify, request
from datetime import datetime
from sqlalchemy import and_
from lib.db.db_manager import DBManager
from models.api.record import Record
from models.db.record import Record_DB
from lib.api.responses import Create, Update, Read, Delete
from lib.api.exceptions import OtherBadRequest, OtherConflict

record_controller = Blueprint('record_controller', __name__)

@record_controller.route('/digitallibrary/server/api/record', methods=['GET'])
def get_record():
    """
    Get all records in server side digital library. (admin)
    ---
    tags:
        - Record APIs
    produces: application/json
    parameters:
      - in: query
        name: rid
        schema:
            type: string
            example: 7PBC52BAB
        description: reader number after feature construction
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
            example: 201706111205
        description: leanding ocurrence time
    responses:
        200:
            description: ok
            schema:
                type: array
                items:
                    schema:
                        id: Record
                        type: object
                        properties:
                            tid:
                                type: string
                                example: "1"
                            bid:
                                type: string
                                example: "12"
                            rid:
                                type: string
                                example: 7PBC52BAB
                            rtt:
                                type: string
                                example: NPTnTn/sj8R4zuGsBW22ezjgV5DD
                            sta:
                                type: string
                                example: 201705081205
    """

    request_data = request.args
    param = request_data.to_dict()

    # query param
    rid = param["rid"] if "rid" in param else ""
    stat = Record_DB.rid.like(f'%{rid}%')
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
