import redis
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ScaleFlow API")

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

class TaskRequest(BaseModel):
    task_name: str
    payload: dict

@app.post("/submit-task")
async def submit_task(request: TaskRequest):
    task_data = {
        "name": request.task_name,
        "data": str(request.payload)
    }

    r.lpush("task_queue", str(task_data))

    return {"message": "Task successfully enqueued!", "task": request.task_name}

@app.get("/health")
async def health():
    return {"status": "System is up and Redis connection will be tested"}
