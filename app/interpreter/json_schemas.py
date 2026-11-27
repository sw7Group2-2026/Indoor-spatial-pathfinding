from pydantic import BaseModel
import json

class UserQuery(BaseModel):
    attributes: list[str] | None
    room_number: str | None
    building_name: str | None
    address: str | None
    floor_number: int | None
    accessibility: bool | None

    @classmethod
    def getJson(cls):
        return cls.model_json_schema()

    @classmethod
    def validate(cls, response):
        return cls.model_validate_json(response)

class ValidAttributes(BaseModel):
    feature_type: list[str] | None
    room_description: list[str] | None

    @classmethod
    def getJson(cls):
        return cls.model_json_schema()