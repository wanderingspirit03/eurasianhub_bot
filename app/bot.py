import os
import asyncio
import logging
import re
from typing import Any, Dict, Optional

import httpx

from .agent_setup import agent, _initialize_knowledge_async


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
POLL_INTERVAL = float(os.getenv("TELEGRAM_POLL_INTERVAL", "2"))
LOG_LEVEL = os.getenv("TELEGRAM_LOG_LEVEL", "INFO").upper()

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
logger = logging.getLogger("telegram.bot")


def _extract_text(resp: Any) -> str:
    if isinstance(resp, str):
        return resp
    for key in ("content", "text", "output_text"):
        if hasattr(resp, key):
            val = getattr(resp, key)
            if isinstance(val, str):
                return val
    try:
        return str(resp)
    except Exception:
        return ""


async def generate_reply(prompt: str) -> str:
    try:
        res = await agent.run_async(prompt)
    except AttributeError:
        res = agent.run(prompt)
    return _extract_text(res)


def _sanitize_reply(text: str) -> str:
    if not text:
        return ""
    lines = []
    for raw_line in text.splitlines():
        line = re.sub(r"^\s*#+\s*", "", raw_line)
        line = re.sub(r"(?<!\w)#([A-Za-z0-9_]+)", r"\1", line)
        lines.append(line)
    sanitized = "\n".join(lines).strip()
    return sanitized


async def send_message(client: httpx.AsyncClient, chat_id: int | str, text: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    clean_text = _sanitize_reply(text)
    payload = {"chat_id": chat_id, "text": clean_text, "parse_mode": "Markdown"}
    logger.info("Sending reply", extra={"chat_id": chat_id, "preview": text[:80]})
    await client.post(url, json=payload, timeout=20)


async def handle_update(client: httpx.AsyncClient, update: Dict[str, Any]) -> Optional[int]:
    msg = update.get("message") or update.get("edited_message")
    if not msg:
        return None
    chat = msg.get("chat", {})
    chat_id = chat.get("id")
    text = msg.get("text")
    if not chat_id or not text:
        return None
    logger.info("Received message", extra={"chat_id": chat_id, "text": text})
    reply = await generate_reply(text)
    if reply:
        await send_message(client, chat_id, reply)
    return update.get("update_id")


async def poll() -> None:
    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN is not set")
    await _initialize_knowledge_async()
    offset = None
    async with httpx.AsyncClient() as client:
        while True:
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
                params: Dict[str, Any] = {"timeout": 20}
                if offset is not None:
                    params["offset"] = offset
                r = await client.get(url, params=params, timeout=30)
                data = r.json()
                if data.get("ok") and data.get("result"):
                    logger.info("Processing updates", extra={"count": len(data["result"])})
                    for upd in data["result"]:
                        last_id = await handle_update(client, upd)
                        if last_id is not None:
                            offset = last_id + 1
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Polling loop error")
            await asyncio.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    asyncio.run(poll())
