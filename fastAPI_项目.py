from fastapi import FastAPI

import uvicorn

app = FastAPI()#实例化

@app.get('/')# 装饰器，当用到这个方法的时候就会找到这个函数,/后面是路由地址
async def root():# async是一个异步框架，可以不用写，但是
    return {"message":"hello"}

@app.get('/cai')# 路由方式http://127.0.0.1:8080/cai
async def cai():
    return {'message':'hello cai'}

if __name__== '__main__':
    uvicorn.run("fastAPI:app",host="127.0.0.1",port = 8080,reload= True)
  # 分别代表定义app = FastAPI()的'文件名','ip地址','端口号(别搞成字符串)'
  # reload代表:你改了代码并保存后，服务器会自动重启，不用手动关掉再重新运行