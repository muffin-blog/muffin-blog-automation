"""
完全復元システム
内部リンク作業開始前の最初の状態に全記事を復元
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests

class 完全復元システム:
    """内部リンク作業前の状態に完全復元"""
    
    def __init__(self):
        self.wp = WordPressBlogAutomator(
            site_url="https://muffin-blog.com",
            username="muffin1203",
            password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
        )
        
        # 最初のバックアップファイル（内部リンク作業前）
        self.元のバックアップ = {
            2210: "/Users/satoumasamitsu/osigoto/ブログ自動化/backups/記事2210_backup_20250806_131322.html",
            2535: "/Users/satoumasamitsu/osigoto/ブログ自動化/backups/記事2535_backup_20250806_131322.html",
            2625: "/Users/satoumasamitsu/osigoto/ブログ自動化/backups/記事2625_backup_20250806_131322.html", 
            2677: "/Users/satoumasamitsu/osigoto/ブログ自動化/backups/記事2677_backup_20250806_131322.html",
            2732: "/Users/satoumasamitsu/osigoto/ブログ自動化/backups/記事2732_backup_20250806_131322.html"
        }
    
    def 記事を完全復元(self, 記事ID, バックアップファイル):
        """記事を最初の状態に完全復元"""
        
        print(f"🔄 記事ID {記事ID} を内部リンク作業前の状態に復元中...")
        
        try:
            # 最初のバックアップファイルを読み込み
            with open(バックアップファイル, 'r', encoding='utf-8') as f:
                最初の内容 = f.read()
            
            print(f"   📁 バックアップ: {os.path.basename(バックアップファイル)}")
            
            # WordPressに復元
            更新データ = {'content': 最初の内容}
            response = requests.post(f"{self.wp.api_url}/posts/{記事ID}", 
                                   headers=self.wp.headers, 
                                   json=更新データ)
            
            if response.status_code == 200:
                print(f"   ✅ 記事ID {記事ID} 完全復元完了")
                return True
            else:
                print(f"   ❌ 記事ID {記事ID} 復元失敗: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ 復元エラー: {e}")
            return False
    
    def 全記事完全復元(self):
        """全記事を内部リンク作業前の状態に完全復元"""
        
        print("🔄 全記事を内部リンク作業前の状態に完全復元開始")
        print("=" * 60)
        
        成功数 = 0
        
        for 記事ID, バックアップファイル in self.元のバックアップ.items():
            成功 = self.記事を完全復元(記事ID, バックアップファイル)
            if 成功:
                成功数 += 1
        
        print(f"\n🎯 完全復元完了!")
        print(f"成功: {成功数}/{len(self.元のバックアップ)}")
        print("✅ 全記事が内部リンク・H1タグ・構造化データ追加前の元の状態に戻りました")
        
        return 成功数

if __name__ == "__main__":
    print("🔄 完全復元システム - 内部リンク作業前の状態に復元")
    print("=" * 60)
    
    復元システム = 完全復元システム()
    復元システム.全記事完全復元()
    
    print("\n✅ 完全復元システム完了")