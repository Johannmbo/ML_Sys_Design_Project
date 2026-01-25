from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional, Dict

class OfferRequest(BaseModel):
    UsingLLM: str = "mistral-small-latest"
    ClientRequest: str
    BusinessRules: Optional[str] = "Standard rules"
    Language: str = "en"

class OfferDetails(BaseModel):
    OfferId: str
    TotalAmount: float
    Currency: str
    DocumentLink: str
    RawMarkdown: str

class OfferResponse(BaseModel):
    Worker: str
    SubmissionId: UUID
    Status: str
    FinalOffer: Optional[OfferDetails] = None