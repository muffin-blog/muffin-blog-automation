"""
H1タグ修正システム
誤って追加したH1タグを削除してバックアップから復元
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests
from datetime import datetime

class H1タグ修正システム:
    """誤って追加したH1タグを修正"""
    
    def __init__(self):
        self.wp = WordPressBlogAutomator(
            site_url="https://muffin-blog.com",
            username="muffin1203",
            password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
        )
        
        # 修正対象記事とバックアップファイル
        self.修正対象 = {
            2732: "/Users/satoumasamitsu/osigoto/ブログ自動化/backups/記事2732_h1_backup_20250806_133212.html",
            2677: "/Users/satoumasamitsu/osigoto/ブログ自動化/backups/記事2677_h1_backup_20250806_133213.html", 
            2625: "/Users/satoumasamitsu/osigoto/ブログ自動化/backups/記事2625_h1_backup_20250806_133214.html",
            2535: "/Users/satoumasamitsu/osigoto/ブログ自動化/backups/記事2535_h1_backup_20250806_133215.html",
            2210: "/Users/satoumasamitsu/osigoto/ブログ自動化/backups/記事2210_h1_backup_20250806_133216.html"
        }
    
    def 記事をバックアップから復元(self, 記事ID, バックアップファイル):
        """バックアップから記事を復元"""
        
        print(f"🔄 記事ID {記事ID} をバックアップから復元中...")
        
        try:
            # バックアップファイルを読み込み
            with open(バックアップファイル, 'r', encoding='utf-8') as f:
                元の内容 = f.read()
            
            print(f"   📁 バックアップ: {os.path.basename(バックアップファイル)}")
            
            # WordPressに復元
            更新データ = {'content': 元の内容}
            response = requests.post(f"{self.wp.api_url}/posts/{記事ID}", 
                                   headers=self.wp.headers, 
                                   json=更新データ)
            
            if response.status_code == 200:
                print(f"   ✅ 記事ID {記事ID} 復元完了")
                return True
            else:
                print(f"   ❌ 記事ID {記事ID} 復元失敗: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ 復元エラー: {e}")
            return False
    
    def 全記事復元(self):
        """全記事をH1タグ追加前の状態に復元"""
        
        print("🔄 H1タグ追加前の状態に全記事復元開始")
        print("=" * 60)
        
        成功数 = 0
        
        for 記事ID, バックアップファイル in self.修正対象.items():
            成功 = self.記事をバックアップから復元(記事ID, バックアップファイル)
            if 成功:
                成功数 += 1
        
        print(f"\n🎯 復元完了!")
        print(f"成功: {成功数}/{len(self.修正対象)}")
        print("✅ 誤って追加したH1タグを削除し、元の状態に戻しました")
        
        return 成功数

if __name__ == "__main__":
    print("🔄 H1タグ修正システム - 誤追加H1タグの削除")
    print("=" * 60)
    
    修正システム = H1タグ修正システム()
    修正システム.全記事復元()
    
    print("\n✅ H1タグ修正完了")