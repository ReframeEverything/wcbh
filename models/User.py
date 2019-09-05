from typing import List
from uuid import uuid4
from requests import Response
from flask import request, url_for
from sqlalchemy import func
import datetime
from db import db
import random
import string


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(50), primary_key=True)
    playerId = db.Column(db.string(9), unique=True)
    username = db.Column(db.String(36), unique=True)
    ip = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.TIMESTAMP(), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP(), default=datetime.datetime.utcnow)
    last_online = db.Column(db.TIMESTAMP(), default=datetime.datetime.utcnow)

    settings = db.relationship(
        "UserSettingsModel", lazy="joined", cascade="all, delete-orphan"
    )

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_playerId(cls, playerId):
        return cls.query.filter_by(playerId=playerId).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def get_new_PlayerId():
        return (random.sample(random.choice(string.ascii_uppercase), 3) +
                random.sample(range(0, 10), 6))

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


class UserSettingsModel(db.Model):
    __tablename__ = "user_settings"
    id = db.Column(db.Integer, primary_key=True)

    notifications = db.Column(db.Boolean(), default=bool(True))
    public = db.Column(db.Boolean(), default=bool(True))
    language = db.Column(db.Text(), default=str('English'))

    user_id = db.Column(db.String(50), db.ForeignKey(
        "users.id"), nullable=False)
    user = db.relationship("UserModel")

    @classmethod
    def find_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
