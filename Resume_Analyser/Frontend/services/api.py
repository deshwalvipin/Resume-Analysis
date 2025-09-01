import requests

API_URL = "http://127.0.0.1:8000/analyze"  # change if your backend URL/port differs

def analyze_resume(resume_file_bytes: bytes, resume_name: str, jd_text: str, timeout: int = 120):
    files = {"resume": (resume_name, resume_file_bytes, "application/octet-stream")}
    data = [("jds", jd_text)]
    r = requests.post(API_URL, files=files, data=data, timeout=timeout)
    r.raise_for_status()
    return r.json()
