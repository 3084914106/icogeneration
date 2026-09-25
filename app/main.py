from tkinter import messagebox

from core.generator import generate_icon
from models.requests import IconGenerateRequest
from ui.window import get_user_input


def main():
    # 打开窗口，并等待用户完成输入
    user_input = get_user_input()

    # 如果用户取消输入或没有返回数据，直接结束程序
    if not user_input:
        return

    request = IconGenerateRequest(
        prompt=user_input["prompt"],
        count=user_input["count"],
    )

    try:
        outputs = generate_icon(request)
    except Exception as error:
        messagebox.showerror("生成失败", str(error))
        return

    if outputs:
        messagebox.showinfo(
            "生成完成",
            f"成功生成 {len(outputs)} 个 ICO 文件。\n保存位置：{outputs[0]}",
        )
    else:
        messagebox.showwarning("生成失败", "没有生成可用的 ICO 文件。")


if __name__ == "__main__":
    main()
