from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(message: str = "Success", data = None):# 最终要响应的格式
    response = {
        "code": 200,
        "message": message,
        "data": data or {}
    }
    # 确保任何的fastAPI、Pydantic、ORM对象都能被序列化为JSON格式
    return JSONResponse(content=jsonable_encoder(response))