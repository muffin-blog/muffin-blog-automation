"""
不要ファイル削除・整理システム
無駄なファイルとテスト記事を自動削除
"""

import os
import sys
import requests
import json
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator

class ファイル整理システム:
    """不要ファイルとテスト記事の自動削除システム"""
    
    def __init__(self):
        self.wp = WordPressBlogAutomator(
            site_url="https://muffin-blog.com",
            username="muffin1203",
            password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
        )
        
        self.プロジェクトルート = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 削除対象ファイルパターン
        self.削除対象ファイル = [
            "test_openai_integration.py",
            "generate_first_article.py",  # 重複記事作成した失敗作
            "企画書_競合に勝つ記事自動生成システム.md",  # 無駄な企画書
            "advanced_blog_generator.py"  # OpenAI使用の失敗システム
        ]
        
        # 保持すべき重要ファイル
        self.重要ファイル = [
            "wordpress_api.py",  # WordPress API接続
            "site_health_monitor.py",  # サイト監視
            "auto_decision_system.py",  # 自立判断システム
            "ファイル削除・整理システム.py",  # このファイル
            "fix_broken_amazon_links.py",  # リンク修正（成功例）
            "マスタープラン_ブログ改善戦略.md"  # 全体戦略
        ]
    
    def 不要ファイル削除(self):
        """不要なファイルを削除"""
        
        print("🗑️ 不要ファイル削除開始")
        print("=" * 50)
        
        削除カウント = 0
        
        # プロジェクト全体をスキャン
        for root, dirs, files in os.walk(self.プロジェクトルート):
            for file in files:
                ファイルパス = os.path.join(root, file)
                相対パス = os.path.relpath(ファイルパス, self.プロジェクトルート)
                
                # 削除対象かチェック
                if file in self.削除対象ファイル:
                    try:
                        os.remove(ファイルパス)
                        print(f"✅ 削除: {相対パス}")
                        削除カウント += 1
                    except Exception as e:
                        print(f"❌ 削除失敗: {相対パス} - {e}")
                
                # .pycファイル削除
                elif file.endswith('.pyc'):
                    try:
                        os.remove(ファイルパス)
                        print(f"✅ キャッシュ削除: {相対パス}")
                        削除カウント += 1
                    except:
                        pass
        
        print(f"\n📊 削除完了: {削除カウント}ファイル")
        return 削除カウント
    
    def テスト記事削除(self):
        """WordPressのテスト記事を削除"""
        
        print("\n🗑️ WordPressテスト記事削除開始")
        print("=" * 50)
        
        try:
            # 全記事取得
            response = requests.get(f"{self.wp.api_url}/posts?per_page=100", headers=self.wp.headers)
            
            if response.status_code != 200:
                print("❌ 記事取得失敗")
                return 0
            
            posts = response.json()
            削除カウント = 0
            
            # テスト記事の判定
            テスト記事キーワード = [
                "テスト",
                "test", 
                "Test",
                "Claude",
                "自動生成",
                "動作確認"
            ]
            
            保持記事ID = [2732, 2677, 2625, 2535, 2210, 649]  # 重要記事
            
            for post in posts:
                post_id = post['id']
                title = post['title']['rendered']
                status = post['status']
                
                # 重要記事は保護
                if post_id in 保持記事ID:
                    print(f"🛡️ 保護: ID{post_id} - {title}")
                    continue
                
                # テスト記事判定
                is_test = any(keyword in title for keyword in テスト記事キーワード)
                
                # 下書きで3日以上経過した記事
                作成日 = datetime.strptime(post['date'], "%Y-%m-%dT%H:%M:%S")
                経過日数 = (datetime.now() - 作成日).days
                is_old_draft = status == 'draft' and 経過日数 > 3
                
                if is_test or is_old_draft:
                    削除理由 = "テスト記事" if is_test else "古い下書き"
                    
                    print(f"🤔 削除候補: ID{post_id} - {title[:30]}... ({削除理由})")
                    print(f"   削除しますか？ (y/n): ", end="")
                    
                    # 自動判定（テスト記事は自動削除、下書きは確認）
                    if is_test:
                        確認 = "y"
                        print("y (自動)")
                    else:
                        continue  # 下書きは手動確認のため一旦スキップ
                    
                    if 確認.lower() == 'y':
                        try:
                            delete_response = requests.delete(
                                f"{self.wp.api_url}/posts/{post_id}?force=true",
                                headers=self.wp.headers
                            )
                            
                            if delete_response.status_code == 200:
                                print(f"✅ 削除成功: ID{post_id}")
                                削除カウント += 1
                            else:
                                print(f"❌ 削除失敗: ID{post_id}")
                                
                        except Exception as e:
                            print(f"❌ 削除エラー: ID{post_id} - {e}")
            
            print(f"\n📊 テスト記事削除完了: {削除カウント}記事")
            return 削除カウント
            
        except Exception as e:
            print(f"❌ テスト記事削除エラー: {e}")
            return 0
    
    def ファイル構造表示(self):
        """整理後のファイル構造を表示"""
        
        print("\n📁 整理後のファイル構造")
        print("=" * 50)
        
        重要ディレクトリ = ['core', 'scripts', 'reports']
        
        for ディレクトリ in 重要ディレクトリ:
            ディレクトリパス = os.path.join(self.プロジェクトルート, ディレクトリ)
            
            if os.path.exists(ディレクトリパス):
                print(f"\n📂 {ディレクトリ}/")
                
                for file in sorted(os.listdir(ディレクトリパス)):
                    if file.endswith('.py') or file.endswith('.md'):
                        ファイルパス = os.path.join(ディレクトリパス, file)
                        サイズ = os.path.getsize(ファイルパス)
                        サイズKB = round(サイズ / 1024, 1)
                        
                        if file in self.重要ファイル or any(重要 in file for 重要 in ['内部リンク', 'SEO', '監視']):
                            print(f"   ✅ {file} ({サイズKB}KB)")
                        else:
                            print(f"   📄 {file} ({サイズKB}KB)")
    
    def 完全整理実行(self):
        """完全な整理を実行"""
        
        print("🧹 ブログ自動化システム完全整理開始")
        print("=" * 60)
        
        # 1. 不要ファイル削除
        ファイル削除数 = self.不要ファイル削除()
        
        # 2. テスト記事削除  
        記事削除数 = self.テスト記事削除()
        
        # 3. 整理結果表示
        self.ファイル構造表示()
        
        print(f"\n✅ 整理完了")
        print(f"📊 結果:")
        print(f"   削除ファイル数: {ファイル削除数}")
        print(f"   削除記事数: {記事削除数}")
        print(f"   システムがすっきり整理されました！")

if __name__ == "__main__":
    print("🧹 ファイル削除・整理システム")
    print("=" * 50)
    
    整理システム = ファイル整理システム()
    整理システム.完全整理実行()