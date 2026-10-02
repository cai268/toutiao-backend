# @app.get()
# @app.post()
# @app.put()
# @app.delete()

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/get')
async def get():
    return {'message':'get'}

@app.post('/post')
async def post():
  return {'message':'post'}

@app.put('/put')
async def put():
   return {'message':'put'}

@app.delete('/delete')
async def delete():
   return {'message':'delete'}

if __name__ == '__main__':
   uvicorn.run('fastAPi接口文档:app',host='127.0.0.1',port=8080,reload=True)
