import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from utils.exception import register_exception_handlers
import sys
from pathlib import Path
from routers import favorite, history, news, users
from routers.AI_chat import chat,memory,health

root = Path(__file__).parent
sys.path.insert(0,str(root))
app = FastAPI()

register_exception_handlers(app)  # 注册全局异常处理器

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:6000",
        "http://127.0.0.1:6000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)
app.include_router(memory.router)
app.include_router(chat.router)
app.include_router(health.router)

web_dir = root / "web"
app.mount("/web", StaticFiles(directory=web_dir), name="web")


@app.get("/", include_in_schema=False)
async def web_index():
    return FileResponse(web_dir / "index.html")



if __name__ == '__main__':
   uvicorn.run('main:app',host='127.0.0.1',port=8000,reload=True)
