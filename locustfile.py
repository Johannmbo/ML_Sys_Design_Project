from locust import HttpUser, task, between
import uuid

class OfferGeneratorUser(HttpUser):
    wait_time = between(1, 5)  

    @task
    def generate_offer(self):
        
        payload = {
            "UsingLLM": "GPT-4",
            "ClientRequest": "Требуется поставка 10 ноутбуков для офиса",
            "BusinessRules": "Скидка 5% при заказе от 5 штук",
            "Language": "ru"
        }
        
        
        with self.client.post("/submit", json=payload, catch_response=True) as response:
            if response.status_code == 202:
                submission_id = response.json().get("SubmissionId")
                
                self.client.get(f"/result/{submission_id}", name="/result/[id]")
            else:
                response.failure(f"Failed with status: {response.status_code}")