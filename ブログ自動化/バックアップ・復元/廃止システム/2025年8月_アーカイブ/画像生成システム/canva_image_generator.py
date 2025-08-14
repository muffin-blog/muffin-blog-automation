"""
Canva API連携による自動画像生成システム
Claude主導のブログ自動化システム用
"""

import requests
import json
import os
from typing import Dict, List, Optional, Tuple
import tempfile
from urllib.parse import urlparse

class CanvaImageGenerator:
    """Canva APIを使用した自動画像生成システム"""
    
    def __init__(self, api_key: str):
        """
        初期化
        
        Args:
            api_key: Canva API キー
        """
        self.api_key = api_key
        self.base_url = "https://api.canva.com/rest/v1"
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def test_connection(self) -> bool:
        """Canva API接続をテストする"""
        try:
            response = requests.get(f"{self.base_url}/me", headers=self.headers)
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Canva API接続成功: {user_data.get('display_name', 'Unknown')}")
                return True
            else:
                print(f"❌ Canva API接続失敗: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Canva接続エラー: {e}")
            return False
    
    def get_design_templates(self, query: str = "", category: str = "blog") -> List[Dict]:
        """
        利用可能なデザインテンプレートを取得
        
        Args:
            query: 検索キーワード
            category: テンプレートカテゴリ
        
        Returns:
            テンプレートのリスト
        """
        params = {
            'query': query,
            'category': category,
            'limit': 20
        }
        
        try:
            response = requests.get(f"{self.base_url}/design-templates", 
                                  headers=self.headers, 
                                  params=params)
            if response.status_code == 200:
                return response.json().get('data', [])
            else:
                print(f"テンプレート取得失敗: {response.status_code}")
                return []
        except Exception as e:
            print(f"テンプレート取得エラー: {e}")
            return []
    
    def select_template_by_theme(self, article_theme: str) -> Optional[str]:
        """
        記事テーマに基づいて最適なテンプレートを選択
        
        Args:
            article_theme: 記事のテーマ（例：Audible、投資、学習など）
        
        Returns:
            選択されたテンプレートID
        """
        theme_keywords = {
            'audible': ['audio', 'music', 'learning', 'education'],
            'オーディオブック': ['audio', 'book', 'learning', 'education'],
            '投資': ['business', 'finance', 'money', 'investment'],
            'お金': ['business', 'finance', 'money'],
            '学習': ['education', 'learning', 'study'],
            '自己啓発': ['motivation', 'personal development', 'growth'],
            '習慣': ['lifestyle', 'habit', 'daily'],
            'デジタル': ['technology', 'digital', 'app'],
            'ツール': ['productivity', 'tool', 'app']
        }
        
        # テーマに対応するキーワードを取得
        keywords = []
        theme_lower = article_theme.lower()
        for key, values in theme_keywords.items():
            if key in theme_lower:
                keywords.extend(values)
                break
        
        if not keywords:
            keywords = ['blog', 'general']
        
        # 各キーワードでテンプレートを検索
        for keyword in keywords:
            templates = self.get_design_templates(query=keyword)
            if templates:
                # 最初に見つかったテンプレートを使用
                return templates[0].get('id')
        
        return None
    
    def create_design_from_template(self, 
                                  template_id: str, 
                                  title: str,
                                  subtitle: str = "",
                                  brand_colors: List[str] = None) -> Optional[str]:
        """
        テンプレートからデザインを作成
        
        Args:
            template_id: 使用するテンプレートのID
            title: メインタイトル
            subtitle: サブタイトル（オプション）
            brand_colors: ブランドカラー（HEXコード）
        
        Returns:
            作成されたデザインのID
        """
        if brand_colors is None:
            brand_colors = ['#2563eb', '#1d4ed8', '#1e40af']  # デフォルトブルー系
        
        design_data = {
            'template_id': template_id,
            'elements': [
                {
                    'type': 'text',
                    'content': title,
                    'style': {
                        'font_size': 'large',
                        'font_weight': 'bold',
                        'color': brand_colors[0]
                    }
                }
            ]
        }
        
        if subtitle:
            design_data['elements'].append({
                'type': 'text',
                'content': subtitle,
                'style': {
                    'font_size': 'medium',
                    'color': brand_colors[1]
                }
            })
        
        try:
            response = requests.post(f"{self.base_url}/designs", 
                                   headers=self.headers, 
                                   json=design_data)
            if response.status_code == 201:
                design = response.json()
                design_id = design.get('id')
                print(f"✅ デザイン作成成功: ID {design_id}")
                return design_id
            else:
                print(f"デザイン作成失敗: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"デザイン作成エラー: {e}")
            return None
    
    def export_design(self, design_id: str, format: str = "png", size: str = "1920x1080") -> Optional[str]:
        """
        デザインを画像としてエクスポート
        
        Args:
            design_id: デザインのID
            format: 出力フォーマット（png, jpg）
            size: 画像サイズ
        
        Returns:
            エクスポートされた画像のURL
        """
        export_data = {
            'format': format,
            'size': size,
            'quality': 'high'
        }
        
        try:
            response = requests.post(f"{self.base_url}/designs/{design_id}/export", 
                                   headers=self.headers, 
                                   json=export_data)
            if response.status_code == 200:
                export_info = response.json()
                image_url = export_info.get('url')
                print(f"✅ 画像エクスポート成功: {image_url}")
                return image_url
            else:
                print(f"画像エクスポート失敗: {response.status_code}")
                return None
        except Exception as e:
            print(f"画像エクスポートエラー: {e}")
            return None
    
    def download_image(self, image_url: str, save_path: str) -> bool:
        """
        画像をダウンロードして保存
        
        Args:
            image_url: 画像のURL
            save_path: 保存先のパス
        
        Returns:
            成功時True、失敗時False
        """
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ 画像保存成功: {save_path}")
                return True
            else:
                print(f"画像ダウンロード失敗: {response.status_code}")
                return False
        except Exception as e:
            print(f"画像ダウンロードエラー: {e}")
            return False
    
    def create_blog_image(self, 
                         title: str, 
                         theme: str = "blog",
                         subtitle: str = "",
                         save_directory: str = "images") -> Optional[str]:
        """
        ブログ記事用の画像を作成
        
        Args:
            title: 記事タイトル
            theme: 記事テーマ
            subtitle: サブタイトル
            save_directory: 画像保存ディレクトリ
        
        Returns:
            保存された画像のパス
        """
        # 保存ディレクトリを作成
        os.makedirs(save_directory, exist_ok=True)
        
        # テーマに基づいてテンプレート選択
        template_id = self.select_template_by_theme(theme)
        if not template_id:
            print(f"適切なテンプレートが見つかりませんでした: {theme}")
            return None
        
        # デザイン作成
        design_id = self.create_design_from_template(template_id, title, subtitle)
        if not design_id:
            print("デザイン作成に失敗しました")
            return None
        
        # 画像エクスポート
        image_url = self.export_design(design_id)
        if not image_url:
            print("画像エクスポートに失敗しました")
            return None
        
        # 画像ダウンロード・保存
        timestamp = int(time.time())
        filename = f"blog_image_{timestamp}.png"
        save_path = os.path.join(save_directory, filename)
        
        if self.download_image(image_url, save_path):
            return save_path
        else:
            return None
    
    def create_multiple_sizes(self, 
                             title: str, 
                             theme: str = "blog") -> Dict[str, Optional[str]]:
        """
        複数サイズの画像を作成（アイキャッチ、SNS用など）
        
        Args:
            title: 記事タイトル
            theme: 記事テーマ
        
        Returns:
            サイズ別の画像パス辞書
        """
        sizes = {
            'featured': '1920x1080',  # アイキャッチ用
            'social': '1200x630',     # SNS用
            'thumbnail': '400x400'    # サムネイル用
        }
        
        results = {}
        
        # テンプレート選択
        template_id = self.select_template_by_theme(theme)
        if not template_id:
            print(f"適切なテンプレートが見つかりませんでした: {theme}")
            return {size: None for size in sizes.keys()}
        
        # デザイン作成
        design_id = self.create_design_from_template(template_id, title)
        if not design_id:
            print("デザイン作成に失敗しました")
            return {size: None for size in sizes.keys()}
        
        # 各サイズで画像生成
        for size_name, dimensions in sizes.items():
            image_url = self.export_design(design_id, size=dimensions)
            if image_url:
                timestamp = int(time.time())
                filename = f"blog_{size_name}_{timestamp}.png"
                save_path = os.path.join("images", filename)
                
                os.makedirs("images", exist_ok=True)
                if self.download_image(image_url, save_path):
                    results[size_name] = save_path
                else:
                    results[size_name] = None
            else:
                results[size_name] = None
        
        return results

# テスト・デモ用のシンプルな画像生成クラス
class SimpleImageGenerator:
    """Canva APIが利用できない場合の代替画像生成"""
    
    @staticmethod
    def create_simple_image(title: str, 
                          theme: str = "blog", 
                          width: int = 1920, 
                          height: int = 1080) -> str:
        """
        プロフェッショナルなブログ画像を生成
        PIL（Pillow）を使用してより洗練されたデザイン
        """
        try:
            from PIL import Image, ImageDraw, ImageFont, ImageFilter
            import textwrap
            import time
        except ImportError:
            print("⚠️ Pillowが必要です: pip install Pillow")
            return ""
        
        # テーマ別カラーパレット
        theme_colors = {
            'audible': {
                'primary': '#FF9500',
                'secondary': '#1A1A1A', 
                'accent': '#FFB84D',
                'background': '#2B2B2B'
            },
            'learning': {
                'primary': '#4285F4',
                'secondary': '#1E88E5',
                'accent': '#90CAF9',
                'background': '#E3F2FD'
            },
            'money': {
                'primary': '#10B981',
                'secondary': '#059669',
                'accent': '#6EE7B7',
                'background': '#ECFDF5'
            },
            'productivity': {
                'primary': '#8B5CF6',
                'secondary': '#7C3AED',
                'accent': '#C4B5FD',
                'background': '#F5F3FF'
            },
            'default': {
                'primary': '#2563EB',
                'secondary': '#1D4ED8',
                'accent': '#93C5FD',
                'background': '#EFF6FF'
            }
        }
        
        colors = theme_colors.get(theme.lower(), theme_colors['default'])
        
        # グラデーション背景画像作成
        img = Image.new('RGB', (width, height), color=colors['background'])
        draw = ImageDraw.Draw(img)
        
        # グラデーション背景を描画
        for y in range(height):
            gradient_factor = y / height
            r1, g1, b1 = tuple(int(colors['primary'][i:i+2], 16) for i in (1, 3, 5))
            r2, g2, b2 = tuple(int(colors['secondary'][i:i+2], 16) for i in (1, 3, 5))
            
            r = int(r1 + (r2 - r1) * gradient_factor)
            g = int(g1 + (g2 - g1) * gradient_factor)
            b = int(b1 + (b2 - b1) * gradient_factor)
            
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # デコレーション要素（円や図形）
        circle_size = width // 15
        draw.ellipse([width - circle_size * 2, height // 10, 
                     width - circle_size // 2, height // 10 + circle_size], 
                    fill=colors['accent'])
        
        draw.ellipse([circle_size // 2, height - circle_size * 2, 
                     circle_size * 2, height - circle_size // 2], 
                    fill=colors['accent'])
        
        # フォント設定
        title_font_size = min(width, height) // 12
        subtitle_font_size = title_font_size // 2
        
        # 複数のフォントパスを試行
        font_paths = [
            "/System/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Times.ttc",
            "/Library/Fonts/Arial.ttf",
            "/usr/share/fonts/truetype/arial.ttf"  # Linux用
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
        
        # フォントが見つからない場合はデフォルトフォントを使用
        if title_font is None:
            print("⚠️ カスタムフォントが見つかりません。デフォルトフォントを使用します。")
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            # デフォルトフォントの場合はサイズを大きくする
            title_font_size = 60
            subtitle_font_size = 30
        
        # タイトルテキストを分割
        lines = textwrap.wrap(title, width=25)
        
        # 全体のテキスト高さを計算
        title_height = len(lines) * title_font_size * 1.2
        subtitle_height = subtitle_font_size * 1.5
        total_text_height = title_height + subtitle_height + 50
        
        # 開始Y位置
        y_start = (height - total_text_height) / 2
        
        # 背景ボックス（半透明）
        box_padding = 40
        box_x1 = width // 10
        box_y1 = y_start - box_padding
        box_x2 = width - width // 10
        box_y2 = y_start + total_text_height + box_padding
        
        # 半透明の背景ボックス
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rounded_rectangle([box_x1, box_y1, box_x2, box_y2], 
                                     radius=20, fill=(255, 255, 255, 180))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # タイトルテキストを描画
        current_y = y_start
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) / 2
            
            # テキストに影を追加
            draw.text((x + 2, current_y + 2), line, fill='#000000', font=title_font)
            draw.text((x, current_y), line, fill=colors['secondary'], font=title_font)
            current_y += title_font_size * 1.2
        
        # サブタイトル（テーマ名）を追加
        theme_text = f"💡 {theme.upper()} TIPS"
        bbox = draw.textbbox((0, 0), theme_text, font=subtitle_font)
        subtitle_width = bbox[2] - bbox[0]
        subtitle_x = (width - subtitle_width) / 2
        subtitle_y = current_y + 30
        
        draw.text((subtitle_x + 1, subtitle_y + 1), theme_text, fill='#000000', font=subtitle_font)
        draw.text((subtitle_x, subtitle_y), theme_text, fill=colors['primary'], font=subtitle_font)
        
        # ブランド情報を追加
        brand_text = "muffin-blog.com"
        brand_font_size = max(subtitle_font_size // 2, 20)  # 最小サイズを保証
        
        brand_font = None
        for font_path in font_paths:
            try:
                brand_font = ImageFont.truetype(font_path, brand_font_size)
                break
            except (OSError, IOError):
                continue
        
        if brand_font is None:
            brand_font = ImageFont.load_default()
            brand_font_size = 20
        
        brand_bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
        brand_width = brand_bbox[2] - brand_bbox[0]
        brand_x = width - brand_width - 40
        brand_y = height - 50
        
        draw.text((brand_x, brand_y), brand_text, fill=colors['accent'], font=brand_font)
        
        # 画像保存
        timestamp = int(time.time())
        filename = f"professional_blog_image_{timestamp}.png"
        save_path = os.path.join("images", filename)
        
        os.makedirs("images", exist_ok=True)
        img.save(save_path, quality=95)
        
        print(f"✅ プロフェッショナル画像作成完了: {save_path}")
        return save_path

# 使用例
if __name__ == "__main__":
    import time
    
    # Canva API設定（実際のAPIキーが必要）
    CANVA_API_KEY = "your_canva_api_key"
    
    # 簡易テスト（Canva APIキーがある場合）
    if CANVA_API_KEY != "your_canva_api_key":
        canva_gen = CanvaImageGenerator(CANVA_API_KEY)
        
        if canva_gen.test_connection():
            # テスト画像作成
            image_path = canva_gen.create_blog_image(
                title="Audibleで人生を変える読書術",
                theme="audible",
                subtitle="忙しい社会人のための効率的学習法"
            )
            print(f"作成された画像: {image_path}")
    else:
        # Canva APIが利用できない場合のフォールバック
        print("⚠️ Canva APIキーが設定されていません")
        print("シンプル画像生成を使用します...")
        
        simple_gen = SimpleImageGenerator()
        image_path = simple_gen.create_simple_image(
            title="Audibleで人生を変える読書術",
            theme="audible"
        )
        print(f"作成された画像: {image_path}")