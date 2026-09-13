from functools import lru_cache
from typing import ClassVar
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    应用配置类

    配置项会自动从以下来源读取（优先级从高到低）：
    1. 环境变量
    2. .env 文件
    3. 默认值

    安全须知：
    - 敏感信息（API Key、密码等）默认值均为 None / 空，切勿在代码中写入真实凭据；
      这些值只通过 .env 或环境变量提供，且 .env 已被 .gitignore 忽略，不会提交到仓库。
    """
    base_url:Path = Path(__file__).parent.parent.parent
    model_config:ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=str(base_url / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # ==================== 应用基础配置 ====================
    
    PROJECT_NAME: str = Field(default="", description="项目名称")
    API_V1_PREFIX: str = Field(default="/api/v1", description="API 路由前缀")
    DEBUG: bool = Field(default=True, description="调试模式")

    # ==================== 数据库 / 中间件（非敏感参数可保留本地默认值） ====================
    MYSQL_HOST: str = Field(default="127.0.0.1", description="MySQL 主机")
    MYSQL_PORT: int = Field(default=3306, description="MySQL 端口")
    MYSQL_USER: str = Field(default="root", description="MySQL 用户")
    MYSQL_PASSWORD: str | None = Field(default=None, description="MySQL 密码（来自 .env）")
    MYSQL_DATABASE: str = Field(default="argus", description="MySQL 数据库名")
    SQLALCHEMY_DATABASE_URI: str | None = Field(
        default=None, description="完整数据库连接串（可选，提供后覆盖下方拼接）"
    )

    REDIS_HOST: str = Field(default="127.0.0.1", description="Redis 主机")
    REDIS_PORT: int = Field(default=6379, description="Redis 端口")
    REDIS_DB: int = Field(default=0, description="Redis DB 索引")
    REDIS_PASSWORD: str | None = Field(default=None, description="Redis 密码（来自 .env）")
    REDIS_URI: str | None = Field(
        default=None, description="完整 Redis 连接串（可选，提供后覆盖下方拼接）"
    )

    MILVUS_HOST: str = Field(default="127.0.0.1", description="Milvus 主机")
    MILVUS_PORT: int = Field(default=19530, description="Milvus 端口")
    MILVUS_URI: str | None = Field(
        default=None, description="完整 Milvus 连接串（可选，提供后覆盖下方拼接）"
    )

    # ==================== AI 服务配置 ====================
    # 硅基流动 API
    SF_API_KEY: str | None = Field(default=None, description="硅基流动 API Key")
    SF_BASE_URL: str | None = Field(default=None, description="硅基流动 Base URL")

    # 阿里百炼 API
    AL_BAILIAN_API_KEY: str | None = Field(default=None, description="阿里百炼 API Key")
    AL_BAILIAN_BASE_URL: str | None = Field(default=None, description="阿里百炼 Base URL")

    # OpenAI（兼容接口）
    OPENAI_API_KEY: str | None = Field(default=None, description="OpenAI API Key")
    OPENAI_BASE_URL: str | None = Field(
        default="https://api.openai.com/v1", description="OpenAI Base URL"
    )
    OPENAI_MODEL: str | None = Field(default="gpt-4o", description="OpenAI 模型名")

    # ==================== 模型配置 ====================
    MAIN_MODEL_NAME: str | None = Field(
        default="Qwen/Qwen3-32B", description="主模型名称"
    )
    SUB_MODEL_NAME:str|None=Field(
        default="qwen3-max",description="子模型名称"
    )

    # ==================== MCP / 百度搜索 ====================
    MCP_SERVER_URI: str | None = Field(
        default=None, description="通用 MCP server 地址（可选）"
    )
    BAIDU_SEARCH_MCP_COMMAND: str = Field(
        default="npx -y baidu-search-mcp",
        description="百度搜索 MCP server 的启动命令（stdio 模式使用）",
    )
    BAIDU_SEARCH_MCP_URL: str | None = Field(
        default=None, description="百度搜索 MCP server 的 SSE 地址（SSE 模式使用，可选）"
    )
    BAIDU_SEARCH_MCP_TOOL: str = Field(
        default="baidu_search", description="搜索工具名（不同 server 命名不同，可用 list_tools() 确认）"
    )

    # ==================== CORS ====================
    BACKEND_CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:5173"], description="允许跨域的来源"
    )

    # ==================== 日志配置 ====================
    LOG_LEVEL: str = Field(default="INFO", description="日志级别: DEBUG/INFO/WARNING/ERROR")
    LOG_TO_FILE: bool = Field(default=True, description="是否将日志写入文件")
    LOG_DIR: Path = Field(default=base_url / "logs", description="日志文件存放目录")

    # -------------------- 拼接属性 --------------------
    @property
    def database_uri(self) -> str:
        if self.SQLALCHEMY_DATABASE_URI:
            return self.SQLALCHEMY_DATABASE_URI
        pwd = self.MYSQL_PASSWORD or ""
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{pwd}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
        )
    @property
    def async_database_url(self):
        if self.SQLALCHEMY_DATABASE_URI:
            return self.SQLALCHEMY_DATABASE_URI
        pwd = self.MYSQL_PASSWORD or ""
        return (
            f"mysql+aiomysql://{self.MYSQL_USER}:{pwd}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
        )
    @property
    def redis_uri(self) -> str:
        if self.REDIS_URI:
            return self.REDIS_URI
        auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @property
    def milvus_uri(self) -> str:
        if self.MILVUS_URI:
            return self.MILVUS_URI
        return f"http://{self.MILVUS_HOST}:{self.MILVUS_PORT}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
