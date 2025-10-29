# OpenAI API

## Key Links
- Overview: https://platform.openai.com/docs/overview
- API reference: https://platform.openai.com/docs/api-reference
- Organization settings (org_id): https://platform.openai.com/settings/organization/general

## Hackathon Perk
- Attendees must create personal accounts and share their org_id with organizers to receive credits.

## Quickstart (Python)
```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Summarize vibeHack in 20 words."}],
)
print(resp.choices[0].message.content)
```

## Tips
- Keep prompts focused; cache repeated calls to save tokens.
- For retrieval-augmented generation, use text-embedding-3-small/large and store vectors (e.g., LanceDB).
- Use structured output (JSON mode) for scoring, judging rubrics, or evaluation pipelines.
