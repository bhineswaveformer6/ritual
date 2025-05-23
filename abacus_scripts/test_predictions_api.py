import requests
import time

api_key = 's2_0eddb08477204f8d80420d6cafd2a7ba'
deployment_token = '67c53e635fa14ed4b1a975275f976fbc'
deployment_id = '6500f090a'
url = 'https://apps.abacus.ai/api/v0/predict'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
query_data = {
    "alpha": 10.0,
    "beta": 15.0,
    "theta": 8.0,
    "delta": 4.0,
    "user_id": "101584emotiv_user_20250522"
}
data = {
    "deployment_token": deployment_token,
    "deployment_id": deployment_id,
    "query_data": query_data
}
start = time.time()
response = requests.post(url, json=data, headers=headers)
latency = (time.time() - start) * 1000
print(f'Status Code: {response.status_code}')
print(f'Response: {response.json()}')
print(f'Latency: {latency:.2f} ms')
