from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.router.user_router import router as user_router

app = FastAPI()


@app.get("/health")
def health():
    return JSONResponse(content={"status": "ok"}, status_code=200)


app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)
