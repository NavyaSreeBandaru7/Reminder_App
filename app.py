import os
import json
import uuid
import base64
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data storage
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
REMINDERS_FILE = os.path.join(DATA_DIR, "reminders.json")

# Data models
class Reminder(BaseModel):
    id: str
    title: str
    description: str
    due_date: str
    due_time: str
    priority: str
    created_at: str
    completed: bool
    voice_note: str = ""

class CreateReminderRequest(BaseModel):
    title: str
    description: str
    due_date: str
    due_time: str
    priority: str
    voice_note: str = ""

# Load/save reminders
def load_reminders():
    try:
        if os.path.exists(REMINDERS_FILE):
            with open(REMINDERS_FILE, "r") as f:
                return json.load(f)
        return []
    except:
        return []

def save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f)

# API endpoints
@app.get("/", response_class=HTMLResponse)
async def read_index():
    return FileResponse("index.html")

@app.get("/api/reminders")
async def get_reminders():
    return load_reminders()

@app.post("/api/reminders")
async def create_reminder(request: CreateReminderRequest):
    reminders = load_reminders()
    new_reminder = Reminder(
        id=str(uuid.uuid4()),
        title=request.title,
        description=request.description,
        due_date=request.due_date,
        due_time=request.due_time,
        priority=request.priority,
        created_at=datetime.now().isoformat(),
        completed=False,
        voice_note=request.voice_note
    )
    reminders.append(new_reminder.dict())
    save_reminders(reminders)
    return new_reminder

@app.put("/api/reminders/{reminder_id}")
async def update_reminder(reminder_id: str, request: Request):
    data = await request.json()
    reminders = load_reminders()
    for r in reminders:
        if r["id"] == reminder_id:
            r.update(data)
            save_reminders(reminders)
            return r
    raise HTTPException(status_code=404, detail="Reminder not found")

@app.delete("/api/reminders/{reminder_id}")
async def delete_reminder(reminder_id: str):
    reminders = load_reminders()
    reminders = [r for r in reminders if r["id"] != reminder_id]
    save_reminders(reminders)
    return {"status": "success"}

# AI insights endpoint
@app.post("/api/ai-insights")
async def get_ai_insights(request: Request):
    data = await request.json()
    title = data.get("title", "")
    description = data.get("description", "")
    
    # Simple AI logic
    return {
        "insights": f"**AI Insights for '{title}'**:\n\n"
        f"This seems like an important task. Consider preparing in advance by gathering all necessary materials. "
        f"Set multiple reminders if it's critical. {'You provided detailed notes - good job!' if description else ''}"
    }

# Voice notes endpoint
@app.post("/api/save-voice-note")
async def save_voice_note(request: Request):
    data = await request.json()
    audio_data = data.get("audio_data")
    if not audio_data:
        raise HTTPException(status_code=400, detail="No audio data provided")
    
    # Save audio to file
    os.makedirs("static/voice_notes", exist_ok=True)
    filename = f"voice_note_{uuid.uuid4()}.wav"
    filepath = os.path.join("static", "voice_notes", filename)
    
    # Decode base64 audio data
    try:
        audio_bytes = base64.b64decode(audio_data.split(",")[1])
        with open(filepath, "wb") as f:
            f.write(audio_bytes)
    except:
        raise HTTPException(status_code=500, detail="Failed to save audio")
    
    return {"path": f"/static/voice_notes/{filename}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8501)
