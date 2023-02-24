import requests
from flask import Blueprint, jsonify, request, current_app
from datetime import datetime
from dataclasses import asdict
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
# from models.api.reader import Reader
from models.api.record import Record

from lib.api.responses import Create, Update, Read, Delete
from lib.api.exceptions import OtherBadRequest, OtherConflict, OtherNotFound
from lib.feature_generation import feature_construction

reader_controller = Blueprint("reader_controller", __name__)




@reader_controller.route(
    "/digitallibrary/client/api/reader/<rid>/record", methods=["GET"]
)
def get_reader_record(rid):
    """
    Get the reader's record in client side digital library. (admin, worker, reader)
    ---
    tags:
        - Reader APIs
    produces: application/json
    parameters:
      - in: path
        name: rid
        schema:
            type: string
            example: 2019IN013
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
    
    # get param
    request_data = request.args
    param = request_data.to_dict()


    # issue the new query to server side digital library
    url = "http://{}:{}/digitallibrary/server/api/reader/{}/record".format(
        current_app.config["DLSERVER"]["host"],
        current_app.config["DLSERVER"]["port"],
        # trainsform the original query
        feature_construction(rid)
    )
    response_data = requests.get(url, params = param)
    records = []
    try:
        for record in response_data.json():
            record = Record(**record)
            cipher = AES.new(current_app.config["AES"]["key"], AES.MODE_EAX, nonce = current_app.config["AES"]["nonce"])
            rtt = cipher.decrypt(b64decode(record.rtt.encode('ascii'))).decode('utf-8')
            if rtt == rid + record.sta:
                records.append(record)
    except TypeError as e:
        raise OtherBadRequest("Invalid response data: %s" % e)


    resp = Read(payload=records)
    return jsonify(resp.payload), resp.status_code


@reader_controller.route(
    "/digitallibrary/client/api/reader/<rid>/record", methods=["POST"]
)
def create_reader_record(rid):
    """
    Create the reader's record in server side digital library. (admin, worker, reader)
    ---
    tags:
        - Reader APIs
    produces: application/json
    parameters:
      - in: path
        name: rid
        schema:
            type: string
            example: 2019IN013
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
    responses:
        201:
            description: created
    """


    request_data = request.get_json()
    try:
        record = Record(**request_data, rid=feature_construction(rid), sta=datetime.now())
    except TypeError as e:
        raise OtherBadRequest("Invalid request data: %s" % e)


    data = (rid + record.sta).encode('utf-8')
    cipher = AES.new(current_app.config["AES"]["key"], AES.MODE_EAX, nonce = current_app.config["AES"]["nonce"])
    # store as ascii string
    record.rtt = b64encode(cipher.encrypt(data)).decode('ascii')


    # issue the new query
    url = "http://{}:{}/digitallibrary/server/api/reader/{}/record".format(
        current_app.config["DLSERVER"]["host"],
        current_app.config["DLSERVER"]["port"],
        record.rid
    )
    response_data = requests.post(url, json = asdict(record))
    
    if not response_data.ok:
        raise OtherBadRequest(response_data.reason)


    resp = Create()
    return jsonify(resp.payload), resp.status_code
