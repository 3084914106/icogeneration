# window.py
# 职责：创建输入窗口、收集用户输入、组装成 IconGenerateRequest、调用生成流程

# 导入 tkinter，用于构建 GUI 界面
import tkinter as tk

# 从 models/requests.py 导入统一定义的请求数据类
# 这样 window 和 generator 用的是同一个类，不会出现字段对不上的问题
from models.requests import IconGenerateRequest


# 定义获取用户输入的函数
def get_user_input():
    # 创建 tkinter 主窗口实例
    root = tk.Tk()

    # 设置窗口标题
    root.title("输入窗口")

    # 设置窗口尺寸：宽400 × 高220（比原版高一些，因为多了一个数量输入框）
    root.geometry("300x200")

    # ---- 第一行：prompt 输入 ----

    # 创建标签，提示用户输入 prompt
    tk.Label(root, text="请输入内容：", font=("SimHei", 12)).pack(pady=10)

    # 创建 prompt 输入框
    entry = tk.Entry(root, font=("SimHei", 11), width=40)
    # 放置到窗口
    entry.pack(pady=5)

    # ---- 第二行：count 输入 ----

    # 创建标签，提示用户输入生成数量
    tk.Label(root, text="生成数量：", font=("SimHei", 12)).pack(pady=5)

    # 用字典存储返回结果，方便嵌套函数修改
    result = {}

    # 确认按钮回调函数
    def on_confirm():
        # 读取 prompt 输入框内容，去掉首尾空格
        result["prompt"] = entry.get().strip()
        # 读取 count 输入框内容，转换为整数
        result["count"] = 1
        # 关闭窗口，退出 mainloop
        root.destroy()

    # 创建确认按钮，点击触发 on_confirm
    tk.Button(root, text="确认", command=on_confirm, font=("SimHei", 11)).pack(pady=15)

    # 启动事件循环，阻塞等待用户操作
    root.mainloop()

    # 返回收集到的用户输入字典
    return result


# 当该文件作为主程序直接运行时
# ... 前面不变 ...

if __name__ == "__main__":
    # 获取用户输入
    data = get_user_input()

    # 组装请求对象
    request = IconGenerateRequest(
        prompt=data.get("prompt", ""),
        count=data.get("count", 1)
    )

    # 导入生成函数
    from core.generator import generate_icon

    # 调用生成函数
    outputs = generate_icon(request)

    # 打印结果
    print(f"生成完成，共 {len(outputs)} 张图片：")
    for path in outputs:
        print(f"  → {path}")