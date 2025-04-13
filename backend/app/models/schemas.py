
from pydantic import BaseModel

class InferenceRequest(BaseModel):
    client_id: str
    query: str

class InferenceResponse(BaseModel):
    response: str
