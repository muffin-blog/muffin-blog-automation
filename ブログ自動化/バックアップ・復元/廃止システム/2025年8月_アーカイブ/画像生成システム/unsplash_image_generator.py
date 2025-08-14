"""
Unsplash APIを使用した高品質ブログ画像生成システム
無料で高品質な画像を取得し、タイトルテキストを合成
"""

import requests
import json
import os
from typing import Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import io
import time

class UnsplashImageGenerator:
    """Unsplash APIを使用した画像生成システム"""
    
    def __init__(self, access_key: str = None):
        # Unsplash API設定（無料プラン: 5000リクエスト/月）
        self.access_key = access_key or "YOUR_UNSPLASH_ACCESS_KEY"
        self.base_url = "https://api.unsplash.com"
        self.headers = {
            'Authorization': f'Client-ID {self.access_key}',
            'Accept-Version': 'v1'
        }
    
    def search_images(self, query: str, orientation: str = "landscape") -> list:
        """キーワードで画像を検索"""
        try:
            params = {
                'query': query,
                'orientation': orientation,
                'per_page': 10,
                'order_by': 'relevant'
            }
            
            response = requests.get(f"{self.base_url}/search/photos", 
                                  headers=self.headers, 
                                  params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('results', [])
            else:
                print(f"❌ 画像検索エラー: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ 検索エラー: {e}")
            return []
    
    def download_image(self, image_url: str) -> Optional[Image.Image]:
        """画像をダウンロード"""
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                return Image.open(io.BytesIO(response.content))
            return None
        except Exception as e:
            print(f"❌ 画像ダウンロードエラー: {e}")
            return None
    
    def add_text_overlay(self, image: Image.Image, title: str, theme: str = "blog") -> Image.Image:
        """画像にテキストオーバーレイを追加"""
        
        # 画像をリサイズ
        target_size = (1920, 1080)
        image = image.resize(target_size, Image.Resampling.LANCZOS)
        
        # テーマ別カラー設定
        theme_colors = {
            'audible': {'primary': '#FF9500', 'secondary': '#FFFFFF', 'bg': (0, 0, 0, 120)},
            'learning': {'primary': '#4285F4', 'secondary': '#FFFFFF', 'bg': (0, 0, 0, 120)},
            'money': {'primary': '#10B981', 'secondary': '#FFFFFF', 'bg': (0, 0, 0, 120)},
            'productivity': {'primary': '#8B5CF6', 'secondary': '#FFFFFF', 'bg': (0, 0, 0, 120)},
            'default': {'primary': '#2563EB', 'secondary': '#FFFFFF', 'bg': (0, 0, 0, 120)}
        }
        
        colors = theme_colors.get(theme.lower(), theme_colors['default'])
        
        # オーバーレイ作成
        overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # 半透明の背景ボックス
        box_height = 300
        box_y = (image.height - box_height) // 2
        draw.rectangle([0, box_y, image.width, box_y + box_height], 
                      fill=colors['bg'])
        
        # フォント設定
        try:
            title_font_size = 72
            subtitle_font_size = 36
            
            font_paths = [
                "/System/Library/Fonts/Arial.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "/System/Library/Fonts/Times.ttc"
            ]
            
            title_font = None
            for font_path in font_paths:
                try:
                    title_font = ImageFont.truetype(font_path, title_font_size)
                    subtitle_font = ImageFont.truetype(font_path, subtitle_font_size)
                    break
                except:
                    continue
            
            if title_font is None:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # テキストを分割
        import textwrap
        lines = textwrap.wrap(title, width=25)
        
        # テキストを中央に配置
        total_text_height = len(lines) * title_font_size * 1.2
        y_start = box_y + (box_height - total_text_height) // 2
        
        # タイトルテキストを描画
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (image.width - text_width) // 2
            y = y_start + i * title_font_size * 1.2
            
            # 影効果
            draw.text((x + 2, y + 2), line, fill=(0, 0, 0, 150), font=title_font)
            # メインテキスト
            draw.text((x, y), line, fill=colors['secondary'], font=title_font)
        
        # サブタイトル
        subtitle = f"💡 {theme.upper()} TIPS"
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        subtitle_width = bbox[2] - bbox[0]
        subtitle_x = (image.width - subtitle_width) // 2
        subtitle_y = y_start + total_text_height + 20
        
        draw.text((subtitle_x + 1, subtitle_y + 1), subtitle, fill=(0, 0, 0, 150), font=subtitle_font)
        draw.text((subtitle_x, subtitle_y), subtitle, fill=colors['primary'], font=subtitle_font)
        
        # ブランド情報
        brand_text = "muffin-blog.com"
        brand_font_size = 24
        try:
            brand_font = ImageFont.truetype(font_paths[0], brand_font_size)
        except:
            brand_font = ImageFont.load_default()
        
        brand_bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
        brand_width = brand_bbox[2] - brand_bbox[0]
        brand_x = image.width - brand_width - 40
        brand_y = image.height - 60
        
        draw.text((brand_x, brand_y), brand_text, fill=colors['primary'], font=brand_font)
        
        # オーバーレイを元画像に合成
        result = Image.alpha_composite(image.convert('RGBA'), overlay)
        return result.convert('RGB')
    
    def create_blog_image(self, title: str, theme: str = "blog", keywords: list = None) -> Optional[str]:
        """ブログ画像を作成"""
        
        print(f"🎨 Unsplash画像生成開始: {title}")
        
        # キーワード生成
        if not keywords:
            theme_keywords = {
                'audible': ['audio', 'books', 'reading', 'learning'],
                'learning': ['education', 'study', 'knowledge', 'growth'],
                'money': ['finance', 'investment', 'business', 'success'],
                'productivity': ['work', 'office', 'efficiency', 'technology'],
                'default': ['business', 'technology', 'modern', 'professional']
            }
            keywords = theme_keywords.get(theme.lower(), theme_keywords['default'])
        
        # 複数キーワードで検索
        best_image = None
        for keyword in keywords:
            print(f"🔍 '{keyword}' で画像検索中...")
            images = self.search_images(keyword)
            
            if images:
                # 最初の画像を使用
                image_data = images[0]
                image_url = image_data['urls']['regular']  # 高解像度版
                
                # 画像をダウンロード
                downloaded_image = self.download_image(image_url)
                if downloaded_image:
                    best_image = downloaded_image
                    print(f"✅ 画像取得成功: {keyword}")
                    break
            
            time.sleep(0.5)  # API制限対策
        
        if not best_image:
            print("❌ 適切な画像が見つかりませんでした")
            return None
        
        # テキストオーバーレイを追加
        final_image = self.add_text_overlay(best_image, title, theme)
        
        # 画像を保存
        timestamp = int(time.time())
        filename = f"unsplash_blog_image_{timestamp}.png"
        save_path = os.path.join("images", filename)
        
        os.makedirs("images", exist_ok=True)
        final_image.save(save_path, quality=95)
        
        print(f"✅ Unsplash画像作成完了: {save_path}")
        return save_path

# テスト実行
if __name__ == "__main__":
    # テスト用（実際のAPIキーは https://unsplash.com/developers で取得）
    print("Unsplash API画像生成テスト")
    print("注意: 実際の使用には Unsplash API キーが必要です")
    print("https://unsplash.com/developers でアカウント作成してください")
    
    # APIキーなしでもテスト可能（デモ用）
    generator = UnsplashImageGenerator()
    
    # デモ画像作成（APIキーがないため失敗しますが、システムは動作します）
    result = generator.create_blog_image(
        title="Unsplash APIで美しい画像を生成",
        theme="productivity",
        keywords=["computer", "workspace", "modern"]
    )