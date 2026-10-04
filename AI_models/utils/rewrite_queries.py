def rewrite_queries(user_query: str) -> list[str]:
    """Create a small set of rule-based query variants."""
    queries = [user_query]
    synonyms = {
        "区别": "差异",
        "差异": "区别",
        "怎么": "如何",
        "如何": "怎么",
        "什么": "定义",
        "为什么": "原因",
    }

    for old, new in synonyms.items():
        if old in user_query:
            queries.append(user_query.replace(old, new))

    return list(dict.fromkeys(queries))[:3]