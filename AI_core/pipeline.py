from collections.abc import Iterator
from typing import Any

from langchain.messages import HumanMessage

from AI_core.agents import get_analyzer_agent,get_output_agent
from AI_core.executor import executor
from AI_models.exceptions import ExternalServiceError
from AI_models.memory.manager import build_thread_id
from AI_models.utils.parser import parse_json



# 调用大模型，并给出答复
class ChatPipeline:
    def __init__(
        self,
        output_agent=None,
        analyzer_agent=None,
        executor_fn=executor,
    ):
        self._output_agent = output_agent
        self._analyzer_agent = analyzer_agent
        self._executor_fn = executor_fn

    @property
    def output_agent(self):# 拿到输出答复
        if self._output_agent is None:
            self._output_agent = get_output_agent()
        return self._output_agent

    @property
    def analyzer_agent(self):# 拿到输入答复
        if self._analyzer_agent is None:
            self._analyzer_agent = get_analyzer_agent()
        return self._analyzer_agent

    @staticmethod
    def _extract_content(response: dict) -> str:# 提取agent的文本答复并将类型(可能是json)转化为字符串返回
        content = response["messages"][-1].content
        return ChatPipeline._content_to_text(content)

    @staticmethod
    def _content_to_text(content: Any) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict):
                    parts.append(str(item.get("text", "")))
                else:
                    parts.append(str(item))
            return "\n".join(part for part in parts if part)
        return str(content)

    def _route(self, message: str, mode: str) -> dict:# 用户提出auto->调用analyzer。否则直接返回。返回字典
        if mode != "auto":
            return {"route": mode, "query": message}

        response = self.analyzer_agent.invoke(
            {"messages": [HumanMessage(message)]}
        )
        return parse_json(self._extract_content(response), message)# 将analyser回复先转为str，然后拼接转为dict

    def chat(self, request, user_id: int) -> "ChatResponse":
        from schemas.chat import ChatResponse

        try:
            thread_id = build_thread_id(user_id, request.dialog_id)
            decision = self._route(request.message, request.mode)
            route = decision.get("route", "rag")# 先拿到字典里的route，否则默认rag
            query = decision.get("query", request.message)
            retrieval = self._executor_fn(decision, request.message)

            if retrieval:
                final_input = (
                    f"用户问题:{request.message}\n\n"
                    f"检索结果:{retrieval}"
                )
            else:
                final_input = f"用户问题:{request.message}"

            response = self.output_agent.invoke(
                {"messages": [HumanMessage(final_input)]},
                {"configurable": {"thread_id": thread_id}},
            )

            return ChatResponse(
                dialog_id=request.dialog_id,
                mode=request.mode,
                route=route,
                query=query,
                retrieval=retrieval or None,
                answer=self._extract_content(response),
            )
        except ExternalServiceError:
            raise
        except Exception as exc:
            raise ExternalServiceError(
                f"Agent 服务调用失败：{exc}"
            ) from exc

    def stream(self, request, user_id: int) -> Iterator[dict[str, Any]]:
        try:
            thread_id = build_thread_id(user_id, request.dialog_id)
            yield {
                "event": "status",
                "data": {"message": "正在分析问题"},
            }

            decision = self._route(request.message, request.mode)
            route = decision.get("route", "rag")
            query = decision.get("query", request.message)
            yield {
                "event": "meta",
                "data": {
                    "dialog_id": request.dialog_id,
                    "mode": request.mode,
                    "route": route,
                    "query": query,
                },
            }

            if route == "direct":
                retrieval = ""
            else:
                yield {
                    "event": "status",
                    "data": {"message": "正在检索相关资料"},
                }
                retrieval = self._executor_fn(decision, request.message)

            final_input = (
                f"用户问题:{request.message}\n\n检索结果:{retrieval}"
                if retrieval
                else f"用户问题:{request.message}"
            )
            yield {
                "event": "status",
                "data": {"message": "正在生成回答"},
            }

            answer_parts = []
            for chunk, _metadata in self.output_agent.stream(
                {"messages": [HumanMessage(final_input)]},
                {"configurable": {"thread_id": thread_id}},
                stream_mode="messages",
            ):
                content = self._content_to_text(
                    getattr(chunk, "content", "")
                )
                if not content:
                    continue
                answer_parts.append(content)
                yield {
                    "event": "token",
                    "data": {"content": content},
                }

            answer = "".join(answer_parts)
            yield {
                "event": "done",
                "data": {
                    "dialog_id": request.dialog_id,
                    "mode": request.mode,
                    "route": route,
                    "query": query,
                    "retrieval": retrieval or None,
                    "answer": answer,
                },
            }
        except ExternalServiceError as exc:
            yield {
                "event": "error",
                "data": {"message": str(exc)},
            }
        except Exception as exc:
            yield {
                "event": "error",
                "data": {"message": f"Agent 服务调用失败：{exc}"},
            }


def chat(request, user_id: int) -> "ChatResponse":
    return ChatPipeline().chat(request, user_id)
