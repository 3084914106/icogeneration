# core/generator.py
# 职责：接收 IconGenerateRequest，调用硅基流动 API 生成图标，保存并返回路径

import requests
import os
from dotenv import load_dotenv
from models.requests import IconGenerateRequest

load_dotenv()

DL_HEADERS = {...}  # 不变


def generate_icon(request: IconGenerateRequest):
    api_key = os.getenv("SILICONFLOW_API_KEY", "")
    if not api_key:
        raise ValueError("❌ 未找到 SILICONFLOW_API_KEY，请检查 .env 文件")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # ---- 第三步：请求体 ----
    payload = {
        "model": "Kwai-Kolors/Kolors",
        "prompt": f"{request.prompt}, icon, flat design, minimalist, transparent background, high contrast, vector art",
        "image_size": "1024x1024",
        "batch_size": max(1, min(request.count, 4)),
        "num_inference_steps": 20,
        "guidance_scale": 7.5
    }

    # ---- 第四步：发送请求 ----
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=120)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 错误 {response.status_code}: {response.text[:300]}")
        raise
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        raise

    # ---- 第五步：解析响应 ----
    result = response.json()

    # ---- 第六步：下载并保存图片 ----
    os.makedirs("./output", exist_ok=True)
    saved_paths = []

    for i, img_info in enumerate(result.get("images", [])):
        img_url = img_info.get("url")
        if not img_url:
            continue

        try:
            img_resp = requests.get(img_url, headers=DL_HEADERS, timeout=60)
            img_resp.raise_for_status()

            # 不校验 Content-Type，直接按 PNG 保存
            out_path = f"./output/icon_{request.prompt[:8]}_{i}.png"
            with open(out_path, "wb") as f:
                f.write(img_resp.content)

            saved_paths.append(out_path)
            print(f"✅ 保存成功: {out_path}")

        except Exception as e:
            print(f"❌ 第{i}张下载失败: {e}")

    # ---- 第七步：返回结果 ----
    return saved_paths