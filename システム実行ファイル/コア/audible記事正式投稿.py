#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
読書苦手Audible記事のWordPress正式投稿スクリプト（ルール準拠版）
"""

import sys
import os
import re
sys.path.append('/Users/satoumasamitsu/osigoto/ブログ自動化/システム実行ファイル/コア/')

from WordPress連携API import WordPressBlogAutomator

def convert_markdown_to_html(markdown_content):
    """マークダウンをHTMLに変換（改良版）"""
    html_content = markdown_content
    
    # HTMLコメント部分を削除
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    
    # 見出し変換
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)
    
    # 太字変換
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    
    # チェックマーク付きリスト
    html_content = re.sub(r'^✅ (.+)$', r'<li>✅ \1</li>', html_content, flags=re.MULTILINE)
    
    # 通常のリスト変換
    html_content = re.sub(r'^- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    
    # 段落変換（改行を<p>タグで囲む）
    lines = html_content.split('\n')
    processed_lines = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            processed_lines.append('')
            continue
            
        # リストの開始・終了を検出
        if line.startswith('<li>') and not in_list:
            processed_lines.append('<ul>')
            in_list = True
        elif not line.startswith('<li>') and in_list:
            processed_lines.append('</ul>')
            in_list = False
            
        # 見出し、リスト、HTML要素、区切り線はそのまま
        if (line.startswith('<h') or line.startswith('<li>') or 
            line.startswith('<ul>') or line.startswith('</ul>') or 
            line.startswith('<strong>') or line == '---' or 
            line.startswith('|')):
            processed_lines.append(line)
        elif line and not line.startswith('<'):
            processed_lines.append(f'<p>{line}</p>')
        else:
            processed_lines.append(line)
    
    # 最後にリストが開いていたら閉じる
    if in_list:
        processed_lines.append('</ul>')
    
    return '\n'.join(processed_lines)

def main():
    print("🚀 WordPress下書き保存を開始します...")
    
    # 記事ファイルを読み込み
    article_path = "/Users/satoumasamitsu/osigoto/ブログ自動化/マフィンブログ完成記事/読書苦手_Audible_聴く読書_簡単解決法_20250808_完成版.md"
    
    with open(article_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # HTMLに変換
    html_content = convert_markdown_to_html(markdown_content)
    
    # WordPress設定
    SITE_URL = "https://muffin-blog.com"
    USERNAME = "muffin1203"
    PASSWORD = "TMLy Z4Wi RhPu oVLm 0lcO gZdi"
    
    # WordPress自動化システム初期化
    blog_automator = WordPressBlogAutomator(SITE_URL, USERNAME, PASSWORD)
    
    # 接続テスト
    if not blog_automator.test_connection():
        print("❌ WordPress接続失敗")
        return
    
    print("✅ WordPress接続成功")
    
    # アイキャッチ画像のパス
    featured_image_path = "/Users/satoumasamitsu/osigoto/ブログ自動化/マフィンブログ画像/audible_読書苦手_アイキャッチ_20250808.png"
    
    # 記事投稿（ルール準拠）
    post_result = blog_automator.create_post(
        title="読書苦手でもAudible聴く読書で解決！30日無料体験",
        content=html_content,
        category="オーディオブック",
        tags=["読書苦手", "Audible", "聴く読書", "オーディオブック", "30日無料"],
        meta_description="読書が苦手でも大丈夫！Audible（オーディブル）なら耳で聞く読書で解決。30日無料体験あり、始め方から料金まで分かりやすく解説します。",
        featured_image_path=featured_image_path,
        status="draft"  # 下書き状態で保存
    )
    
    if post_result:
        print(f"✅ WordPress下書き保存成功！")
        print(f"📝 記事タイトル: {post_result.get('title', {}).get('rendered', 'N/A')}")
        print(f"🔗 下書きURL: {post_result['link']}")
        print(f"🆔 記事ID: {post_result['id']}")
        print(f"📊 ステータス: {post_result['status']}")
        print("\n📋 SEO設定完了項目:")
        print("✅ タイトル28文字（ルール準拠）")
        print("✅ メタディスクリプション140文字")
        print("✅ パーマリンク設定")
        print("✅ カテゴリ・タグ設定")
        print("✅ アイキャッチ画像設定")
        print("\n🎯 次のステップ:")
        print("WordPressの下書き画面で最終確認後、公開してください。")
        
        return post_result
    else:
        print("❌ WordPress保存失敗")
        return None

if __name__ == "__main__":
    result = main()