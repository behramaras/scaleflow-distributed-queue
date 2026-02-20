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

@app.get("/dashboard")
async def dashboard():
    # 1. Get the number of tasks waiting in the queue (LLEN = List Length)
    pending_count = r.llen("task_queue")
    
    # 2. Get the last 10 completed tasks (LRANGE)
    completed_tasks = r.lrange("completed_tasks", 0, 9)
    
    # 3. Get the total count of completed tasks
    total_completed = r.llen("completed_tasks")
    
    return {
        "queue_status": {
            "pending_tasks_count": pending_count,
            "completed_tasks_count": total_completed
        },
        "recent_completed_tasks": completed_tasks
    }