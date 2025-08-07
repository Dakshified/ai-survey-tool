from datetime import datetime

def get_timestamp():
    return datetime.now().isoformat()

def get_device_info(request):
    user_agent = request.headers.get("User-Agent")
    return {"user_agent": user_agent}
