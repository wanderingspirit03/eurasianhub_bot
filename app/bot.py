import os
import asyncio
import logging
import re
from typing import Any, Dict, Optional

import httpx
from agno.tools.telegram import TelegramTools

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


async def generate_reply(prompt: str, *, user_id: str, session_id: str) -> str:
    run_async = getattr(agent, "run_async", None)
    if callable(run_async):
        res = await run_async(
            prompt,
            user_id=user_id,
            session_id=session_id,
            metadata={"channel": "telegram", "chat_id": user_id},
        )
    else:
        res = await asyncio.to_thread(
            agent.run,
            prompt,
            user_id=user_id,
            session_id=session_id,
            metadata={"channel": "telegram", "chat_id": user_id},
        )
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
    # Use official Agno TelegramTools to send messages
    clean_text = _sanitize_reply(text)
    logger.info("Sending reply", extra={"chat_id": chat_id, "preview": clean_text[:80]})
    tool = TelegramTools(token=TELEGRAM_TOKEN, chat_id=chat_id)
    # send_message is sync; offload to a thread to avoid blocking the loop
    await asyncio.to_thread(tool.send_message, clean_text)


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
    key = str(chat_id)
    reply = await generate_reply(text, user_id=key, session_id=key)
    if reply:
        await send_message(client, chat_id, reply)
    return update.get("update_id")


async def poll() -> None:
    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN is not set")
    await _initialize_knowledge_async()
    offset = None
    max_concurrency = int(os.getenv("TELEGRAM_MAX_CONCURRENCY", "8"))
    sem = asyncio.Semaphore(max_concurrency)

    async with httpx.AsyncClient() as client:
        while True:
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
                params: Dict[str, Any] = {"timeout": 20}
                if offset is not None:
                    params["offset"] = offset
                r = await client.get(url, params=params, timeout=30)
                data = r.json()
                updates = data.get("result") or []
                if data.get("ok") and updates:
                    logger.info("Processing updates", extra={"count": len(updates)})

                    async def _run_one(upd: Dict[str, Any]) -> Optional[int]:
                        async with sem:
                            return await handle_update(client, upd)

                    results = await asyncio.gather(*[asyncio.create_task(_run_one(u)) for u in updates], return_exceptions=True)
                    processed_ids: list[int] = []
                    for res in results:
                        if isinstance(res, Exception):
                            logger.exception("Handler error", exc_info=res)
                            continue
                        if res is not None:
                            processed_ids.append(int(res))
                    if processed_ids:
                        offset = max(processed_ids) + 1
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Polling loop error")
            await asyncio.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    asyncio.run(poll())
