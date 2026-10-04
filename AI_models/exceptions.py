class AssistantError(Exception):# 定义父类，下面都是子类，返回异常的时候只需要调用父类就行了
    """Base exception for application errors."""


class ConfigurationError(AssistantError):
    """Raised when required configuration is missing or invalid."""


class KnowledgeBaseError(AssistantError):
    """Raised when the local knowledge base cannot be used."""


class ExternalServiceError(AssistantError):
    """Raised when an external service fails."""