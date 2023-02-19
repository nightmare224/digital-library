# from os import getenv
from configparser import ConfigParser
from urllib.parse import quote as urlquote
from flask import Flask
from flasgger import Swagger

# from keycloakOIDC import KeycloakOIDCBackendFlask
from lib.db.db_manager import DBManager
## DB
import models.db.reader
import models.db.literature
import models.db.record

## controller
from controllers.reader_controller import reader_controller
# from controllers.anime_controller import anime_controller
from controllers.error_controller import error_controller
# from init import init_anime


##### Setting #####
config_parser = ConfigParser()
config_parser.read("conf/config.ini")
# connect to db
DBManager().db_uri(
    "default",
    "{}://{}:{}@{}:{}/{}".format(
        config_parser["DATABASE"]["Connector"],
        config_parser["DATABASE"]["Username"],
        urlquote(config_parser["DATABASE"]["Password"]),
        config_parser["DATABASE"]["Host"],
        config_parser["DATABASE"]["Port"],
        config_parser["DATABASE"]["DatabaseName"],
    ),
    pool_size=5,
    pool_timeout=30,
)
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

# register controller
app.register_blueprint(reader_controller)
# app.register_blueprint(anime_controller)
app.register_blueprint(error_controller)

# keycloak
# koidc = KeycloakOIDCBackendFlask(f"./lib/keycloak/secrets/anime-reminder-secrets.json")
# init_anime()

if __name__ == '__main__':
    app.run(
        host = config_parser["FLASK"]["Host"],
        port = config_parser["FLASK"]["Port"],
        debug = config_parser["FLASK"]["DebugMode"]
    )