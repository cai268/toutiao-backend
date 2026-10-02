import uvicorn
from fastapi import FastAPI,Path,Query,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from fastapi.responses import HTMLResponse,FileResponse
from utils.exception import register_exception_handlers
import sys
from pathlib import Path
from routers import favorite, history, news, users

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




if __name__ == '__main__':
   uvicorn.run('main:app',host='127.0.0.1',port=8000,reload=True)
