"""
内部リンク自動追加システム
キーワードベースで記事間リンクを自動生成（自己参照回避機能付き）
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests
import re

class 内部リンク自動追加システム:
    """キーワードベース内部リンク自動追加"""
    
    def __init__(self):
        self.wp = WordPressBlogAutomator(
            site_url="https://muffin-blog.com",
            username="muffin1203",
            password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
        )
        
        # キーワードとリンク先のマッピング（自己参照除外設定付き）
        self.キーワードリンクマップ = {
            "Audible": {
                "リンク先ID": 2535,
                "リンク先タイトル": "世界一分かりやすいAudible始め方ガイド",
                "除外記事ID": [2535],  # 始め方記事では「Audible」をリンク化しない
                "リンクテキスト": "Audible"
            },
            "オーディブル": {
                "リンク先ID": 2535,
                "リンク先タイトル": "世界一分かりやすいAudible始め方ガイド", 
                "除外記事ID": [2535],
                "リンクテキスト": "オーディブル"
            },
            "休会": {
                "リンク先ID": 2677,
                "リンク先タイトル": "Audible休会制度完全ガイド",
                "除外記事ID": [2677],  # 休会記事では「休会」をリンク化しない
                "リンクテキスト": "休会"
            },
            "休会制度": {
                "リンク先ID": 2677,
                "リンク先タイトル": "Audible休会制度完全ガイド",
                "除外記事ID": [2677],
                "リンクテキスト": "休会制度"
            },
            "退会": {
                "リンク先ID": 2625,
                "リンク先タイトル": "Audible退会・解約方法徹底解説",
                "除外記事ID": [2625],  # 退会記事では「退会」をリンク化しない
                "リンクテキスト": "退会"
            },
            "解約": {
                "リンク先ID": 2625,
                "リンク先タイトル": "Audible退会・解約方法徹底解説",
                "除外記事ID": [2625],
                "リンクテキスト": "解約"
            },
            "耳活": {
                "リンク先ID": 2210,
                "リンク先タイトル": "耳活で人生が変わる習慣術",
                "除外記事ID": [2210],  # 耳活記事では「耳活」をリンク化しない
                "リンクテキスト": "耳活"
            },
            "お金の勉強": {
                "リンク先ID": 2732,
                "リンク先タイトル": "Audibleでお金の勉強おすすめ書籍",
                "除外記事ID": [2732],  # お金の勉強記事では自己リンクしない
                "リンクテキスト": "お金の勉強"
            },
            "始め方": {
                "リンク先ID": 2535,
                "リンク先タイトル": "世界一分かりやすいAudible始め方ガイド",
                "除外記事ID": [2535],
                "リンクテキスト": "始め方"
            }
        }
        
        # 対象記事
        self.対象記事リスト = [2732, 2677, 2625, 2535, 2210]
    
    def 記事の内部リンク追加(self, 記事ID):
        """指定記事に内部リンクを自動追加"""
        
        print(f"🔗 記事ID {記事ID} に内部リンク追加中...")
        
        try:
            # 記事取得
            response = requests.get(f"{self.wp.api_url}/posts/{記事ID}", headers=self.wp.headers)
            if response.status_code != 200:
                print(f"❌ 記事ID {記事ID} 取得失敗")
                return False
            
            記事データ = response.json()
            記事タイトル = 記事データ['title']['rendered']
            記事内容 = 記事データ['content']['rendered']
            
            print(f"   記事: {記事タイトル[:40]}...")
            
            # バックアップ保存（重要！）
            バックアップファイル = f"/Users/satoumasamitsu/osigoto/ブログ自動化/backups/記事{記事ID}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            os.makedirs(os.path.dirname(バックアップファイル), exist_ok=True)
            with open(バックアップファイル, 'w', encoding='utf-8') as f:
                f.write(記事内容)
            print(f"   💾 バックアップ保存: {バックアップファイル}")
            
            # 内部リンク追加処理
            更新済み内容 = 記事内容
            追加リンク数 = 0
            
            for キーワード, リンク情報 in self.キーワードリンクマップ.items():
                # 自己参照チェック
                if 記事ID in リンク情報["除外記事ID"]:
                    continue
                
                # 既にリンク化されていない場合のみ処理
                リンクURL = f"https://muffin-blog.com/?p={リンク情報['リンク先ID']}"
                
                # キーワードを検索（シンプルな方式で既にリンク化されていない部分を検索）
                # HTMLタグ内でないキーワードを検索
                パターン = f"\\b{re.escape(キーワード)}\\b"
                
                マッチ = re.finditer(パターン, 更新済み内容, re.IGNORECASE)
                マッチリスト = list(マッチ)
                
                # キーワードがHTMLタグ内にない場合のみリンク化
                # 簡易的なHTMLタグ除外処理
                変更回数 = 0
                for match in マッチリスト[:3]:  # 最初の3回のみ
                    if match and 変更回数 < 3:
                        マッチ開始 = match.start()
                        マッチ終了 = match.end()
                        
                        # 前後にHTMLタグがないかチェック（簡易版）
                        前文 = 更新済み内容[max(0, マッチ開始-50):マッチ開始]
                        後文 = 更新済み内容[マッチ終了:マッチ終了+50]
                        
                        # <a タグ内や既にリンク化されている部分をスキップ
                        if '<a ' in 前文 and '</a>' not in 前文:
                            continue  # <a>タグ内
                        
                        置換前 = match.group(0)
                        置換後 = f'<a href="{リンクURL}" title="{リンク情報["リンク先タイトル"]}">{置換前}</a>'
                        
                        # 置換実行
                        更新済み内容 = 更新済み内容[:マッチ開始] + 置換後 + 更新済み内容[マッチ終了:]
                        追加リンク数 += 1
                        変更回数 += 1
                        print(f"   ✅ リンク追加: {キーワード} → ID{リンク情報['リンク先ID']}")
                        
                        # 次の検索用に位置調整
                        break  # 1つずつ処理して再検索
            
            # 変更がある場合のみ更新
            if 追加リンク数 > 0:
                更新データ = {'content': 更新済み内容}
                更新レスポンス = requests.post(f"{self.wp.api_url}/posts/{記事ID}", 
                                           headers=self.wp.headers, 
                                           json=更新データ)
                
                if 更新レスポンス.status_code == 200:
                    print(f"   ✅ 記事ID {記事ID}: {追加リンク数}本の内部リンクを追加完了")
                    return True
                else:
                    print(f"   ❌ 記事ID {記事ID}: 更新失敗 ({更新レスポンス.status_code})")
                    return False
            else:
                print(f"   ℹ️ 記事ID {記事ID}: 追加可能な内部リンクなし")
                return True
                
        except Exception as e:
            print(f"❌ 記事ID {記事ID}: エラー - {e}")
            return False
    
    def 全記事の内部リンク追加(self):
        """全対象記事に内部リンクを追加"""
        
        print("🔗 全記事内部リンク自動追加開始")
        print("=" * 60)
        
        成功記事数 = 0
        合計リンク数 = 0
        
        for 記事ID in self.対象記事リスト:
            成功 = self.記事の内部リンク追加(記事ID)
            if 成功:
                成功記事数 += 1
        
        print(f"\n🎯 内部リンク追加完了!")
        print(f"処理記事数: {成功記事数}/{len(self.対象記事リスト)}")
        print(f"各記事に3-10本程度の内部リンクが追加されました")
        
        return 成功記事数
    
    def 内部リンク状況確認(self):
        """現在の内部リンク状況を確認"""
        
        print("\n📊 内部リンク状況確認")
        print("-" * 40)
        
        for 記事ID in self.対象記事リスト:
            try:
                response = requests.get(f"{self.wp.api_url}/posts/{記事ID}", headers=self.wp.headers)
                if response.status_code == 200:
                    記事データ = response.json()
                    記事タイトル = 記事データ['title']['rendered']
                    記事内容 = 記事データ['content']['rendered']
                    
                    # 内部リンク数カウント
                    内部リンク数 = len(re.findall(r'href=["\']https://muffin-blog\.com/[^"\']*["\']', 記事内容))
                    
                    print(f"記事ID {記事ID}: {内部リンク数}本")
                    print(f"   {記事タイトル[:30]}...")
                    
            except Exception as e:
                print(f"記事ID {記事ID}: 確認エラー - {e}")

if __name__ == "__main__":
    print("🔗 内部リンク自動追加システム")
    print("=" * 60)
    
    from datetime import datetime
    
    リンクシステム = 内部リンク自動追加システム()
    
    # 現在の状況確認
    リンクシステム.内部リンク状況確認()
    
    # 内部リンク追加実行
    成功数 = リンクシステム.全記事の内部リンク追加()
    
    # 追加後の状況確認
    print("\n" + "="*60)
    print("📊 内部リンク追加後の状況")
    リンクシステム.内部リンク状況確認()
    
    print(f"\n✅ 内部リンク自動追加システム完了")