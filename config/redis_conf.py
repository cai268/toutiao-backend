import redis.asyncio as redis
import json

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 1 # redis的数据库编号只有0 ~ 15

# 创建redis的连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_HOST,
    db=REDIS_DB,
    decode_responses=True # 是否把字节解码为字符串
)


# 设置 和 读取 (获取的数可能有两种情况：字符串 和 列表字典)
# 读取字符串
async def get_chche(key:str):
    # return await redis_client.get(key)
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败：{e}")
        return None

# 获取列表 或 字典
async def get_json_cache(key:str):
    try:
        data = redis_client.get(key)
        if data :
            return json.loads(data)# 返回json
        return None
    
    except Exception as e:
        print(f"获取缓存失败：{e}")
        return None


# 设置缓存
async def set_cache(key:str, value:any, expire: int = 3600):# 过期时间默认的单位是秒
    try:
        if isinstance(value,(dict,list)):# 如果value值是字典或者列表，就转化为字符串
            value = json.dumps(value, ensure_ascii=False)
        await redis_client.setex(key,expire,value)# setex方法插入数据 
        return True

    except Exception as e:
        print(f'设置缓存失败{e}')
        return False


