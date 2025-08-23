#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全記事データを完全修正
- 404エラー記事を削除
- SEO記事のメタデータを自動取得
- 全記事の画像URLを適切に取得
"""

import json
import requests
from urllib.parse import urlparse
import re

class ArticlesFixer:
    def __init__(self):
        self.articles_path = 'public/content/articles/articles.json'
        
    def check_url_status(self, url):
        """URLの有効性をチェック"""
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            return response.status_code != 404
        except:
            return False
    
    def get_meta_from_html(self, url):
        """HTMLからメタデータを取得"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return None
                
            html = response.text
            
            # タイトル取得
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
            title = title_match.group(1) if title_match else ""
            # サイト名を除去
            if ' | ' in title:
                title = title.split(' | ')[0]
            elif ' - ' in title:
                title = title.split(' - ')[0]
            
            # メタディスクリプション取得（短い形式）
            desc_match = re.search(r'<meta\s+(?:name="description"\s+content="([^"]+)"|content="([^"]+)"\s+name="description")', html, re.IGNORECASE)
            description = desc_match.group(1) or desc_match.group(2) if desc_match else ""
            
            # 150文字に制限
            if len(description) > 150:
                description = description[:147] + "..."
            
            # OGP画像取得
            og_image_match = re.search(r'<meta\s+(?:property="og:image"\s+content="([^"]+)"|content="([^"]+)"\s+property="og:image")', html, re.IGNORECASE)
            thumbnail = og_image_match.group(1) or og_image_match.group(2) if og_image_match else None
            
            # 日付取得
            date_match = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', html)
            if not date_match:
                date_match = re.search(r'<time[^>]*datetime="(\d{4}-\d{2}-\d{2})', html)
            date = date_match.group(1) if date_match else "2024-01-01"
            
            return {
                'title': title,
                'description': description,
                'thumbnail': thumbnail,
                'date': date
            }
        except Exception as e:
            print(f"❌ エラー: {url} - {e}")
            return None
    
    def extract_domain_name(self, url):
        """URLからドメイン名を抽出してクライアント名を推測"""
        domain = urlparse(url).netloc
        
        if 'minerva-sleep' in domain:
            return 'ミネルヴァスリープ'
        elif 'my-best.com' in domain:
            return 'マイベスト'
        elif 'baumclinic' in domain:
            return 'バウムクリニック'
        elif 'note.com' in domain:
            return 'note'
        else:
            # ドメイン名から推測
            name = domain.replace('www.', '').split('.')[0]
            return name.title()
    
    def generate_tags_from_content(self, title, description, url):
        """コンテンツからタグを生成"""
        tags = []
        content = (title + " " + description).lower()
        
        # キーワードマッピング
        tag_map = {
            '睡眠': '睡眠',
            'マットレス': 'マットレス',
            '枕': '枕',
            'ダイエット': 'ダイエット',
            '健康': '健康',
            '美容': '美容',
            'モバイル': 'モバイル',
            'uq': 'UQモバイル',
            '投資': '投資',
            '節約': '節約',
            'seo': 'SEO'
        }
        
        for keyword, tag in tag_map.items():
            if keyword in content and tag not in tags:
                tags.append(tag)
        
        # URLからもタグ生成
        if 'sleep' in url or 'minerva' in url:
            if '睡眠' not in tags:
                tags.append('睡眠')
        
        return tags[:5]  # 最大5個
    
    def fix_all_articles(self):
        """全記事を修正"""
        print("🔧 全記事データ修正開始...")
        
        # 既存データ読み込み
        with open(self.articles_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # SEO記事を修正
        print("\n📊 SEO記事を修正中...")
        fixed_seo = []
        for article in data['seoArticles']:
            url = article['url']
            print(f"🔍 確認中: {url}")
            
            # URL有効性チェック
            if not self.check_url_status(url):
                print(f"❌ 404エラー: スキップ")
                continue
            
            # メタデータ取得
            meta = self.get_meta_from_html(url)
            if meta:
                # 既存データを更新
                article['title'] = meta['title'] or article.get('title', '')
                article['description'] = meta['description'] or article.get('description', '')[:150]
                article['thumbnail'] = meta['thumbnail'] or article.get('thumbnail')
                article['date'] = meta['date'] or article.get('date', '2024-01-01')
                
                # クライアント名設定
                if 'client' not in article or not article['client']:
                    article['client'] = self.extract_domain_name(url)
                
                # タグ生成
                article['tags'] = self.generate_tags_from_content(
                    article['title'], 
                    article['description'],
                    url
                )
                
                print(f"✅ 修正完了: {article['title'][:30]}...")
            else:
                print(f"⚠️ メタ取得失敗、既存データ保持")
            
            fixed_seo.append(article)
        
        # ブログ記事を修正（404チェック）
        print("\n📝 ブログ記事を確認中...")
        fixed_blog = []
        for article in data['blogArticles']:
            url = article['url']
            
            # 404エラー記事を除外
            if '404' in article.get('title', '') or 'ページが見つかりません' in article.get('title', ''):
                print(f"🗑️ 404記事を削除: {url}")
                continue
            
            # URL有効性チェック
            if url != 'https://muffin-blog.com/' and not self.check_url_status(url):
                print(f"❌ 404エラー: {url} - スキップ")
                continue
            
            fixed_blog.append(article)
            print(f"✅ 保持: {article['title'][:30]}...")
        
        # データ更新
        data['seoArticles'] = fixed_seo
        data['blogArticles'] = fixed_blog
        
        # 保存
        with open(self.articles_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n🎉 修正完了！")
        print(f"   SEO記事: {len(fixed_seo)}件")
        print(f"   ブログ記事: {len(fixed_blog)}件")
        print(f"   削除: {len(data.get('seoArticles', [])) + len(data.get('blogArticles', [])) - len(fixed_seo) - len(fixed_blog)}件")

if __name__ == "__main__":
    fixer = ArticlesFixer()
    fixer.fix_all_articles()