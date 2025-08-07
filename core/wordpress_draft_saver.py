"""
WordPressへ下書き保存システム
SEO最適化、アイキャッチ画像、メタ情報を含む包括的な記事投稿システム
"""

import os
import sys
import requests
import json
import base64
from datetime import datetime
import re

# パスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
from image_generation.unsplash_image_generator import UnsplashImageGenerator

class WordPressDraftSaver:
    """WordPress下書き保存システム"""
    
    def __init__(self):
        # WordPress API初期化
        self.wp = WordPressBlogAutomator(
            site_url="https://muffin-blog.com",
            username="muffin1203", 
            password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
        )
        
        # Unsplash画像生成初期化（後で実装）
        # self.image_generator = UnsplashImageGenerator()
        
    def extract_article_info(self, markdown_content):
        """マークダウン記事から情報を抽出"""
        lines = markdown_content.split('\n')
        
        # メタ情報抽出
        meta_info = {}
        in_meta = False
        
        for line in lines:
            if line.strip().startswith('<!--'):
                in_meta = True
                continue
            elif line.strip().endswith('-->'):
                in_meta = False
                continue
            elif in_meta and '-' in line:
                if 'メインキーワード:' in line:
                    meta_info['main_keyword'] = line.split(':', 1)[1].strip()
                elif 'サブキーワード:' in line:
                    meta_info['sub_keywords'] = line.split(':', 1)[1].strip()
                elif '対象読者:' in line:
                    meta_info['target_audience'] = line.split(':', 1)[1].strip()
                elif '記事の目的:' in line:
                    meta_info['purpose'] = line.split(':', 1)[1].strip()
        
        # タイトル抽出
        title = ""
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        # 記事本文抽出（メタ情報とタイトルを除く）
        content_lines = []
        skip_meta = True
        title_found = False
        
        for line in lines:
            if line.strip().endswith('-->'):
                skip_meta = False
                continue
            elif skip_meta:
                continue
            elif line.startswith('# ') and not title_found:
                title_found = True
                continue
            else:
                content_lines.append(line)
        
        content = '\n'.join(content_lines).strip()
        
        return {
            'title': title,
            'content': content,
            'meta_info': meta_info
        }
    
    def optimize_title_seo(self, title):
        """タイトルをSEO最適化（28-32文字）"""
        if len(title) >= 28 and len(title) <= 32:
            return title
        
        if len(title) > 32:
            # 32文字以下に短縮
            # 重要な部分を残して調整
            if '！' in title:
                parts = title.split('！')
                main_part = parts[0]
                if len(main_part) <= 30:
                    return main_part + '！完全ガイド'
            
            # それでも長い場合は切り詰める
            return title[:29] + '...'
        
        elif len(title) < 28:
            # 28文字以上に拡張
            if not '2025年' in title:
                title = title.replace('！', '！2025年最新')
            if len(title) < 28:
                title += '【完全版】'
        
        return title
    
    def generate_meta_description(self, content, max_length=120):
        """メタディスクリプション生成"""
        # 記事の最初の部分から抽出
        text = re.sub(r'[「」\n]', '', content)
        text = re.sub(r'\*\*.*?\*\*', '', text)  # 太字除去
        text = re.sub(r'##.*?\n', '', text)  # 見出し除去
        
        # 最初の文章を取得
        sentences = text.split('。')
        description = ""
        
        for sentence in sentences:
            if sentence.strip() and not sentence.startswith('マフィン'):
                if len(description + sentence + '。') <= max_length:
                    description += sentence + '。'
                else:
                    break
        
        if not description:
            description = "audiobook.jpの単品購入方法とAudible比較、セール情報を詳しく解説。お得に購入する方法をご紹介します。"
        
        return description
    
    def save_draft_to_wordpress(self, article_data):
        """WordPress下書き保存実行"""
        
        print("🔄 WordPress下書き保存を開始...")
        
        # タイトル最適化
        optimized_title = self.optimize_title_seo(article_data['title'])
        print(f"📝 最適化タイトル: {optimized_title} ({len(optimized_title)}文字)")
        
        # 28-32文字の範囲に調整
        if len(optimized_title) < 28:
            optimized_title = article_data['title'][:32] if len(article_data['title']) >= 28 else article_data['title'] + "【2025年最新版】"
        
        print(f"📝 最終タイトル: {optimized_title} ({len(optimized_title)}文字)")
        
        # メタディスクリプション生成  
        meta_description = self.generate_meta_description(article_data['content'])
        print(f"📄 メタディスクリプション: {meta_description[:50]}...")
        
        # 投稿データ構成
        post_data = {
            'title': optimized_title,
            'content': article_data['content'],
            'status': 'draft',  # 下書き状態
            'meta': {
                'description': meta_description,
                '_yoast_wpseo_metadesc': meta_description,  # Yoast SEO
                '_yoast_wpseo_title': optimized_title,
            }
        }
        
        # カテゴリー設定（オーディオブック関連）
        # TODO: カテゴリーIDを動的に取得
        post_data['categories'] = [1]  # 暫定
        
        try:
            # WordPress API投稿
            response = requests.post(
                f"{self.wp.api_url}/posts",
                headers=self.wp.headers,
                json=post_data
            )
            
            if response.status_code in [200, 201]:
                post_id = response.json()['id']
                post_url = response.json()['link']
                
                print(f"✅ WordPress下書き保存成功!")
                print(f"📄 投稿ID: {post_id}")
                print(f"🔗 URL: {post_url}")
                
                # TODO: アイキャッチ画像設定
                # self.set_featured_image(post_id, article_data['meta_info']['main_keyword'])
                
                return {
                    'success': True,
                    'post_id': post_id,
                    'post_url': post_url,
                    'title': optimized_title
                }
            else:
                print(f"❌ 投稿失敗: {response.status_code}")
                print(f"エラー: {response.text}")
                return {'success': False, 'error': response.text}
                
        except Exception as e:
            print(f"❌ 投稿エラー: {e}")
            return {'success': False, 'error': str(e)}
    
    def set_featured_image(self, post_id, keyword):
        """アイキャッチ画像設定（未実装）"""
        # TODO: Unsplash画像取得とWordPress設定
        print(f"🖼️ アイキャッチ画像設定: {keyword} (未実装)")
        pass

def save_article_as_draft(markdown_file_path):
    """マークダウン記事をWordPress下書きとして保存"""
    
    saver = WordPressDraftSaver()
    
    # 接続テスト
    if not saver.wp.test_connection():
        print("❌ WordPress接続失敗")
        return None
    
    # ファイル読み込み
    try:
        with open(markdown_file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except Exception as e:
        print(f"❌ ファイル読み込みエラー: {e}")
        return None
    
    # 記事情報抽出
    article_data = saver.extract_article_info(markdown_content)
    
    # WordPress保存実行
    result = saver.save_draft_to_wordpress(article_data)
    
    return result

if __name__ == "__main__":
    # テスト実行
    article_file = "/Users/satoumasamitsu/osigoto/ブログ自動化/マフィンブログ完成記事/audiobook_jp単品購入ガイド_完成版.md"
    
    result = save_article_as_draft(article_file)
    
    if result and result['success']:
        print(f"\n🎉 記事保存完了!")
        print(f"タイトル: {result['title']}")
        print(f"URL: {result['post_url']}")
    else:
        print(f"\n❌ 記事保存失敗")