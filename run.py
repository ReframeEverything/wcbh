from app import app
from db import db
from ma import ma
from marshmallow import ValidationError
from flask import jsonify

db.init_app(app)
ma.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400
