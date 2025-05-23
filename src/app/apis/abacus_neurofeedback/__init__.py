from fastapi import APIRouter, HTTPException
import requests
import time
from pydantic import BaseModel

router = APIRouter()

class EEGInput(BaseModel):
    alpha: float
    beta: float
    theta: float
    delta: float
    user_id: str

class PredictionResponse(BaseModel):
    response: str
    latency: float

@router.post("/neurofeedback", response_model=PredictionResponse)
async def get_neurofeedback(input: EEGInput):
    try:
        api_key = "s2_0eddb08477204f8d80420d6cafd2a7ba"  # From Settings > API Keys
        deployment_token = "67c53e635fa14ed4b1a975275f976fbc"  # From Deployments
        if not api_key or not deployment_token:
            raise HTTPException(status_code=500, detail="Missing Abacus.AI secrets")

        deployment_id = "6500f090a"
        url = "https://apps.abacus.ai/api/v0/predict"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        query_data = {
            "alpha": input.alpha,
            "beta": input.beta,
            "theta": input.theta,
            "delta": input.delta,
            "user_id": input.user_id
        }
        data = {
            "deployment_token": deployment_token,
            "deployment_id": deployment_id,
            "query_data": query_data
        }
        start = time.time()
        response = requests.post(url, json=data, headers=headers)
        latency = (time.time() - start) * 1000
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        result = response.json()
        # Adjust based on actual response format
        prediction = result.get("response", "No prediction returned")
        return PredictionResponse(response=prediction, latency=latency)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
