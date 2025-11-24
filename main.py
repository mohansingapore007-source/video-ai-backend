from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upscale-video")
async def upscale_video(file: UploadFile = File(...)):
    # Ippo test-ku just original video thirumba return panrom
    data = await file.read()
    buf = io.BytesIO(data)
    return StreamingResponse(
        buf,
        media_type="video/mp4",
        headers={"Content-Disposition": 'attachment; filename="upscaled_4k.mp4"'}
    )
  
