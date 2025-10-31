# Perplexity Chat Completions

## Key Links
- Chat Completions: https://docs.perplexity.ai/api-reference/chat-completions-post
- SDK guide: https://docs.perplexity.ai/guides/chat-completions-sdk
- Models (Sonar family): https://docs.perplexity.ai/getting-started/models/
- API keys & groups: https://www.perplexity.ai/account/api/keys

## Essentials
- Base URL: `https://api.perplexity.ai`
- Endpoint: `POST /chat/completions`
- Auth: `Authorization: Bearer $PERPLEXITY_API_KEY`
- Models: `sonar`, `sonar-pro`, `sonar-deep-research`, `sonar-reasoning`, `sonar-reasoning-pro`

## Core Params
- `messages`: OpenAI-compatible array of `{role, content}` (string or content parts).
- Sampling: `temperature` (default 0.2), `top_p`.
- Length: `max_tokens`.
- Streaming: `stream: true` returns `text/event-stream` chunks.
- Search control: `search_mode` (`web|academic|sec`), `search_domain_filter`, `disable_search`, `enable_search_classifier`, `web_search_options.search_context_size` (`low|medium|high`).
- Media: `return_images`, `media_response.overrides.{return_videos,return_images}`.
- Deep research only: `reasoning_effort` = `low|medium|high` (impacts reasoning token usage).

## Quickstart (curl)
```bash
curl -sS https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar",
    "messages": [
      {"role": "system", "content": "Be precise and concise."},
      {"role": "user", "content": "Top 3 sights in London this weekend?"}
    ],
    "search_mode": "web",
    "max_tokens": 300
  }'
```

## Streaming (curl)
```bash
curl -N https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar-reasoning",
    "messages": [{"role": "user", "content": "Summarize latest AI news."}],
    "stream": true
  }'
```

## Python (requests)
```python
import os, requests

payload = {
    "model": "sonar-deep-research",
    "messages": [
        {"role": "system", "content": "Be precise and concise."},
        {"role": "user", "content": "Compare SEC climate disclosure rules vs EU CSRD."}
    ],
    "reasoning_effort": "low",
    "search_mode": "sec",
}

r = requests.post(
    "https://api.perplexity.ai/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}",
        "Content-Type": "application/json",
    },
    json=payload,
    timeout=60,
)
print(r.json()["choices"][0]["message"]["content"])  # basic parse
```

## Async (Deep Research only)
- Endpoint: `POST /async/chat/completions` with `model: "sonar-deep-research"`.
- Poll: `GET /async/chat/completions/{request_id}`. Useful for long research tasks.

## Tips
- OpenAI-compatible: schema and fields align; swap base URL and model name.
- Use `search_domain_filter` allow/deny lists to steer sources.
- Prefer `web_search_options.search_context_size: medium` for balanced cost vs context.

## Plain English
- Perplexity can browse the web; choose `sonar-deep-research` for deeper, slower research or `sonar/sonar-pro` for quick answers.
- If you see `401`, confirm `PERPLEXITY_API_KEY` and the right API Group are set.
