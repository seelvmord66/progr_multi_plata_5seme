from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime



class AcelerometroModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    nome_empresa:str
    nome_equip: str
    acelerometroY: list
    temp:float
    dt_cria: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "properties": {
                "_id": {"type": "string", "format": "ObjectId"},
                "nome_empresa": {"type": "string"},
                "nome_equip": {"type": "string"},
                "acelerometroY": {"type": "list"},
                "temp": {"type": "number"},
                "dt_cria": {"type": "string", "format": "date-time"}
            },
            "required": ["nome_empresa","nome_equip", "acelerometroY",'temp']
        }
