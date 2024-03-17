#!/usr/bin/python3
""" Lifelift Application """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, render_template, make_response, jsonify #session
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from flasgger.utils import swag_from

host = environ.get('LFTLIFT_API_HOST', '0.0.0.0')
port = environ.get('LFTLIFT_API_PORT', 5000)

app = Flask(__name__)

app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': host}})
swagger = Swagger(app)

# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# global strict slashes
# app.url_map.strict_slashes = False

# app.secret_key = 'super secret key'
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# session(app)

@app.route('/index',  methods=['GET'])
@app.route('/', methods=['GET'])
def status():
    """ Status of API """
    return jsonify({"status": "OK"})



@app.teardown_appcontext
def teardown_db(exception):
    """
    after each request, this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    print(error)
    return make_response(jsonify({'error': "Not found"}), 404)

app.config['SWAGGER'] = {
    'title': 'LifeLisft clone Restful API',
    'uiversion': 1
}



if __name__ == "__main__":
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    # port = environ.get('LIFELIFT_API_PORT')
    # if port is None:
    #     port = 5000
    # host = environ.get('LIFELIFT_API_HOST')
    # if host is None:
    #     host = 'localhost'
    # app.run(host=host, port=port, threaded=True, use_reloader=False)
    app.run(host=host, port=port)