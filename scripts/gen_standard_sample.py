"""Generate pic_standard_sample.png — standard printed-font BP UI with HR at same height as SYS."""
import random
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

IMG_W, IMG_H = 800, 600
OUT_PATH = Path("pic/pic_standard_sample.png")

# tablet_app dark style (matching clean_010)
style = {
    "bg": (20, 25, 40),
    "card_bg": (35, 40, 55),
    "fg": (220, 225, 240),
    "accent": (100, 200, 150),
    "secondary": (140, 145, 165),
    "danger": (255, 100, 100),
}


def get_font(size):
    paths = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyhbd.ttc",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]
    for p in paths:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


systolic, diastolic, heart_rate = 132, 82, 128

img = Image.new("RGB", (IMG_W, IMG_H), style["bg"])
draw = ImageDraw.Draw(img, "RGBA")

title_font = get_font(28)
big_font = get_font(64)
mid_font = get_font(36)
small_font = get_font(20)
tiny_font = get_font(16)

# Header bar
header_h = 44
draw.rectangle([0, 0, IMG_W, header_h], fill=style["card_bg"])
draw.text((20, 10), "HealthAgent", fill=style["accent"], font=title_font)
draw.text((IMG_W - 80, 12), f"{random.randint(9,22):02d}:{random.randint(0,59):02d}",
          fill=style["secondary"], font=small_font)

# Title
title_y = header_h + 25
draw.text((30, title_y), "血压测量结果", fill=style["fg"], font=title_font)
draw.text((30, title_y + 35), "Blood Pressure Reading", fill=style["secondary"], font=tiny_font)

# Main card
card_x, card_y = 40, title_y + 75
card_w, card_h = IMG_W - 80, 320

# Card with rounded corners + shadow
shadow_off = 3
draw.rounded_rectangle(
    [card_x + shadow_off, card_y + shadow_off, card_x + card_w + shadow_off, card_y + card_h + shadow_off],
    radius=12, fill=(0, 0, 0, 40),
)
draw.rounded_rectangle(
    [card_x, card_y, card_x + card_w, card_y + card_h], radius=12,
    fill=style["card_bg"], outline=style["secondary"], width=1,
)

# SYS (top-left)
sys_x = card_x + 30
sys_y = card_y + 40
draw.text((sys_x, sys_y), "收缩压 SYS", fill=style["secondary"], font=small_font)
draw.text((sys_x, sys_y + 30), str(systolic), fill=style["fg"], font=big_font)
draw.text((sys_x + len(str(systolic)) * 38 + 10, sys_y + 52), "mmHg",
          fill=style["secondary"], font=mid_font)

# Divider line
div_y = sys_y + 115
draw.line([(card_x + 40, div_y), (card_x + card_w - 40, div_y)], fill=style["secondary"], width=1)

# DIA (bottom-left)
dia_y = div_y + 20
draw.text((sys_x, dia_y), "舒张压 DIA", fill=style["secondary"], font=small_font)
draw.text((sys_x, dia_y + 30), str(diastolic), fill=style["fg"], font=big_font)
draw.text((sys_x + len(str(diastolic)) * 38 + 10, dia_y + 52), "mmHg",
          fill=style["secondary"], font=mid_font)

# HR on the right side — raised to same Y as SYS number (no heart icon to avoid font tofu)
hr_x = card_x + card_w - 300
hr_y = card_y + 40
draw.text((hr_x, hr_y), "心率", fill=style["secondary"], font=small_font)
draw.text((hr_x, hr_y + 30), str(heart_rate), fill=style["danger"], font=big_font)
draw.text((hr_x + len(str(heart_rate)) * 38 + 10, hr_y + 52), "bpm",
          fill=style["secondary"], font=mid_font)

# Bottom info
info_y = card_y + card_h + 20
draw.text((30, info_y),
          f"测量时间: 2026-05-0{random.randint(1,5)} {random.randint(8,22):02d}:{random.randint(0,59):02d}",
          fill=style["secondary"], font=small_font)
draw.text((30, info_y + 30), f"设备: HAG-{random.randint(100,999)} | 用户: 张**",
          fill=style["secondary"], font=small_font)

# Bottom nav bar
nav_y = IMG_H - 50
draw.rectangle([0, nav_y, IMG_W, IMG_H], fill=style["card_bg"])
nav_items = ["首页", "测量", "趋势", "我的"]
for i, item in enumerate(nav_items):
    cx = IMG_W * (i + 0.5) / 4
    color = style["accent"] if i == 1 else style["secondary"]
    draw.text((cx - 20, nav_y + 15), item, fill=color, font=small_font)

# Subtle camera effects
arr = np.array(img).astype("int16")
noise = np.random.normal(0, 4, arr.shape).astype("int16")
arr = np.clip(arr + noise, 0, 255).astype("uint8")
img = Image.fromarray(arr)
img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
img.save(str(OUT_PATH), "PNG")
print(f"Saved {OUT_PATH} | BP: {systolic}/{diastolic} HR:{heart_rate}")
