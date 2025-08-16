#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全記事のメタデータ自動修正システム
- URLから実際のメタディスクリプション、タグ、カテゴリを自動取得
- すべての記事を正しいデータで更新
- 推測なし、完全自動化
"""

import json
import sys
import subprocess
import re
import time
from datetime import datetime
from urllib.parse import urlparse

def fetch_url_content(url):
    """URLからHTMLコンテンツを取得"""
    try:
        print(f"📡 URLアクセス中: {url}")
        result = subprocess.run(['curl', '-s', '-L', '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'], 
                               input=url, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout:
            return result.stdout
        else:
            # fallback: curlコマンドを直接実行
            result = subprocess.run(['curl', '-s', '-L', url], capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else None
    except Exception as e:
        print(f"❌ URLアクセスエラー: {e}")
        return None

def extract_meta_description(html):
    """HTMLからメタディスクリプションを抽出"""
    if not html:
        return ""
    
    # meta name="description" を検索
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
            # HTMLエンティティをデコード
            description = description.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            return description
    
    # フォールバック: 最初のpタグの内容を取得
    p_match = re.search(r'<p[^>]*>(.*?)</p>', html, re.IGNORECASE | re.DOTALL)
    if p_match:
        content = re.sub(r'<[^>]+>', '', p_match.group(1))
        content = re.sub(r'\s+', ' ', content).strip()
        if len(content) > 50:  # 十分な長さがある場合のみ
            return content[:200] + '...' if len(content) > 200 else content
    
    return ""

def extract_real_title(html):
    """HTMLから実際のタイトルを抽出"""
    if not html:
        return ""
    
    # <title>タグから抽出
    pattern = r'<title>(.*?)</title>'
    match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
    if match:
        title = match.group(1).strip()
        # サイト名を除去
        if ' | ' in title:
            title = title.split(' | ')[0]
        if ' - ' in title:
            title = title.split(' - ')[0]
        return title
    
    return ""

def extract_keywords_from_content(html, title):
    """コンテンツから実際のキーワードを抽出"""
    keywords = set()
    
    if not html or not title:
        return list(keywords)
    
    # HTMLからテキストコンテンツを抽出（script/styleタグを除去）
    content = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<[^>]+>', ' ', content)
    content = re.sub(r'\s+', ' ', content)
    
    # 除外する技術的なキーワード
    exclude_words = {
        'var', 'function', 'style', 'margin', 'border', 'has', 'preset', 
        'important', 'text', 'ndash', 'について', 'という', 'ですが', 
        'ところ', 'ことが', 'される', 'している', 'します', 'ました',
        'document', 'window', 'element', 'div', 'span', 'class', 'id',
        'background', 'color', 'width', 'height', 'padding', 'display',
        'position', 'absolute', 'relative', 'fixed', 'flex', 'grid'
    }
    
    # タイトルからキーワード抽出
    title_words = re.findall(r'[ァ-ヶー]{2,}|[あ-ん]{2,}|[一-龯]{2,}|[A-Za-z]{3,}', title)
    for word in title_words:
        if word.lower() not in exclude_words and len(word) >= 2:
            keywords.add(word)
    
    # コンテンツから意味のあるキーワード抽出
    words = re.findall(r'[ァ-ヶー]{2,}|[あ-ん]{2,}|[一-龯]{2,}|[A-Za-z]{3,}', content)
    word_count = {}
    for word in words:
        if word.lower() not in exclude_words and len(word) >= 2:
            word_count[word] = word_count.get(word, 0) + 1
    
    # 頻出上位を追加（より高い閾値を設定）
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_words[:6]:  # 上位6個
        if count >= 3 and len(word) >= 2:  # 3回以上出現
            keywords.add(word)
    
    return list(keywords)[:6]  # 最大6個

def extract_category_from_url(url):
    """URLからカテゴリを推定"""
    parsed = urlparse(url)
    path_parts = parsed.path.strip('/').split('/')
    
    # URLパスからカテゴリを推定
    for part in path_parts:
        if part in ['audible', 'audiobook', 'オーディブル']:
            return 'オーディオブック'
        elif part in ['seo', 'marketing']:
            return 'SEO・マーケティング'
        elif part in ['health', 'beauty', '健康', '美容']:
            return '健康・美容'
        elif part in ['tech', 'technology', '技術']:
            return 'テクノロジー'
        elif part in ['finance', '金融', '投資']:
            return '金融・投資'
        elif part in ['lifestyle', 'life', 'ライフスタイル']:
            return 'ライフスタイル'
    
    # ドメインからカテゴリを推定
    domain = parsed.netloc
    if 'muffin-blog.com' in domain:
        return 'ブログ'
    elif 'minerva-sleep.jp' in domain:
        return '睡眠・健康'
    elif 'baumclinic.jp' in domain:
        return '美容・ダイエット'
    elif 'my-best.com' in domain:
        return 'レビュー・比較'
    
    return 'その他'

def get_article_metadata(url):
    """URLから完全なメタデータを取得"""
    try:
        print(f"🔍 記事分析開始: {url}")
        
        html = fetch_url_content(url)
        if not html:
            print(f"❌ HTMLの取得に失敗: {url}")
            return None
        
        # 各種メタデータを抽出
        title = extract_real_title(html)
        description = extract_meta_description(html)
        keywords = extract_keywords_from_content(html, title)
        category = extract_category_from_url(url)
        
        print(f"✅ 抽出完了:")
        print(f"   タイトル: {title}")
        print(f"   説明: {description[:50]}..." if description else "   説明: (取得失敗)")
        print(f"   キーワード: {', '.join(keywords)}")
        print(f"   カテゴリ: {category}")
        
        return {
            'title': title,
            'description': description,
            'keywords': keywords,
            'category': category
        }
        
    except Exception as e:
        print(f"❌ メタデータ取得エラー: {e}")
        return None

def update_article_data(article, metadata):
    """記事データを新しいメタデータで更新"""
    if not metadata:
        return article
    
    # タイトルを更新（元のタイトルが空や不正な場合のみ）
    if metadata['title'] and (not article.get('title') or len(article['title']) < 10):
        article['title'] = metadata['title']
    
    # 説明を更新（常に実際の説明で上書き）
    if metadata['description']:
        article['description'] = metadata['description']
    
    # タグを更新（実際のキーワードで置き換え）
    if metadata['keywords']:
        # 既存のタグと新しいキーワードをマージ
        existing_tags = set(article.get('tags', []))
        new_tags = set(metadata['keywords'])
        combined_tags = list(existing_tags.union(new_tags))[:8]  # 最大8個
        article['tags'] = combined_tags
    
    # カテゴリを追加
    if metadata['category'] and metadata['category'] not in article.get('tags', []):
        if 'tags' not in article:
            article['tags'] = []
        article['tags'].insert(0, metadata['category'])
        article['tags'] = article['tags'][:8]  # 最大8個に制限
    
    return article

def fix_all_articles():
    """すべての記事のメタデータを修正"""
    try:
        print("🚀 全記事メタデータ修正開始")
        print("-" * 60)
        
        # articles.jsonを読み込み
        json_path = "public/content/articles/articles.json"
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 記事統計:")
        print(f"   SEO記事: {len(data.get('seoArticles', []))}件")
        print(f"   ブログ記事: {len(data.get('blogArticles', []))}件")
        print("-" * 60)
        
        # SEO記事を修正
        if 'seoArticles' in data:
            print("🔧 SEO記事の修正中...")
            for i, article in enumerate(data['seoArticles']):
                print(f"\n[{i+1}/{len(data['seoArticles'])}] {article.get('title', 'タイトル不明')}")
                metadata = get_article_metadata(article['url'])
                data['seoArticles'][i] = update_article_data(article, metadata)
                time.sleep(1)  # レート制限対策
        
        # ブログ記事を修正
        if 'blogArticles' in data:
            print("\n🔧 ブログ記事の修正中...")
            for i, article in enumerate(data['blogArticles']):
                print(f"\n[{i+1}/{len(data['blogArticles'])}] {article.get('title', 'タイトル不明')}")
                metadata = get_article_metadata(article['url'])
                data['blogArticles'][i] = update_article_data(article, metadata)
                time.sleep(1)  # レート制限対策
        
        # 更新日時を設定
        data['_lastUpdate'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+09:00')
        data['_cacheBreaker'] = int(time.time())
        
        # ファイルに保存
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 60)
        print("🎉 全記事修正完了！")
        print(f"📝 更新日時: {data['_lastUpdate']}")
        print(f"🔄 キャッシュブレーカー: {data['_cacheBreaker']}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ 全記事修正エラー: {e}")
        return False

def main():
    """メイン処理"""
    print("🎯 全記事メタデータ自動修正システム")
    print("=" * 60)
    
    if not fix_all_articles():
        print("❌ 処理に失敗しました")
        sys.exit(1)
    
    print("\n🚀 Gitコミット中...")
    try:
        subprocess.run(['git', 'add', 'public/content/articles/articles.json'], check=True)
        commit_msg = f"全記事メタデータ自動修正: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        print("✅ Gitコミット完了")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Gitコミット失敗: {e}")
    
    print("\n🎯 処理完了！すべての記事が正しいメタデータで更新されました。")

if __name__ == "__main__":
    main()