import os
import json
from fastapi import FastAPI, Request, Query, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io

from app.agent import VoiceAgentEngine
from app.audio_service import AudioService

app = FastAPI(
    title="Divyasree 'Whispers of the Wind' Voice Agent Suite",
    description="Production-grade AI Voice Agent developed for Revspot AI Assessment",
    version="2.4.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Singleton Voice Agent for the active simulator session
agent_engine = VoiceAgentEngine()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def get_index():
    return FileResponse("app/static/index.html")

@app.post("/api/chat")
async def chat_turn(req: ChatRequest):
    result = agent_engine.process_turn(req.message)
    return {
        "reply": result["reply"],
        "state": result["state"]
    }

@app.post("/api/reset")
async def reset_session():
    agent_engine.reset()
    return {"status": "reset", "state": agent_engine.state}

@app.get("/api/tts")
async def get_tts(text: str = Query(..., description="Text to synthesize to speech")):
    try:
        mp3_bytes = await AudioService.synthesize_to_bytes(text)
        return StreamingResponse(io.BytesIO(mp3_bytes), media_type="audio/mpeg")
    except Exception as e:
        return Response(content=str(e), status_code=500)

@app.get("/api/flows")
async def get_conversation_flows():
    with open("data/conversation_flows.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/api/project")
async def get_project_knowledge():
    with open("data/project_knowledge.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/api/download-pdf")
async def download_system_prompt_pdf():
    pdf_path = "Divyasree_WOW_Voice_Agent_System_Prompt.pdf"
    if os.path.exists(pdf_path):
        return FileResponse(
            pdf_path,
            filename="Divyasree_WOW_Voice_Agent_System_Prompt.pdf",
            media_type="application/pdf"
        )
    return Response(content="PDF not found", status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
