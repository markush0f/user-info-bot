from fastapi import FastAPI, JSONResponse

app = FastAPI()


@app.get("/health")
def health():
    return JSONResponse(content={"status": "ok"})

@app.post("")
def insert_user_info():
    