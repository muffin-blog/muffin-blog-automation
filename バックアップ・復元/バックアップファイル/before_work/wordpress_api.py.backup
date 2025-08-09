"""
WordPress REST API接続とブログ記事投稿の自動化スクリプト
Claude主導のブログ自動化システム
"""

import requests
import json
import base64
from datetime import datetime
from typing import Dict, List, Optional
import os

class WordPressBlogAutomator:
    """WordPress REST APIを使用したブログ記事自動投稿システム"""
    
    def __init__(self, site_url: str, username: str, password: str):
        """
        初期化
        
        Args:
            site_url: WordPressサイトのURL (例: https://muffin-blog.com)
            username: WordPress管理者ユーザー名
            password: WordPressアプリケーションパスワード
        """
        self.site_url = site_url.rstrip('/')
        self.api_url = f"{self.site_url}/wp-json/wp/v2"
        self.username = username
        self.password = password
        
        # 認証情報をBase64エンコード
        credentials = f"{username}:{password}"
        self.auth_header = base64.b64encode(credentials.encode()).decode()
        
        self.headers = {
            'Authorization': f'Basic {self.auth_header}',
            'Content-Type': 'application/json'
        }
    
    def test_connection(self) -> bool:
        """API接続をテストする"""
        try:
            response = requests.get(f"{self.api_url}/users/me", headers=self.headers)
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ API接続成功: {user_data.get('name', 'Unknown')} として認証")
                return True
            else:
                print(f"❌ API接続失敗: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ 接続エラー: {e}")
            return False
    
    def get_categories(self) -> List[Dict]:
        """既存のカテゴリ一覧を取得"""
        try:
            response = requests.get(f"{self.api_url}/categories", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"カテゴリ取得失敗: {response.status_code}")
                return []
        except Exception as e:
            print(f"カテゴリ取得エラー: {e}")
            return []
    
    def get_tags(self) -> List[Dict]:
        """既存のタグ一覧を取得"""
        try:
            response = requests.get(f"{self.api_url}/tags", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"タグ取得失敗: {response.status_code}")
                return []
        except Exception as e:
            print(f"タグ取得エラー: {e}")
            return []
    
    def find_or_create_category(self, category_name: str) -> int:
        """カテゴリを検索、存在しなければ作成"""
        categories = self.get_categories()
        
        # 既存カテゴリを検索
        for cat in categories:
            if cat['name'].lower() == category_name.lower():
                return cat['id']
        
        # 新規カテゴリ作成
        data = {'name': category_name}
        try:
            response = requests.post(f"{self.api_url}/categories", 
                                   headers=self.headers, 
                                   json=data)
            if response.status_code == 201:
                new_category = response.json()
                print(f"✅ 新規カテゴリ作成: {category_name}")
                return new_category['id']
            else:
                print(f"カテゴリ作成失敗: {response.status_code}")
                return 1  # デフォルトカテゴリ
        except Exception as e:
            print(f"カテゴリ作成エラー: {e}")
            return 1
    
    def find_or_create_tags(self, tag_names: List[str]) -> List[int]:
        """タグを検索、存在しなければ作成"""
        existing_tags = self.get_tags()
        tag_ids = []
        
        for tag_name in tag_names:
            # 既存タグを検索
            found = False
            for tag in existing_tags:
                if tag['name'].lower() == tag_name.lower():
                    tag_ids.append(tag['id'])
                    found = True
                    break
            
            # 新規タグ作成
            if not found:
                data = {'name': tag_name}
                try:
                    response = requests.post(f"{self.api_url}/tags", 
                                           headers=self.headers, 
                                           json=data)
                    if response.status_code == 201:
                        new_tag = response.json()
                        tag_ids.append(new_tag['id'])
                        print(f"✅ 新規タグ作成: {tag_name}")
                    else:
                        print(f"タグ作成失敗: {tag_name}")
                except Exception as e:
                    print(f"タグ作成エラー: {e}")
        
        return tag_ids
    
    def upload_featured_image(self, image_path: str, alt_text: str = "") -> Optional[int]:
        """アイキャッチ画像をアップロード"""
        if not os.path.exists(image_path):
            print(f"画像ファイルが見つかりません: {image_path}")
            return None
        
        try:
            with open(image_path, 'rb') as img_file:
                files = {'file': img_file}
                headers = {'Authorization': f'Basic {self.auth_header}'}
                
                response = requests.post(f"{self.api_url}/media", 
                                       headers=headers, 
                                       files=files)
                
                if response.status_code == 201:
                    media_data = response.json()
                    media_id = media_data['id']
                    
                    # alt属性を設定
                    if alt_text:
                        update_data = {'alt_text': alt_text}
                        requests.post(f"{self.api_url}/media/{media_id}", 
                                    headers=self.headers, 
                                    json=update_data)
                    
                    print(f"✅ 画像アップロード成功: ID {media_id}")
                    return media_id
                else:
                    print(f"画像アップロード失敗: {response.status_code}")
                    return None
        except Exception as e:
            print(f"画像アップロードエラー: {e}")
            return None
    
    def create_post(self, 
                   title: str, 
                   content: str, 
                   category: str = "未分類",
                   tags: List[str] = None,
                   meta_description: str = "",
                   featured_image_path: str = "",
                   status: str = "draft",
                   schedule_date: Optional[str] = None) -> Optional[Dict]:
        """
        記事を作成・投稿
        
        Args:
            title: 記事タイトル
            content: 記事本文（HTML形式）
            category: カテゴリ名
            tags: タグのリスト
            meta_description: SEO用メタディスクリプション
            featured_image_path: アイキャッチ画像のパス
            status: 記事ステータス ('draft', 'publish', 'future')
            schedule_date: 予約投稿日時 (ISO形式: '2025-08-10T09:00:00')
        
        Returns:
            投稿データ、失敗時はNone
        """
        if tags is None:
            tags = []
        
        # カテゴリとタグのIDを取得
        category_id = self.find_or_create_category(category)
        tag_ids = self.find_or_create_tags(tags)
        
        # アイキャッチ画像のアップロード
        featured_media_id = None
        if featured_image_path:
            featured_media_id = self.upload_featured_image(featured_image_path, title)
        
        # 投稿データ作成
        post_data = {
            'title': title,
            'content': content,
            'categories': [category_id],
            'tags': tag_ids,
            'status': status,
            'meta': {
                'description': meta_description
            }
        }
        
        # アイキャッチ画像設定
        if featured_media_id:
            post_data['featured_media'] = featured_media_id
        
        # 予約投稿設定
        if schedule_date and status == 'future':
            post_data['date'] = schedule_date
        
        try:
            response = requests.post(f"{self.api_url}/posts", 
                                   headers=self.headers, 
                                   json=post_data)
            
            if response.status_code == 201:
                post_info = response.json()
                print(f"✅ 記事投稿成功: {title}")
                print(f"   URL: {post_info['link']}")
                print(f"   ID: {post_info['id']}")
                return post_info
            else:
                print(f"❌ 記事投稿失敗: {response.status_code}")
                print(f"   エラー: {response.text}")
                return None
        except Exception as e:
            print(f"❌ 記事投稿エラー: {e}")
            return None
    
    def test_post_creation(self):
        """テスト投稿を作成"""
        test_content = """
        <h2>Claude自動化システムのテスト記事</h2>
        <p>この記事はClaude主導のブログ自動化システムによって自動生成・投稿されました。</p>
        <p>システムが正常に動作していることを確認するためのテスト投稿です。</p>
        
        <h3>自動化機能</h3>
        <ul>
            <li>記事の自動作成</li>
            <li>WordPress REST APIでの投稿</li>
            <li>カテゴリ・タグの自動設定</li>
            <li>SEO最適化</li>
        </ul>
        
        <p>このテストが成功すれば、本格的なブログ自動化が開始できます！</p>
        """
        
        return self.create_post(
            title="【テスト】Claude自動化システム動作確認",
            content=test_content,
            category="テスト",
            tags=["Claude", "自動化", "テスト"],
            meta_description="Claude主導のブログ自動化システムの動作確認用テスト記事です。",
            status="draft"  # 下書きとして保存
        )

# 使用例
if __name__ == "__main__":
    # 設定情報（実際の値は環境変数や設定ファイルから読み込み）
    SITE_URL = "https://muffin-blog.com"
    USERNAME = "muffin1203"  # WordPress管理者ユーザー名
    PASSWORD = "TMLy Z4Wi RhPu oVLm 0lcO gZdi"  # WordPressアプリケーションパスワード
    
    # 自動化システムの初期化
    blog_automator = WordPressBlogAutomator(SITE_URL, USERNAME, PASSWORD)
    
    # 接続テスト
    if blog_automator.test_connection():
        print("🚀 WordPress API接続成功！")
        
        # テスト投稿作成
        print("🚀 テスト投稿を開始します...")
        test_result = blog_automator.test_post_creation()
        if test_result:
            print("✅ テスト投稿完了！WordPressの下書きを確認してください。")
            print(f"記事URL: {test_result['link']}")
        else:
            print("❌ テスト投稿失敗")
    else:
        print("❌ WordPress API接続失敗")