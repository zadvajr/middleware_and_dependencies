from fastapi import FastAPI, Depends

app = FastAPI()

def get_user():
    return {"user": "Francis Peter"}

@app.get("/user")
def view_user_profile(user: dict = Depends(get_user)):
    return {"message": f"Hello {user['user']}!"}