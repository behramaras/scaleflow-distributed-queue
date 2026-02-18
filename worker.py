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
            # task[1] contains the actual data
            print(f"📦 New task received: {task[1]}")
            
            # 3. Simulate processing the task
            print("⚙️ Processing...")
            time.sleep(2) # Simulate 2 seconds of work
            
            print("✅ Task completed successfully!")
            print("-" * 30)

if __name__ == "__main__":
    process_tasks()