from AI_models.tools.rag import Get_Notes
from AI_models.tools.web import Bocha_Search


def executor(
    decision: dict,
    user_query: str,
    rag_tool=Get_Notes,
    web_tool=Bocha_Search,
) -> str:
    route = decision.get("route", "rag")
    query = decision.get("query", user_query)

    if route == "rag":
        return rag_tool.invoke(query)
    if route == "web":
        return web_tool.invoke(query)
    if route == "both":
        result_rag = rag_tool.invoke(query)
        result_web = web_tool.invoke(query)
        return f"rag检索:{result_rag}\n\nweb搜索:{result_web}\n"
    if route == "direct":
        return ""
    return rag_tool.invoke(user_query)