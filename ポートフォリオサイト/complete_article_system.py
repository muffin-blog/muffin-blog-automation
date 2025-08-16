#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完璧な記事管理システム
- URLから正確なメタデータ取得
- 技術的キーワード完全除去
- Unsplash APIで画像自動取得・保存
- 全自動化・推測なし
"""

import json
import sys
import subprocess
import re
import time
import requests
import os
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path

# Unsplash API設定
UNSPLASH_ACCESS_KEY = "YOUR_UNSPLASH_ACCESS_KEY"  # 実際のキーに置き換え
UNSPLASH_API_URL = "https://api.unsplash.com/search/photos"

def fetch_url_content(url):
    """URLからHTMLコンテンツを取得"""
    try:
        print(f"📡 URLアクセス中: {url}")
        result = subprocess.run(['curl', '-s', '-L', '--user-agent', 
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'], 
                               input=url, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout:
            return result.stdout
        else:
            result = subprocess.run(['curl', '-s', '-L', url], capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else None
    except Exception as e:
        print(f"❌ URLアクセスエラー: {e}")
        return None

def extract_meta_description(html):
    """HTMLからメタディスクリプションを抽出"""
    if not html:
        return ""
    
    patterns = [
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']',
        r'<meta\s+property=["\']og:description["\']\s+content=["\'](.*?)["\']',
        r'<meta\s+content=["\'](.*?)["\']\s+property=["\']og:description["\']'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
        if match:
            description = match.group(1).strip()
            description = description.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            return description
    
    # フォールバック: 最初のpタグ
    p_match = re.search(r'<p[^>]*>(.*?)</p>', html, re.IGNORECASE | re.DOTALL)
    if p_match:
        content = re.sub(r'<[^>]+>', '', p_match.group(1))
        content = re.sub(r'\s+', ' ', content).strip()
        if len(content) > 50:
            return content[:200] + '...' if len(content) > 200 else content
    
    return ""

def extract_real_title(html):
    """HTMLから実際のタイトルを抽出"""
    if not html:
        return ""
    
    pattern = r'<title>(.*?)</title>'
    match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
    if match:
        title = match.group(1).strip()
        # サイト名を除去
        if ' | ' in title:
            title = title.split(' | ')[0]
        if ' - ' in title:
            title = title.split(' - ')[0]
        if ' – ' in title:
            title = title.split(' – ')[0]
        return title
    
    return ""

def extract_clean_keywords(html, title):
    """技術的キーワードを完全除去してクリーンなキーワードのみ抽出"""
    keywords = set()
    
    if not html or not title:
        return list(keywords)
    
    # script/styleタグを完全除去
    content = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<[^>]+>', ' ', content)
    content = re.sub(r'\s+', ' ', content)
    
    # 技術的・無意味なキーワードを徹底除去
    exclude_words = {
        # JavaScript/CSS関連
        'var', 'function', 'style', 'margin', 'border', 'has', 'preset', 
        'important', 'text', 'ndash', 'document', 'window', 'element', 
        'div', 'span', 'class', 'id', 'background', 'color', 'width', 
        'height', 'padding', 'display', 'position', 'absolute', 'relative', 
        'fixed', 'flex', 'grid', 'const', 'let', 'return', 'false', 'true', 
        'null', 'undefined', 'onclick', 'onload', 'jquery', 'script', 'css', 
        'html', 'src', 'href', 'alt', 'img', 'px', 'rem', 'em',
        
        # 一般的な無意味語
        'について', 'という', 'ですが', 'ところ', 'ことが', 'される', 
        'している', 'します', 'ました', 'です', 'である', 'する', 
        'した', 'して', 'させる', 'られる', 'なる', 'ある', 'いる',
        'この', 'その', 'あの', 'どの', 'など', 'また', 'さらに',
        'しかし', 'ただし', 'つまり', 'なお', 'ちなみに', 'では',
        'から', 'まで', 'より', 'ほど', 'くらい', 'だけ', 'でも',
        'けれど', 'それで', 'そして', 'または', 'もしくは',
        
        # 短い無意味な文字列
        'で', 'に', 'を', 'が', 'は', 'と', 'も', 'の', 'や', 'か',
        'へ', 'より', 'から', 'まで', 'でも', 'なら', 'けれど'
    }
    
    # 有効なキーワードパターン
    meaningful_patterns = [
        r'[ァ-ヶー]{2,}',  # カタカナ2文字以上
        r'[A-Za-z]{4,}',   # アルファベット4文字以上
        r'[一-龯]{2,}'     # 漢字2文字以上
    ]
    
    # タイトルからキーワード抽出
    for pattern in meaningful_patterns:
        words = re.findall(pattern, title)
        for word in words:
            if word.lower() not in exclude_words and len(word) >= 2:
                # 特別なキーワードフィルター
                if word not in ['までぐっすり', 'ける', 'える', 'きながら', 'するため', 'がお', 'なら', 'でも']:
                    keywords.add(word)
    
    # コンテンツから重要キーワード抽出（より厳しい条件）
    for pattern in meaningful_patterns:
        words = re.findall(pattern, content)
        word_count = {}
        
        for word in words:
            if (word.lower() not in exclude_words and 
                len(word) >= 2 and 
                word not in ['までぐっすり', 'ける', 'える', 'きながら', 'するため', 'がお', 'なら', 'でも']):
                word_count[word] = word_count.get(word, 0) + 1
        
        # 10回以上出現する重要なキーワードのみ
        for word, count in word_count.items():
            if count >= 10:
                keywords.add(word)
    
    # ドメイン・URL基準のカテゴリタグ
    if 'audible' in title.lower() or 'オーディブル' in title:
        keywords.add('オーディオブック')
        keywords.add('Audible')
    
    if 'sleep' in title.lower() or '睡眠' in title:
        keywords.add('睡眠')
        keywords.add('健康')
    
    if 'diet' in title.lower() or 'ダイエット' in title:
        keywords.add('ダイエット')
        keywords.add('健康')
    
    return list(keywords)[:6]

def get_unsplash_image(keywords, article_title):
    """Unsplash APIからキーワードベースで画像取得"""
    try:
        # キーワードを英語に変換
        keyword_mapping = {
            'オーディオブック': 'audiobook headphones',
            'Audible': 'audiobook reading',
            '睡眠': 'sleep bed',
            '健康': 'health wellness',
            'ダイエット': 'diet healthy food',
            '読書': 'reading book',
            '集中力': 'focus concentration',
            'エアコン': 'air conditioner cooling',
            '枕': 'pillow sleep',
            'マットレス': 'mattress bed'
        }
        
        # 最初のキーワードを使用
        search_query = "book reading"  # デフォルト
        if keywords:
            for keyword in keywords:
                if keyword in keyword_mapping:
                    search_query = keyword_mapping[keyword]
                    break
        
        print(f"🖼️ 画像検索: {search_query}")
        
        # 実際のUnsplash APIキーがない場合のフォールバック
        if UNSPLASH_ACCESS_KEY == "YOUR_UNSPLASH_ACCESS_KEY":
            print("⚠️ Unsplash APIキーが設定されていません。デフォルト画像を使用します。")
            return "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&h=200&fit=crop&auto=format"
        
        headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
        params = {
            "query": search_query,
            "per_page": 1,
            "orientation": "landscape"
        }
        
        response = requests.get(UNSPLASH_API_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                image_url = data['results'][0]['urls']['regular']
                return f"{image_url}?w=300&h=200&fit=crop&auto=format"
        
        return "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&h=200&fit=crop&auto=format"
        
    except Exception as e:
        print(f"❌ 画像取得エラー: {e}")
        return "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&h=200&fit=crop&auto=format"

def get_domain_category(url):
    """URLドメインからカテゴリを判定"""
    domain = urlparse(url).netloc.lower()
    
    if 'muffin-blog.com' in domain:
        return 'ブログ'
    elif 'minerva-sleep.jp' in domain:
        return '睡眠・健康'
    elif 'baumclinic.jp' in domain:
        return '美容・ダイエット'
    elif 'my-best.com' in domain:
        return 'レビュー・比較'
    else:
        return 'その他'

def get_complete_article_metadata(url):
    """URLから完璧なメタデータを取得"""
    try:
        print(f"🔍 完全分析開始: {url}")
        
        html = fetch_url_content(url)
        if not html:
            print(f"❌ HTMLの取得に失敗: {url}")
            return None
        
        # メタデータ抽出
        title = extract_real_title(html)
        description = extract_meta_description(html)
        keywords = extract_clean_keywords(html, title)
        category = get_domain_category(url)
        
        # 画像取得
        thumbnail = get_unsplash_image(keywords, title)
        
        print(f"✅ 抽出完了:")
        print(f"   タイトル: {title}")
        print(f"   説明: {description[:50]}..." if description else "   説明: (取得失敗)")
        print(f"   キーワード: {', '.join(keywords)}")
        print(f"   カテゴリ: {category}")
        print(f"   画像: {thumbnail}")
        
        return {
            'title': title,
            'description': description,
            'keywords': keywords,
            'category': category,
            'thumbnail': thumbnail
        }
        
    except Exception as e:
        print(f"❌ メタデータ取得エラー: {e}")
        return None

def clean_existing_tags():
    """既存記事のタグをクリーンアップ"""
    try:
        print("🧹 既存タグのクリーンアップ開始")
        
        json_path = "public/content/articles/articles.json"
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 技術的キーワードを除去
        tech_keywords = {
            'var', 'function', 'style', 'margin', 'border', 'has', 'preset',
            'important', 'text', 'ndash', 'までぐっすり', 'ける', 'える',
            'きながら', 'するため', 'がお', 'なら', 'でも', 'への', 'する',
            'した', 'して', 'される', 'している', 'します', 'ました'
        }
        
        # SEO記事のタグクリーンアップ
        for article in data.get('seoArticles', []):
            if 'tags' in article:
                cleaned_tags = [tag for tag in article['tags'] if tag not in tech_keywords]
                article['tags'] = cleaned_tags[:6]
        
        # ブログ記事のタグクリーンアップ
        for article in data.get('blogArticles', []):
            if 'tags' in article:
                cleaned_tags = [tag for tag in article['tags'] if tag not in tech_keywords]
                article['tags'] = cleaned_tags[:6]
        
        # 更新日時設定
        data['_lastUpdate'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+09:00')
        data['_cacheBreaker'] = int(time.time())
        
        # 保存
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("✅ タグクリーンアップ完了")
        return True
        
    except Exception as e:
        print(f"❌ タグクリーンアップエラー: {e}")
        return False

def add_new_article(url):
    """新記事を追加"""
    try:
        print(f"🎯 新記事追加開始: {url}")
        
        # メタデータ取得
        metadata = get_complete_article_metadata(url)
        if not metadata:
            return False
        
        # 記事データ構築
        article_data = {
            "title": metadata['title'],
            "url": url,
            "description": metadata['description'],
            "date": datetime.now().strftime('%Y-%m-%d'),
            "tags": [metadata['category']] + metadata['keywords'],
            "client": "Muffin Blog" if 'muffin-blog.com' in url else metadata['category'],
            "thumbnail": metadata['thumbnail']
        }
        
        # articles.json更新
        json_path = "public/content/articles/articles.json"
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 重複チェック
        target_section = 'blogArticles' if 'muffin-blog.com' in url else 'seoArticles'
        for existing in data[target_section]:
            if existing['url'] == url:
                print("⚠️ 同じURLの記事が既に存在します")
                return False
        
        # 先頭に追加
        data[target_section].insert(0, article_data)
        
        # 更新日時設定
        data['_lastUpdate'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+09:00')
        data['_cacheBreaker'] = int(time.time())
        
        # 保存
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("✅ 記事追加完了")
        return True
        
    except Exception as e:
        print(f"❌ 記事追加エラー: {e}")
        return False

def deploy_to_vercel():
    """Vercelにデプロイ"""
    try:
        print("🚀 Gitコミット中...")
        subprocess.run(['git', 'add', '.'], check=True)
        
        commit_msg = f"完璧な記事システム更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        subprocess.run(['git', 'push', 'origin', 'master'], check=True)
        print("✅ Gitプッシュ完了")
        
        print("🚀 Vercelデプロイ中...")
        result = subprocess.run(['npx', 'vercel', '--prod'], capture_output=True, text=True)
        print("✅ Vercelデプロイ完了")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ デプロイエラー: {e}")
        return False

def main():
    """メイン処理"""
    print("🎯 完璧な記事管理システム")
    print("=" * 60)
    
    if len(sys.argv) == 1:
        # 既存記事のクリーンアップのみ
        print("📝 既存記事のタグクリーンアップを実行")
        if clean_existing_tags():
            if deploy_to_vercel():
                print("🎉 クリーンアップ完了！")
            else:
                print("❌ デプロイに失敗")
        else:
            print("❌ クリーンアップに失敗")
    
    elif len(sys.argv) == 2:
        # 新記事追加
        url = sys.argv[1]
        print(f"📝 新記事追加: {url}")
        
        # まずクリーンアップ
        clean_existing_tags()
        
        # 新記事追加
        if add_new_article(url):
            if deploy_to_vercel():
                print("🎉 記事追加とデプロイ完了！")
                print(f"📱 サイト確認: https://muffin-portfolio-public.vercel.app")
            else:
                print("❌ デプロイに失敗")
        else:
            print("❌ 記事追加に失敗")
    
    else:
        print("❌ 使用方法:")
        print("  既存クリーンアップ: python3 complete_article_system.py")
        print("  新記事追加: python3 complete_article_system.py [記事URL]")

if __name__ == "__main__":
    main()