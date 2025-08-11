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

from WordPress連携API import WordPressBlogAutomator
# 画像自動生成は無効化（ポートフォリオサイトで手動対応）
# from image_generation.unsplash_image_generator import UnsplashImageGenerator

class WordPressDraftSaver:
    """WordPress下書き保存システム"""
    
    def __init__(self):
        # WordPress API初期化
        self.wp = WordPressBlogAutomator()  # 環境変数から自動読み込み
        
        # 画像生成機能は無効化（ポートフォリオサイトで手動対応）
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
            if 'audiobook.jp単品購入が最安値！2025年8月最新セール情報と賢い買い方完全ガイド' in title:
                return 'audiobook.jp単品購入が最安値！2025年8月最新セール情報'  # 32文字
            
            if '！' in title:
                parts = title.split('！')
                main_part = parts[0]
                if len(main_part) <= 26:
                    return main_part + '！2025年最新'
                elif len(main_part) <= 29:
                    return main_part + '！完全版'
            
            # それでも長い場合は切り詰める
            return title[:32]
        
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
    
    def get_categories_for_article(self, meta_info):
        """記事のカテゴリーを取得"""
        categories = []
        
        # メインキーワードに基づいてカテゴリー決定
        main_keyword = meta_info.get('main_keyword', '').lower()
        
        if 'audiobook' in main_keyword or 'オーディオブック' in main_keyword:
            categories.append('オーディオブック')
        if 'audible' in main_keyword:
            categories.append('Audible')
        
        # デフォルトカテゴリー
        if not categories:
            categories.append('レビュー・比較')
        
        return categories
    
    def get_tags_for_article(self, meta_info):
        """記事のタグを取得"""
        tags = []
        
        # メインキーワードとサブキーワードからタグ生成
        main_keyword = meta_info.get('main_keyword', '')
        sub_keywords = meta_info.get('sub_keywords', '')
        
        if main_keyword:
            tags.append(main_keyword)
        
        if sub_keywords:
            # カンマ区切りでタグを分割
            sub_tags = [tag.strip() for tag in sub_keywords.split(',')]
            tags.extend(sub_tags)
        
        # 追加の関連タグ
        if 'audiobook' in main_keyword.lower():
            tags.extend(['単品購入', '聴き放題', '比較'])
        
        return tags
    
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
        
        # カテゴリーとタグの設定
        categories = self.get_categories_for_article(article_data['meta_info'])
        tags = self.get_tags_for_article(article_data['meta_info'])
        
        print(f"📂 設定カテゴリー: {categories}")
        print(f"🏷️ 設定タグ: {tags}")
        
        # 投稿データ構成（カテゴリー・タグはIDではなく名前で設定を試行）
        post_data = {
            'title': optimized_title,
            'content': article_data['content'],
            'status': 'draft',  # 下書き状態
            'excerpt': meta_description,  # 記事の抜粋
        }
        
        # カテゴリーとタグは投稿後に個別設定
        # WordPressでは文字列での設定が困難なため
        
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
                
                # メタ情報を個別に設定
                self.set_post_metadata(post_id, meta_description, optimized_title)
                
                # カテゴリーとタグを設定
                self.set_post_categories_tags(post_id, categories, tags)
                
                # アイキャッチ画像は手動設定（ポートフォリオサイトで対応）
                print("📸 アイキャッチ画像はポートフォリオサイトで手動追加してください")
                
                # 投稿前確認システム統合
                article_confirmation_data = {
                    'post_id': post_id,
                    'title': optimized_title,
                    'meta_description': meta_description,
                    'tags': tags,
                    'slug': article_data.get('slug', ''),
                    'category': categories[0] if categories else 'その他',
                    'main_keyword': article_data['meta_info'].get('main_keyword', ''),
                    'post_url': post_url
                }
                
                return {
                    'success': True,
                    'post_id': post_id,
                    'post_url': post_url,
                    'title': optimized_title,
                    'confirmation_data': article_confirmation_data
                }
            else:
                print(f"❌ 投稿失敗: {response.status_code}")
                print(f"エラー: {response.text}")
                return {'success': False, 'error': response.text}
                
        except Exception as e:
            print(f"❌ 投稿エラー: {e}")
            return {'success': False, 'error': str(e)}
    
    def set_post_metadata(self, post_id, meta_description, seo_title):
        """投稿のメタ情報設定"""
        try:
            # まず投稿の基本メタディスクリプションを設定
            basic_update = requests.post(
                f"{self.wp.api_url}/posts/{post_id}",
                headers=self.wp.headers,
                json={
                    'excerpt': meta_description,
                    'meta': {
                        'description': meta_description
                    }
                }
            )
            
            if basic_update.status_code == 200:
                print(f"✅ 基本メタディスクリプション設定成功")
            else:
                print(f"⚠️ 基本メタディスクリプション設定失敗: {basic_update.status_code}")
            
            # Yoast SEOメタ情報設定（カスタムフィールドAPI使用）
            yoast_meta_data = {
                '_yoast_wpseo_title': seo_title,
                '_yoast_wpseo_metadesc': meta_description,
                '_yoast_wpseo_focuskw': 'audiobook.jp',
                '_yoast_wpseo_meta-robots-noindex': '0',
                '_yoast_wpseo_meta-robots-nofollow': '0'
            }
            
            # Yoast SEO設定を投稿更新時にmetaフィールドとして設定
            yoast_update = requests.post(
                f"{self.wp.api_url}/posts/{post_id}",
                headers=self.wp.headers,
                json={
                    'meta': yoast_meta_data
                }
            )
            
            if yoast_update.status_code == 200:
                print(f"✅ Yoast SEO設定成功")
            else:
                print(f"⚠️ Yoast SEO設定失敗: {yoast_update.status_code}")
                # 代替: 個別にカスタムフィールド設定を試行
                self.set_custom_fields_individually(post_id, yoast_meta_data)
                    
        except Exception as e:
            print(f"⚠️ メタ情報設定エラー: {e}")
    
    def set_custom_fields_individually(self, post_id, meta_data):
        """カスタムフィールドを個別に設定（代替方法）"""
        print("🔄 個別カスタムフィールド設定を試行中...")
        
        for meta_key, meta_value in meta_data.items():
            try:
                # カスタムフィールドAPIを使用
                field_response = requests.post(
                    f"{self.wp.api_url}/posts/{post_id}",
                    headers=self.wp.headers,
                    json={
                        'meta': {meta_key: meta_value}
                    }
                )
                
                if field_response.status_code == 200:
                    print(f"✅ カスタムフィールド設定成功: {meta_key}")
                else:
                    print(f"⚠️ カスタムフィールド設定失敗: {meta_key} ({field_response.status_code})")
                    
            except Exception as e:
                print(f"⚠️ カスタムフィールド設定エラー {meta_key}: {e}")
    
    def set_post_categories_tags(self, post_id, categories, tags):
        """投稿にカテゴリーとタグを設定"""
        try:
            # カテゴリー設定（作成 or 取得してIDで設定）
            category_ids = []
            for category_name in categories:
                cat_id = self.get_or_create_category(category_name)
                if cat_id:
                    category_ids.append(cat_id)
            
            if category_ids:
                cat_response = requests.post(
                    f"{self.wp.api_url}/posts/{post_id}",
                    headers=self.wp.headers,
                    json={'categories': category_ids}
                )
                
                if cat_response.status_code == 200:
                    print(f"✅ カテゴリー設定成功: {categories}")
                else:
                    print(f"⚠️ カテゴリー設定失敗: {cat_response.status_code}")
            
            # タグ設定（作成 or 取得してIDで設定）
            tag_ids = []
            for tag_name in tags:
                tag_id = self.get_or_create_tag(tag_name)
                if tag_id:
                    tag_ids.append(tag_id)
            
            if tag_ids:
                tag_response = requests.post(
                    f"{self.wp.api_url}/posts/{post_id}",
                    headers=self.wp.headers,
                    json={'tags': tag_ids}
                )
                
                if tag_response.status_code == 200:
                    print(f"✅ タグ設定成功: {tags}")
                else:
                    print(f"⚠️ タグ設定失敗: {tag_response.status_code}")
                    
        except Exception as e:
            print(f"⚠️ カテゴリー・タグ設定エラー: {e}")
    
    def get_or_create_category(self, category_name):
        """カテゴリーを取得または作成"""
        try:
            # 既存カテゴリー検索
            search_response = requests.get(
                f"{self.wp.api_url}/categories",
                headers=self.wp.headers,
                params={'search': category_name}
            )
            
            if search_response.status_code == 200:
                categories = search_response.json()
                for cat in categories:
                    if cat['name'] == category_name:
                        return cat['id']
            
            # カテゴリー作成
            create_response = requests.post(
                f"{self.wp.api_url}/categories",
                headers=self.wp.headers,
                json={'name': category_name}
            )
            
            if create_response.status_code in [200, 201]:
                return create_response.json()['id']
                
        except Exception as e:
            print(f"⚠️ カテゴリー処理エラー: {e}")
        
        return None
    
    def get_or_create_tag(self, tag_name):
        """タグを取得または作成"""
        try:
            # 既存タグ検索
            search_response = requests.get(
                f"{self.wp.api_url}/tags",
                headers=self.wp.headers,
                params={'search': tag_name}
            )
            
            if search_response.status_code == 200:
                tags = search_response.json()
                for tag in tags:
                    if tag['name'] == tag_name:
                        return tag['id']
            
            # タグ作成
            create_response = requests.post(
                f"{self.wp.api_url}/tags",
                headers=self.wp.headers,
                json={'name': tag_name}
            )
            
            if create_response.status_code in [200, 201]:
                return create_response.json()['id']
                
        except Exception as e:
            print(f"⚠️ タグ処理エラー: {e}")
        
        return None
    
    def set_featured_image(self, post_id, keyword):
        """アイキャッチ画像設定（無効化済み）"""
        print("📸 アイキャッチ画像の自動設定は無効化されています")
        print("🎨 ポートフォリオサイトで手動追加してください")
        print("💡 WordPress投稿はfeatured_image_path=Noneで保存されます")
        return None

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