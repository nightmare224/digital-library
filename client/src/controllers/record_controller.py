
import requests
from flask import Blueprint, jsonify, request, current_app
from models.api.record import Record
from lib.api.responses import Create, Update, Read, Delete
from lib.api.exceptions import OtherBadRequest, OtherConflict
from lib.feature_generation import feature_construction

record_controller = Blueprint('record_controller', __name__)

@record_controller.route('/digitallibrary/client/api/record', methods=['GET'])
def get_record():
    """
    Get all records in client side digital library.
    ---
    tags:
        - Record APIs
    produces: application/json
    parameters:
      - in: query
        name: rid_ptn
        schema:
            type: string
            example: 2019IN013
        description: find read number with this pattern
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

    if "rid_ptn" in param:
        param["rid_ptn"] = feature_construction(param["rid_ptn"])

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
            records.append(record)
    except TypeError as e:
        raise OtherBadRequest("Invalid response data: %s" % e)


    resp = Read(payload=records)
    return jsonify(resp.payload), resp.status_code
