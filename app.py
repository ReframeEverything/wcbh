from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from marshmallow import ValidationError
#from dotenv import Dotenv
from dotenv import load_dotenv

#from db import db
#from ma import ma

from resources.User import (
    Register,
    Authenticate,
    User,
    Settings,
    UsernameCheck,
    Test
)

app = Flask(__name__)
load_dotenv(verbose=True)
#dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env"))
# os.environ.update(dotenv)

app.config.from_object("default_config")
app.config.from_envvar(
    "APPLICATION_SETTINGS"
)  # override with config.py (APPLICATION_SETTINGS points to config.py)

api = Api(app)

# SECURITY
jwt = JWTManager(app)  # not creating /auth
migrate = Migrate(app, db)


'''# create all tables and startup
@app.before_first_request
def create_tables():
    db.create_all()


# schema validations
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400'''

'''
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    return{'is_admin': False}


@jwt.token_in_blacklist_loader
def token_in_blacklist_callback(decrypted_token):
    jti = decrypted_token['jti']
    return BlacklistTokenModel.find_by_token(jti) is not None


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verfication failed',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }), 401
'''

# USER
api.add_resource(Test, "/test")
api.add_resource(Register, "/register")
api.add_resource(UsernameCheck, "/checkavailability/<username>")
api.add_resource(Authenticate, "/auth")
api.add_resource(User, "/user/<_id>")
api.add_resource(Settings, "/usersettings/<_id>")

if __name__ == '__main__':
    #from db import db
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
