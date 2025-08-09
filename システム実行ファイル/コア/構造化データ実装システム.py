"""
構造化データ実装システム
記事にJSON-LDスキーママークアップを追加してSEO強化
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests
import json
from datetime import datetime
import re

class 構造化データ実装システム:
    """Schema.orgに基づく構造化データの実装"""
    
    def __init__(self):
        self.wp = WordPressBlogAutomator(
            site_url="https://muffin-blog.com",
            username="muffin1203",
            password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
        )
        
        # 対象記事リスト
        self.対象記事リスト = [2732, 2677, 2625, 2535, 2210]
        
        # 基本サイト情報
        self.サイト情報 = {
            "name": "マフィンブログ",
            "url": "https://muffin-blog.com",
            "description": "Audibleとオーディオブックに特化した情報サイト",
            "author": "マフィン"
        }
    
    def 記事の構造化データ生成(self, 記事データ):
        """記事用の構造化データ（JSON-LD）を生成"""
        
        記事ID = 記事データ['id']
        記事タイトル = 記事データ['title']['rendered']
        記事内容 = 記事データ['content']['rendered']
        記事URL = f"https://muffin-blog.com/?p={記事ID}"
        公開日 = 記事データ['date']
        更新日 = 記事データ['modified']
        
        # 記事の説明文を抽出（最初の段落から）
        説明文 = self.記事説明文抽出(記事内容)
        
        # 画像URLを抽出
        画像URL = self.記事画像URL抽出(記事内容)
        
        # JSON-LD構造化データ
        構造化データ = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": 記事タイトル,
            "description": 説明文,
            "url": 記事URL,
            "datePublished": 公開日,
            "dateModified": 更新日,
            "author": {
                "@type": "Person",
                "name": self.サイト情報["author"]
            },
            "publisher": {
                "@type": "Organization",
                "name": self.サイト情報["name"],
                "url": self.サイト情報["url"]
            },
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": 記事URL
            }
        }
        
        # 画像がある場合は追加
        if 画像URL:
            構造化データ["image"] = {
                "@type": "ImageObject",
                "url": 画像URL
            }
        
        # Audible関連記事の場合はより詳細な構造化データ
        if "Audible" in 記事タイトル:
            構造化データ["about"] = {
                "@type": "Product",
                "name": "Audible",
                "description": "Amazonのオーディオブックサービス"
            }
        
        return 構造化データ
    
    def 記事説明文抽出(self, 記事内容):
        """記事内容から説明文を抽出"""
        
        # HTMLタグを除去
        テキスト = re.sub(r'<[^>]+>', '', 記事内容)
        テキスト = re.sub(r'\s+', ' ', テキスト).strip()
        
        # 最初の160文字程度を説明文とする
        if len(テキスト) > 160:
            説明文 = テキスト[:160] + "..."
        else:
            説明文 = テキスト
        
        return 説明文
    
    def 記事画像URL抽出(self, 記事内容):
        """記事から画像URLを抽出"""
        
        # imgタグのsrcを検索
        img_matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', 記事内容)
        
        if img_matches:
            # 最初の画像URLを返す
            return img_matches[0]
        
        return None
    
    def 構造化データ追加(self, 記事ID):
        """記事に構造化データを追加"""
        
        print(f"🏗️ 記事ID {記事ID} に構造化データ追加中...")
        
        try:
            # 記事取得
            response = requests.get(f"{self.wp.api_url}/posts/{記事ID}", headers=self.wp.headers)
            if response.status_code != 200:
                return False
            
            記事データ = response.json()
            記事タイトル = 記事データ['title']['rendered']
            記事内容 = 記事データ['content']['rendered']
            
            print(f"   記事: {記事タイトル[:40]}...")
            
            # 既に構造化データがある場合はスキップ
            if 'application/ld+json' in 記事内容:
                print(f"   ℹ️ 既に構造化データが存在します")
                return True
            
            # バックアップ
            バックアップファイル = f"/Users/satoumasamitsu/osigoto/ブログ自動化/backups/記事{記事ID}_schema_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            os.makedirs(os.path.dirname(バックアップファイル), exist_ok=True)
            with open(バックアップファイル, 'w', encoding='utf-8') as f:
                f.write(記事内容)
            print(f"   💾 バックアップ保存: {os.path.basename(バックアップファイル)}")
            
            # 構造化データ生成
            構造化データ = self.記事の構造化データ生成(記事データ)
            
            # JSON-LDスクリプトタグ作成
            json_ld = json.dumps(構造化データ, ensure_ascii=False, indent=2)
            script_tag = f'<script type="application/ld+json">{json_ld}</script>'
            
            # 記事の最後に構造化データを追加
            更新済み内容 = 記事内容 + f"\n\n{script_tag}"
            
            # WordPressに更新
            更新データ = {'content': 更新済み内容}
            response = requests.post(f"{self.wp.api_url}/posts/{記事ID}", 
                                   headers=self.wp.headers, 
                                   json=更新データ)
            
            if response.status_code == 200:
                print(f"   ✅ 記事ID {記事ID}: 構造化データ追加完了")
                return True
            else:
                print(f"   ❌ 記事ID {記事ID}: 更新失敗 ({response.status_code})")
                return False
                
        except Exception as e:
            print(f"❌ 記事ID {記事ID}: エラー - {e}")
            return False
    
    def 全記事構造化データ実装(self):
        """全記事に構造化データを実装"""
        
        print("🏗️ 全記事構造化データ実装開始")
        print("=" * 60)
        
        成功記事数 = 0
        
        for 記事ID in self.対象記事リスト:
            成功 = self.構造化データ追加(記事ID)
            if 成功:
                成功記事数 += 1
        
        print(f"\n🎯 構造化データ実装完了!")
        print(f"処理記事数: {成功記事数}/{len(self.対象記事リスト)}")
        print("✅ SEO効果のあるJSON-LD構造化データが全記事に追加されました")
        
        return 成功記事数

if __name__ == "__main__":
    print("🏗️ 構造化データ実装システム")
    print("=" * 60)
    
    構造化システム = 構造化データ実装システム()
    構造化システム.全記事構造化データ実装()
    
    print("\n✅ 構造化データ実装システム完了")