"""
WordPressサイトバックアップシステム
記事データ、メディア、設定情報を自動バックアップ
"""

import os
import sys
import requests
import json
from datetime import datetime
import time

# パスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator

class WordPressBackupSystem:
    """WordPressバックアップシステム"""
    
    def __init__(self):
        # WordPress API初期化
        self.wp = WordPressBlogAutomator(
            site_url="https://muffin-blog.com",
            username="muffin1203", 
            password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
        )
        
        # バックアップ保存先ディレクトリ
        self.backup_dir = "/Users/satoumasamitsu/osigoto/ブログ自動化/バックアップ・復元/backups"
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # 現在時刻でバックアップフォルダ作成
        self.current_backup_dir = os.path.join(
            self.backup_dir, 
            f"wordpress_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        os.makedirs(self.current_backup_dir, exist_ok=True)
    
    def backup_posts(self):
        """全記事をバックアップ"""
        print("📄 記事データをバックアップ中...")
        
        try:
            # 全記事を取得（公開済み + 下書き）
            all_posts = []
            page = 1
            per_page = 100
            
            while True:
                response = requests.get(
                    f"{self.wp.api_url}/posts",
                    headers=self.wp.headers,
                    params={
                        'page': page,
                        'per_page': per_page,
                        'status': 'publish,draft,private'
                    }
                )
                
                if response.status_code != 200:
                    break
                
                posts = response.json()
                if not posts:
                    break
                
                all_posts.extend(posts)
                page += 1
                
                print(f"  📝 {len(posts)}件の記事を取得 (ページ{page-1})")
                time.sleep(0.5)  # API制限対策
            
            # JSONファイルとして保存
            posts_file = os.path.join(self.current_backup_dir, "posts_backup.json")
            with open(posts_file, 'w', encoding='utf-8') as f:
                json.dump(all_posts, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 記事バックアップ完了: {len(all_posts)}件 → {posts_file}")
            return len(all_posts)
            
        except Exception as e:
            print(f"❌ 記事バックアップエラー: {e}")
            return 0
    
    def backup_pages(self):
        """固定ページをバックアップ"""
        print("📑 固定ページをバックアップ中...")
        
        try:
            # 全固定ページを取得
            response = requests.get(
                f"{self.wp.api_url}/pages",
                headers=self.wp.headers,
                params={'per_page': 100, 'status': 'publish,draft,private'}
            )
            
            if response.status_code == 200:
                pages = response.json()
                
                # JSONファイルとして保存
                pages_file = os.path.join(self.current_backup_dir, "pages_backup.json")
                with open(pages_file, 'w', encoding='utf-8') as f:
                    json.dump(pages, f, ensure_ascii=False, indent=2)
                
                print(f"✅ 固定ページバックアップ完了: {len(pages)}件")
                return len(pages)
            else:
                print(f"⚠️ 固定ページ取得失敗: {response.status_code}")
                return 0
                
        except Exception as e:
            print(f"❌ 固定ページバックアップエラー: {e}")
            return 0
    
    def backup_categories(self):
        """カテゴリーをバックアップ"""
        print("📂 カテゴリーをバックアップ中...")
        
        try:
            response = requests.get(
                f"{self.wp.api_url}/categories",
                headers=self.wp.headers,
                params={'per_page': 100}
            )
            
            if response.status_code == 200:
                categories = response.json()
                
                # JSONファイルとして保存
                categories_file = os.path.join(self.current_backup_dir, "categories_backup.json")
                with open(categories_file, 'w', encoding='utf-8') as f:
                    json.dump(categories, f, ensure_ascii=False, indent=2)
                
                print(f"✅ カテゴリーバックアップ完了: {len(categories)}件")
                return len(categories)
            else:
                print(f"⚠️ カテゴリー取得失敗: {response.status_code}")
                return 0
                
        except Exception as e:
            print(f"❌ カテゴリーバックアップエラー: {e}")
            return 0
    
    def backup_tags(self):
        """タグをバックアップ"""
        print("🏷️ タグをバックアップ中...")
        
        try:
            response = requests.get(
                f"{self.wp.api_url}/tags",
                headers=self.wp.headers,
                params={'per_page': 100}
            )
            
            if response.status_code == 200:
                tags = response.json()
                
                # JSONファイルとして保存
                tags_file = os.path.join(self.current_backup_dir, "tags_backup.json")
                with open(tags_file, 'w', encoding='utf-8') as f:
                    json.dump(tags, f, ensure_ascii=False, indent=2)
                
                print(f"✅ タグバックアップ完了: {len(tags)}件")
                return len(tags)
            else:
                print(f"⚠️ タグ取得失敗: {response.status_code}")
                return 0
                
        except Exception as e:
            print(f"❌ タグバックアップエラー: {e}")
            return 0
    
    def backup_media(self):
        """メディアファイル情報をバックアップ"""
        print("🖼️ メディアファイルをバックアップ中...")
        
        try:
            # メディアライブラリの情報を取得
            all_media = []
            page = 1
            
            while True:
                response = requests.get(
                    f"{self.wp.api_url}/media",
                    headers=self.wp.headers,
                    params={
                        'page': page,
                        'per_page': 100
                    }
                )
                
                if response.status_code != 200:
                    break
                
                media = response.json()
                if not media:
                    break
                
                all_media.extend(media)
                page += 1
                
                print(f"  🖼️ {len(media)}件のメディアを取得")
                time.sleep(0.5)
            
            # JSONファイルとして保存
            media_file = os.path.join(self.current_backup_dir, "media_backup.json")
            with open(media_file, 'w', encoding='utf-8') as f:
                json.dump(all_media, f, ensure_ascii=False, indent=2)
            
            print(f"✅ メディアバックアップ完了: {len(all_media)}件")
            return len(all_media)
            
        except Exception as e:
            print(f"❌ メディアバックアップエラー: {e}")
            return 0
    
    def backup_users(self):
        """ユーザー情報をバックアップ"""
        print("👤 ユーザー情報をバックアップ中...")
        
        try:
            response = requests.get(
                f"{self.wp.api_url}/users",
                headers=self.wp.headers,
                params={'per_page': 100}
            )
            
            if response.status_code == 200:
                users = response.json()
                
                # パスワード等機密情報を除去
                safe_users = []
                for user in users:
                    safe_user = {
                        'id': user.get('id'),
                        'name': user.get('name'),
                        'slug': user.get('slug'),
                        'description': user.get('description'),
                        'roles': user.get('roles'),
                        'capabilities': user.get('capabilities')
                    }
                    safe_users.append(safe_user)
                
                # JSONファイルとして保存
                users_file = os.path.join(self.current_backup_dir, "users_backup.json")
                with open(users_file, 'w', encoding='utf-8') as f:
                    json.dump(safe_users, f, ensure_ascii=False, indent=2)
                
                print(f"✅ ユーザーバックアップ完了: {len(safe_users)}件")
                return len(safe_users)
            else:
                print(f"⚠️ ユーザー取得失敗: {response.status_code}")
                return 0
                
        except Exception as e:
            print(f"❌ ユーザーバックアップエラー: {e}")
            return 0
    
    def create_backup_summary(self, stats):
        """バックアップサマリーを作成"""
        summary = {
            'backup_date': datetime.now().isoformat(),
            'site_url': 'https://muffin-blog.com',
            'backup_location': self.current_backup_dir,
            'statistics': stats,
            'total_items': sum(stats.values())
        }
        
        summary_file = os.path.join(self.current_backup_dir, "backup_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        # Markdown形式のサマリーも作成
        md_summary = f"""# WordPressバックアップレポート

## バックアップ情報
- **実行日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
- **サイトURL**: https://muffin-blog.com
- **保存先**: {self.current_backup_dir}

## バックアップ統計
- **記事**: {stats.get('posts', 0)}件
- **固定ページ**: {stats.get('pages', 0)}件
- **カテゴリー**: {stats.get('categories', 0)}件
- **タグ**: {stats.get('tags', 0)}件
- **メディアファイル**: {stats.get('media', 0)}件
- **ユーザー**: {stats.get('users', 0)}件

**合計**: {sum(stats.values())}項目

## バックアップファイル
- `posts_backup.json` - 全記事データ
- `pages_backup.json` - 固定ページデータ
- `categories_backup.json` - カテゴリーデータ
- `tags_backup.json` - タグデータ
- `media_backup.json` - メディアファイル情報
- `users_backup.json` - ユーザー情報（機密情報除く）
- `backup_summary.json` - バックアップサマリー

## 注意事項
- このバックアップはWordPress REST API経由で取得したデータです
- データベースの完全バックアップではありません
- 復元時は各種制約にご注意ください
"""
        
        md_file = os.path.join(self.current_backup_dir, "バックアップレポート.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_summary)
        
        return summary
    
    def execute_full_backup(self):
        """完全バックアップを実行"""
        print(f"🚀 WordPressバックアップを開始...")
        print(f"📁 バックアップ先: {self.current_backup_dir}")
        
        if not self.wp.test_connection():
            print("❌ WordPress接続失敗")
            return None
        
        # バックアップ統計
        stats = {}
        
        # 各種データのバックアップ
        stats['posts'] = self.backup_posts()
        stats['pages'] = self.backup_pages() 
        stats['categories'] = self.backup_categories()
        stats['tags'] = self.backup_tags()
        stats['media'] = self.backup_media()
        stats['users'] = self.backup_users()
        
        # サマリー作成
        summary = self.create_backup_summary(stats)
        
        print(f"\n🎉 WordPressバックアップ完了!")
        print(f"📊 合計 {sum(stats.values())} 項目をバックアップ")
        print(f"📁 保存先: {self.current_backup_dir}")
        
        return summary

def execute_wordpress_backup():
    """WordPressバックアップ実行関数"""
    backup_system = WordPressBackupSystem()
    return backup_system.execute_full_backup()

if __name__ == "__main__":
    # バックアップ実行
    result = execute_wordpress_backup()
    
    if result:
        print(f"\n✅ バックアップ成功")
        print(f"保存先: {result['backup_location']}")
    else:
        print(f"\n❌ バックアップ失敗")