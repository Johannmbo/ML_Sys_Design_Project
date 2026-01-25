import uuid
import asyncio
import logging
from Inference.llm_client import ask_llm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_full_pipeline(request_id: str, data: dict, db_mock: dict):
    """
    Background task to process the LLM request and update the mock DB.
    """
    try:
        logger.info(f"Task {request_id} started.")
        
    
        db_mock[request_id]["status"] = "Generating"
        
        # Extract relevant info from data
        client_req = data.get("ClientRequest", "No request text provided.")
        rules = data.get("BusinessRules", "Standard 15% margin.")
        
        # Call the LLM
        system_prompt = "You are an expert sales engineer. Create a detailed commercial proposal in Markdown."
        user_prompt = f"Client Requirements: {client_req}\nBusiness Rules: {rules}"
        
        logger.info(f"Calling LLM for Task {request_id}...")
        generated_text = await ask_llm(system_prompt, user_prompt)
        
        if not generated_text or len(generated_text) < 10:
            generated_text = "Error: The LLM returned an empty or too short response."

        # Mock final offer structure
        final_payload = {
            "OfferId": str(uuid.uuid4()),
            "TotalAmount": 1500.0,
            "Currency": "USD",
            "DocumentLink": f"http://storage.local/offers/{request_id}.pdf",
            "RawMarkdown": str(generated_text) 
        }

    
        db_mock[request_id]["status"] = "Completed"
        db_mock[request_id]["result"] = final_payload
        
        logger.info(f"Task {request_id} completed. RawMarkdown size: {len(generated_text)}")

    except Exception as e:
        logger.error(f"Error in task {request_id}: {str(e)}")
        db_mock[request_id]["status"] = "Error"
        db_mock[request_id]["result"] = {"RawMarkdown": f"Error during generation: {str(e)}"}