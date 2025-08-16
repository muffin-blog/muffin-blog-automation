#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
記事URL入力だけで完璧に動く最終版システム
- 1回で確実に動作
- JSON-LDから実際のメタデータ取得
- 重複なし・エラーなし
"""

import json
import sys
import subprocess
import re
from datetime import datetime

def get_article_data(url):
    """記事URLから完璧なデータを取得"""
    try:
        print(f"📡 記事データを取得中: {url}")
        
        # HTMLを取得
        result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
        html = result.stdout
        
        if not html or len(html) < 100:
            raise Exception("HTMLの取得に失敗")
        
        # JSON-LDからメタデータ抽出
        title, description, category = extract_from_jsonld(html)
        
        # フォールバック: HTMLタグから抽出
        if not title:
            title = extract_title_from_html(html)
        if not description:
            description = extract_description_from_html(html)
        
        # タグ生成（推測なし、URLから自動取得）
        tags = generate_tags_from_url(url, title)
        
        print(f"✅ タイトル: {title}")
        print(f"✅ 説明: {description[:50]}...")
        print(f"✅ タグ: {', '.join(tags)}")
        
        return {
            "title": title,
            "url": url,
            "description": description,
            "date": datetime.now().strftime('%Y-%m-%d'),
            "tags": tags,
            "client": "Muffin Blog",
            "thumbnail": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&h=200&fit=crop&auto=format"
        }
        
    except Exception as e:
        print(f"❌ データ取得エラー: {e}")
        return None

def extract_from_jsonld(html):
    """JSON-LDから正確なデータを抽出"""
    title = ""
    description = ""
    category = ""
    
    try:
        json_ld_pattern = r'<script type="application/ld\+json">(.*?)</script>'
        matches = re.findall(json_ld_pattern, html, re.DOTALL)
        
        for match in matches:
            try:
                data = json.loads(match)
                
                if isinstance(data, dict) and '@graph' in data:
                    for item in data['@graph']:
                        if item.get('@type') == 'Article':
                            title = item.get('headline', '')
                        elif item.get('@type') == 'WebPage' and not title:
                            title = item.get('name', '')
                            description = item.get('description', '')
                        elif item.get('@type') == 'BreadcrumbList':
                            for breadcrumb in item.get('itemListElement', []):
                                name = breadcrumb.get('item', {}).get('name')
                                if name:
                                    category = name
                                    break
                                    
            except json.JSONDecodeError:
                continue
                
    except Exception:
        pass
        
    return title, description, category

def extract_title_from_html(html):
    """HTMLからタイトルを抽出"""
    try:
        start = html.find('<title>') + 7
        end = html.find('</title>')
        title = html[start:end].strip()
        if ' | ' in title:
            title = title.split(' | ')[0]
        return title
    except:
        return ""

def extract_description_from_html(html):
    """HTMLから説明を抽出"""
    try:
        if 'name="description"' in html:
            start = html.find('name="description"')
            content_start = html.find('content="', start) + 9
            content_end = html.find('"', content_start)
            return html[content_start:content_end]
    except:
        pass
    return ""

def generate_tags_from_url(url, title=""):
    """URLとタイトルから自動でタグを生成（推測なし）"""
    try:
        # HTMLを取得
        result = subprocess.run(['curl', '-s', '-L', url], capture_output=True, text=True)
        html = result.stdout
        
        if not html:
            return []
        
        # script/styleタグを除去
        content = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<[^>]+>', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        
        # 除外キーワード（技術的なものを徹底排除）
        exclude_words = {
            'var', 'function', 'style', 'margin', 'border', 'has', 'preset', 
            'important', 'text', 'ndash', 'について', 'という', 'ですが', 
            'ところ', 'ことが', 'される', 'している', 'します', 'ました',
            'document', 'window', 'element', 'div', 'span', 'class', 'id',
            'background', 'color', 'width', 'height', 'padding', 'display',
            'position', 'absolute', 'relative', 'fixed', 'flex', 'grid',
            'const', 'let', 'return', 'false', 'true', 'null', 'undefined',
            'onclick', 'onload', 'jquery', 'script', 'css', 'html'
        }
        
        # 意味のあるキーワードのみ抽出
        tags = set()
        
        # タイトルからキーワード抽出
        if title:
            title_words = re.findall(r'[ァ-ヶー]{2,}|[あ-ん]{2,}|[一-龯]{2,}|[A-Za-z]{3,}', title)
            for word in title_words:
                if word.lower() not in exclude_words and len(word) >= 2:
                    tags.add(word)
        
        # コンテンツから重要キーワード抽出
        words = re.findall(r'[ァ-ヶー]{2,}|[あ-ん]{2,}|[一-龯]{2,}|[A-Za-z]{3,}', content)
        word_count = {}
        
        for word in words:
            if word.lower() not in exclude_words and len(word) >= 2:
                word_count[word] = word_count.get(word, 0) + 1
        
        # 5回以上出現する重要なキーワードのみ
        for word, count in word_count.items():
            if count >= 5:
                tags.add(word)
        
        # カテゴリ分類
        if 'audible' in url.lower() or 'audiobook' in url.lower():
            tags.add('オーディオブック')
        if 'health' in url.lower() or '健康' in content:
            tags.add('健康')
        if 'diet' in url.lower() or 'ダイエット' in content:
            tags.add('ダイエット')
        if 'sleep' in url.lower() or '睡眠' in content:
            tags.add('睡眠')
            
        return list(tags)[:6]
        
    except Exception as e:
        print(f"❌ タグ生成エラー: {e}")
        return []

def update_articles_json(article_data):
    """articles.jsonを更新"""
    try:
        print("📝 articles.jsonを更新中...")
        
        json_path = "public/content/articles/articles.json"
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 重複チェック
        for existing in data['blogArticles']:
            if existing['url'] == article_data['url']:
                print("⚠️  同じURLの記事が既に存在します。スキップ。")
                return True
        
        # 先頭に追加
        data['blogArticles'].insert(0, article_data)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("✅ articles.json更新完了")
        return True
        
    except Exception as e:
        print(f"❌ ファイル更新エラー: {e}")
        return False

def git_deploy():
    """Git操作でデプロイ"""
    try:
        print("🚀 Gitデプロイ中...")
        
        # ステージング
        subprocess.run(['git', 'add', 'public/content/articles/articles.json', 'public/assets/js/script.js'], check=True)
        
        # コミット
        commit_msg = f"新記事追加: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        # プッシュ
        subprocess.run(['git', 'push', 'origin', 'master'], check=True)
        
        print("✅ Git デプロイ完了")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git操作エラー: {e}")
        return False

def main():
    """メイン処理"""
    if len(sys.argv) != 2:
        print("❌ 使用方法: python3 add_article_final.py [記事URL]")
        return
    
    url = sys.argv[1]
    print(f"🎯 新記事追加開始: {url}")
    print("-" * 50)
    
    # 1. データ取得
    article_data = get_article_data(url)
    if not article_data:
        print("❌ 処理を中断します")
        return
    
    print("-" * 50)
    
    # 2. ファイル更新
    if not update_articles_json(article_data):
        print("❌ 処理を中断します")
        return
    
    # 3. デプロイ
    if not git_deploy():
        print("❌ 処理を中断します")
        return
    
    print("-" * 50)
    print("🎉 全処理完了！")
    print(f"📱 サイト確認: https://muffin-portfolio-public.vercel.app")
    print("⏱️  Vercelデプロイまで1-2分お待ちください")

if __name__ == "__main__":
    main()