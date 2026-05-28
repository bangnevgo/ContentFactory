"""Apify API client for Instagram data."""

import json
import urllib.request
import time


class ApifyClient:
    """Wrapper for Apify API calls."""

    def __init__(self, token):
        self.token = token
        self.base = "https://api.apify.com/v2"

    def run_actor(self, actor_id, input_data):
        """Start an actor run."""
        url = f"{self.base}/acts/{actor_id}/runs"
        data = json.dumps(input_data).encode()
        req = urllib.request.Request(
            url, data=data,
            headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"},
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read().decode())

    def get_run_status(self, run_id):
        """Check run status."""
        url = f"{self.base}/actor-runs/{run_id}?token={self.token}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.token}"})
        resp = urllib.request.urlopen(req, timeout=10)
        return json.loads(resp.read().decode())["data"]["status"]

    def get_dataset(self, dataset_id):
        """Fetch dataset items."""
        url = f"{self.base}/datasets/{dataset_id}/items?token={self.token}&format=json&clean=true"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.token}"})
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read().decode())

    def run_and_wait(self, actor_id, input_data, max_wait=120):
        """Run actor and poll until done."""
        result = self.run_actor(actor_id, input_data)
        run_id = result["data"]["id"]
        dataset_id = result["data"]["defaultDatasetId"]

        for _ in range(max_wait // 10):
            time.sleep(10)
            status = self.get_run_status(run_id)
            if status == "SUCCEEDED":
                return self.get_dataset(dataset_id)
            elif status in ("FAILED", "ABORTED", "TIMED-OUT"):
                return {"error": f"Run {status}"}

        return {"error": "Timeout"}
