from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[1] # 定位项目根目录
load_dotenv(PROJECT_ROOT / ".env", override=False)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "multi-agent-assistant"
    environment: str = "development"
    log_level: str = "INFO"
    host: str = "127.0.0.1"
    port: int = 8000

    deepseek_api_key: str | None = None
    bocha_api_key: str | None = None

    chat_model: str = "deepseek-v4-pro"
    embedding_model_name: str = (
        "D:/AI_tool/embedding_models/BAAI/models/"
        "BAAI--bge-base-zh-v1.5/snapshots/master"
    )
    embedding_device: str = "cpu"

    data_dir: Path = Field(default=PROJECT_ROOT / "data")# PROJECT_ROOT / "data"是根路径+相对路径=绝对路径
    local_doc_db_dir: Path = Field(
        default=PROJECT_ROOT / "AI_kb" / "local_doc_db"
    )
    sqlite_dir: Path = Field(default=PROJECT_ROOT / "AI_kb" / "SQlite")
    default_data_file: Path | None = None

    @staticmethod
    def _absolute(path: Path) -> Path:# 将相对路径转为绝对路径，绝对路径就直接拿来用
        return path if path.is_absolute() else PROJECT_ROOT / path

    @property
    def resolved_data_dir(self) -> Path:
        return self._absolute(self.data_dir)

    @property
    def resolved_local_doc_db_dir(self) -> Path:
        return self._absolute(self.local_doc_db_dir)

    @property
    def resolved_sqlite_dir(self) -> Path:
        return self._absolute(self.sqlite_dir)

    @property
    def legacy_data_dir(self) -> Path:
        return PROJECT_ROOT / "notebook" / "data"

    @property
    def legacy_local_doc_db_dir(self) -> Path:
        return PROJECT_ROOT / "notebook" / "local_doc_db"

    @property
    def vectorstore_read_dir(self) -> Path:
        primary = self.resolved_local_doc_db_dir
        legacy = self.legacy_local_doc_db_dir
        if (primary / "chroma.sqlite3").exists() or not legacy.exists():
            return primary
        return legacy

    @property
    def parent_db_write_path(self) -> Path:
        return self.resolved_local_doc_db_dir / "parent_documents.sqlite3"

    @property
    def parent_db_read_path(self) -> Path:
        primary = self.parent_db_write_path# 新父库里的导包
        legacy = self.legacy_local_doc_db_dir / "parent_documents.sqlite3"
        return primary if primary.exists() or not legacy.exists() else legacy

    @property
    def memory_db_path(self) -> Path:
        return self.resolved_sqlite_dir / "checkpoint.db"

    def resolve_data_file(self, file_path: str | Path | None = None) -> Path:
        if file_path is not None:
            candidate = Path(file_path).expanduser()
            if not candidate.is_absolute():
                candidate = PROJECT_ROOT / candidate
            return candidate.resolve()

        if self.default_data_file is not None:
            candidate = self._absolute(self.default_data_file).expanduser()
            if candidate.exists(): 
                return candidate.resolve()

        for directory in (self.resolved_data_dir, self.legacy_data_dir):
            if not directory.exists():
                continue
            files = sorted(directory.glob("*.pdf")) + sorted(directory.glob("*.txt"))
            if files:
                return files[0].resolve()

        return (self.resolved_data_dir / "knowledge.pdf").resolve()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
