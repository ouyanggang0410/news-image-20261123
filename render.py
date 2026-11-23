#!/usr/bin/env python3
"""THE HORIZON — render the 23 November 2026 world news as one 1024x1024 image.

Pure Python standard library only: the PNG is written by hand
(zlib + struct), and every letter is drawn from a stroke font
defined in this file, so the render runs anywhere python3 runs,
with no network and no third-party packages.

    python3 render.py            # writes news-image.png (1024x1024)

Layout: a newspaper front page. Masthead, one lead story, six
stories in two columns, a briefs strip, a by-the-numbers box,
and a source footer.
"""

import math
import struct
import sys
import zlib

import news

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (163, 22, 33)
GREY = (110, 104, 92)
LIGHT = (226, 219, 203)


# ---------------------------------------------------------------- PNG writer

def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def save_png(path, pixels, w=W, h=H):
    """pixels: list of rows, each a list of (r, g, b) tuples."""
    raw = b"".join(
        b"\x00" + b"".join(bytes(px) for px in row) for row in pixels
    )
    png = (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
        + _chunk(b"IDAT", zlib.compress(raw, 9))
        + _chunk(b"IEND", b"")
    )
    with open(path, "wb") as f:
        f.write(png)


# ------------------------------------------------------------------ canvas

class Canvas:
    def __init__(self, w=W, h=H, bg=PAPER):
        self.w, self.h = w, h
        self.px = [[bg for _ in range(w)] for _ in range(h)]

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = color

    def rect(self, x, y, w, h, color):
        for yy in range(max(0, y), min(self.h, y + h)):
            row = self.px[yy]
            for xx in range(max(0, x), min(self.w, x + w)):
                row[xx] = color

    def hline(self, x, y, w, color, thick=1):
        self.rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.rect(x, y, thick, h, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            for ox in range(thick):
                for oy in range(thick):
                    self.set(x0 + ox, y0 + oy, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def save(self, path):
        save_png(path, self.px, self.w, self.h)


# ------------------------------------------------------------- stroke font
# Glyphs are polylines on a 0..12 grid: baseline y=12, cap height 12,
# x-height 8 (lowercase sit on baseline, ascenders reach y=0),
# descenders reach y=16. Each glyph: (advance, [polyline, ...]).
# Drawn with line segments, scaled by the requested size.

def _glyphs():
    g = {}
    # Uppercase: built from straight strokes on the 0..12 grid.
    g["A"] = (11, [[(1, 12), (5.5, 0), (10, 12)], [(3, 8), (8, 8)]])
    g["B"] = (10, [[(1, 0), (1, 12)], [(1, 0), (7, 0), (9, 2), (9, 5), (7, 6), (1, 6)], [(1, 6), (8, 6), (9.5, 8), (9.5, 10), (7, 12), (1, 12)]])
    g["C"] = (10, [[(9, 2), (7, 0), (3, 0), (1, 2), (1, 10), (3, 12), (7, 12), (9, 10)]])
    g["D"] = (11, [[(1, 0), (1, 12)], [(1, 0), (7, 0), (10, 3), (10, 9), (7, 12), (1, 12)]])
    g["E"] = (9, [[(8, 0), (1, 0), (1, 12), (8, 12)], [(1, 6), (6, 6)]])
    g["F"] = (9, [[(8, 0), (1, 0), (1, 12)], [(1, 6), (6, 6)]])
    g["G"] = (11, [[(9, 2), (7, 0), (3, 0), (1, 2), (1, 10), (3, 12), (7, 12), (9, 10), (9, 7), (6, 7)]])
    g["H"] = (11, [[(1, 0), (1, 12)], [(10, 0), (10, 12)], [(1, 6), (10, 6)]])
    g["I"] = (5, [[(2.5, 0), (2.5, 12)], [(0, 0), (5, 0)], [(0, 12), (5, 12)]])
    g["J"] = (9, [[(8, 0), (8, 10), (6, 12), (2, 12), (1, 10)]])
    g["K"] = (11, [[(1, 0), (1, 12)], [(9, 0), (1, 6)], [(3, 6), (10, 12)]])
    g["L"] = (9, [[(1, 0), (1, 12), (9, 12)]])
    g["M"] = (13, [[(1, 12), (1, 0), (6.5, 8), (12, 0), (12, 12)]])
    g["N"] = (11, [[(1, 12), (1, 0), (10, 12), (10, 0)]])
    g["O"] = (11, [[(8, 0), (3, 0), (1, 2), (1, 10), (3, 12), (8, 12), (10, 10), (10, 2), (8, 0)]])
    g["P"] = (10, [[(1, 12), (1, 0)], [(1, 0), (7, 0), (9, 2), (9, 5), (7, 6), (1, 6)]])
    g["Q"] = (11, [[(8, 0), (3, 0), (1, 2), (1, 10), (3, 12), (8, 12), (10, 10), (10, 2), (8, 0)], [(7, 9), (11, 13)]])
    g["R"] = (10, [[(1, 12), (1, 0)], [(1, 0), (7, 0), (9, 2), (9, 5), (7, 6), (1, 6)], [(4, 6), (10, 12)]])
    g["S"] = (10, [[(9, 2), (7, 0), (3, 0), (1, 2), (1, 5), (3, 6), (8, 6), (9, 7), (9, 10), (7, 12), (3, 12), (1, 10)]])
    g["T"] = (11, [[(0, 0), (11, 0)], [(5.5, 0), (5.5, 12)]])
    g["U"] = (11, [[(1, 0), (1, 10), (3, 12), (8, 12), (10, 10), (10, 0)]])
    g["V"] = (11, [[(1, 0), (5.5, 12), (10, 0)]])
    g["W"] = (14, [[(1, 0), (3.5, 12), (7, 4), (10.5, 12), (13, 0)]])
    g["X"] = (11, [[(1, 0), (10, 12)], [(10, 0), (1, 12)]])
    g["Y"] = (11, [[(1, 0), (5.5, 6), (10, 0)], [(5.5, 6), (5.5, 12)]])
    g["Z"] = (10, [[(1, 0), (9, 0), (1, 12), (9, 12)]])
    # Digits.
    g["0"] = (11, [[(8, 0), (3, 0), (1, 2), (1, 10), (3, 12), (8, 12), (10, 10), (10, 2), (8, 0)]])
    g["1"] = (6, [[(4, 0), (4, 12)], [(2, 2), (4, 0)], [(1, 12), (5, 12)]])
    g["2"] = (10, [[(1, 2), (3, 0), (7, 0), (9, 2), (9, 5), (5, 8), (1, 12), (9, 12)]])
    g["3"] = (10, [[(1, 1), (3, 0), (7, 0), (9, 2), (9, 5), (7, 6), (5, 6)], [(7, 6), (9, 8), (9, 10), (7, 12), (3, 12), (1, 10)]])
    g["4"] = (10, [[(8, 0), (8, 12)], [(8, 6), (1, 6), (3, 0)]])
    g["5"] = (10, [[(9, 0), (1, 0), (1, 6), (7, 6), (9, 8), (9, 10), (7, 12), (3, 12), (1, 10)]])
    g["6"] = (10, [[(9, 1), (7, 0), (3, 0), (1, 2), (1, 10), (3, 12), (7, 12), (9, 10), (9, 7), (7, 6), (3, 6), (1, 8)]])
    g["7"] = (10, [[(1, 0), (9, 0), (6, 12)]])
    g["8"] = (10, [[(7, 0), (3, 0), (1, 2), (1, 5), (3, 6), (7, 6), (9, 5), (9, 2), (7, 0)], [(3, 6), (1, 8), (1, 10), (3, 12), (7, 12), (9, 10), (9, 8), (7, 6)]])
    g["9"] = (10, [[(1, 11), (3, 12), (7, 12), (9, 10), (9, 2), (7, 0), (3, 0), (1, 2), (1, 5), (3, 6), (7, 6), (9, 4)]])
    # Lowercase: x-height top y=4, baseline y=12, descenders to y=16.
    g["a"] = (10, [[(8, 5), (3, 4), (1, 6), (1, 10), (3, 12), (8, 12), (9, 10), (9, 5)], [(9, 5), (9, 12)]])
    g["b"] = (10, [[(1, 0), (1, 12)], [(1, 12), (7, 12), (9, 10), (9, 6), (7, 4), (1, 4)]])
    g["c"] = (9, [[(8, 6), (6, 4), (3, 4), (1, 6), (1, 10), (3, 12), (6, 12), (8, 10)]])
    g["d"] = (10, [[(9, 0), (9, 12)], [(9, 12), (3, 12), (1, 10), (1, 6), (3, 4), (9, 4)]])
    g["e"] = (10, [[(9, 6), (7, 4), (3, 4), (1, 6), (1, 9), (2, 12), (6, 12), (9, 10)], [(1, 8), (9, 8)]])
    g["f"] = (7, [[(5, 0), (3, 0), (1, 2), (1, 12)], [(0, 4), (5, 4)]])
    g["g"] = (10, [[(9, 4), (9, 12), (7, 16), (3, 16), (1, 14)], [(9, 12), (3, 12), (1, 10), (1, 6), (3, 4), (9, 4)]])
    g["h"] = (10, [[(1, 0), (1, 12)], [(1, 4), (7, 4), (9, 6), (9, 12)]])
    g["i"] = (4, [[(2, 4), (2, 12)], [(2, 0), (2, 1)]])
    g["j"] = (6, [[(4, 4), (4, 14), (2, 16), (1, 15)], [(4, 0), (4, 1)]])
    g["k"] = (10, [[(1, 0), (1, 12)], [(8, 4), (1, 9)], [(3, 8), (9, 12)]])
    g["l"] = (4, [[(2, 0), (2, 12)]])
    g["m"] = (15, [[(1, 12), (1, 4), (5, 4), (7, 6), (7, 12)], [(7, 4), (11, 4), (13, 6), (13, 12)]])
    g["n"] = (10, [[(1, 12), (1, 4), (7, 4), (9, 6), (9, 12)]])
    g["o"] = (10, [[(7, 4), (3, 4), (1, 6), (1, 10), (3, 12), (7, 12), (9, 10), (9, 6), (7, 4)]])
    g["p"] = (10, [[(1, 4), (1, 16)], [(1, 12), (7, 12), (9, 10), (9, 6), (7, 4), (1, 4)]])
    g["q"] = (10, [[(9, 4), (9, 16)], [(9, 12), (3, 12), (1, 10), (1, 6), (3, 4), (9, 4)]])
    g["r"] = (8, [[(1, 12), (1, 4)], [(1, 4), (6, 4), (7, 6)]])
    g["s"] = (9, [[(8, 6), (6, 4), (3, 4), (1, 6), (1, 8), (3, 9), (6, 9), (8, 10), (8, 11), (6, 12), (3, 12), (1, 10)]])
    g["t"] = (7, [[(3, 0), (3, 12), (5, 12), (6, 11)], [(0, 4), (6, 4)]])
    g["u"] = (10, [[(1, 4), (1, 10), (3, 12), (7, 12), (9, 10), (9, 4)]])
    g["v"] = (10, [[(1, 4), (5, 12), (9, 4)]])
    g["w"] = (14, [[(1, 4), (3.5, 12), (7, 6), (10.5, 12), (13, 4)]])
    g["x"] = (10, [[(1, 4), (9, 12)], [(9, 4), (1, 12)]])
    g["y"] = (10, [[(1, 4), (5, 12), (9, 4)], [(5, 12), (5, 16), (3, 16), (1, 15)]])
    g["z"] = (9, [[(1, 4), (8, 4), (1, 12), (8, 12)]])
    # Punctuation and symbols.
    g["."] = (4, [[(2, 12), (2, 13)]])
    g[","] = (4, [[(2, 12), (2, 13)], [(2, 13), (1, 16)]])
    g[":"] = (4, [[(2, 4), (2, 5)], [(2, 11), (2, 12)]])
    g[";"] = (4, [[(2, 4), (2, 5)], [(2, 11), (2, 12)], [(2, 12), (1, 16)]])
    g["!"] = (4, [[(2, 0), (2, 9)], [(2, 11), (2, 12)]])
    g["?"] = (8, [[(1, 2), (3, 0), (6, 0), (7, 2), (7, 4), (4, 6), (4, 8)], [(4, 11), (4, 12)]])
    g["'"] = (4, [[(2, 0), (1, 3)]])
    g["\""] = (7, [[(2, 0), (1, 3)], [(5, 0), (4, 3)]])
    g["-"] = (8, [[(1, 7), (7, 7)]])
    g["–"] = (9, [[(1, 7), (8, 7)]])
    g["—"] = (11, [[(0, 7), (10, 7)]])
    g["("] = (6, [[(5, 0), (2, 3), (2, 9), (5, 12)]])
    g[")"] = (6, [[(1, 0), (4, 3), (4, 9), (1, 12)]])
    g["&"] = (11, [[(8, 4), (6, 4), (4, 6), (8, 12), (10, 10), (8, 8), (2, 8), (1, 10), (2, 12), (5, 12), (9, 6), (9, 2), (7, 0), (5, 1)]])
    g["%"] = (12, [[(1, 0), (10, 12)], [(4, 0), (1, 0), (1, 3), (4, 3), (4, 0)], [(11, 9), (8, 9), (8, 12), (11, 12), (11, 9)]])
    g["$"] = (10, [[(5, -1), (5, 13)], [(9, 2), (7, 0), (3, 0), (1, 2), (1, 5), (3, 6), (8, 6), (9, 7), (9, 10), (7, 12), (3, 12), (1, 10)]])
    g["/"] = (9, [[(7, 0), (2, 12)]])
    g["|"] = (4, [[(2, 0), (2, 12)]])
    g["·"] = (4, [[(2, 6), (2, 7)]])
    g["’"] = (4, [[(2, 0), (1, 3)]])
    g["“"] = (7, [[(2, 3), (1, 0)], [(5, 3), (4, 0)]])
    g["”"] = (7, [[(2, 0), (1, 3)], [(5, 0), (4, 3)]])
    g[" "] = (6, [])
    return g


GLYPHS = _glyphs()

# ------------------------------------------------------------ text drawing

def text_width(text, size):
    """Width in pixels of text drawn at cap-height `size`."""
    scale = size / 12.0
    total = 0.0
    for ch in text:
        adv, _ = GLYPHS.get(ch, GLYPHS["?"])
        total += adv * scale
    return total


def draw_text(cv, x, y, text, size, color=INK, spacing=0):
    """Draw text with top at y (cap top), size = cap height in px."""
    scale = size / 12.0
    thick = max(1, int(round(size / 14.0)))
    cx = float(x)
    for ch in text:
        adv, strokes = GLYPHS.get(ch, GLYPHS["?"])
        for poly in strokes:
            pts = [(cx + px * scale, y + py * scale) for px, py in poly]
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                cv.line(int(round(x0)), int(round(y0)),
                        int(round(x1)), int(round(y1)), color, thick)
        cx += adv * scale + spacing
    return cx


def draw_centered(cv, cx, y, text, size, color=INK, spacing=0):
    draw_text(cv, cx - text_width(text, size) / 2.0, y, text, size, color, spacing)


def wrap(text, size, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if text_width(trial, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_para(cv, x, y, text, size, max_w, color=INK, leading=None):
    """Draw a wrapped paragraph; returns y just below the last line."""
    leading = leading or int(size * 1.45)
    for line in wrap(text, size, max_w):
        draw_text(cv, x, y, line, size, color)
        y += leading
    return y


def draw_headline(cv, x, y, text, size, max_w, color=INK, leading=None):
    """Headline: wrapped, returns y below it."""
    return draw_para(cv, x, y, text, size, max_w, color, leading or int(size * 1.15))


# ------------------------------------------------------------------ layout

def render(out_path="news-image.png"):
    cv = Canvas()
    mx = 44                      # page margin
    content_w = W - 2 * mx

    # --- top rule + date line
    cv.hline(mx, 30, content_w, INK, 4)
    draw_text(cv, mx, 44, news.DATE_LINE, 15, INK, spacing=1)
    right = "No. 327  |  PRICE: ONE WORLD"
    draw_text(cv, W - mx - text_width(right, 15), 44, right, 15, INK, spacing=1)
    cv.hline(mx, 66, content_w, INK, 1)

    # --- masthead
    draw_centered(cv, W / 2, 74, news.MASTHEAD, 72, INK, spacing=6)
    draw_centered(cv, W / 2, 154, news.TAGLINE, 14, RED, spacing=4)
    cv.hline(mx, 178, content_w, INK, 4)
    cv.hline(mx, 184, content_w, INK, 1)

    # --- lead story
    y = 202
    draw_text(cv, mx, y, news.LEAD["kicker"], 13, RED, spacing=1)
    y += 22
    y = draw_headline(cv, mx, y, news.LEAD["headline"], 44, content_w, INK)
    y += 6
    for para in news.LEAD["body"]:
        y = draw_para(cv, mx, y, para, 14, content_w, leading=19)
        y += 2
    y += 6
    cv.hline(mx, y, content_w, INK, 2)
    y += 14

    # --- six stories, two columns
    col_w = (content_w - 28) // 2
    col_x = [mx, mx + col_w + 28]
    col_y = [y, y]
    for i, st in enumerate(news.STORIES):
        cx, cy = col_x[i % 2], col_y[i % 2]
        draw_text(cv, cx, cy, st["kicker"], 12, RED, spacing=1)
        cy += 18
        cy = draw_headline(cv, cx, cy, st["headline"], 19, col_w)
        cy += 3
        cy = draw_para(cv, cx, cy, st["body"], 11, col_w, leading=14)
        cy += 8
        col_y[i % 2] = cy
    y = max(col_y) + 2
    cv.hline(mx, y, content_w, INK, 2)
    y += 14

    # --- briefs strip, two columns (no heading: the rule does the work)
    brief_y = [y, y]
    for i, (kicker, text) in enumerate(news.BRIEFS):
        bx = mx + (i % 2) * (col_w + 28)
        by = draw_para(cv, bx, brief_y[i % 2], kicker + ": " + text, 11, col_w, leading=14)
        brief_y[i % 2] = by + 2
    y = max(brief_y) + 4
    cv.hline(mx, y, content_w, INK, 2)
    y += 12

    # --- by the numbers (no heading)
    box_w = (content_w - 3 * 16) // 4
    for i, (num, label) in enumerate(news.NUMBERS):
        bx = mx + i * (box_w + 16)
        cv.rect(bx, y, box_w, 68, LIGHT)
        draw_centered(cv, bx + box_w / 2, y + 8, num, 28, RED)
        draw_para(cv, bx + 8, y + 42, label, 10, box_w - 16, INK)
    y += 68 + 10
    cv.hline(mx, y, content_w, INK, 4)

    # --- footer
    draw_text(cv, mx, y + 12, news.FOOTER, 11, GREY)

    cv.save(out_path)
    return out_path


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "news-image.png"
    render(path)
    print("wrote", path)

