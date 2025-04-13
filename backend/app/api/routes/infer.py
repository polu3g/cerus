
from fastapi import APIRouter, HTTPException
from app.services.llm_infer import generate_inference
from app.models.schemas import InferenceRequest, InferenceResponse

router = APIRouter()

@router.post("/infer", response_model=InferenceResponse)
async def infer(request: InferenceRequest):
    try:
        return generate_inference(request.client_id, request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
