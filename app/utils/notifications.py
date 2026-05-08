from datetime import datetime

import aiohttp

from app.settings import settings


async def send_discord_notification(
    endpoint: str,
    method: str,
    team_id: str | None = None,
    ip: str | None = None,
) -> None:
    """Send Discord notification without blocking the request."""
    if not settings.DISCORD_WEBHOOK_URL:
        return

    try:
        embed = {
            "title": "🔔 HLTV API Request",
            "color": 5814783,  # azul
            "fields": [
                {"name": "Endpoint", "value": endpoint, "inline": True},
                {"name": "Method", "value": method, "inline": True},
                {"name": "Team ID", "value": team_id or "N/A", "inline": True},
                {"name": "IP", "value": ip or "Unknown", "inline": True},
                {
                    "name": "Timestamp",
                    "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "inline": False,
                },
            ],
            "footer": {"text": "HLTV API Monitor"},
        }

        async with aiohttp.ClientSession() as session:
            await session.post(settings.DISCORD_WEBHOOK_URL, json={"embeds": [embed]})
    except Exception:
        # não deixa a notificação quebrar a API
        pass
