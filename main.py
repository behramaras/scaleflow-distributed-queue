from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import redis
import time
import json

app = FastAPI(title="ScaleFlow API")

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Get the client's IP address
    client_ip = request.client.host
    # Create a unique key for the current minute (Fixed Window)
    current_minute = time.strftime("%H:%M")
    key = f"rate_limit:{client_ip}:{current_minute}"
    
    # Increment the request count in Redis
    request_count = r.incr(key)
    
    # If it's a new key, set an expiration to clean up memory
    if request_count == 1:
        r.expire(key, 59)
        
    # LIMIT: 5 requests per minute
    if request_count > 5:
        return JSONResponse(
            status_code=429,
            content={
                "error": "Too many requests",
                "message": "Rate limit exceeded. Please try again later."
            }
        )
    
    # Proceed to the actual endpoint
    response = await call_next(request)
    return response

class TaskRequest(BaseModel):
    task_name: str
    payload: dict

@app.post("/submit-task")
async def submit_task(request: TaskRequest):
    task_data = {
        "name": request.task_name,
        "data": str(request.payload),
        "created_at": time.time()
    }

    r.lpush("task_queue", json.dumps(task_data))

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
