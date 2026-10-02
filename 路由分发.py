from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path

root = Path(__file__).parent
sys.path.insert(0,str(root))

from api.book import api_book
from api.user import api_user

app = FastAPI()

app.include_router(api_book,prefix='/book',tags=["图书接口"])
app.include_router(api_user,prefix='/user',tags=["用户接口"])

if __name__ == '__main__':
   uvicorn.run('路由分发:app',host='127.0.0.1',port=8080,reload=True)