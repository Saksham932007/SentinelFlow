from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Labeling Backend")

class LabelRequest(BaseModel):
    transaction_id: str
    label: int

@app.post('/label')
async def label(req: LabelRequest):
    # Store label in a label store (DB, file, etc.) - placeholder
    return {"status": "ok", "transaction_id": req.transaction_id}
