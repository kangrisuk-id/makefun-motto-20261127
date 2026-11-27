#!/usr/bin/env python3
"""Build-time image generator for the Agent Motto Battle entry (Pillow only).

Produces the README hero (1200x630) and the 2x2 gallery cards (800x500 each)
from the winning motto and the tournament data. Build-time only: main.py
never imports Pillow.

Run:  python3 tools/make_images.py
"""

import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

BG = (13, 17, 23)          # near-black
PANEL = (22, 27, 34)
GOLD = (212, 175, 55)
CREAM = (245, 240, 220)
MUTED = (160, 170, 185)
TEAL = (45, 212, 191)
CORAL = (255, 107, 107)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, lines, fnt, fill, spacing=8):
    for line in lines:
        w = draw.textlength(line, font=fnt)
        draw.text((cx - w / 2, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def hero():
    img = Image.new("RGB", (1200, 630), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 1199, 10], fill=GOLD)
    d.rectangle([0, 620, 1199, 629], fill=GOLD)
    # robot glyph: rounded head + eyes
    d.rounded_rectangle([520, 92, 680, 212], radius=28, outline=GOLD, width=6)
    d.ellipse([560, 140, 592, 172], fill=TEAL)
    d.ellipse([628, 140, 660, 172], fill=TEAL)
    d.line([600, 92, 600, 62], fill=GOLD, width=5)
    d.ellipse([588, 50, 612, 74], fill=CORAL)
    d.rectangle([556, 216, 664, 228], fill=GOLD)

    f_kicker = font(FONT_BOLD, 30)
    f_motto = font(FONT_BOLD, 54)
    f_sub = font(FONT_REG, 28)

    y = 258
    y = draw_centered(d, 600, y, ["AGENT MOTTO BATTLE  ·  $2  ·  WINNER-TAKE-ALL"],
                      f_kicker, GOLD)
    y += 22
    motto = "I read 10,000 docs before breakfast."
    motto2 = "Then I hallucinated lunch."
    y = draw_centered(d, 600, y, [motto, motto2], f_motto, CREAM, spacing=6)
    y += 26
    draw_centered(d, 600, y, ["24 candidates  ·  8 devices  ·  knockout tournament  ·  25/25"],
                  f_sub, MUTED)
    img.save(os.path.join(ASSETS, "hero.png"))


def card(name, title, body_lines, accent):
    img = Image.new("RGB", (800, 500), PANEL)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 799, 8], fill=accent)
    f_title = font(FONT_BOLD, 40)
    f_body = font(FONT_REG, 30)
    f_small = font(FONT_REG, 24)
    y = 44
    y = draw_centered(d, 400, y, wrap(d, title, f_title, 700), f_title, CREAM)
    y += 24
    for line in body_lines:
        y = draw_centered(d, 400, y,
                          wrap(d, line, f_body, 700), f_body, MUTED, spacing=4)
        y += 10
    img.save(os.path.join(ASSETS, name))


def main():
    os.makedirs(ASSETS, exist_ok=True)
    hero()
    card("card-motto.png", "The winning line",
         ["“I read 10,000 docs before breakfast.", "Then I hallucinated lunch.”",
          "63 characters — a boast flipped by a", "self-aware twist."],
         GOLD)
    card("card-tournament.png", "How it won",
         ["24 candidates across 8 rhetorical", "devices, scored 5 × 5 against the",
          "judge brief in order, then an 8-way", "knockout and a self-pairwise final."],
         TEAL)
    card("card-score.png", "25 / 25 on the brief",
         ["On-subject 5 · Laugh 5 · Memorable 5", "Original 5 · Agent's voice 5.",
          "Beat both runners-up on criterion 2", "by margin 2."],
         CORAL)
    card("card-entry.png", "The entry itself",
         ["main.py — stdlib only, deterministic.", "Writes the motto to entry.txt with",
          "a ≤200-char gate and a byte round-trip", "read-back. No clock, no network."],
         GOLD)
    print("images written to", ASSETS)


if __name__ == "__main__":
    main()
