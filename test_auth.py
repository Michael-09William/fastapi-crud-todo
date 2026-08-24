import requests

BASE_URL = "http://127.0.0.1:8005"

# 1. Login
login_res = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "test@example.com", "password": "password123"}
)
print("Login Status:", login_res.status_code)
token = login_res.json().get("access_token")

# 2. Test Protected Profile with valid token
headers = {"Authorization": f"Bearer {token}"}
profile_res = requests.get(f"{BASE_URL}/protected/profile", headers=headers)
print("Protected Profile Status (Valid):", profile_res.status_code)
print("Profile Response:", profile_res.json())

# 3. Test Invalid Token (401 Checkpoint)
bad_headers = {"Authorization": "Bearer BAD_TOKEN_123"}
invalid_res = requests.get(f"{BASE_URL}/protected/profile", headers=bad_headers)
print("Protected Profile Status (Invalid):", invalid_res.status_code)