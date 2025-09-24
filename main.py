from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# Configure CORS middleware for a robust local setup
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NumberRequest(BaseModel):
    phone_number: str
    
class NumberStatus(BaseModel):
    status: str
    risk_score: int
    recommended_action: str
    latest_recycled_date: Optional[str] = None
    first_seen_date: Optional[str] = None
    associated_services: Optional[List[str]] = None

mock_data = {
    "+237671123456": {
        "status": "reassigned",
        "risk_score": 95,
        "recommended_action": "block_sms_otp",
        "latest_recycled_date": "2025-06-01",
        "first_seen_date": "2025-09-10",
        "associated_services": ["WhatsApp", "Facebook", "X"]
    },
    "+237672987654": {
        "status": "active",
        "risk_score": 10,
        "recommended_action": "allow_otp",
        "latest_recycled_date": None,
        "first_seen_date": "2024-01-01",
        "associated_services": ["Bank", "Google", "WhatsApp"]
    },
    "+237691112233": {
        "status": "inactive",
        "risk_score": 50,
        "recommended_action": "proceed_with_caution",
        "latest_recycled_date": "2024-12-01",
        "first_seen_date": "2024-10-15",
        "associated_services": ["Jumia"]
    },
    "+237650000000": {
        "status": "unknown",
        "risk_score": 0,
        "recommended_action": "allow_otp",
        "latest_recycled_date": None,
        "first_seen_date": None,
        "associated_services": []
    }
}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Secure Number Verification API!"}

@app.post("/api/v1/number-status", response_model=NumberStatus)
async def get_number_status(request:NumberRequest):
    phone_number= request.phone_number
    status_info= mock_data.get(phone_number)
    
    if status_info:
        return status_info
    else:
        raise HTTPException(
            status_code= 404, detail="Phone number not found or not available in our records."
        )