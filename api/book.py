from fastapi import APIRouter

api_book = APIRouter()

@api_book.get('/get')
async def get():
    return {'message':'get'}

@api_book.post('/post')
async def post():
  return {'message':'post'}

@api_book.put('/put')
async def put():
   return {'message':'put'}

@api_book.delete('/delete')
async def delete():
   return {'message':'delete'}