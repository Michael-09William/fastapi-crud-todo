import requests

BASE_URL = "http://127.0.0.1:8005"

# 1. Login
login_res = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "test@example.com", "password": "password123"}
)
token = login_res.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

# 2. Test Profile (Reused Guard) -> 200
profile_res = requests.get(f"{BASE_URL}/protected/profile", headers=headers)
print("Profile Status:", profile_res.status_code)

# 3. Test Dashboard (Checkpoint Reused Guard) -> 200
dashboard_res = requests.get(f"{BASE_URL}/protected/dashboard", headers=headers)
print("Dashboard Status:", dashboard_res.status_code, dashboard_res.json())

# 4. Test Dashboard Bad Token -> 401
bad_res = requests.get(f"{BASE_URL}/protected/dashboard", headers={"Authorization": "Bearer BAD_TOKEN"})
print("Dashboard Bad Token Status:", bad_res.status_code)

# 5. Test Logout -> 204
logout_res = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
print("Logout Status:", logout_res.status_code)