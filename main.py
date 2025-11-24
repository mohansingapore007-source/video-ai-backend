from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======= IMPORTANT: unga AI provider details =======
AI_API_URL = "https://YOUR_AI_PROVIDER_URL/upscale-video"
AI_API_KEY = "YOUR_SECRET_API_KEY"
# ===================================================

@app.post("/upscale-video")
async def upscale_video(file: UploadFile = File(...)):
    # client → backend
    original_bytes = await file.read()

    # backend → AI provider
    try:
        resp = requests.post(
            AI_API_URL,
            headers={
                "Authorization": f"Bearer {AI_API_KEY}"
            },
            files={
                "file": (file.filename, original_bytes, file.content_type)
            },
            data={
                "target_resolution": "4k"   # provider depend, example only
            },
            timeout=600,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service unreachable: {e}")

    if resp.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {resp.status_code} - {resp.text}",
        )

    upscaled_bytes = io.BytesIO(resp.content)

    return StreamingResponse(
        upscaled_bytes,
        media_type="video/mp4",
        headers={
            "Content-Disposition": 'attachment; filename="upscaled_4k.mp4"'
        },
    )
    
