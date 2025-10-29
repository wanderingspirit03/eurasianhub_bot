# Prodia API

## Key Links
- Docs: https://docs.prodia.com/
- Inference reference: https://docs.prodia.com/reference/inference

## Hackathon Perk
- $100 credits for every participant, plus $1000 bonus to the top project that uses Prodia.

## Quickstart (curl)
```bash
curl -X POST https://api.prodia.com/v2/job \
  -H "Authorization: Bearer $PRODIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "job": {
      "type": "text-to-image",
      "prompt": "dreamy watercolor skyline of London at night",
      "steps": 20
    }
  }'
```

## Notes
- Jobs are async; poll `/v2/job/{id}` to check status or use SDK helpers.
- Supports text-to-image, image-to-image, upscaling, and more; pick fast models for live demos.
- Cache generated assets locally to avoid re-generation delays during judging.
