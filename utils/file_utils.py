"""备注解释：提供创建目录、检查文件和生成文件名等通用文件操作。"""

from pathlib import Path


def ensure_directory(directory: Path) -> Path:
    """确保目录存在并返回该目录。"""
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def icon_filename(index: int) -> str:
    """生成形如 ``icon_001.ico`` 的默认文件名。"""
    return f"icon_{index:03d}.ico"
