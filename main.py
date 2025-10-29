import asyncio
import os

import uvicorn

from app.agent_setup import app as fastapi_app
from app.bot import poll as run_bot


async def run_web() -> None:
    host = os.getenv("PORTFOLIO_AGENT_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", os.getenv("PORTFOLIO_AGENT_PORT", "8000")))
    log_level = os.getenv("UVICORN_LOG_LEVEL", "info")
    config = uvicorn.Config(fastapi_app, host=host, port=port, log_level=log_level, reload=False)
    server = uvicorn.Server(config)
    await server.serve()


async def run_hybrid() -> None:
    tasks = [
        asyncio.create_task(run_web(), name="agentos-web"),
        asyncio.create_task(run_bot(), name="telegram-bot"),
    ]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
    for task in pending:
        task.cancel()
    for task in pending:
        try:
            await task
        except asyncio.CancelledError:
            pass
    for task in done:
        task.result()


async def main() -> None:
    mode = os.getenv("RUN_MODE", "hybrid").lower()
    if mode == "web":
        await run_web()
    elif mode == "bot":
        await run_bot()
    elif mode == "hybrid":
        await run_hybrid()
    else:
        raise ValueError(f"Unsupported RUN_MODE: {mode}")


if __name__ == "__main__":
    asyncio.run(main())
