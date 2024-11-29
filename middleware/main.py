from fastapi import FastAPI, Request
import time

app = FastAPI()

async def logger(request: Request, call_next):
    print(f"Request Received: {request.method} {request.url}")
    start_time = time.time()
    response = await call_next(request)
    end_time = time.perf_counter()
    process_time = start_time - end_time
    print(f"Duration: {process_time}")
    return response

app.middleware("http")(logger)

@app.get("/")
async def home():
    return {"message": "This endpoint has a middleware"}
