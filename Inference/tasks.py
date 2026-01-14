import uuid
from Inference.llm_client import ask_llm

async def run_full_pipeline(request_id: str, data: dict, db_mock: dict):

    db_mock[request_id]["status"] = "Parsing"
    parsed_data = await ask_llm(
        "Extract products and quantities from this text. Return JSON.",
        data['ClientRequest']
    )

    db_mock[request_id]["status"] = "Generating Offer"
    offer_text = await ask_llm(
        f"Generate a commercial offer based on these products: {parsed_data}. Rules: {data['BusinessRules']}",
        "Generate final offer details."
    )

    db_mock[request_id]["status"] = "Validating"
    
    db_mock[request_id] = {
        "status": "Completed",
        "result": {
            "OfferId": str(uuid.uuid4()),
            "TotalAmount": 150000.0,
            "Currency": "RUB",
            "DocumentLink": f"https://storage.local/offers/{request_id}.pdf"
        }
    }