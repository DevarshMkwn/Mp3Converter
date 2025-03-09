import os, requests

def token(request):
    if not request.headers.get('Authorization'):
        return None, ("missing token", 401)
    if not request.headers.get('Authorization').startswith('Bearer '):
        return None, ("invalid token type", 401)
    token = request.headers.get("Authorization")
    response = requests.post(f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate", headers=token)
    if response.status_code != 200:
        return None,(response.text, response.status_code) 
    return response.text, None