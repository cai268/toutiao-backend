# 新闻相关的缓存方法：新闻分类的读取和写入
# key - value
from config.redis_conf import get_json_cache,set_cache


CATEGORIES_KEY = "news:categories"


# 获取新闻分类缓存
async def get_cache_categories():
    return await get_json_cache(CATEGORIES_KEY)



# 写入新闻分类缓存：缓存数据，过期时间
async def set_cache_categories(data:list[dict[str,any]],expire: int = 7200):
    return await set_cache(key=CATEGORIES_KEY,value=data,expire=expire)