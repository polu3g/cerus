# app/api/routes/template.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

class PromptTemplateRequest(BaseModel):
    client_id: str
    intent_prompt: str
    infer_prompt: str

@router.post("/savetemplate")
def save_prompt_template(payload: PromptTemplateRequest):
    try:
        base_path = "app/prompts"
        os.makedirs(base_path, exist_ok=True)

        intent_path = os.path.join(base_path, f"{payload.client_id}_intent.txt")
        infer_path = os.path.join(base_path, f"{payload.client_id}_infer.txt")

        with open(intent_path, "w") as f:
            f.write(payload.intent_prompt)

        with open(infer_path, "w") as f:
            f.write(payload.infer_prompt)

        return {"message": "Templates saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
