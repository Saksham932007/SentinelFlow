from locust import HttpUser, task, between
import json

class APIUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def predict(self):
        payload = {"nameOrig": "C000001"}
        self.client.post("/predict", json=payload)
