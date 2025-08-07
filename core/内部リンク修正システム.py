"""
内部リンク修正システム
破損したリンクを修正し、正しい内部リンクを再設定
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests
import re
from datetime import datetime

class 内部リンク修正システム:
    """破損した内部リンクを修正"""
    
    def __init__(self):
        self.wp = WordPressBlogAutomator(
            site_url="https://muffin-blog.com",
            username="muffin1203", 
            password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
        )
    
    def 記事を復元(self, 記事ID):
        """バックアップから記事を復元"""
        
        print(f"📋 記事ID {記事ID} をバックアップから復元中...")
        
        try:
            # 最新のクリーンなバックアップを探す
            バックアップファイル = f"/Users/satoumasamitsu/osigoto/ブログ自動化/backups/記事{記事ID}_backup_20250806_131351.html"
            
            with open(バックアップファイル, 'r', encoding='utf-8') as f:
                元の内容 = f.read()
            
            # WordPress APIで復元
            更新データ = {'content': 元の内容}
            response = requests.post(f"{self.wp.api_url}/posts/{記事ID}", 
                                   headers=self.wp.headers, 
                                   json=更新データ)
            
            if response.status_code == 200:
                print(f"✅ 記事ID {記事ID} 復元完了")
                return True
            else:
                print(f"❌ 記事ID {記事ID} 復元失敗: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 復元エラー: {e}")
            return False
    
    def 正しい内部リンクを追加(self, 記事ID):
        """正しい方法で内部リンクを追加"""
        
        print(f"🔗 記事ID {記事ID} に正しい内部リンクを追加...")
        
        try:
            # 記事取得
            response = requests.get(f"{self.wp.api_url}/posts/{記事ID}", headers=self.wp.headers)
            if response.status_code != 200:
                return False
            
            記事データ = response.json()
            記事内容 = 記事データ['content']['rendered']
            
            # バックアップ
            バックアップファイル = f"/Users/satoumasamitsu/osigoto/ブログ自動化/backups/記事{記事ID}_fixed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            os.makedirs(os.path.dirname(バックアップファイル), exist_ok=True)
            with open(バックアップファイル, 'w', encoding='utf-8') as f:
                f.write(記事内容)
            
            更新済み内容 = 記事内容
            
            # 記事2732専用の安全なリンク追加
            if 記事ID == 2732:
                # 「Audible」を1回だけリンク化（最初の出現のみ、既存リンクを避ける）
                if '忙しくて読書する時間がないので、<strong>Audible</strong>で聴きたい' in 更新済み内容:
                    更新済み内容 = 更新済み内容.replace(
                        '忙しくて読書する時間がないので、<strong>Audible</strong>で聴きたい',
                        '忙しくて読書する時間がないので、<strong><a href="https://muffin-blog.com/?p=2535" title="世界一分かりやすいAudible始め方ガイド">Audible</a></strong>で聴きたい'
                    )
                    print("   ✅ 'Audible'をリンク化")
                
                # 「退会」をリンク化
                if 'でも、いつでも退会できるので安心です。' in 更新済み内容:
                    更新済み内容 = 更新済み内容.replace(
                        'でも、いつでも<strong>退会</strong>できるので安心です。',
                        'でも、いつでも<strong><a href="https://muffin-blog.com/?p=2625" title="Audible退会・解約方法徹底解説">退会</a></strong>できるので安心です。'
                    )
                    print("   ✅ '退会'をリンク化")
            
            # 更新実行
            更新データ = {'content': 更新済み内容}
            更新レスポンス = requests.post(f"{self.wp.api_url}/posts/{記事ID}", 
                                       headers=self.wp.headers, 
                                       json=更新データ)
            
            if 更新レスポンス.status_code == 200:
                print(f"✅ 記事ID {記事ID} 正しいリンク追加完了")
                return True
            else:
                print(f"❌ 記事ID {記事ID} 更新失敗")
                return False
                
        except Exception as e:
            print(f"❌ エラー: {e}")
            return False

if __name__ == "__main__":
    print("🔧 内部リンク修正システム")
    print("=" * 60)
    
    修正システム = 内部リンク修正システム()
    
    # 記事2732を修正
    print("1. バックアップから復元...")
    修正システム.記事を復元(2732)
    
    print("\n2. 正しい内部リンクを追加...")
    修正システム.正しい内部リンクを追加(2732)
    
    print("\n✅ 内部リンク修正完了")