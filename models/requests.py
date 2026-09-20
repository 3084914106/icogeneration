# 导入 dataclass 装饰器，用于快速定义只存数据的类
from dataclasses import dataclass


# 用 @dataclass 定义图标生成请求的数据结构
# 这个文件是全局唯一的 Request 定义，window.py 和 generator.py 都从这里导入
@dataclass
class IconGenerateRequest:
    prompt: str   # 用户输入的提示词，描述想要生成什么样的图标
    count: int    # 需要生成的图标数量