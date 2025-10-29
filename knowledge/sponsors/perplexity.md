# Perplexity API

## Key Links
- Quickstart: https://docs.perplexity.ai/getting-started/quickstart
- Chat Completions reference: https://docs.perplexity.ai/api-reference/chat-completions
- API keys & groups: https://www.perplexity.ai/account/api/keys

## Hackathon Perk
- Credits applied to API Groups; each participant or team lead must create a Group and key.

## Setup Checklist
1. Create account: https://www.perplexity.ai/
2. Create an API Group and generate a key (UI linked above).
3. Set `PERPLEXITY_API_KEY` in your environment.

## Quickstart (Python)
```python
import os
import requests

resp = requests.post(
    "https://api.perplexity.ai/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [{"role": "user", "content": "Hello!"}],
    },
)
print(resp.json())
```

## Notes
- API is OpenAI-compatible; swap base URL and model name to migrate existing clients.
- Supports "online" models with live web-retrieval; use for research-heavy hacks.
