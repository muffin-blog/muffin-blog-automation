"""
Audible記事専用アイキャッチ画像生成システム
読書苦手な人向けの温かみのあるデザインを自動生成
"""

import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap

# 親ディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class AudibleEyecatchGenerator:
    """Audible記事専用のアイキャッチ画像生成クラス"""
    
    def __init__(self, save_directory: str = "/Users/satoumasamitsu/osigoto/ブログ自動化/マフィンブログ画像"):
        self.save_directory = save_directory
        os.makedirs(save_directory, exist_ok=True)
    
    def create_audible_eyecatch(self, 
                              title: str = "読書苦手でも大丈夫！聴く読書で解決",
                              subtitle: str = "30日無料体験",
                              filename: str = "audible_読書苦手_アイキャッチ_20250808.png",
                              width: int = 1200,
                              height: int = 630) -> str:
        """
        Audible記事用の温かみのあるアイキャッチ画像を生成
        
        Args:
            title: メインタイトル
            subtitle: サブタイトル
            filename: ファイル名
            width: 画像幅
            height: 画像高さ
        
        Returns:
            保存された画像のパス
        """
        
        # 温かみのあるカラーパレット（読書苦手な人にも安心感を与える色）
        colors = {
            'primary': '#FF6B35',      # 温かいオレンジ（Audibleカラー）
            'secondary': '#2C3E50',    # 落ち着いたダークブルー
            'accent': '#F39C12',       # 親しみやすい黄色
            'background1': '#FFF8F0',  # 柔らかいクリーム色
            'background2': '#FFE5D9',  # 優しいピーチ色
            'text_dark': '#2C3E50',
            'text_light': '#FFFFFF',
            'warm_pink': '#FFB6C1',    # 温かいピンク
        }
        
        # 背景にグラデーションを作成
        img = Image.new('RGB', (width, height), color=colors['background1'])
        draw = ImageDraw.Draw(img)
        
        # 縦方向のグラデーション背景
        for y in range(height):
            gradient_factor = y / height
            
            # background1からbackground2へのグラデーション
            r1, g1, b1 = tuple(int(colors['background1'][i:i+2], 16) for i in (1, 3, 5))
            r2, g2, b2 = tuple(int(colors['background2'][i:i+2], 16) for i in (1, 3, 5))
            
            r = int(r1 + (r2 - r1) * gradient_factor)
            g = int(g1 + (g2 - g1) * gradient_factor)
            b = int(b1 + (b2 - b1) * gradient_factor)
            
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # デコレーション要素（イヤホンを表現する円形要素）
        # 大きな装飾円（イヤホンのイメージ）
        circle_size = min(width, height) // 8
        
        # 左上の装飾円
        draw.ellipse([width // 20, height // 20, 
                     width // 20 + circle_size, height // 20 + circle_size], 
                    fill=colors['warm_pink'], outline=colors['primary'], width=3)
        
        # 右下の装飾円
        draw.ellipse([width - width // 20 - circle_size, height - height // 20 - circle_size, 
                     width - width // 20, height - height // 20], 
                    fill=colors['accent'], outline=colors['primary'], width=3)
        
        # 音波を表現する円弧
        for i in range(3):
            arc_radius = 50 + i * 25
            arc_x = width // 4
            arc_y = height // 2
            
            draw.arc([arc_x - arc_radius, arc_y - arc_radius, 
                     arc_x + arc_radius, arc_y + arc_radius], 
                    start=300, end=420, 
                    fill=colors['primary'], width=3)
        
        # 本のアイコンを表現する矩形
        book_width = 60
        book_height = 80
        book_x = width - 150
        book_y = height // 3
        
        # 本の背景
        draw.rounded_rectangle([book_x, book_y, book_x + book_width, book_y + book_height], 
                             radius=5, fill=colors['primary'])
        
        # 本のページを表現する線
        for i in range(3):
            line_y = book_y + 15 + i * 20
            draw.line([book_x + 10, line_y, book_x + book_width - 10, line_y], 
                     fill=colors['text_light'], width=2)
        
        # フォント設定
        title_font_size = min(width, height) // 16
        subtitle_font_size = title_font_size // 2
        
        # フォントパスを試行
        font_paths = [
            "/System/Library/Fonts/HelveticaNeue.ttc",
            "/System/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/Library/Fonts/Arial.ttf",
        ]
        
        title_font = None
        subtitle_font = None
        
        for font_path in font_paths:
            try:
                title_font = ImageFont.truetype(font_path, title_font_size)
                subtitle_font = ImageFont.truetype(font_path, subtitle_font_size)
                print(f"✅ フォント読み込み成功: {font_path}")
                break
            except (OSError, IOError):
                continue
        
        # フォントが見つからない場合はデフォルトを使用
        if title_font is None:
            print("⚠️ カスタムフォントが見つかりません。デフォルトフォントを使用します。")
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            title_font_size = 48
            subtitle_font_size = 24
        
        # タイトルを適切な長さで改行
        title_lines = []
        if len(title) > 15:
            # 「読書苦手でも大丈夫！」と「聴く読書で解決」に分割
            if "！" in title:
                parts = title.split("！")
                title_lines.append(parts[0] + "！")
                if len(parts) > 1 and parts[1]:
                    title_lines.append(parts[1])
            else:
                title_lines = textwrap.wrap(title, width=15)
        else:
            title_lines = [title]
        
        # 全体のテキスト高さを計算
        line_height = title_font_size * 1.3
        total_title_height = len(title_lines) * line_height
        subtitle_height = subtitle_font_size * 1.5
        total_text_height = total_title_height + subtitle_height + 40
        
        # テキスト開始位置（中央配置）
        text_start_y = (height - total_text_height) / 2
        
        # 背景ボックス（半透明の白）
        box_padding = 30
        max_text_width = 0
        
        # 最大テキスト幅を計算
        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            max_text_width = max(max_text_width, text_width)
        
        # サブタイトル幅もチェック
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        max_text_width = max(max_text_width, subtitle_width)
        
        box_x1 = (width - max_text_width) / 2 - box_padding
        box_y1 = text_start_y - box_padding
        box_x2 = (width + max_text_width) / 2 + box_padding
        box_y2 = text_start_y + total_text_height + box_padding
        
        # 半透明の背景ボックスを描画
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # 角丸の背景ボックス
        overlay_draw.rounded_rectangle([box_x1, box_y1, box_x2, box_y2], 
                                     radius=15, fill=(255, 255, 255, 200))
        
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # タイトルテキストを描画
        current_y = text_start_y
        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            text_x = (width - text_width) / 2
            
            # テキストに軽い影を追加（読みやすさ向上）
            draw.text((text_x + 1, current_y + 1), line, fill='#888888', font=title_font)
            # メインテキスト
            draw.text((text_x, current_y), line, fill=colors['text_dark'], font=title_font)
            
            current_y += line_height
        
        # サブタイトル描画
        subtitle_x = (width - subtitle_width) / 2
        subtitle_y = current_y + 20
        
        # サブタイトル背景（アクセントカラー）
        subtitle_bg_padding = 10
        draw.rounded_rectangle([subtitle_x - subtitle_bg_padding, subtitle_y - 5,
                              subtitle_x + subtitle_width + subtitle_bg_padding, 
                              subtitle_y + subtitle_font_size + 10], 
                             radius=8, fill=colors['accent'])
        
        draw.text((subtitle_x, subtitle_y), subtitle, fill=colors['text_light'], font=subtitle_font)
        
        # イヤホンアイコンを描画（簡単な表現）
        headphone_x = 80
        headphone_y = height - 120
        headphone_size = 40
        
        # ヘッドフォンの左側
        draw.ellipse([headphone_x - headphone_size//2, headphone_y - headphone_size//2,
                     headphone_x + headphone_size//2, headphone_y + headphone_size//2], 
                    fill=colors['primary'], outline=colors['secondary'], width=2)
        
        # ヘッドフォンの右側
        draw.ellipse([headphone_x + 60, headphone_y - headphone_size//2,
                     headphone_x + 60 + headphone_size, headphone_y + headphone_size//2], 
                    fill=colors['primary'], outline=colors['secondary'], width=2)
        
        # ヘッドバンド
        draw.arc([headphone_x - 10, headphone_y - 60,
                 headphone_x + 90, headphone_y - 10], 
                start=0, end=180, fill=colors['secondary'], width=4)
        
        # ブランド情報
        brand_text = "muffin-blog.com"
        brand_font_size = max(subtitle_font_size // 2, 16)
        
        brand_font = None
        for font_path in font_paths:
            try:
                brand_font = ImageFont.truetype(font_path, brand_font_size)
                break
            except (OSError, IOError):
                continue
        
        if brand_font is None:
            brand_font = ImageFont.load_default()
        
        brand_bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
        brand_width = brand_bbox[2] - brand_bbox[0]
        brand_x = width - brand_width - 30
        brand_y = height - 40
        
        draw.text((brand_x, brand_y), brand_text, fill=colors['secondary'], font=brand_font)
        
        # 「Audible」ロゴ風テキスト（小さく）
        audible_text = "Audible"
        audible_font_size = brand_font_size + 4
        audible_font = None
        
        for font_path in font_paths:
            try:
                audible_font = ImageFont.truetype(font_path, audible_font_size)
                break
            except (OSError, IOError):
                continue
        
        if audible_font is None:
            audible_font = brand_font
        
        audible_x = 30
        audible_y = height - 80
        draw.text((audible_x, audible_y), audible_text, fill=colors['primary'], font=audible_font)
        
        # 画像保存
        save_path = os.path.join(self.save_directory, filename)
        img.save(save_path, 'PNG', quality=95)
        
        print(f"✅ Audibleアイキャッチ画像作成完了: {save_path}")
        return save_path

def main():
    """メイン実行関数"""
    
    generator = AudibleEyecatchGenerator()
    
    # 指定された仕様で画像生成
    image_path = generator.create_audible_eyecatch(
        title="読書苦手でも大丈夫！聴く読書で解決",
        subtitle="30日無料体験",
        filename="audible_読書苦手_アイキャッチ_20250808.png",
        width=1200,
        height=630
    )
    
    print(f"🎨 アイキャッチ画像が作成されました: {image_path}")
    print(f"📏 サイズ: 1200x630px (SNS最適化)")
    print(f"🎯 alt属性用文章: 読書が苦手でも安心！Audibleなら聴く読書で解決できることを表現したアイキャッチ画像")
    
    return image_path

if __name__ == "__main__":
    main()