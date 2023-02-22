
from flask import Blueprint, jsonify, request

from models.api.record import Record
from lib.api.responses import Create, Update, Read, Delete
from lib.api.exceptions import OtherBadRequest, OtherConflict

record_controller = Blueprint('record_controller', __name__)

@record_controller.route('/digitallibrary/client/api/record', methods=['GET'])
def get_record():
    """
    Get all records in client side digital library.
    ---
    tags:
        - Record APIs
    produces: application/json
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
                                example: w
                            sta:
                                type: string
                                example: 201705081205
    """

    

    records = []
    with DBManager().session_ctx() as session:
        records_db = session.query(Record_DB).all()
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
