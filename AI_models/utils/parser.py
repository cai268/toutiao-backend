import json


def parse_json(text: str, fallback_query: str = "") -> dict:
    try:
        return json.loads(text)
    except (TypeError, json.JSONDecodeError):
        pass

    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            return json.loads(text[start:end])
    except (TypeError, json.JSONDecodeError):
        pass

    return {"route": "rag", "query": fallback_query}