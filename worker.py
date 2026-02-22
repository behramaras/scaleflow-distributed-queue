import redis
import time
import json

# 1. Connect to Redis (Same bridge as the API)
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def process_tasks():
    print("🚀 Worker is running, waiting for tasks...")
    
    while True:
        # 2. Fetch task from Redis (BRPOP: Wait until data is available)
        # Pull the oldest task from the 'task_queue' list
        task = r.brpop("task_queue", timeout=0)
        
        if task:
                    raw_data = task[1]
                    # Convert JSON string back to a Python dictionary
                    task_dict = json.loads(raw_data)
                    
                    task_name = task_dict.get("name")
                    print(f"📦 Processing task: {task_name}")
                    
                    time.sleep(2)
                    
                    # Log completion
                    r.lpush("completed_tasks", f"Success: {task_name} at {time.strftime('%H:%M:%S')}")
                    print(f"✅ Task {task_name} completed!")
                    print("-" * 30)


if __name__ == "__main__":
    process_tasks()