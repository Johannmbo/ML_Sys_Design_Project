from locust import HttpUser, task, between

class AISalesUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def test_full_flow(self):
        payload = {
            "UsingLLM": "mistral-small-latest",
            "ClientRequest": "Need 5 Dell R740 servers with 128GB RAM.",
            "BusinessRules": "15% margin",
            "Language": "en"
        }
        
        with self.client.post("/submit", json=payload, catch_response=True) as response:
            if response.status_code == 202:
                submission_id = response.json().get("SubmissionId")
            
                for _ in range(5):
                    res = self.client.get(f"/result/{submission_id}", name="/result/[id]")
                    if res.status_code == 200 and res.json().get("Status") == "Completed":
                        response.success()
                        break
            else:
                response.failure(f"Submission failed with status {response.status_code}")