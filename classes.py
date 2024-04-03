from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime



class AcelerometroModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    nome_equip: str
    acelerometroX: float
    acelerometroY: float
    acelerometroZ: float
    dt_cria: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "properties": {
                "_id": {"type": "string", "format": "ObjectId"},
                "nome_equip": {"type": "string"},
                "acelerometroX": {"type": "number"},
                "acelerometroY": {"type": "number"},
                "acelerometroZ": {"type": "number"},
                "dt_cria": {"type": "string", "format": "date-time"}
            },
            "required": ["nome_equip", "acelerometroX", "acelerometroY", "acelerometroZ"]
        }
