"""将 PNG 图片转换为包含多个常用尺寸的 ICO 文件。"""

from pathlib import Path

from PIL import Image


ICON_SIZES = [(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]

def png_to_ico(png_path: Path, ico_path: Path) -> Path:
    """保留透明度，将 PNG 缩放为多尺寸图标并保存到 ``ico_path``。"""
    with Image.open(png_path) as image:
        image.convert("RGBA").save(ico_path, format="ICO", sizes=ICON_SIZES)

    return ico_path
