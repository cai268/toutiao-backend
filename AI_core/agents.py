from functools import lru_cache

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_deepseek import ChatDeepSeek

from config.chat_conf import get_settings
from AI_models.exceptions import ConfigurationError
from AI_models.memory.chekpointer import get_checkpointer
from AI_models.prompt.analyzer import ANALYZER_PROMPT
from AI_models.prompt.synth import SYNTH_PROMPT


def _create_chat_model() -> ChatDeepSeek:
    settings = get_settings()
    if not settings.deepseek_api_key:
        raise ConfigurationError(
            "DEEPSEEK_API_KEY 未配置，请检查项目根目录下的 .env 文件"
        )
    return ChatDeepSeek(
        model=settings.chat_model,
        api_key=settings.deepseek_api_key,
    )


@lru_cache(maxsize=1)
def get_output_agent():
    chat_model = _create_chat_model()
    middleware = SummarizationMiddleware(
        model=chat_model,
        trigger=("messages", 6),
        keep=("messages", 3),
    )
    return create_agent(
        model=chat_model,
        system_prompt=SYNTH_PROMPT,
        checkpointer=get_checkpointer(),
        middleware=[middleware],
    )


@lru_cache(maxsize=1)
def get_analyzer_agent():
    return create_agent(
        model=_create_chat_model(),
        system_prompt=ANALYZER_PROMPT,
    )
