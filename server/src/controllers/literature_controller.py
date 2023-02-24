
from flask import Blueprint, jsonify, request

from lib.db.db_manager import DBManager
from models.api.literature import Literature
from models.db.literature import Literature_DB
from lib.api.responses import Create, Update, Read, Delete
from lib.api.exceptions import OtherBadRequest, OtherConflict

literature_controller = Blueprint('literature_controller', __name__)

@literature_controller.route('/digitallibrary/server/api/literature', methods=['GET'])
def get_literature():
    """
    Get all literatures in server side digital library. (admin)
    ---
    tags:
        - Literature APIs
    produces: application/json
    responses:
        200:
            description: ok
            schema:
                type: array
                items:
                    schema:
                        id: Literature
                        type: object
                        properties:
                            bid:
                                type: string
                                example: 0
                            tle:
                                type: string
                                example: Ulysses
                            type:
                                type: string
                                example: Novel
    """
    
    literatures = []
    with DBManager().session_ctx() as session:
        literatures_db = session.query(Literature_DB).all()
        for literature_db in literatures_db:
            literature = Literature(
                bid=literature_db.bid,
                tle=literature_db.tle,
                type=literature_db.type
            )
            literatures.append(literature)

    resp = Read(payload = literatures)
    return jsonify(resp.payload), resp.status_code

@literature_controller.route('/digitallibrary/server/api/literature', methods=['POST'])
def create_literature():
    """
    Create a literature in server side digital library. (admin)
    ---
    tags:
        - Literature APIs
    produces: application/json
    responses:
        201:
            description: created
    parameters:
      - in: body
        name: Literature
        schema:
            type: array
            items:
                schema:
                    id: LiteratureCreate
                    type: object
                    properties:
                        tle:
                            type: string
                            example: Ulysses
                        type:
                            type: string
                            example: Novel
    """    

    request_data = request.get_json()
    try:
        literatures = []
        for literature in request_data:
            literature = Literature(**literature)
            literatures.append(literature)
    except TypeError as e:
        raise OtherBadRequest('Invalid request data: %s'%e)

    with DBManager().session_ctx() as session:
        for literature in literatures:
            literature_db = Literature_DB(
                tle = literature.tle,
                type = literature.type
            )
            session.add(literature_db)

    resp = Create()
    return jsonify(resp.payload), resp.status_code