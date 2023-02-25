
import requests
import re
from flask import Blueprint, jsonify, request, current_app
from Crypto.Cipher import AES
from dataclasses import asdict
from base64 import b64encode, b64decode
from models.api.record import Record, Record_verbose
from models.api.reader import Reader
from lib.api.responses import Create, Update, Read, Delete
from lib.api.exceptions import OtherBadRequest, OtherConflict
from lib.feature_generation import feature_construction

record_controller = Blueprint('record_controller', __name__)

@record_controller.route('/digitallibrary/client/api/record', methods=['GET'])
def get_record():
    """
    Get all records in client side digital library. (admin, worker)
    ---
    tags:
        - Record APIs
    produces: application/json
    parameters:
      - in: query
        name: verbose
        schema:
            type: string
            example: "0"
        required: true
        description: set verbose to 1 show reader info
      - in: query
        name: rid
        schema:
            type: string
            example: 2019IN013
        description: reader number
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
                                example: w
                            sta:
                                type: string
                                example: 201705081205
    """

    request_data = request.args
    param = request_data.to_dict()    

    # if verbose is True show also reader inforamtion
    verbose = bool(int(param["verbose"]))


    # get original rid if in parameter
    rid = param["rid"] if "rid" in param else ""

    rid_to_reader = {}
    if verbose:
        url = "http://{}:{}/digitallibrary/server/api/reader".format(
            current_app.config["DLSERVER"]["host"],
            current_app.config["DLSERVER"]["port"]
        )
        response_data = requests.get(url, params = {"rid": rid})
        try:
            for reader in response_data.json():
                reader = Reader(**reader)
                rid_to_reader[reader.rid] = reader
        except:
            raise OtherBadRequest("Reader information miss")

    # do feature construction if rid in parameter
    if rid:
        param["rid"] = feature_construction(param["rid"])

    # issue the new query
    url = "http://{}:{}/digitallibrary/server/api/record".format(
        current_app.config["DLSERVER"]["host"],
        current_app.config["DLSERVER"]["port"]
    )
    response_data = requests.get(url, params = param)
    records = []
    try:
        for record in response_data.json():
            record = Record(**record)
            cipher = AES.new(current_app.config["AES"]["key"], AES.MODE_EAX, nonce = current_app.config["AES"]["nonce"])
            rtt = cipher.decrypt(b64decode(record.rtt.encode('ascii'))).decode('utf-8')
            result = re.match(f'^({rid}\S*){record.sta}$', rtt)
            if result:
                if verbose:
                    rid_tmp = result.group(1)
                    reader = rid_to_reader[rid_tmp]
                    record = Record_verbose(**asdict(record), tle = reader.tle, type = reader.type)
                records.append(record)
    except TypeError as e:
        raise OtherBadRequest("Invalid response data: %s" % e)


    resp = Read(payload=records)
    return jsonify(resp.payload), resp.status_code
