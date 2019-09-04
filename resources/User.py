from flask_restful import Resource, request
import datetime
from flask_jwt_extended import (
    create_access_token,
    jwt_refresh_token_required,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt_claims,
    get_raw_jwt
)

from models.User import (
    UserModel,
    UserSettingsModel
)

from schema.User import (
    UserSchema,
    UserSettingsSchema
)

user_schema = UserSchema()
settings_schema = UserSettingsSchema()


class UsernameCheck(Resource):
    def get(self, username: str):
        user = UserModel.find_by_username(username.lower())
        return{"available": user is None}, 200


class Register(Resource):
    def post(self):
        user = user_schema.load(request.get_json(), partial=True)

        # prevent double account
        if UserModel.find_by_id(user.id):
            return {'message': 'Account already exists'}, 401

        user.username = user.username.lower()
        user.ip = request.remote_addr

        # assign unique id
        player_id = None
        while player_id is None:
            temp = UserModel.get_new_PlayerId()
            if UserModel.find_by_playerId(temp) is None:
                player_id = temp

        # user creation
        user.playerId = player_id
        user.save_to_db()

        # settings creation
        settings = UserSettingsModel(user_id=user.id)
        settings.save_to_db()
        return


class Authenticate(Resource):
    def post(self):
        pass


class User(Resource):
    def get(self, _id: str):
        user = UserModel.find_by_id(_id)
        Settings = UserSettingsModel.find_by_user(_id)

        if user:
            return {'user': user_schema.dump(user),
                    'settings': settings_schema.dump(Settings)}, 200

        return {'message': 'Account not found'}, 404

    def put(self, _id: str):
        user = UserModel.find_by_id(_id)
        if user:
            data = user_schema.load(request.get_json(), partial=True)
            if data.username:
                user.username = data.username
            if data.last_online:
                user.last_online = datetime.datetime.utcnow
            user.updated_at = datetime.datetime.utcnow
            user.save_to_db()
            return {'message': 'Account updated'}, 200

        return {'message': 'Account not found'}, 404

    def delete(self, _id: str):
        user = UserModel.find_by_id(_id)
        if user:
            user.delete_from_db()
            return {'message': 'Account deleted'}, 200

        return {'message': 'Account not found'}, 404


class Settings(Resource):
    def put(self, _id: str):
        user = UserModel.find_by_id(_id)
        settings = UserSettingsModel.find_by_user(_id)

        if settings:
            data = settings_schema.load(request.get_json(), partial=True)

            if data.notifications is not None:
                settings.notifications = data.notifications

            if data.public is not None:
                settings.public = data.public

            if data.language:
                settings.language = data.language

            user.updated_at = datetime.datetime.utcnow
            user.save_to_db()
            settings.save_to_db()
            return {'message': 'Account updated'}, 200

        return {'message': 'Account not found'}, 404
