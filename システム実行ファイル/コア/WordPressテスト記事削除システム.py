"""
WordPressテスト記事削除システム（バックアップ付き）
削除前に自動バックアップ、最新版のみ保持
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests
import json
from datetime import datetime
import glob

class WordPressテスト記事削除システム:
    """バックアップ付きテスト記事削除システム"""
    
    def __init__(self):
        self.wp = WordPressBlogAutomator(
            site_url="https://muffin-blog.com",
            username="muffin1203",
            password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
        )
        
        # バックアップディレクトリ
        self.バックアップディレクトリ = "/Users/satoumasamitsu/osigoto/ブログ自動化/backups/deleted_posts"
        os.makedirs(self.バックアップディレクトリ, exist_ok=True)
        
        # 絶対削除禁止記事（保護対象）
        self.保護記事ID = [
            2732,  # Audibleでお金の勉強（公開済み）
            2677,  # Audible休会制度（公開済み）
            2625,  # Audible退会・解約（公開済み）
            2535,  # Audible始め方ガイド（公開済み）
            2210,  # 耳活で人生が変わる（公開済み）
            649,   # コミっと車検（公開済み）
            2809,  # あなたが作成中：オーディオファースト作品
            2775   # あなたが作成中：読書苦手でもAudible
        ]
        
        # 削除対象記事（明確に指定）
        self.削除対象記事ID = [
            2791,  # 【テスト】Claude自動化システム動作確認
            2833,  # SWELLブロック動作テスト
            2825,  # SWELLブロックテスト
            2819,  # 【吹き出しテスト】...
            2889,  # 重複記事（私の失敗作）
            2808,  # 判断保留：削除対象
            2802,  # 判断保留：削除対象
            2764   # 判断保留：削除対象
        ]
    
    def 記事をバックアップ(self, 記事ID):
        """記事を削除前にバックアップ"""
        
        try:
            # 記事データ取得
            response = requests.get(f"{self.wp.api_url}/posts/{記事ID}", headers=self.wp.headers)
            if response.status_code != 200:
                print(f"❌ 記事ID {記事ID}: 取得失敗")
                return False
                
            記事データ = response.json()
            記事タイトル = 記事データ['title']['rendered']
            
            # バックアップファイル名
            日時 = datetime.now().strftime('%Y%m%d_%H%M%S')
            ファイル名 = f"記事{記事ID}_{日時}.json"
            バックアップファイルパス = os.path.join(self.バックアップディレクトリ, ファイル名)
            
            # バックアップデータ準備
            バックアップデータ = {
                "記事ID": 記事ID,
                "削除日時": datetime.now().isoformat(),
                "記事データ": 記事データ,
                "復元用データ": {
                    "title": 記事データ['title']['rendered'],
                    "content": 記事データ['content']['rendered'],
                    "excerpt": 記事データ['excerpt']['rendered'],
                    "status": 記事データ['status'],
                    "categories": 記事データ['categories'],
                    "tags": 記事データ['tags']
                }
            }
            
            # バックアップ保存
            with open(バックアップファイルパス, 'w', encoding='utf-8') as f:
                json.dump(バックアップデータ, f, ensure_ascii=False, indent=2)
            
            print(f"💾 バックアップ保存: {記事タイトル[:30]}...")
            print(f"   ファイル: {ファイル名}")
            
            # 古いバックアップ削除（最新のみ保持）
            self.古いバックアップ削除(記事ID)
            
            return True
            
        except Exception as e:
            print(f"❌ 記事ID {記事ID}: バックアップ失敗 - {e}")
            return False
    
    def 古いバックアップ削除(self, 記事ID):
        """指定記事の古いバックアップを削除（最新のみ保持）"""
        
        try:
            # 該当記事のバックアップファイルを検索
            パターン = os.path.join(self.バックアップディレクトリ, f"記事{記事ID}_*.json")
            バックアップファイル一覧 = glob.glob(パターン)
            
            # 作成日時順にソート（最新が最後）
            バックアップファイル一覧.sort(key=lambda x: os.path.getctime(x))
            
            # 最新以外を削除
            if len(バックアップファイル一覧) > 1:
                削除対象 = バックアップファイル一覧[:-1]  # 最新以外
                for ファイル in 削除対象:
                    os.remove(ファイル)
                    print(f"   🗑️ 古いバックアップ削除: {os.path.basename(ファイル)}")
                    
        except Exception as e:
            print(f"⚠️ 古いバックアップ削除エラー: {e}")
    
    def 記事を削除(self, 記事ID):
        """記事をWordPressから削除"""
        
        try:
            # 削除実行
            response = requests.delete(
                f"{self.wp.api_url}/posts/{記事ID}?force=true",
                headers=self.wp.headers
            )
            
            if response.status_code == 200:
                print(f"✅ 削除成功: ID{記事ID}")
                return True
            else:
                print(f"❌ 削除失敗: ID{記事ID} ({response.status_code})")
                return False
                
        except Exception as e:
            print(f"❌ 削除エラー: ID{記事ID} - {e}")
            return False
    
    def 安全削除実行(self):
        """安全な削除プロセス実行"""
        
        print("🗑️ WordPressテスト記事削除システム")
        print("=" * 60)
        print(f"削除対象: {len(self.削除対象記事ID)}件")
        print(f"保護対象: {len(self.保護記事ID)}件")
        
        削除成功数 = 0
        バックアップ成功数 = 0
        
        for 記事ID in self.削除対象記事ID:
            print(f"\n🔄 記事ID {記事ID} 処理中...")
            
            # 保護記事チェック（念のため）
            if 記事ID in self.保護記事ID:
                print(f"🛡️ 保護記事のため削除をスキップ")
                continue
            
            # Step 1: バックアップ
            バックアップ成功 = self.記事をバックアップ(記事ID)
            if バックアップ成功:
                バックアップ成功数 += 1
            else:
                print(f"⚠️ バックアップ失敗のため削除を中止")
                continue
            
            # Step 2: 削除実行
            削除成功 = self.記事を削除(記事ID)
            if 削除成功:
                削除成功数 += 1
        
        # 結果報告
        print(f"\n📊 削除プロセス完了")
        print(f"=" * 40)
        print(f"バックアップ成功: {バックアップ成功数}件")
        print(f"削除成功: {削除成功数}件")
        print(f"保護記事数: {len(self.保護記事ID)}件")
        
        # バックアップ一覧表示
        print(f"\n📁 保存されたバックアップ:")
        バックアップファイル = glob.glob(os.path.join(self.バックアップディレクトリ, "*.json"))
        for ファイル in sorted(バックアップファイル):
            ファイル名 = os.path.basename(ファイル)
            サイズ = round(os.path.getsize(ファイル) / 1024, 1)
            print(f"   📄 {ファイル名} ({サイズ}KB)")
        
        return 削除成功数
    
    def 削除記事復元(self, 記事ID):
        """削除した記事をバックアップから復元"""
        
        print(f"🔄 記事ID {記事ID} の復元...")
        
        try:
            # バックアップファイル検索
            パターン = os.path.join(self.バックアップディレクトリ, f"記事{記事ID}_*.json")
            バックアップファイル一覧 = glob.glob(パターン)
            
            if not バックアップファイル一覧:
                print(f"❌ 記事ID {記事ID}: バックアップが見つかりません")
                return False
            
            # 最新のバックアップを取得
            最新バックアップ = max(バックアップファイル一覧, key=lambda x: os.path.getctime(x))
            
            with open(最新バックアップ, 'r', encoding='utf-8') as f:
                バックアップデータ = json.load(f)
            
            復元データ = バックアップデータ["復元用データ"]
            
            # WordPress記事作成
            response = requests.post(
                f"{self.wp.api_url}/posts",
                headers=self.wp.headers,
                json=復元データ
            )
            
            if response.status_code == 201:
                新記事データ = response.json()
                新記事ID = 新記事データ['id']
                print(f"✅ 復元成功: 新記事ID {新記事ID}")
                print(f"   タイトル: {復元データ['title']}")
                return 新記事ID
            else:
                print(f"❌ 復元失敗: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 復元エラー: {e}")
            return False

if __name__ == "__main__":
    print("🗑️ WordPressテスト記事削除システム（バックアップ付き）")
    print("=" * 60)
    
    削除システム = WordPressテスト記事削除システム()
    
    print("🛡️ 保護記事:")
    for 記事ID in 削除システム.保護記事ID:
        print(f"   ID{記事ID}")
    
    print(f"\n🗑️ 削除対象記事:")
    for 記事ID in 削除システム.削除対象記事ID:
        print(f"   ID{記事ID}")
    
    print(f"\n実行しますか？ (y/n): ", end="")
    
    # 自動実行（バッチ処理用）
    確認 = "y"
    print("y")
    
    if 確認.lower() == 'y':
        削除数 = 削除システム.安全削除実行()
        print(f"\n✅ 削除システム完了: {削除数}件削除")
    else:
        print("キャンセルしました")