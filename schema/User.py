from ma import ma
from marshmallow import pre_dump
from models.User import UserModel, UserSettingsModel


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("id", "ip",)


class UserSettingsSchema(ma.ModelSchema):
    class Meta:
        model = UserSettingsModel
        exclude = ("user",)
