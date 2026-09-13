import logging
from logging.handlers import RotatingFileHandler

from backend.app.core.config import settings

# 模块级幂等标志：避免给 Logger 实例挂载自定义属性（类型检查器不认可）
_configured = False


def setup_logging() -> None:
    """配置全局日志：控制台 + 可选文件（滚动切割）。幂等，重复调用安全。"""
    global _configured
    if _configured:
        return

    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    root = logging.getLogger()
    root.setLevel(log_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    if settings.LOG_TO_FILE:
        settings.LOG_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            settings.LOG_DIR / "argus.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

    _configured = True
    logging.getLogger(__name__).info("Logging initialized (level=%s)", settings.LOG_LEVEL)


def get_logger(name: str) -> logging.Logger:
    """获取项目 logger，统一以传入 name 命名。"""
    return logging.getLogger(name)
