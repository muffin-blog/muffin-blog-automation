"""
改良版Unsplash画像システム
記事テーマに最適化されたSEOフレンドリーなアイキャッチ画像生成
WordPress統合対応
"""

import os
import sys
import requests
import json
from typing import Optional, Dict, List
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import io
import base64
from datetime import datetime

# パス追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class EnhancedUnsplashSystem:
    """改良版Unsplash画像生成・WordPress統合システム"""
    
    def __init__(self, unsplash_access_key: str = None):
        # Unsplash API設定
        self.access_key = unsplash_access_key or "YOUR_UNSPLASH_ACCESS_KEY_HERE" 
        self.base_url = "https://api.unsplash.com"
        self.headers = {
            'Authorization': f'Client-ID {self.access_key}',
            'Accept-Version': 'v1'
        }
        
        # 画像最適化設定
        self.optimal_sizes = {
            "wordpress_featured": (1200, 630),  # WordPress推奨アイキャッチサイズ
            "og_image": (1200, 630),            # OGP画像サイズ
            "thumbnail": (300, 157)             # サムネイルサイズ
        }
        
        # WordPress統合用
        self.wordpress_api = None
    
    def search_optimized_images(self, main_keyword: str, sub_keywords: List[str] = None) -> List[Dict]:
        """記事キーワードに基づく最適画像検索"""
        
        print(f"🖼️ 画像検索開始: {main_keyword}")
        
        # 検索クエリ最適化
        search_queries = self.build_search_queries(main_keyword, sub_keywords or [])
        
        all_images = []
        
        for query in search_queries:
            try:
                params = {
                    'query': query,
                    'orientation': 'landscape',
                    'per_page': 20,
                    'order_by': 'relevance'
                }
                
                response = requests.get(
                    f"{self.base_url}/search/photos", 
                    headers=self.headers, 
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    images = data.get('results', [])
                    
                    # 画像品質フィルタリング
                    filtered_images = self.filter_high_quality_images(images)
                    all_images.extend(filtered_images)
                    
                    print(f"   📸 '{query}': {len(filtered_images)}枚取得")
                    
                else:
                    print(f"   ❌ 検索エラー ({query}): {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ 検索例外 ({query}): {e}")
                continue
        
        # 重複除去・スコアリング
        unique_images = self.deduplicate_and_score(all_images, main_keyword)
        
        print(f"✅ 最適化された画像: {len(unique_images)}枚")
        return unique_images[:10]  # トップ10を返す
    
    def build_search_queries(self, main_keyword: str, sub_keywords: List[str]) -> List[str]:
        """検索クエリ構築"""
        queries = []
        
        # メインキーワードベース
        if "audiobook" in main_keyword.lower():
            queries.extend([
                "audiobook headphones reading",
                "podcast listening music",
                "audio book technology", 
                "headphones smartphone reading"
            ])
        elif "audible" in main_keyword.lower():
            queries.extend([
                "audible listening headphones",
                "audiobook technology smartphone",
                "podcast audio reading"
            ])
        elif "kindle" in main_keyword.lower():
            queries.extend([
                "kindle e-reader book",
                "digital reading tablet",
                "e-book technology reading"
            ])
        
        # 一般的なフォールバック
        if not queries:
            queries.extend([
                f"{main_keyword} technology",
                f"{main_keyword} digital",
                "reading technology modern",
                "digital lifestyle modern"
            ])
        
        return queries
    
    def filter_high_quality_images(self, images: List[Dict]) -> List[Dict]:
        """高品質画像フィルタリング"""
        filtered = []
        
        for img in images:
            # 品質チェック条件
            width = img.get('width', 0)
            height = img.get('height', 0)
            likes = img.get('likes', 0)
            downloads = img.get('downloads', 0)
            
            # フィルタリング条件
            if (width >= 1200 and 
                height >= 600 and 
                likes >= 10 and
                'premium' not in img.get('tags', []) and
                self.is_suitable_content(img)):
                
                filtered.append(img)
        
        return filtered
    
    def is_suitable_content(self, image: Dict) -> bool:
        """画像内容の適合性チェック"""
        description = image.get('alt_description', '').lower()
        tags = [tag.get('title', '').lower() for tag in image.get('tags', [])]
        
        # 不適切なコンテンツ除外
        unsuitable_terms = ['nsfw', 'adult', 'violence', 'politics']
        content_text = description + ' ' + ' '.join(tags)
        
        return not any(term in content_text for term in unsuitable_terms)
    
    def deduplicate_and_score(self, images: List[Dict], main_keyword: str) -> List[Dict]:
        """重複除去とスコアリング"""
        seen_ids = set()
        scored_images = []
        
        for img in images:
            img_id = img.get('id')
            if img_id in seen_ids:
                continue
            seen_ids.add(img_id)
            
            # スコア計算
            score = self.calculate_image_score(img, main_keyword)
            img['relevance_score'] = score
            scored_images.append(img)
        
        # スコア順でソート
        return sorted(scored_images, key=lambda x: x['relevance_score'], reverse=True)
    
    def calculate_image_score(self, image: Dict, main_keyword: str) -> float:
        """画像関連性スコア計算"""
        score = 0.0
        
        # 基本品質スコア
        likes = image.get('likes', 0)
        downloads = image.get('downloads', 0)
        score += min(likes / 100, 1.0) * 30  # いいね数（最大30点）
        score += min(downloads / 1000, 1.0) * 20  # ダウンロード数（最大20点）
        
        # サイズ適合性
        width = image.get('width', 0)
        height = image.get('height', 0)
        aspect_ratio = width / height if height > 0 else 0
        
        if 1.8 <= aspect_ratio <= 2.0:  # WordPress推奨比率
            score += 25
        elif 1.5 <= aspect_ratio <= 2.2:
            score += 15
        
        # キーワード関連性
        description = image.get('alt_description', '').lower()
        tags = [tag.get('title', '').lower() for tag in image.get('tags', [])]
        content = description + ' ' + ' '.join(tags)
        
        keyword_variants = [main_keyword.lower(), 'audio', 'book', 'read', 'tech', 'digital']
        for variant in keyword_variants:
            if variant in content:
                score += 5
        
        return min(score, 100.0)  # 最大100点
    
    def download_and_optimize_image(self, image_data: Dict, keyword: str) -> Dict:
        """画像ダウンロード・最適化"""
        
        print(f"📥 画像最適化開始: {image_data.get('id', 'unknown')}")
        
        try:
            # 画像ダウンロード
            image_url = image_data['urls']['regular']  # 高品質だがファイルサイズ適度
            response = requests.get(image_url)
            response.raise_for_status()
            
            # PIL Image作成
            img = Image.open(io.BytesIO(response.content))
            img = img.convert('RGB')  # JPEG互換性確保
            
            # WordPress推奨サイズに最適化
            optimized_img = self.resize_for_wordpress(img)
            
            # SEO最適化ファイル名生成
            filename = self.generate_seo_filename(keyword, image_data.get('id', ''))
            
            # 画像をバイト配列で保存
            img_buffer = io.BytesIO()
            optimized_img.save(img_buffer, format='JPEG', quality=85, optimize=True)
            img_buffer.seek(0)
            
            print(f"✅ 画像最適化完了: {filename}")
            
            return {
                'success': True,
                'filename': filename,
                'image_data': img_buffer.getvalue(),
                'alt_text': self.generate_alt_text(keyword, image_data),
                'caption': image_data.get('alt_description', ''),
                'photographer': image_data.get('user', {}).get('name', ''),
                'unsplash_url': image_data.get('links', {}).get('html', ''),
                'size': len(img_buffer.getvalue())
            }
            
        except Exception as e:
            print(f"❌ 画像処理エラー: {e}")
            return {'success': False, 'error': str(e)}
    
    def resize_for_wordpress(self, img: Image.Image) -> Image.Image:
        """WordPress推奨サイズにリサイズ"""
        target_size = self.optimal_sizes['wordpress_featured']
        
        # アスペクト比を保持してリサイズ
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # 背景色で不足分を補完（必要に応じて）
        if img.size != target_size:
            background = Image.new('RGB', target_size, (245, 245, 245))
            x = (target_size[0] - img.width) // 2
            y = (target_size[1] - img.height) // 2
            background.paste(img, (x, y))
            img = background
        
        return img
    
    def generate_seo_filename(self, keyword: str, image_id: str) -> str:
        """SEO最適化ファイル名生成"""
        # キーワードを安全なファイル名に変換
        safe_keyword = keyword.replace(' ', '-').replace('.', '').lower()
        safe_keyword = ''.join(c for c in safe_keyword if c.isalnum() or c == '-')
        
        timestamp = datetime.now().strftime("%Y%m%d")
        return f"{safe_keyword}-{timestamp}-{image_id[:8]}.jpg"
    
    def generate_alt_text(self, keyword: str, image_data: Dict) -> str:
        """SEO最適化alt属性生成"""
        description = image_data.get('alt_description', '')
        
        if description:
            # 既存の説明にキーワードを組み込み
            if keyword.lower() not in description.lower():
                alt_text = f"{keyword}に関する{description}"
            else:
                alt_text = description
        else:
            # デフォルトalt属性
            alt_text = f"{keyword}についてのイメージ画像"
        
        # 長すぎる場合は短縮
        return alt_text[:125] if len(alt_text) > 125 else alt_text
    
    def upload_to_wordpress_media(self, optimized_image: Dict, wordpress_api) -> Optional[int]:
        """WordPress メディアライブラリにアップロード"""
        
        if not optimized_image['success']:
            return None
        
        try:
            # WordPress Media API エンドポイント
            media_url = f"{wordpress_api.api_url}/media"
            
            # ファイルデータ準備
            files = {
                'file': (
                    optimized_image['filename'],
                    optimized_image['image_data'],
                    'image/jpeg'
                )
            }
            
            # メタデータ
            data = {
                'alt_text': optimized_image['alt_text'],
                'caption': optimized_image.get('caption', ''),
                'title': optimized_image['filename'].replace('-', ' ').replace('.jpg', '')
            }
            
            # アップロード実行
            response = requests.post(
                media_url,
                headers={'Authorization': wordpress_api.headers['Authorization']},
                files=files,
                data=data
            )
            
            if response.status_code in [200, 201]:
                media_data = response.json()
                media_id = media_data['id']
                
                print(f"✅ WordPress画像アップロード完了: ID {media_id}")
                return media_id
            else:
                print(f"❌ 画像アップロードエラー: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 画像アップロード例外: {e}")
            return None
    
    def set_post_featured_image(self, post_id: int, media_id: int, wordpress_api) -> bool:
        """投稿にアイキャッチ画像設定"""
        
        try:
            update_url = f"{wordpress_api.api_url}/posts/{post_id}"
            data = {'featured_media': media_id}
            
            response = requests.post(
                update_url,
                headers=wordpress_api.headers,
                json=data
            )
            
            if response.status_code == 200:
                print(f"✅ アイキャッチ画像設定完了: 投稿ID {post_id}, メディアID {media_id}")
                return True
            else:
                print(f"❌ アイキャッチ設定エラー: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ アイキャッチ設定例外: {e}")
            return False
    
    def process_article_featured_image(self, main_keyword: str, sub_keywords: List[str], 
                                     post_id: int, wordpress_api) -> Dict:
        """記事用アイキャッチ画像の完全処理"""
        
        print(f"🖼️ アイキャッチ画像処理開始: {main_keyword}")
        
        # 1. 最適画像検索
        candidate_images = self.search_optimized_images(main_keyword, sub_keywords)
        
        if not candidate_images:
            return {'success': False, 'reason': 'No suitable images found'}
        
        # 2. ベスト画像選択
        best_image = candidate_images[0]  # スコア最高の画像
        
        # 3. 画像ダウンロード・最適化
        optimized_image = self.download_and_optimize_image(best_image, main_keyword)
        
        if not optimized_image['success']:
            return {'success': False, 'reason': 'Image optimization failed'}
        
        # 4. WordPress アップロード
        media_id = self.upload_to_wordpress_media(optimized_image, wordpress_api)
        
        if not media_id:
            return {'success': False, 'reason': 'WordPress upload failed'}
        
        # 5. アイキャッチ画像設定
        featured_set = self.set_post_featured_image(post_id, media_id, wordpress_api)
        
        if not featured_set:
            return {'success': False, 'reason': 'Featured image setting failed'}
        
        print(f"🎉 アイキャッチ画像処理完了!")
        
        return {
            'success': True,
            'media_id': media_id,
            'filename': optimized_image['filename'],
            'alt_text': optimized_image['alt_text'],
            'photographer': optimized_image['photographer'],
            'unsplash_url': optimized_image['unsplash_url']
        }

# 使用例とテスト
if __name__ == "__main__":
    # システムテスト
    enhanced_unsplash = EnhancedUnsplashSystem()
    
    # テスト検索
    test_keyword = "audiobook.jp"
    test_sub_keywords = ["audible", "comparison", "guide"]
    
    images = enhanced_unsplash.search_optimized_images(test_keyword, test_sub_keywords)
    
    print(f"\n🧪 テスト結果: {len(images)}枚の画像を取得")
    
    if images:
        # 最高スコア画像の詳細表示
        best_image = images[0]
        print(f"🏆 ベスト画像:")
        print(f"   ID: {best_image.get('id')}")
        print(f"   スコア: {best_image.get('relevance_score', 0):.1f}")
        print(f"   サイズ: {best_image.get('width')}x{best_image.get('height')}")
        print(f"   説明: {best_image.get('alt_description', 'N/A')}")
        
        # 画像最適化テスト
        optimized = enhanced_unsplash.download_and_optimize_image(best_image, test_keyword)
        
        if optimized['success']:
            print(f"✅ 画像最適化成功: {optimized['filename']} ({optimized['size']} bytes)")
        else:
            print(f"❌ 画像最適化失敗: {optimized['error']}")