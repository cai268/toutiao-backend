import bcrypt

# bcrypt 算法本身只处理前 72 字节，超出部分会被拒绝，需要手动截断
BCRYPT_MAX_BYTES = 72


def _to_bytes(password: str) -> bytes:
    """把明文密码编码为字节，并按 bcrypt 的长度限制截断"""
    return password.encode("utf-8")[:BCRYPT_MAX_BYTES]


def get_hash_password(password: str) -> str:
    """对明文密码进行哈希，返回可存储的字符串"""
    hashed = bcrypt.hashpw(_to_bytes(password), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """校验明文密码与已存储的哈希是否匹配"""
    return bcrypt.checkpw(
        _to_bytes(plain_password),
        hashed_password.encode("utf-8"),
    )