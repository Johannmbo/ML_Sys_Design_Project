from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional, Dict

class OfferRequest(BaseModel):
    UsingLLM: str = "GPT-4"
    ClientRequest: str
    BusinessRules: Optional[str] = "Standard rules"
    Language: str = "ru"

class OfferDetails(BaseModel):
    OfferId: str
    TotalAmount: float
    Currency: str
    DocumentLink: str

class OfferResponse(BaseModel):
    SubmissionId: UUID
    Status: str
    FinalOffer: Optional[OfferDetails] = None