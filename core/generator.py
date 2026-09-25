# core/generator.py
import requests
import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv
from models.requests import IconGenerateRequest
from core.converter import png_to_ico

# 找项目根目录，加载 .env
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# 下载图片用的浏览器头
DL_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Referer": "https://api.siliconflow.cn/"
}


def generate_icon(request: IconGenerateRequest):
    """
    调用 SiliconFlow 文生图接口
    返回：生成图片的文件路径列表
    """

    # ---- 第一步：API 地址 ----
    url = "https://api.siliconflow.cn/v1/images/generations"

    # ---- 第二步：读 API Key ----
    api_key = os.getenv("SILICONFLOW_API_KEY", "sk-emllrlmwlxysjlwgqbvbabjenhowfzputdshemdxuudukzmu")
    if not api_key:
        raise ValueError("❌ 未找到 SILICONFLOW_API_KEY，请检查 .env 文件")

    # ---- 第三步：请求头 ----
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # ---- 第四步：请求体 ----
    payload = {
        "model": "Kwai-Kolors/Kolors",
        "prompt": f"{request.prompt}, icon, flat design, minimalist, transparent background, high contrast, vector art",
        "image_size": "1024x1024",
        "batch_size": max(1, min(request.count, 4)),
        "num_inference_steps": 20,
        "guidance_scale": 7.5
    }

    # ---- 第五步：发送请求 ----
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=120)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 错误 {response.status_code}: {response.text[:300]}")
        raise
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        raise

    # ---- 第六步：解析响应 ----
    result = response.json()

    # ---- 第七步：下载并保存图片 ----
    output_dir = os.path.join(
        os.path.expanduser("~"),
        "Pictures",
        "ICO图标生成器"
    )
    os.makedirs(output_dir, exist_ok=True)
    saved_paths = []

    for i, img_info in enumerate(result.get("images", [])):
        img_url = img_info.get("url")
        if not img_url:
            continue

        try:
            img_resp = requests.get(img_url, headers=DL_HEADERS, timeout=60)
            img_resp.raise_for_status()

            with tempfile.NamedTemporaryFile(
                suffix=".png", dir=output_dir, delete=False
            ) as temp_image:
                temp_image.write(img_resp.content)
                temp_path = temp_image.name

            ico_path = os.path.join(output_dir, f"icon_{request.prompt[:8]}_{i}.ico")
            try:
                png_to_ico(Path(temp_path), Path(ico_path))
            finally:
                os.remove(temp_path)

            saved_paths.append(ico_path)
            print(f"✅ 保存成功: {ico_path}")

        except Exception as e:
            print(f"❌ 第{i}张图片处理失败: {e}")

    # ---- 第八步：返回结果 ----
    return saved_paths
