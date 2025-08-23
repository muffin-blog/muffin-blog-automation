#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
記事自動追加システム - 完全版
WordPressから全データを自動取得し、ポートフォリオサイトに追加
"""

import json
import sys
import subprocess
import re
import requests
from datetime import datetime
from urllib.parse import urlparse

class ArticleAutoAdder:
    def __init__(self):
        self.articles_json_path = "public/content/articles/articles.json"
        
    def validate_url(self, url):
        """URLの検証とWordPressサイトかの確認"""
        try:
            # URLが有効か確認
            response = requests.head(url, allow_redirects=True, timeout=10)
            if response.status_code == 404:
                print(f"❌ エラー: URLが存在しません（404エラー）")
                return False
            elif response.status_code >= 400:
                print(f"❌ エラー: URLにアクセスできません（ステータス: {response.status_code}）")
                return False
            
            print(f"✅ URL検証成功: {url}")
            return True
            
        except requests.RequestException as e:
            print(f"❌ URLアクセスエラー: {e}")
            return False
    
    def get_wordpress_data(self, url):
        """WordPress REST APIからデータを取得"""
        try:
            # URLからドメインを抽出
            parsed = urlparse(url)
            domain = f"{parsed.scheme}://{parsed.netloc}"
            
            # スラッグを取得
            path = parsed.path.strip('/')
            slug = path.split('/')[-1] if path else None
            
            if not slug:
                print("⚠️ WordPress APIが使用できません。HTMLから取得します。")
                return self.get_data_from_html(url)
            
            print(f"📡 WordPress APIからデータ取得中...")
            
            # REST APIエンドポイント
            api_url = f"{domain}/wp-json/wp/v2/posts?slug={slug}"
            
            try:
                response = requests.get(api_url, timeout=10)
                if response.status_code == 200:
                    posts = response.json()
                    if posts and len(posts) > 0:
                        return self.parse_wordpress_post(posts[0], domain)
            except:
                pass
            
            # APIが使えない場合はHTMLから取得
            print("⚠️ WordPress APIが使用できません。HTMLから取得します。")
            return self.get_data_from_html(url)
            
        except Exception as e:
            print(f"⚠️ WordPress API取得失敗: {e}")
            return self.get_data_from_html(url)
    
    def parse_wordpress_post(self, post, domain):
        """WordPress投稿データを解析"""
        try:
            # タイトル（HTMLタグを除去）
            title = re.sub(r'<[^>]+>', '', post.get('title', {}).get('rendered', ''))
            
            # 説明文（Yoast SEOまたは抜粋）
            description = post.get('yoast_meta', {}).get('yoast_wpseo_metadesc', '')
            if not description:
                description = re.sub(r'<[^>]+>', '', post.get('excerpt', {}).get('rendered', ''))
            if not description:
                content = re.sub(r'<[^>]+>', '', post.get('content', {}).get('rendered', ''))
                description = content[:150] + '...' if len(content) > 150 else content
            
            # 日付
            date = post.get('date', '').split('T')[0]
            
            # アイキャッチ画像を取得
            thumbnail = None
            if post.get('featured_media'):
                try:
                    media_url = f"{domain}/wp-json/wp/v2/media/{post['featured_media']}"
                    media_response = requests.get(media_url, timeout=5)
                    if media_response.status_code == 200:
                        media_data = media_response.json()
                        thumbnail = media_data.get('source_url')
                        print(f"✅ アイキャッチ画像取得: {thumbnail}")
                except:
                    pass
            
            # カテゴリとタグを取得
            tags = []
            
            # カテゴリ取得
            if post.get('categories'):
                try:
                    cat_url = f"{domain}/wp-json/wp/v2/categories?include={','.join(map(str, post['categories']))}"
                    cat_response = requests.get(cat_url, timeout=5)
                    if cat_response.status_code == 200:
                        categories = cat_response.json()
                        for cat in categories:
                            tags.append(cat.get('name'))
                except:
                    pass
            
            # タグ取得
            if post.get('tags'):
                try:
                    tag_url = f"{domain}/wp-json/wp/v2/tags?include={','.join(map(str, post['tags']))}"
                    tag_response = requests.get(tag_url, timeout=5)
                    if tag_response.status_code == 200:
                        wp_tags = tag_response.json()
                        for tag in wp_tags:
                            tags.append(tag.get('name'))
                except:
                    pass
            
            # タグが空の場合、タイトルから生成
            if not tags:
                tags = self.generate_tags_from_title(title)
            
            print(f"✅ WordPress APIからデータ取得成功")
            print(f"   タイトル: {title}")
            print(f"   説明: {description[:50]}...")
            print(f"   タグ: {', '.join(tags)}")
            print(f"   画像: {'あり' if thumbnail else 'なし'}")
            
            return {
                "title": title,
                "description": description,
                "date": date,
                "tags": tags[:6],  # 最大6個
                "thumbnail": thumbnail
            }
            
        except Exception as e:
            print(f"❌ WordPress投稿解析エラー: {e}")
            return None
    
    def get_data_from_html(self, url):
        """HTMLから直接データを取得（フォールバック）"""
        try:
            print(f"📡 HTMLからデータ取得中...")
            
            response = requests.get(url, timeout=10)
            html = response.text
            
            # タイトル取得
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
            title = title_match.group(1) if title_match else ""
            if ' | ' in title:
                title = title.split(' | ')[0]
            
            # メタディスクリプション取得
            desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html, re.IGNORECASE)
            if not desc_match:
                desc_match = re.search(r'<meta\s+content="([^"]+)"\s+name="description"', html, re.IGNORECASE)
            description = desc_match.group(1) if desc_match else ""
            
            # OGP画像取得
            og_image_match = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html, re.IGNORECASE)
            if not og_image_match:
                og_image_match = re.search(r'<meta\s+content="([^"]+)"\s+property="og:image"', html, re.IGNORECASE)
            thumbnail = og_image_match.group(1) if og_image_match else None
            
            # 日付取得（複数パターン）
            date = datetime.now().strftime('%Y-%m-%d')
            date_patterns = [
                r'<time[^>]*datetime="(\d{4}-\d{2}-\d{2})',
                r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})',
                r'(\d{4}年\d{1,2}月\d{1,2}日)'
            ]
            for pattern in date_patterns:
                date_match = re.search(pattern, html)
                if date_match:
                    date_str = date_match.group(1)
                    if '年' in date_str:
                        # 日本語形式を変換
                        date_str = re.sub(r'(\d{4})年(\d{1,2})月(\d{1,2})日', r'\1-\2-\3', date_str)
                    date = date_str
                    break
            
            # タグ生成
            tags = self.generate_tags_from_title(title)
            
            print(f"✅ HTMLからデータ取得成功")
            print(f"   タイトル: {title}")
            print(f"   説明: {description[:50]}...")
            print(f"   タグ: {', '.join(tags)}")
            print(f"   画像: {'あり' if thumbnail else 'なし'}")
            
            return {
                "title": title,
                "description": description,
                "date": date,
                "tags": tags,
                "thumbnail": thumbnail
            }
            
        except Exception as e:
            print(f"❌ HTML解析エラー: {e}")
            return None
    
    def generate_tags_from_title(self, title):
        """タイトルからタグを生成"""
        tags = []
        
        # キーワードマッピング
        keyword_map = {
            'Audible': 'オーディオブック',
            'オーディブル': 'オーディオブック',
            '読書': '読書術',
            '集中': '集中力向上',
            'SEO': 'SEO',
            'AI': 'AI活用',
            '睡眠': '睡眠改善',
            '健康': '健康',
            'ブログ': 'ブログ運営',
            '投資': '投資',
            '節約': '節約術',
            'WordPress': 'WordPress'
        }
        
        for keyword, tag in keyword_map.items():
            if keyword.lower() in title.lower() and tag not in tags:
                tags.append(tag)
        
        # タグが少ない場合は汎用タグを追加
        if len(tags) < 2:
            tags.append("ライフハック")
        
        return tags[:6]
    
    def detect_article_type(self, url):
        """記事タイプを判定（ブログ or SEO）"""
        # マフィンブログのドメイン
        if 'muffin-blog.com' in url:
            return 'blogArticles'
        else:
            return 'seoArticles'
    
    def add_article(self, url):
        """記事を追加するメイン処理"""
        print(f"🎯 記事追加処理開始: {url}")
        print("-" * 50)
        
        # URL検証
        if not self.validate_url(url):
            return False
        
        # データ取得
        article_data = self.get_wordpress_data(url)
        if not article_data:
            print("❌ データ取得に失敗しました")
            return False
        
        # 記事タイプを判定
        article_type = self.detect_article_type(url)
        
        # 完全な記事データを構築
        article_data['url'] = url
        if article_type == 'seoArticles':
            article_data['client'] = self.extract_client_name(url)
        
        # デフォルト画像設定（画像がない場合）
        if not article_data.get('thumbnail'):
            article_data['thumbnail'] = '/assets/images/default-blog-thumbnail.jpg'
        
        print("-" * 50)
        
        # articles.json更新
        if not self.update_articles_json(article_data, article_type):
            return False
        
        # Git操作
        if not self.git_deploy():
            return False
        
        print("-" * 50)
        print("🎉 記事追加完了！")
        print(f"📱 サイト確認: https://muffin-portfolio-public.vercel.app")
        print("⏱️  Vercelデプロイまで1-2分お待ちください")
        
        return True
    
    def extract_client_name(self, url):
        """URLからクライアント名を推測"""
        domain = urlparse(url).netloc
        if 'minerva' in domain:
            return 'ミネルヴァスリープ'
        elif 'note.com' in domain:
            return 'note'
        else:
            return 'クライアント案件'
    
    def update_articles_json(self, article_data, article_type):
        """articles.jsonを更新"""
        try:
            print(f"📝 articles.json更新中...")
            
            # 既存データ読み込み
            with open(self.articles_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 重複チェック
            for existing in data[article_type]:
                if existing['url'] == article_data['url']:
                    print("⚠️  同じURLの記事が既に存在します")
                    return True
            
            # 新記事を先頭に追加
            data[article_type].insert(0, article_data)
            
            # 保存
            with open(self.articles_json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ articles.json更新完了（{article_type}に追加）")
            return True
            
        except Exception as e:
            print(f"❌ ファイル更新エラー: {e}")
            return False
    
    def git_deploy(self):
        """Git操作でデプロイ"""
        try:
            print("🚀 Gitデプロイ中...")
            
            # ステージング
            subprocess.run(['git', 'add', self.articles_json_path], check=True)
            
            # コミット
            commit_msg = f"記事追加: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            
            # プッシュ
            subprocess.run(['git', 'push', 'origin', 'master'], check=True)
            
            print("✅ Gitデプロイ完了")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git操作エラー: {e}")
            print("   （変更がない場合は正常です）")
            return True

def main():
    """メイン処理"""
    if len(sys.argv) != 2:
        print("❌ 使用方法: python3 add_article_auto.py [記事URL]")
        print("例: python3 add_article_auto.py https://muffin-blog.com/your-article/")
        return
    
    url = sys.argv[1]
    
    # ArticleAutoAdderインスタンス作成
    adder = ArticleAutoAdder()
    
    # 記事追加実行
    success = adder.add_article(url)
    
    if not success:
        print("❌ 記事追加に失敗しました")
        sys.exit(1)

if __name__ == "__main__":
    main()