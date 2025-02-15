# agent/main.py
from fastapi import FastAPI, HTTPException, Query
from agent.task_processor import process_task
from fastapi.responses import PlainTextResponse
import os

app = FastAPI()

@app.post("/run")
async def run_task(task: str = Query(...)):
    try:
        result = process_task(task)
        if result.get("status") == "success":
            return {"message": "Task executed successfully", "details": result.get("details", "")}
        else:
            raise HTTPException(status_code=400, detail=result.get("message", "Bad Request"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read", response_class=PlainTextResponse)
async def read_file(path: str = Query(...)):
    # Ensure the path is within /data
    if not path.startswith("/data/"):
        raise HTTPException(status_code=404, detail="File not found")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return content

