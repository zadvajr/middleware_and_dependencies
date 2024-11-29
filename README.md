# Middleware and Dependencies in FastAPI
## Middleware
### What is middleware?
Middleware is a function or class that runs before and/or after every request in your application.

It’s commonly used to add functionality, such as logging, request validation, or modifying responses.

### How Middleware Works
- __Before Request__: Middleware processes the request before it reaches your endpoint.
- __After Response__: Middleware processes the response before it’s sent back to the client.

### Creating Middleware in FastAPI
FastAPI provides a simple way to implement middleware using the @app.middleware decorator or custom middleware classes.

__Example:__

Adding a Simple Middleware
```python
import time

from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http") # or app.middleware("http")(add_process_time_header)(log_middleware)
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
async def read_root():
    return {"message": "Hello, Middleware!"}
```

__Explanation:__

The add_process_time_header middleware calculates the processing time for each request and adds it to the response header.

## Dependencies
### What are Dependencies?
Dependencies are a way to share common logic, functionality, or data across multiple endpoints in FastAPI. They help you keep your code DRY (Don't Repeat Yourself).

### Common Use Cases
- Database connections
- Authentication and authorization
- Validation logic
- Configurations or shared resources

### Defining Dependencies
You define a dependency as a function and then use it in your endpoint. FastAPI will automatically "inject" the results of the dependency function.

__Example:__

Basic Dependency
```python
from fastapi import FastAPI, Depends

app = FastAPI()

def get_user():
    return {"user": "John Doe"}

@app.get("/profile")
def read_profile(user: dict = Depends(get_user)):
    return {"message": f"Hello, {user['user']}!"}
```

__Explanation:__

- The get_user function is a dependency.
- The Depends keyword tells FastAPI to call get_user and pass its result to the user parameter in the read_profile endpoint.

### Dependencies with Parameters
Dependencies can also accept parameters. This is useful for passing configurations or dynamic values.
__Example:__

Dependency with Parameters
```python
from fastapi import FastAPI, Depends

app = FastAPI()

def verify_token(token: str):
    if token != "mysecrettoken":
        raise ValueError("Invalid token")
    return {"token": token}

@app.get("/secure-data")
def get_secure_data(token_data: dict = Depends(verify_token)):
    return {"message": f"Access granted with token {token_data['token']}"}
```

__Explanation:__

- *verify_token* is a dependency with a parameter.
- You can pass a token dynamically to check its validity.

### Dependency Injection with Classes
FastAPI allows you to use classes as dependencies. This is useful for managing state or configurations.

__Example:__

Class-based Dependency
```python
from fastapi import FastAPI, Depends

app = FastAPI()

class Config:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def format_message(self, message: str):
        return f"{self.prefix}: {message}"

def get_config():
    return Config(prefix="INFO")

@app.get("/log")
def log_message(config: Config = Depends(get_config)):
    return {"log": config.format_message("This is a log message.")}
```
__Explanation:__

- The Config class holds some state (prefix).
- *get_config* provides an instance of the class as a dependency.

### Combining Middleware and Dependencies
Middleware and dependencies can work together seamlessly to manage requests and responses.
#### Example: Middleware + Dependency for Logging
```python
from fastapi import FastAPI, Depends, Request
import time

app = FastAPI()

# Middleware to log request time
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request took {process_time:.2f} seconds")
    return response

# Dependency for request authentication
def verify_user(token: str = "defaulttoken"):
    if token != "secrettoken":
        return {"authenticated": False}
    return {"authenticated": True}

@app.get("/data")
def get_data(auth: dict = Depends(verify_user)):
    if not auth["authenticated"]:
        return {"error": "Authentication failed"}
    return {"data": "Here is your secure data!"}
```

### Dependency Overrides
FastAPI allows you to override dependencies. This is especially useful for testing.
#### Example: Overriding a Dependency
```python
from fastapi.testclient import TestClient

app = FastAPI()

def get_data():
    return {"data": "Original Data"}

@app.get("/data")
def read_data(data: dict = Depends(get_data)):
    return data

# Override Dependency for Testing
@app.get("/data", dependencies=[Depends(lambda: {"data": "Mock Data"})])
def override_data():
    return {"data": "Mock Data"}
```

### Key Points to Remember
1.  Middleware runs before and after each request.
2.  Dependencies simplify shared logic, making your code modular and maintainable.
3.  Use Depends to inject dependencies into endpoints.
4.  Dependencies can accept parameters, making them flexible.
5.  Middleware and dependencies can be combined for robust request handling.
