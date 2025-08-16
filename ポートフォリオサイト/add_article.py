#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
記事URL入力だけで全自動でポートフォリオサイトに追加するシステム
"""

import json
import sys
import subprocess
from datetime import datetime

def get_article_info(url):
    """記事URLから全情報を自動取得（JSON-LD使用）"""
    try:
        # curlでHTMLを取得
        result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
        html = result.stdout
        
        # JSON-LDからデータ抽出
        import re
        json_ld_pattern = r'<script type="application/ld\+json">(.*?)</script>'
        json_matches = re.findall(json_ld_pattern, html, re.DOTALL)
        
        title = ""
        description = ""
        tags = []
        
        for json_str in json_matches:
            try:
                data = json.loads(json_str)
                if isinstance(data, dict) and '@graph' in data:
                    for item in data['@graph']:
                        if item.get('@type') == 'Article':
                            title = item.get('headline', '')
                            break
                        if item.get('@type') == 'WebPage':
                            if not title:
                                title = item.get('name', '')
                            description = item.get('description', '')
                        if item.get('@type') == 'BreadcrumbList':
                            for breadcrumb in item.get('itemListElement', []):
                                if breadcrumb.get('item', {}).get('name'):
                                    tags.append(breadcrumb['item']['name'])
                elif isinstance(data, dict) and data.get('@type') == 'Article':
                    title = data.get('headline', '')
                    description = data.get('description', '')
            except:
                continue
        
        # フォールバック: HTMLタグから取得
        if not title:
            title_start = html.find('<title>') + 7
            title_end = html.find('</title>')
            title = html[title_start:title_end].strip()
            if ' | ' in title:
                title = title.split(' | ')[0]
        
        if not description:
            if 'name="description"' in html:
                desc_start = html.find('name="description"')
                content_start = html.find('content="', desc_start) + 9
                content_end = html.find('"', content_start)
                description = html[content_start:content_end]
        
        # タグがない場合は自動生成
        if not tags:
            tags = extract_tags_from_title(title)
        else:
            # 既存タグに自動生成タグを追加
            tags.extend(extract_tags_from_title(title))
            tags = list(set(tags))  # 重複削除
        
        return {
            "title": title,
            "url": url,
            "description": description,
            "date": datetime.now().strftime('%Y-%m-%d'),
            "tags": tags[:8],  # 最大8個
            "client": "Muffin Blog",
            "thumbnail": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&h=200&fit=crop&auto=format"
        }
    except Exception as e:
        print(f"記事情報取得エラー: {e}")
        return None

def extract_tags_from_title(title):
    """タイトルから関連タグを自動抽出"""
    tags = []
    
    # Audible関連
    if 'Audible' in title or 'オーディブル' in title:
        tags.extend(['Audible', 'オーディブル', 'オーディオブック'])
    
    # 読書関連
    if '読書' in title:
        tags.append('読書')
    
    # 集中力・効果系
    if '集中力' in title:
        tags.append('集中力向上')
    if '効果' in title:
        tags.append('読書効果')
    
    # 基本タグ
    if not tags:
        tags = ['ブログ', '記事']
    
    return tags[:6]  # 最大6個

def add_to_articles_json(article_data):
    """articles.jsonに記事を追加"""
    json_path = "/Users/satoumasamitsu/Desktop/osigoto/ポートフォリオサイト/public/content/articles/articles.json"
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # ブログ記事として先頭に追加
        data['blogArticles'].insert(0, article_data)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"ファイル更新エラー: {e}")
        return False

def auto_commit_push():
    """Git自動コミット・プッシュ"""
    try:
        subprocess.run(['git', 'add', 'ポートフォリオサイト/public/content/articles/articles.json'], check=True)
        subprocess.run(['git', 'commit', '-m', f'新記事自動追加: {datetime.now().strftime("%Y-%m-%d")}'], check=True)
        subprocess.run(['git', 'push', 'origin', 'master'], check=True)
        return True
    except Exception as e:
        print(f"Git操作エラー: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("使用方法: python add_article.py [記事URL]")
        return
    
    url = sys.argv[1]
    print(f"記事を取得中: {url}")
    
    # 1. 記事情報自動取得
    article_data = get_article_info(url)
    if not article_data:
        print("記事情報の取得に失敗しました")
        return
    
    print(f"取得完了: {article_data['title']}")
    
    # 2. articles.json更新
    if add_to_articles_json(article_data):
        print("articles.json更新完了")
    else:
        print("ファイル更新失敗")
        return
    
    # 3. Git自動処理
    if auto_commit_push():
        print("Git処理完了 - Vercelが自動デプロイします")
    else:
        print("Git処理失敗")
    
    print("✅ 全処理完了！")

if __name__ == "__main__":
    main()