from pydantic import BaseModel


class HttpErrorResponseModel(BaseModel):
    status_code: int
    detail: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "status_code": 400,
                "detail": "Bad Request"
            }
        }
    }
