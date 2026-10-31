#!/usr/bin/env python3
"""Render the site's product images. Run: python3 tools/shots/render.py [path/to/unlinked-extension]

The popup in the images is the real one from the extension folder (by default ../unlinked-extension,
next to this repo), run with sample numbers. Each image is written to assets/ as WebP at 1x and 2x,
and the picture shown when a link to the site is shared as assets/og-image.jpg.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(HERE))
EXT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(SITE, "..", "unlinked-extension"))
ASSETS = os.path.join(SITE, "assets")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
STATS = {"total": 31, "byReason": {"activity": 14, "notFollowed": 9, "promoted": 6, "module": 2}, "onFeed": True}

# name: (template, width in CSS px, height or None to fit the popup)
# The Advanced view is taller than any page needs, so it is cut below the post types and faded out.
CROP = {"popup-advanced": 1040}
SCENES = {
    "popup": ("popup.html", 560, None),
    "popup-advanced": ("popup.html", 560, None),
    "og": ("og.html", 1200, 630),
}


def screenshot(url, out, width, height):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--default-background-color=00000000", "--blink-settings=preferredColorScheme=1", "--allow-file-access-from-files", "--virtual-time-budget=3000",
                    f"--window-size={width},{height}", f"--screenshot={out}", url],
                   check=True, capture_output=True)


def popup_harness(tmp, advanced):
    """The extension's own popup page, with Chrome's APIs answered by sample data."""
    html = open(os.path.join(EXT, "popup.html"), encoding="utf-8").read()
    version = json.load(open(os.path.join(EXT, "manifest.json")))["version"]
    mock = ("<script>window.chrome = {"
            "storage: { sync: { get: (d, cb) => cb(d === null ? {} : { ...d }), set() {} }, local: { get: (d, cb) => cb({ ...d }) } },"
            f"tabs: {{ query: (q, cb) => cb([{{ id: 1, url: 'https://www.linkedin.com/feed/' }}]), sendMessage: (id, m, cb) => cb({json.dumps(STATS)}), reload() {{}} }},"
            f"runtime: {{ lastError: null, getManifest: () => ({{ version: '{version}' }}) }} }};</script>")
    # No transitions, so switches are drawn in their final position.
    html = html.replace("<head>", f'<head><base href="file://{EXT}/"><style>*, *::before, *::after {{ transition: none !important; }}</style>', 1)
    html = html.replace('<script src="defaults.js"></script>', mock + '<script src="defaults.js"></script>', 1)
    if advanced:
        html = html.replace("</body>", "<script>document.body.classList.add('open')</script></body>", 1)
    path = os.path.join(tmp, f"popup-{'advanced' if advanced else 'presets'}-harness.html")
    open(path, "w", encoding="utf-8").write(html)
    return path


def content_height(png):
    """Height in CSS px of a popup render, up to its last row that is not plain background."""
    im = Image.open(png).convert("RGB")
    bg = im.getpixel((im.width - 1, im.height - 1))
    for y in range(im.height - 1, -1, -1):
        row = im.crop((0, y, im.width, y + 1)).getcolors(im.width)
        if len(row) > 1 or row[0][1] != bg:
            return (y + 1) // 2 + 8
    return im.height // 2


def fade_bottom(png, height):
    im = Image.open(png).convert("RGBA").crop((0, 0, Image.open(png).width, height * 2))
    alpha = im.getchannel("A")
    ramp = 200  # px at 2x
    for y in range(im.height - ramp, im.height):
        k = (im.height - y) / ramp
        row = alpha.crop((0, y, im.width, y + 1)).point(lambda a: int(a * k))
        alpha.paste(row, (0, y))
    im.putalpha(alpha)
    im.save(png)


def save(png, name):
    if name in CROP:
        fade_bottom(png, CROP[name])
    im = Image.open(png)
    im.save(os.path.join(ASSETS, f"{name}-{im.width}.webp"), "WEBP", quality=86, method=6)
    half = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
    half.save(os.path.join(ASSETS, f"{name}-{half.width}.webp"), "WEBP", quality=86, method=6)
    print(f"{name}: {half.width}x{half.height} (and 2x)")


def og(png):
    """The 1200x630 picture shown when a link to the site is shared."""
    im = Image.open(png).convert("RGBA").resize((1200, 630), Image.LANCZOS)
    card = Image.new("RGB", im.size, "white")
    card.paste(im, (0, 0), im)
    card.save(os.path.join(ASSETS, "og-image.jpg"), "JPEG", quality=88, optimize=True, progressive=True)
    print("og-image.jpg: 1200x630")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        heights = {}
        for advanced in (False, True):
            harness = popup_harness(tmp, advanced)
            probe = os.path.join(tmp, "probe.png")
            screenshot(f"file://{harness}", probe, 480, 2400)
            heights[advanced] = content_height(probe)
        for name, (template, width, height) in SCENES.items():
            advanced = name == "popup-advanced"
            popup_h = heights[advanced]
            html = open(os.path.join(HERE, template), encoding="utf-8").read()
            html = (html.replace("{{POPUP}}", "file://" + popup_harness(tmp, advanced))
                        .replace("{{POPUP_H}}", str(popup_h))
                        .replace("{{EXT}}", "file://" + EXT)
                        .replace("{{HERE}}", "file://" + HERE))
            page = os.path.join(tmp, f"{name}.html")
            open(page, "w", encoding="utf-8").write(html)
            png = os.path.join(tmp, f"{name}.png")
            screenshot(f"file://{page}", png, width, height or popup_h + 80)
            if name == "og":
                og(png)
            else:
                save(png, name)


if __name__ == "__main__":
    main()
