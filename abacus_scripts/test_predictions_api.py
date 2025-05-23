import requests
import time

api_key = 's2_0eddb08477204f8d80420d6cafd2a7ba'
deployment_token = '67c53e635fa14ed4b1a975275f976fbc'
deployment_id = 'Ritual_Neurofeedback_Agent_Deployment_Emotiv_20250522'
url = 'https://api.abacus.ai/v0/getChatResponse'
headers = {'Authorization': f'Bearer {api_key}'}
data = {
    'deployment_token': deployment_token,
    'deployment_id': deployment_id,
    'messages': [
        {
            'is_user': True,
            'text': 'EEG data: alpha=10.0, beta=15.0, theta=8.0, delta=4.0, user_id=101584emotiv_user_20250522'
        }
    ],
    'temperature': 0.45
}
start = time.time()
response = requests.post(url, json=data, headers=headers)
latency = (time.time() - start) * 1000
print(f'Status Code: {response.status_code}')
print(f'Response: {response.json()}')
print(f'Latency: {latency:.2f} ms')
