"""备注解释：定义在各模块间传递的图标核心数据结构。"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Icon:
    """图标数据。"""

    source_path: Path
    ico_path: Path | None = None
    prompt: str = ""
