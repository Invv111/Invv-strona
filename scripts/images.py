"""
Makes the WebP files the site loads. Run after adding or replacing a screenshot:

  python scripts/images.py        (needs Pillow)

- img/<x>.jpg            -> img/<x>-800.webp + img/<x>-1400.webp   (hero and "Coming next" tiles)
- img/<plugin>/<n>.jpg   -> img/<plugin>/<n>.webp (1400 wide) + <n>-thumb.webp (320 wide, gallery thumbnails)
- img/<x>-logo.png       -> img/<x>-logo.webp
The .jpg files stay as the source and as link-preview images (Discord).
"""
import glob
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "img")


def save(im, path, width, quality=76):
    im = im.copy()
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6)
    return os.path.getsize(path)


total_before = total_after = 0

for src in glob.glob(os.path.join(IMG, "*.jpg")):
    im = Image.open(src).convert("RGB")
    base = src[:-4]
    total_before += os.path.getsize(src)
    total_after += save(im, base + "-800.webp", 800) + save(im, base + "-1400.webp", 1400)

for src in glob.glob(os.path.join(IMG, "*", "*.jpg")):
    im = Image.open(src).convert("RGB")
    base = src[:-4]
    total_before += os.path.getsize(src)
    total_after += save(im, base + ".webp", 1400) + save(im, base + "-thumb.webp", 320, 70)

for src in glob.glob(os.path.join(IMG, "*-logo.png")):
    im = Image.open(src).convert("RGBA")
    im.thumbnail((128, 128), Image.LANCZOS)          # shown at 128px at most
    im.save(src[:-4] + ".webp", "WEBP", quality=88, method=6)
    total_before += os.path.getsize(src)
    total_after += os.path.getsize(src[:-4] + ".webp")

print(f"jpg/png {total_before // 1024} KB -> webp {total_after // 1024} KB (both sizes)")
