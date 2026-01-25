from fastapi import FastAPI, BackgroundTasks, HTTPException
from Inference.schemas import OfferRequest, OfferResponse
from Inference.tasks import run_full_pipeline
import uuid

app = FastAPI(title="AI Commercial Offer Service")


tasks_db = {}

@app.post("/submit", status_code=202)
async def submit_offer(request: OfferRequest, background_tasks: BackgroundTasks):
    submission_id = str(uuid.uuid4())

    tasks_db[submission_id] = {"status": "Processing", "result": None}
    

    background_tasks.add_task(run_full_pipeline, submission_id, request.dict(), tasks_db)
    
    return {"SubmissionId": submission_id, "message": "Processing started"}

@app.get("/result/{submission_id}", response_model=OfferResponse)
async def get_result(submission_id: str):
    if submission_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks_db[submission_id]
    
    print(f"DEBUG: Task {submission_id} status is {task['status']}")
    
    return {
        "Worker": "LLM-Orchestrator",
        "SubmissionId": submission_id,
        "Status": task["status"],
        "FinalOffer": task["result"] 
    }