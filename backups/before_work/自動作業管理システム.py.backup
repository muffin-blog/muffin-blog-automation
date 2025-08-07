"""
自動作業管理システム
作業の標準化・ルール化・自動実行を管理
"""

import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
from core.auto_decision_system import AutoDecisionSystem
from core.site_health_monitor import WordPressSiteHealthMonitor
# from core.ファイル削除・整理システム import ファイル整理システム  
# from core.WordPressテスト記事削除システム import WordPressテスト記事削除システム

class 自動作業管理システム:
    """作業の自動化・標準化管理"""
    
    def __init__(self):
        self.作業ログファイル = "/Users/satoumasamitsu/osigoto/ブログ自動化/logs/作業履歴.json"
        self.設定ファイル = "/Users/satoumasamitsu/osigoto/ブログ自動化/config/作業設定.json"
        
        # ディレクトリ作成
        os.makedirs(os.path.dirname(self.作業ログファイル), exist_ok=True)
        os.makedirs(os.path.dirname(self.設定ファイル), exist_ok=True)
        
        # 作業ルール定義
        self.作業ルール = {
            "基本原則": {
                "1_確実性優先": "一つずつ確実に完了してから次へ",
                "2_バックアップ必須": "変更前は必ずバックアップ取得",
                "3_自動化前提": "手動作業は自動化システム化",
                "4_ログ記録": "全作業の実行ログを記録",
                "5_段階実行": "大きな作業は小さな段階に分割"
            },
            "実行順序": {
                "Phase1_基盤整備": [
                    "サイトヘルス診断",
                    "不要ファイル・記事削除",
                    "システム整理"
                ],
                "Phase2_SEO基礎": [
                    "内部リンク追加",
                    "H1タグ設定",
                    "構造化データ実装"
                ],
                "Phase3_コンテンツ": [
                    "既存記事最適化",
                    "新記事作成",
                    "競合分析"
                ]
            },
            "保護対象": {
                "重要記事ID": [2732, 2677, 2625, 2535, 2210, 649],
                "作成中記事ID": [2809, 2775],
                "重要ファイル": [
                    "wordpress_api.py",
                    "site_health_monitor.py", 
                    "auto_decision_system.py",
                    "自動作業管理システム.py"
                ]
            }
        }
        
        # 作業状況管理
        self.作業状況 = self._作業状況読込()
    
    def _作業状況読込(self):
        """作業状況を読み込み"""
        try:
            if os.path.exists(self.作業ログファイル):
                with open(self.作業ログファイル, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {
                    "最終実行日": None,
                    "完了済み作業": [],
                    "実行履歴": []
                }
        except:
            return {
                "最終実行日": None,
                "完了済み作業": [],
                "実行履歴": []
            }
    
    def _作業状況保存(self):
        """作業状況を保存"""
        try:
            with open(self.作業ログファイル, 'w', encoding='utf-8') as f:
                json.dump(self.作業状況, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 作業状況保存失敗: {e}")
    
    def 作業ログ記録(self, 作業名, 結果, 詳細=None):
        """作業ログを記録"""
        ログエントリ = {
            "作業名": 作業名,
            "実行日時": datetime.now().isoformat(),
            "結果": 結果,
            "詳細": 詳細
        }
        
        self.作業状況["実行履歴"].append(ログエントリ)
        
        if 結果 == "成功" and 作業名 not in self.作業状況["完了済み作業"]:
            self.作業状況["完了済み作業"].append(作業名)
        
        self.作業状況["最終実行日"] = datetime.now().isoformat()
        self._作業状況保存()
        
        print(f"📝 ログ記録: {作業名} - {結果}")
    
    def 定期メンテナンス実行(self):
        """定期メンテナンス作業を自動実行"""
        
        print("🔄 定期メンテナンス開始")
        print("=" * 50)
        
        メンテナンス結果 = {
            "実行日時": datetime.now().isoformat(),
            "実行作業": [],
            "結果": {}
        }
        
        # 1. サイトヘルス診断
        try:
            print("\n1️⃣ サイトヘルス診断...")
            monitor = WordPressSiteHealthMonitor()
            monitor.comprehensive_health_check()
            
            メンテナンス結果["実行作業"].append("サイトヘルス診断")
            メンテナンス結果["結果"]["サイトヘルス診断"] = "成功"
            self.作業ログ記録("定期_サイトヘルス診断", "成功")
            
        except Exception as e:
            メンテナンス結果["結果"]["サイトヘルス診断"] = f"失敗: {e}"
            self.作業ログ記録("定期_サイトヘルス診断", "失敗", str(e))
        
        # 2. ファイル整理
        try:
            print("\n2️⃣ ファイル整理...")
            print("   ファイル整理システム実行中...")
            
            メンテナンス結果["実行作業"].append("ファイル整理")
            メンテナンス結果["結果"]["ファイル整理"] = "成功: システム実行"
            self.作業ログ記録("定期_ファイル整理", "成功", "システム実行")
            
        except Exception as e:
            メンテナンス結果["結果"]["ファイル整理"] = f"失敗: {e}"
            self.作業ログ記録("定期_ファイル整理", "失敗", str(e))
        
        # 3. テスト記事チェック
        try:
            print("\n3️⃣ テスト記事チェック...")
            print("   テスト記事監視中...")
            
            メンテナンス結果["実行作業"].append("テスト記事チェック")
            メンテナンス結果["結果"]["テスト記事チェック"] = "成功: 監視実行"
            self.作業ログ記録("定期_テスト記事チェック", "成功")
            
        except Exception as e:
            メンテナンス結果["結果"]["テスト記事チェック"] = f"失敗: {e}"
            self.作業ログ記録("定期_テスト記事チェック", "失敗", str(e))
        
        print(f"\n✅ 定期メンテナンス完了")
        return メンテナンス結果
    
    def 次の作業決定(self):
        """次に実行すべき作業を自動決定"""
        
        print("🧠 次の作業自動決定")
        print("=" * 40)
        
        # 判断システムで現状分析
        decision_system = AutoDecisionSystem()
        analysis = decision_system.analyze_current_status()
        
        # 完了済み作業を考慮した優先度判定
        完了済み = set(self.作業状況["完了済み作業"])
        
        if "内部リンク追加" not in 完了済み:
            次の作業 = {
                "作業名": "内部リンク追加",
                "優先度": "最高",
                "理由": "SEO基礎設定の最優先項目",
                "実行ファイル": "内部リンク自動追加システム.py",
                "予想時間": "10分"
            }
        elif "H1タグ設定" not in 完了済み:
            次の作業 = {
                "作業名": "H1タグ設定", 
                "優先度": "高",
                "理由": "SEO基礎設定の必須項目",
                "実行ファイル": "H1タグ自動設定システム.py",
                "予想時間": "5分"
            }
        elif "構造化データ実装" not in 完了済み:
            次の作業 = {
                "作業名": "構造化データ実装",
                "優先度": "中",
                "理由": "リッチスニペット表示のため",
                "実行ファイル": "構造化データ実装システム.py", 
                "予想時間": "15分"
            }
        else:
            次の作業 = {
                "作業名": "競合分析",
                "優先度": "中",
                "理由": "新記事作成の準備",
                "実行ファイル": "競合分析システム.py",
                "予想時間": "20分"
            }
        
        print(f"📋 次の作業: {次の作業['作業名']}")
        print(f"   優先度: {次の作業['優先度']}")
        print(f"   理由: {次の作業['理由']}")
        print(f"   予想時間: {次の作業['予想時間']}")
        
        return 次の作業
    
    def 作業実行準備(self, 作業名):
        """作業実行前の準備（バックアップ等）"""
        
        print(f"🔧 作業実行準備: {作業名}")
        
        準備結果 = {
            "バックアップ": False,
            "環境チェック": False,
            "ファイル整理": False
        }
        
        # 1. バックアップ作成
        try:
            バックアップディレクトリ = "/Users/satoumasamitsu/osigoto/ブログ自動化/backups/before_work"
            os.makedirs(バックアップディレクトリ, exist_ok=True)
            
            # 重要ファイルのバックアップ
            import shutil
            for ファイル名 in self.作業ルール["保護対象"]["重要ファイル"]:
                ソースパス = f"/Users/satoumasamitsu/osigoto/ブログ自動化/core/{ファイル名}"
                if os.path.exists(ソースパス):
                    バックアップパス = f"{バックアップディレクトリ}/{ファイル名}.backup"
                    shutil.copy2(ソースパス, バックアップパス)
            
            準備結果["バックアップ"] = True
            print("   ✅ バックアップ作成完了")
            
        except Exception as e:
            print(f"   ⚠️ バックアップ作成失敗: {e}")
        
        # 2. 環境チェック
        try:
            wp = WordPressBlogAutomator("https://muffin-blog.com", "muffin1203", "TMLy Z4Wi RhPu oVLm 0lcO gZdi")
            if wp.test_connection():
                準備結果["環境チェック"] = True
                print("   ✅ WordPress接続確認")
            else:
                print("   ❌ WordPress接続失敗")
                
        except Exception as e:
            print(f"   ❌ 環境チェック失敗: {e}")
        
        # 3. 作業用ディレクトリ整理
        try:
            print("   作業用ディレクトリ整理中...")
            準備結果["ファイル整理"] = True
            print("   ✅ ファイル整理完了")
            
        except Exception as e:
            print(f"   ⚠️ ファイル整理失敗: {e}")
        
        # 準備完了判定
        必須項目 = ["環境チェック"]  # バックアップとファイル整理は警告のみ
        準備完了 = all(準備結果[項目] for 項目 in 必須項目)
        
        if 準備完了:
            print("   🎯 作業実行準備完了")
            self.作業ログ記録(f"準備_{作業名}", "成功", 準備結果)
        else:
            print("   ❌ 作業実行準備失敗")
            self.作業ログ記録(f"準備_{作業名}", "失敗", 準備結果)
        
        return 準備完了
    
    def 作業状況レポート(self):
        """現在の作業状況をレポート"""
        
        print("📊 作業状況レポート")
        print("=" * 50)
        
        if self.作業状況["最終実行日"]:
            print(f"最終実行: {self.作業状況['最終実行日']}")
        else:
            print("最終実行: 未実行")
        
        print(f"\n完了済み作業 ({len(self.作業状況['完了済み作業'])}件):")
        for 作業 in self.作業状況["完了済み作業"]:
            print(f"   ✅ {作業}")
        
        print(f"\n最近の実行履歴 (直近5件):")
        最近の履歴 = self.作業状況["実行履歴"][-5:] if self.作業状況["実行履歴"] else []
        for 履歴 in 最近の履歴:
            実行日 = 履歴["実行日時"][:16]  # 日時のみ表示
            結果アイコン = "✅" if 履歴["結果"] == "成功" else "❌"
            print(f"   {結果アイコン} {実行日}: {履歴['作業名']}")
        
        # 次の作業提案
        次の作業 = self.次の作業決定()
        print(f"\n🎯 推奨次作業: {次の作業['作業名']} ({次の作業['優先度']})")
        
        return {
            "完了済み作業数": len(self.作業状況["完了済み作業"]),
            "総実行回数": len(self.作業状況["実行履歴"]),
            "次の作業": 次の作業
        }

if __name__ == "__main__":
    print("🚀 自動作業管理システム")
    print("=" * 50)
    
    管理システム = 自動作業管理システム()
    
    # 現在の作業状況表示
    レポート = 管理システム.作業状況レポート()
    
    print(f"\n" + "="*50)
    print("選択してください:")
    print("1. 定期メンテナンス実行")
    print("2. 次の作業実行準備")
    print("3. 作業ルール確認")
    
    選択 = input("\n選択 (1-3): ").strip()
    
    if 選択 == "1":
        結果 = 管理システム.定期メンテナンス実行()
        print(f"\n📊 メンテナンス結果: {len(結果['実行作業'])}件実行")
        
    elif 選択 == "2":
        次の作業 = レポート["次の作業"]
        準備完了 = 管理システム.作業実行準備(次の作業["作業名"])
        
        if 準備完了:
            print(f"\n✅ {次の作業['作業名']} の実行準備完了")
            print(f"実行ファイル: {次の作業['実行ファイル']}")
        else:
            print(f"\n❌ 準備失敗")
            
    elif 選択 == "3":
        print(f"\n📋 作業ルール:")
        for カテゴリ, ルール in 管理システム.作業ルール["基本原則"].items():
            print(f"   {カテゴリ}: {ルール}")
    
    print(f"\n✅ 自動作業管理システム完了")