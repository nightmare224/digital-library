
from flask import Blueprint, jsonify, request

from lib.db.db_manager import DBManager
from models.api.reader import Reader
from models.db.reader import Reader_DB
from lib.api.responses import Create, Update, Read, Delete
from lib.api.exceptions import OtherBadRequest, OtherConflict

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

    reader = []
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



def is_reader_exist(rid):

    existed = False
    with DBManager().session_ctx() as session:
        reader_db = session.query(Reader_DB).filter_by(rid = rid).one()
        existed = reader_db is not None 

    return existed


# # @anime_controller.route('/animereminder/api/v1/anime/<anime_id>', methods=['PUT'])
# # # @koidc.require_permission("Default Resource")
# # def edit_anime():

# #     users = []
# #     with DBManager().session_ctx() as session:
# #         users_db = session.query(User_DB).all()
# #         for user_db in users_db:
# #             user = User(
# #                 user_id=user_db.user_id
# #             )
# #             users.append(user)

# #     resp = Read(payload = users)
# #     return jsonify(resp.payload), resp.status_code