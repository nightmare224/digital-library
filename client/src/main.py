# from os import getenv
from configparser import ConfigParser
from flask import Flask
from flasgger import Swagger

## controller
from controllers.reader_controller import reader_controller
from controllers.record_controller import record_controller
from controllers.error_controller import error_controller

## AES
from Crypto.Random import get_random_bytes

##### Setting #####
config_parser = ConfigParser()
config_parser.read("conf/config.ini")

# init flask app
app = Flask(__name__)

## Swagger
app.config["SWAGGER"] = {
    "title": config_parser["SWAGGER"]["Title"],
    "description": config_parser["SWAGGER"]["Description"],
    "version": config_parser["SWAGGER"]["Version"],
    "termsOfService": config_parser["SWAGGER"]["TermsOfService"],
    "hide_top_bar": config_parser["SWAGGER"]["HideTopBar"],
    # "static_url_path": "/flasgger_static",
    # "specs_route": "/apidocs/",
    # "specs": [
    #     {
    #         "endpoint": "apispec_1",
    #         "route": "/rpm/api/apispec_1.json",
    #     }
    # ],
}
Swagger(app)

## digital library server
app.config["DLSERVER"] = {
    "host": config_parser["DLSERVER"]["host"],
    "port": config_parser["DLSERVER"]["port"]
}

## AES encrypted
key = get_random_bytes(16)
nonce = get_random_bytes(16)
app.config["AES"] = {
    "key": get_random_bytes(16),
    "nonce": get_random_bytes(16)
}

# register controller
app.register_blueprint(reader_controller)
app.register_blueprint(record_controller)
app.register_blueprint(error_controller)


if __name__ == '__main__':
    app.run(
        host = config_parser["FLASK"]["Host"],
        port = config_parser["FLASK"]["Port"],
        debug = config_parser["FLASK"]["DebugMode"]
    )