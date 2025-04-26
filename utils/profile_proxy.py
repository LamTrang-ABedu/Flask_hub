import requests

PROFILE_SERVICES = [
    "https://profile-faker-service.onrender.com/api/profile",
    # "https://profile-faker-service-vercel.vercel.app/api/profile",
    "https://09ef5a9c-b639-48b8-9bb1-d120097aef06-00-2ub7tkprj1vdf.sisko.replit.dev/api/profile"
]

def generate_profile_proxy(locale="en_US"):
    print(f"generate_profile_proxy: {locale}")
    for url in PROFILE_SERVICES:
        try:
            response = requests.get(url, params=locale, timeout=5, verify=False)
            if response.status_code == 200:
                print(f"generate_profile_proxy: {locale}")
                data = response.json()
                if data:  # Nếu trả về JSON không rỗng
                    return data
        except Exception as e:
            print(f"[Warning] Server {url} failed: {e}")
            continue  # Thử server tiếp theo
    # Nếu không server nào trả lời được
    return {"status": "error", "message": "All servers are unreachable"}
