# Prodia Inference API (v2)

## Key Links
- Docs: https://docs.prodia.com/
- Inference reference: https://docs.prodia.com/reference/inference
- Dashboard (API key): https://app.prodia.com/

## Essentials
- Base URL: `https://api.prodia.com`
- Auth: `Authorization: Bearer $PRODIA_API_KEY`
- Core endpoints: `POST /v2/job` (create), `GET /v2/job/{id}` (fetch/result)
- Content negotiation: set `Accept: image/jpeg|image/png` on `GET /v2/job/{id}` to receive the image bytes directly; omit to receive JSON.

## Quickstart (curl)
Create FLUX Schnell text-to-image, then fetch the image when ready.

```bash
# 1) Submit job (JSON response includes an id)
curl -sS -X POST https://api.prodia.com/v2/job \
  -H "Authorization: Bearer $PRODIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "job": {
      "type": "inference.flux.schnell.txt2img.v2",
      "input": {
        "prompt": "dreamy watercolor skyline of London at night",
        "width": 1024,
        "height": 768,
        "seed": 42
      }
    }
  }'

# 2) Poll until status=="succeeded" (JSON)
curl -sS https://api.prodia.com/v2/job/$JOB_ID \
  -H "Authorization: Bearer $PRODIA_API_KEY"

# 3) Get final image bytes directly
curl -sS https://api.prodia.com/v2/job/$JOB_ID \
  -H "Authorization: Bearer $PRODIA_API_KEY" \
  -H "Accept: image/jpeg" -o out.jpg
```

## Common Job Types (examples)
- `inference.flux.schnell.txt2img.v2` — fast text-to-image
- `inference.rembg.remove-background.v2` — remove background
- `inference.esrgan.x4.upscale.v2` — 4x upscaling

See the Inference reference for full options, inputs, and SDKs.

## Plain English
- Prodia turns text or images into new images. Jobs run asynchronously, so submit, poll, then download.
- Great for demo visuals (hero images, thumbnails). If you get `401`, check that your key is set.
