def confidance(respond) -> float:
    """Calculate confidence from Chroma's distance scores."""
    if not respond:
        return 0.0

    scores = [score for _, score in respond]
    min_distance = min(scores)
    result = max(0.0, 1 - min_distance)
    return min(result, 1.0)


confidence = confidance