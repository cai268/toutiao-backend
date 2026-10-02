from fastapi import APIRouter

api_user = APIRouter()

@api_user.get('/get')
async def get():
    return {'message':'get'}

@api_user.post('/post')
async def post():
  return {'message':'post'}

@api_user.put('/put')
async def put():
   return {'message':'put'}

@api_user.delete('/delete')
async def delete():
   return {'message':'delete'}