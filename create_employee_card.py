#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pptx import Presentation
from pptx.util import Mm, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# 色定義 (RGB)
COLOR_MAIN_RED = RGBColor(253, 112, 102)      # #fd7066
COLOR_LIGHT_BEIGE = RGBColor(251, 223, 210)   # #FBDFD2
COLOR_LIGHT_BLUE = RGBColor(220, 231, 233)    # #DCE7E9
COLOR_DARK_GRAY = RGBColor(78, 75, 76)        # #4E4B4C
COLOR_LIGHT_GRAY = RGBColor(214, 214, 214)    # #D6D6D6
COLOR_WHITE = RGBColor(255, 255, 255)

# カード寸法
CARD_WIDTH = Mm(85.6)
CARD_HEIGHT = Mm(54)

# A4用紙寸法（横向き）
PAGE_WIDTH = Mm(297)
PAGE_HEIGHT = Mm(210)

# マージン
MARGIN = Mm(10)
CARD_GAP = Mm(5)

# カード配置計算
CARDS_PER_ROW = 3
CARDS_PER_COL = 2

# 計算確認
# 横: 10 + 85.6 + 5 + 85.6 + 5 + 85.6 + 10 = 287.4mm (297mm内)
# 縦: 10 + 54 + 5 + 54 + 10 = 133mm (210mm内)

def create_presentation():
    prs = Presentation()

    # スライドサイズを横向きA4に設定
    prs.slide_width = PAGE_WIDTH
    prs.slide_height = PAGE_HEIGHT

    # 空白スライドを追加
    blank_slide_layout = prs.slide_layouts[6]  # 空白レイアウト
    slide = prs.slides.add_slide(blank_slide_layout)

    # スライド背景を白で設定
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_WHITE

    # 6枚のカードを配置
    card_positions = []
    for col in range(CARDS_PER_COL):
        for row in range(CARDS_PER_ROW):
            left = MARGIN + row * (CARD_WIDTH + CARD_GAP)
            top = MARGIN + col * (CARD_HEIGHT + CARD_GAP)
            card_positions.append((left, top))

    for left, top in card_positions:
        draw_card(slide, left, top)

    # ファイルを保存
    output_file = '/home/user/hello-claude/mamawell_employee_card.pptx'
    prs.save(output_file)
    print(f"✓ PowerPointファイルを作成しました: {output_file}")

def draw_card(slide, left, top):
    """
    1枚のカードを描画
    """
    # カード背景（ベージュ系グラデーション）
    card_bg = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        left, top, CARD_WIDTH, CARD_HEIGHT
    )
    card_bg.fill.solid()
    card_bg.fill.fore_color.rgb = COLOR_LIGHT_BEIGE
    card_bg.line.color.rgb = COLOR_LIGHT_GRAY
    card_bg.line.width = Pt(0.5)

    # 上部の装飾パターン（赤いウェーブ）
    wave_top = slide.shapes.add_shape(
        MSO_SHAPE.WAVE,
        left, top, CARD_WIDTH, Mm(8)
    )
    wave_top.fill.solid()
    wave_top.fill.fore_color.rgb = COLOR_MAIN_RED
    wave_top.line.fill.background()

    # 左側のロゴエリア（赤いリボン型）
    logo_left = left + Mm(3)
    logo_top = top + Mm(8)
    logo_size = Mm(18)

    # リボン風のシェイプ
    ribbon = slide.shapes.add_shape(
        MSO_SHAPE.HEART,
        logo_left, logo_top, logo_size, logo_size
    )
    ribbon.fill.solid()
    ribbon.fill.fore_color.rgb = COLOR_MAIN_RED
    ribbon.line.fill.background()

    # ロゴテキスト「mamawell」
    logo_text_box = slide.shapes.add_textbox(
        logo_left + Mm(1),
        logo_top + Mm(10),
        Mm(16),
        Mm(8)
    )
    logo_frame = logo_text_box.text_frame
    logo_frame.clear()
    logo_frame.word_wrap = False
    p = logo_frame.paragraphs[0]
    p.text = "mamawell"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_MAIN_RED
    p.alignment = PP_ALIGN.CENTER

    # 右側のテキストエリア
    text_left = left + Mm(25)
    text_width = CARD_WIDTH - Mm(28)

    # タイトル「常に誠実に」
    title1_box = slide.shapes.add_textbox(
        text_left, top + Mm(5), text_width, Mm(5)
    )
    title1_frame = title1_box.text_frame
    title1_frame.clear()
    p = title1_frame.paragraphs[0]
    p.text = "常に誠実に"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_GRAY

    # サブタイトル「Integrity First」
    subtitle1_box = slide.shapes.add_textbox(
        text_left, top + Mm(9), text_width, Mm(4)
    )
    subtitle1_frame = subtitle1_box.text_frame
    subtitle1_frame.clear()
    p = subtitle1_frame.paragraphs[0]
    p.text = "Integrity First"
    p.font.size = Pt(7)
    p.font.color.rgb = COLOR_MAIN_RED

    # タイトル「仕組みで勝つ」
    title2_box = slide.shapes.add_textbox(
        text_left, top + Mm(15), text_width, Mm(5)
    )
    title2_frame = title2_box.text_frame
    title2_frame.clear()
    p = title2_frame.paragraphs[0]
    p.text = "仕組みで勝つ"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_GRAY

    # サブタイトル「System > Hero」
    subtitle2_box = slide.shapes.add_textbox(
        text_left, top + Mm(19), text_width, Mm(4)
    )
    subtitle2_frame = subtitle2_box.text_frame
    subtitle2_frame.clear()
    p = subtitle2_frame.paragraphs[0]
    p.text = "System > Hero"
    p.font.size = Pt(7)
    p.font.color.rgb = COLOR_MAIN_RED

    # タイトル「前進のために話す」
    title3_box = slide.shapes.add_textbox(
        text_left, top + Mm(25), text_width, Mm(5)
    )
    title3_frame = title3_box.text_frame
    title3_frame.clear()
    p = title3_frame.paragraphs[0]
    p.text = "前進のために話す"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_GRAY

    # サブタイトル「Move Forward Together」
    subtitle3_box = slide.shapes.add_textbox(
        text_left, top + Mm(29), text_width, Mm(4)
    )
    subtitle3_frame = subtitle3_box.text_frame
    subtitle3_frame.clear()
    p = subtitle3_frame.paragraphs[0]
    p.text = "Move Forward Together"
    p.font.size = Pt(7)
    p.font.color.rgb = COLOR_MAIN_RED

if __name__ == '__main__':
    create_presentation()
