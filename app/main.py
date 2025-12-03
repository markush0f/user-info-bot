from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.domains.users.router import router as user_router
from app.domains.projects.router import router as project_router
from app.domains.entities.router import router as entity_router
from app.domains.embeddings.router import router as embedding_router
from app.domains.chats.router import router as chat_router
from app.shared.exceptions.exception_handler import add_exception_handlers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return JSONResponse(content={"status": "ok"}, status_code=200)

add_exception_handlers(app)
app.include_router(user_router)
app.include_router(project_router)
app.include_router(entity_router)
app.include_router(embedding_router)
app.include_router(chat_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)
