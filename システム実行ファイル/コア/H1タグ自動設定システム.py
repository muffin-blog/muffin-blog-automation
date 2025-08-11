"""
H1タグ自動設定システム
記事のH1タグが適切に設定されているかチェックし、必要に応じて修正
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests
import re
from datetime import datetime

class H1タグ自動設定システム:
    """H1タグの設定と最適化"""
    
    def __init__(self):
        self.wp = WordPressBlogAutomator(
            site_url="https://muffin-blog.com",
            username="muffin1203",
            password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
        )
        
        # 対象記事リスト
        self.対象記事リスト = [2732, 2677, 2625, 2535, 2210]
    
    def H1タグ状況確認(self, 記事ID):
        """記事のH1タグ状況を確認"""
        
        try:
            response = requests.get(f"{self.wp.api_url}/posts/{記事ID}", headers=self.wp.headers)
            if response.status_code != 200:
                return None
            
            記事データ = response.json()
            記事タイトル = 記事データ['title']['rendered']
            記事内容 = 記事データ['content']['rendered']
            
            # H1タグを検索
            h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', 記事内容, re.IGNORECASE | re.DOTALL)
            
            状況 = {
                "記事ID": 記事ID,
                "記事タイトル": 記事タイトル,
                "H1タグ数": len(h1_matches),
                "H1タグ内容": h1_matches,
                "記事内容": 記事内容
            }
            
            return 状況
            
        except Exception as e:
            print(f"❌ 記事ID {記事ID}: エラー - {e}")
            return None
    
    def H1タグ最適化(self, 記事ID):
        """H1タグを最適化"""
        
        print(f"🏷️ 記事ID {記事ID} のH1タグ最適化中...")
        
        状況 = self.H1タグ状況確認(記事ID)
        if not 状況:
            return False
        
        記事内容 = 状況["記事内容"]
        記事タイトル = 状況["記事タイトル"]
        
        # バックアップ
        バックアップファイル = f"/Users/satoumasamitsu/osigoto/ブログ自動化/backups/記事{記事ID}_h1_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        os.makedirs(os.path.dirname(バックアップファイル), exist_ok=True)
        with open(バックアップファイル, 'w', encoding='utf-8') as f:
            f.write(記事内容)
        print(f"   💾 バックアップ保存: {os.path.basename(バックアップファイル)}")
        
        更新済み内容 = 記事内容
        変更フラグ = False
        
        # H1タグが存在しない場合は記事タイトルをH1として追加
        if 状況["H1タグ数"] == 0:
            # 記事の最初にH1タグを追加
            h1タグ = f'<h1>{記事タイトル}</h1>'
            
            # 最初のpタグまたはh2タグの前にH1を挿入
            if '<p>' in 更新済み内容:
                更新済み内容 = 更新済み内容.replace('<p>', f'{h1タグ}\n<p>', 1)
                変更フラグ = True
                print(f"   ✅ H1タグ追加: {記事タイトル[:40]}...")
            elif '<h2' in 更新済み内容:
                更新済み内容 = re.sub(r'(<h2[^>]*>)', f'{h1タグ}\n\\1', 更新済み内容, count=1)
                変更フラグ = True
                print(f"   ✅ H1タグ追加: {記事タイトル[:40]}...")
        
        # 複数のH1タグがある場合は最初以外をH2に変換
        elif 状況["H1タグ数"] > 1:
            h1_count = 0
            def h1_replacer(match):
                nonlocal h1_count
                h1_count += 1
                if h1_count == 1:
                    return match.group(0)  # 最初のH1はそのまま
                else:
                    # 2番目以降のH1をH2に変換
                    content = match.group(1)
                    return f'<h2>{content}</h2>'
            
            更新済み内容 = re.sub(r'<h1[^>]*>(.*?)</h1>', h1_replacer, 更新済み内容, flags=re.IGNORECASE | re.DOTALL)
            変更フラグ = True
            print(f"   ✅ 余分なH1タグを{状況['H1タグ数']-1}個H2に変換")
        
        # 変更があった場合のみ更新
        if 変更フラグ:
            更新データ = {'content': 更新済み内容}
            response = requests.post(f"{self.wp.api_url}/posts/{記事ID}", 
                                   headers=self.wp.headers, 
                                   json=更新データ)
            
            if response.status_code == 200:
                print(f"   ✅ 記事ID {記事ID}: H1タグ最適化完了")
                return True
            else:
                print(f"   ❌ 記事ID {記事ID}: 更新失敗 ({response.status_code})")
                return False
        else:
            print(f"   ℹ️ 記事ID {記事ID}: H1タグは既に適切に設定済み")
            return True
    
    def 全記事H1タグ最適化(self):
        """全記事のH1タグを最適化"""
        
        print("🏷️ 全記事H1タグ最適化開始")
        print("=" * 60)
        
        # 現在の状況確認
        print("📊 現在のH1タグ状況:")
        for 記事ID in self.対象記事リスト:
            状況 = self.H1タグ状況確認(記事ID)
            if 状況:
                print(f"記事ID {記事ID}: H1タグ{状況['H1タグ数']}個")
                print(f"   {状況['記事タイトル'][:40]}...")
        
        print("\n" + "-" * 60)
        
        # H1タグ最適化実行
        成功記事数 = 0
        for 記事ID in self.対象記事リスト:
            成功 = self.H1タグ最適化(記事ID)
            if 成功:
                成功記事数 += 1
        
        print(f"\n🎯 H1タグ最適化完了!")
        print(f"処理記事数: {成功記事数}/{len(self.対象記事リスト)}")
        
        # 最適化後の状況確認
        print("\n📊 最適化後のH1タグ状況:")
        for 記事ID in self.対象記事リスト:
            状況 = self.H1タグ状況確認(記事ID)
            if 状況:
                print(f"記事ID {記事ID}: H1タグ{状況['H1タグ数']}個")
                if 状況['H1タグ内容']:
                    print(f"   内容: {状況['H1タグ内容'][0][:40]}...")
        
        return 成功記事数

if __name__ == "__main__":
    print("🏷️ H1タグ自動設定システム")
    print("=" * 60)
    
    H1システム = H1タグ自動設定システム()
    H1システム.全記事H1タグ最適化()
    
    print("\n✅ H1タグ自動設定システム完了")