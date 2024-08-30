from typing import Optional, List

from pydantic import BaseModel


class AreaPayloadModel(BaseModel):
    name: str
    description: str
    module: str
    classroom: str
    campus: str
    department: str
    division: str
    image: Optional[List[List[int]]]


    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "iLabTDI",
                "description": "La mejor area de todas claro que si",
                "module": "N",
                "classroom": "001",
                "campus": "CUCEI",
                "department": "Ingenierias",
                "division": "DIVEC",
                "image": [
                    [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                    [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                    [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]
                ]
            }
        }
    }


class AreaResponseModel(BaseModel):
    id: int
    name: str
    description: str
    module: str
    classroom: str
    campus: str
    department: str
    division: str
    image: Optional[List[List[int]]]


    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "iLabTDI",
                "description": "La mejor area de todas claro que si",
                "module": "N",
                "classroom": "001",
                "campus": "CUCEI",
                "department": "Ingenierias",
                "division": "DIVEC",
                "image": [
                    [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                    [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                    [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]
                ]
            }
        }
    }