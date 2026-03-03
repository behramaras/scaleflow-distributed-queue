# ScaleFlow API 

A robust, high-performance distributed task queue system built with **FastAPI**, **Redis**, and **Docker**. ScaleFlow is designed to handle background tasks reliably with built-in protection and fault-tolerance.

## Key Features

* **Custom Rate Limiting:** Protects the API from abuse using a Redis-based fixed-window algorithm (5 req/min per IP).
* **Asynchronous Task Queue:** Tasks are decoupled from the API for non-blocking performance.
* **Fault-Tolerant Worker:** Built-in retry logic (up to 3 attempts) to handle transient failures.
* **Dead Letter Queue (DLQ):** Automatically isolates permanently failing tasks for manual inspection.
* **Real-time Dashboard:** Monitor pending and completed tasks via a dedicated endpoint.
* **Containerized Architecture:** Fully dockerized for seamless deployment.

## Tech Stack

* **Framework:** FastAPI (Python 3.10+)
* **Task Store:** Redis
* **Validation:** Pydantic
* **Containerization:** Docker & Docker Compose

## Quick Start

Ensure you have [Docker](https://www.docker.com/) installed.

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd ScaleFlow
   ```


2. **Spin up the entire system:**
    ```bash
    docker-compose up --build

    ```


3. **Access the API:**
* **API Docs (Swagger):** `http://localhost:8000/docs`
* **Health Check:** `http://localhost:8000/health`
* **Dashboard:** `http://localhost:8000/dashboard`



## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/submit-task` | Enqueue a new background task (Rate limited). |
| `GET` | `/dashboard` | View queue stats and recent tasks. |
| `GET` | `/health` | Check system and Redis status. |

## Error Handling

If a task fails during processing, the worker will:

1. Retry the task **3 times**.
2. If it still fails, move it to the `dead_letter_queue` in Redis.
