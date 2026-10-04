import re


def clear_data(respond: str) -> str:
    """Remove publisher/contact noise from search results."""
    lines = respond.split("\n")
    keep_lines = []
    noise_keywords = [
        "邮购电话",
        "质量投诉",
        "盗版侵权",
        "咨询联系方式",
        "版权所有",
        "翻印必究",
        "联系及邮购",
        "邮箱",
    ]

    for line in lines:
        if any(keyword in line for keyword in noise_keywords):
            continue
        keep_lines.append(line)

    respond = "\n".join(keep_lines)
    respond = re.sub(
        r"(?:QQ|qq)[\u4e00-\u9fa5]*\s*[: ：]\s*[1-9]\d{3,12}",
        "",
        respond,
        flags=re.IGNORECASE,
    )
    respond = re.sub(
        r"[第]\s*\d+\s*[页|章|版]",
        "",
        respond,
        flags=re.IGNORECASE,
    )
    respond = re.sub(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "",
        respond,
        flags=re.IGNORECASE,
    )
    respond = re.sub(r"\s+", " ", respond)
    return respond.strip()