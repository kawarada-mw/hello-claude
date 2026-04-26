#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mamawell 社員証カード PDF 生成スクリプト
- A4横向き、6枚レイアウト (3列 x 2行)
- 印刷品質のベクターPDF
"""

import os
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ===== フォント登録 =====
JP_FONT   = "IPAGothic"
EN_FONT   = "Helvetica"
FONT_PATH = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
pdfmetrics.registerFont(TTFont(JP_FONT, FONT_PATH))

# ===== 色 =====
RED       = HexColor("#fd7066")
PINK      = HexColor("#FBDFD2")
BLUE_GRAY = HexColor("#DCE7E9")
DARK      = HexColor("#4E4B4C")
LGRAY     = HexColor("#D6D6D6")
WHITE     = HexColor("#FFFFFF")

# ===== ページ・カード寸法 =====
PAGE_W, PAGE_H = landscape(A4)          # 841.89pt × 595.28pt
CARD_W  = 85.6 * mm
CARD_H  = 54   * mm
COLS, ROWS = 3, 2
GAP_X = GAP_Y = 5 * mm
MARGIN_X = (PAGE_W - CARD_W * COLS - GAP_X * (COLS - 1)) / 2
MARGIN_Y = (PAGE_H - CARD_H * ROWS - GAP_Y * (ROWS - 1)) / 2

LOGO_PATH = "/home/user/hello-claude/logo.png"


def card_origin(col, row):
    """カード左下原点（reportlabはY軸が下から上）"""
    x = MARGIN_X + col * (CARD_W + GAP_X)
    y = MARGIN_Y + (ROWS - 1 - row) * (CARD_H + GAP_Y)
    return x, y


# ===== 描画ユーティリティ =====
def filled_oval(c, x, y, w, h, color):
    c.setFillColor(color)
    c.setStrokeColor(color)
    c.ellipse(x, y, x + w, y + h, stroke=0, fill=1)


def draw_card(c, ox, oy):
    """1枚のカードを描画（ox, oyは左下座標）"""

    # 1. 白背景（長方形）
    c.setFillColor(WHITE)
    c.setStrokeColor(LGRAY)
    c.setLineWidth(0.3)
    c.rect(ox, oy, CARD_W, CARD_H, stroke=1, fill=1)

    # 2. 装飾シェイプ（右上：ピンク）
    c.saveState()
    clip_card(c, ox, oy)
    draw_blobs_top_right(c, ox, oy)
    draw_blobs_bottom_left(c, ox, oy)
    draw_wave(c, ox, oy)
    c.restoreState()

    # 3. ロゴ
    draw_logo(c, ox, oy)

    # 4. 価値観テキスト
    draw_values(c, ox, oy)


def clip_card(c, ox, oy):
    """カード矩形でクリッピング（はみ出し装飾を隠す）"""
    p = c.beginPath()
    p.rect(ox, oy, CARD_W, CARD_H)
    c.clipPath(p, stroke=0, fill=0)


def draw_blobs_top_right(c, ox, oy):
    """右上のピンク装飾"""
    filled_oval(c, ox + 58*mm, oy + CARD_H - 14*mm, 32*mm, 22*mm, PINK)
    filled_oval(c, ox + 70*mm, oy + CARD_H - 6*mm,  20*mm, 14*mm, PINK)
    filled_oval(c, ox + 78*mm, oy + CARD_H - 2*mm,  12*mm, 8*mm,  PINK)


def draw_blobs_bottom_left(c, ox, oy):
    """左下のブルーグレー＋ピンク装飾"""
    filled_oval(c, ox - 3*mm,  oy - 6*mm,  32*mm, 18*mm, BLUE_GRAY)
    filled_oval(c, ox + 15*mm, oy - 4*mm,  20*mm, 12*mm, PINK)
    filled_oval(c, ox + 1*mm,  oy - 3*mm,  14*mm, 9*mm,  BLUE_GRAY)


def draw_wave(c, ox, oy):
    """下部の赤い波線"""
    c.setStrokeColor(RED)
    c.setLineWidth(1.2)
    c.setLineCap(1)  # round
    wave_y = oy + 8 * mm
    p = c.beginPath()
    p.moveTo(ox, wave_y)
    segments = [
        (ox + 10*mm, wave_y + 3*mm, ox + 20*mm, wave_y - 2*mm, ox + 30*mm, wave_y + 1*mm),
        (ox + 42*mm, wave_y + 4*mm, ox + 55*mm, wave_y - 3*mm, ox + 65*mm, wave_y),
        (ox + 72*mm, wave_y + 3*mm, ox + 80*mm, wave_y - 1*mm, ox + CARD_W, wave_y + 1*mm),
    ]
    for x1, y1, x2, y2, x3, y3 in segments:
        p.curveTo(x1, y1, x2, y2, x3, y3)
    c.drawPath(p, stroke=1, fill=0)


def draw_logo(c, ox, oy):
    """左側のロゴ（画像があれば埋め込み）"""
    logo_x = ox + 3 * mm
    logo_y = oy + 14 * mm
    logo_w = 32 * mm
    logo_h = 32 * mm

    if os.path.exists(LOGO_PATH):
        c.drawImage(LOGO_PATH, logo_x, logo_y, width=logo_w, height=logo_h,
                    preserveAspectRatio=True, anchor='c', mask='auto')
    else:
        # フォールバック: シェイプでロゴ風を再現
        cx = ox + 19 * mm
        cy = oy + 30 * mm
        filled_oval(c, cx - 10*mm, cy - 5*mm, 14*mm, 12*mm, RED)
        filled_oval(c, cx + 2*mm,  cy - 3*mm, 10*mm,  9*mm, RED)
        filled_oval(c, cx - 1*mm,  cy - 1*mm,  5*mm,  4*mm, WHITE)

    # "mamawell" テキスト
    c.setFont(EN_FONT + "-Bold", 11)
    c.setFillColor(RED)
    c.drawCentredString(ox + 19 * mm, oy + 10 * mm, "mamawell")


def draw_values(c, ox, oy):
    """右側の3つの価値観"""
    items = [
        ("♡",  "常に誠実に",       "Integrity First",       PINK,      oy + 38*mm),
        ("ⓘ",  "仕組みで勝つ",     "System > Hero",         BLUE_GRAY, oy + 24*mm),
        ("⊕",  "前進のために話す", "Move Forward Together", PINK,      oy + 10*mm),
    ]
    icon_x   = ox + 41 * mm
    icon_r   = 3.5 * mm
    text_x   = icon_x + icon_r * 2 + 2 * mm
    text_w   = ox + CARD_W - 2 * mm - text_x

    for icon, jp, en, bg_color, item_y in items:
        # アイコン円
        filled_oval(c, icon_x, item_y, icon_r * 2, icon_r * 2, bg_color)
        c.setFont(EN_FONT, 7)
        c.setFillColor(RED)
        c.drawCentredString(icon_x + icon_r, item_y + icon_r * 0.75, icon)

        # 日本語タイトル
        c.setFont(JP_FONT, 8.5)
        c.setFillColor(DARK)
        c.drawString(text_x, item_y + icon_r, jp)

        # 英語サブタイトル
        c.setFont(EN_FONT, 6.5)
        c.setFillColor(RED)
        c.drawString(text_x, item_y + 1.5 * mm, en)

    # 点線区切り
    c.setStrokeColor(LGRAY)
    c.setLineWidth(0.4)
    c.setDash([1.5, 2.5])
    sep_x0 = ox + 41 * mm
    sep_x1 = ox + CARD_W - 2 * mm
    c.line(sep_x0, oy + 34 * mm, sep_x1, oy + 34 * mm)
    c.line(sep_x0, oy + 20 * mm, sep_x1, oy + 20 * mm)
    c.setDash()  # reset


def draw_trim_marks(c):
    """トンボ（断裁位置マーク）"""
    mark = 2 * mm
    c.setStrokeColor(LGRAY)
    c.setLineWidth(0.25)
    for row in range(ROWS):
        for col in range(COLS):
            x, y = card_origin(col, row)
            for cx, cy in [(x, y), (x + CARD_W, y), (x, y + CARD_H), (x + CARD_W, y + CARD_H)]:
                c.line(cx - mark, cy, cx + mark, cy)
                c.line(cx, cy - mark, cx, cy + mark)


def main():
    out = "/home/user/hello-claude/mamawell_employee_card.pdf"
    c = canvas.Canvas(out, pagesize=landscape(A4))
    c.setTitle("mamawell 社員証カード")

    # 白背景
    c.setFillColor(WHITE)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # 6枚描画
    for row in range(ROWS):
        for col in range(COLS):
            x, y = card_origin(col, row)
            draw_card(c, x, y)

    draw_trim_marks(c)
    c.save()
    print(f"✓ PDF作成完了: {out}")


if __name__ == "__main__":
    main()
