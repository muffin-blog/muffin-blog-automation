#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
既存記事を新システムで再取得・更新
"""

import json
import sys
from add_article_auto import ArticleAutoAdder

def refresh_all_articles():
    """全記事を再取得して更新"""
    
    # 既存データ読み込み
    with open('public/content/articles/articles.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    adder = ArticleAutoAdder()
    
    # ブログ記事を更新
    print("🔄 ブログ記事を更新中...")
    updated_blog = []
    for article in data['blogArticles']:
        url = article['url']
        print(f"\n📡 更新中: {url}")
        
        # WordPress APIから最新データ取得
        new_data = adder.get_wordpress_data(url)
        if new_data:
            new_data['url'] = url
            updated_blog.append(new_data)
            print(f"✅ 更新成功: {new_data['title']}")
        else:
            # 取得失敗した場合は既存データを保持
            print(f"⚠️ 取得失敗、既存データ保持")
            updated_blog.append(article)
    
    # データ更新
    data['blogArticles'] = updated_blog
    
    # 保存
    with open('public/content/articles/articles.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n✅ 全記事の更新完了！")
    print(f"   更新数: {len(updated_blog)}件")

if __name__ == "__main__":
    refresh_all_articles()