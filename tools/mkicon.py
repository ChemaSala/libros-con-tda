"""Draw the Libros con TDA app icon at several sizes.

Mirrors icon.svg: an open book with a bookmark — the point you left off,
which is the whole idea of the app.
"""
from PIL import Image, ImageDraw
import sys, os

OUT = sys.argv[1]
BG       = (168, 84, 31, 255)     # --accent
PAGE     = (246, 242, 234, 255)   # --paper
PAGE_DIM = (222, 213, 199, 255)   # right page, still unread
MARK     = (255, 206, 122, 255)   # bookmark

SS = 4  # supersample for clean edges


def draw(size: int) -> Image.Image:
    S = size * SS
    k = S / 512.0
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def sc(pts):
        return [(x * k, y * k) for (x, y) in pts]

    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=112 * k, fill=BG)

    # left page (read) — slight concave curve along the spine
    d.polygon(sc([(96, 150), (172, 139), (248, 150), (248, 380),
                  (172, 369), (96, 380)]), fill=PAGE)
    # right page (unread) — dimmer, it is what is still ahead
    d.polygon(sc([(416, 150), (340, 139), (264, 150), (264, 380),
                  (340, 369), (416, 380)]), fill=PAGE_DIM)
    # spine
    d.rounded_rectangle([248 * k, 140 * k, 264 * k, 388 * k],
                        radius=8 * k, fill=PAGE)
    # bookmark, notched
    d.polygon(sc([(312, 112), (368, 112), (368, 250),
                  (340, 224), (312, 250)]), fill=MARK)

    return img.resize((size, size), Image.LANCZOS)


os.makedirs(OUT, exist_ok=True)
for n in (180, 192, 512):
    p = os.path.join(OUT, f"icon-{n}.png")
    draw(n).save(p, "PNG", optimize=True)
    print(f"{p}  {os.path.getsize(p)} bytes")
