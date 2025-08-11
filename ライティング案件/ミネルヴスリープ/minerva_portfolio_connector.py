#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ミネルヴスリープ ポートフォリオ連携システム
ポートフォリオサイト記事格納時に公開済みフォルダへも自動記録
"""

import os
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional

class MinervaPortfolioConnector:
    """ミネルヴスリープ記事のポートフォリオ連携とローカル記録システム"""
    
    def __init__(self):
        """初期化"""
        self.portfolio_articles_path = "/Users/satoumasamitsu/Desktop/osigoto/ポートフォリオサイト/public/content/articles/articles.json"
        self.minerva_published_path = "/Users/satoumasamitsu/Desktop/osigoto/ライティング案件/ミネルヴスリープ/記事/1_公開済み/公開記事一覧.md"
        
    def add_minerva_article_to_portfolio(self, article_data: Dict) -> bool:
        """
        ミネルヴスリープ記事をポートフォリオに追加し、同時に公開済みフォルダに記録
        
        Args:
            article_data: 記事情報辞書
                {
                    "title": "記事タイトル",
                    "url": "記事URL", 
                    "description": "記事説明",
                    "date": "2025-08-11",
                    "tags": ["tag1", "tag2"],
                    "thumbnail": "サムネイルURL（オプション）"
                }
        
        Returns:
            成功時True、失敗時False
        """
        try:
            # 1. ポートフォリオサイトのarticles.jsonに追加
            success = self._add_to_portfolio_json(article_data)
            if not success:
                print("❌ ポートフォリオサイトへの追加に失敗しました")
                return False
                
            # 2. 公開済み記録ファイルに追加
            success = self._add_to_published_record(article_data)
            if not success:
                print("⚠️  公開済み記録への追加に失敗しました（ポートフォリオには追加済み）")
                
            print(f"✅ ミネルヴスリープ記事をポートフォリオと公開済み記録に追加しました")
            print(f"   タイトル: {article_data['title']}")
            print(f"   URL: {article_data['url']}")
            
            return True
            
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            return False
    
    def _add_to_portfolio_json(self, article_data: Dict) -> bool:
        """ポートフォリオサイトのarticles.jsonに記事を追加"""
        try:
            # 既存のarticles.json読み込み
            if os.path.exists(self.portfolio_articles_path):
                with open(self.portfolio_articles_path, 'r', encoding='utf-8') as f:
                    articles_data = json.load(f)
            else:
                articles_data = {"seoArticles": [], "blogArticles": []}
            
            # ミネルヴスリープ記事用のデータ構造作成
            portfolio_article = {
                "title": article_data["title"],
                "url": article_data["url"],
                "description": article_data["description"],
                "date": article_data["date"],
                "tags": article_data["tags"],
                "client": "Minerva Sleep",
                "thumbnail": article_data.get("thumbnail", "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=300&h=200&fit=crop&auto=format")
            }
            
            # seoArticlesの先頭に追加（最新記事を上に）
            articles_data["seoArticles"].insert(0, portfolio_article)
            
            # ファイル保存
            with open(self.portfolio_articles_path, 'w', encoding='utf-8') as f:
                json.dump(articles_data, f, ensure_ascii=False, indent=2)
                
            return True
            
        except Exception as e:
            print(f"ポートフォリオ追加エラー: {e}")
            return False
    
    def _add_to_published_record(self, article_data: Dict) -> bool:
        """公開済み記録ファイルに記事情報を追加"""
        try:
            # 既存の公開記事一覧を読み込み
            if os.path.exists(self.minerva_published_path):
                with open(self.minerva_published_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                content = "# ミネルヴスリープ 公開記事一覧\n\n## ポートフォリオサイト掲載記事\n\n"
            
            # 新しい記事情報を作成
            tags_str = ", ".join(article_data["tags"])
            new_record = f"""
### {len(content.split('###'))}. {article_data["title"].split('｜')[0]}記事
- **記事名**: {article_data["title"]}
- **URL**: {article_data["url"]}
- **公開日**: {article_data["date"]}
- **キーワード**: {tags_str}
"""
            
            # 記録ファイル更新（最新記事を「---」の前に挿入）
            if "---" in content:
                parts = content.split("---")
                updated_content = parts[0] + new_record + "\n---" + "---".join(parts[1:])
            else:
                # 最後に記録日時とクライアント情報を追加
                footer = f"""
---

**記録日**: {datetime.now().strftime('%Y年%m月%d日')}  
**掲載サイト**: ポートフォリオサイト (https://muffin-portfolio-public.vercel.app)  
**クライアント**: Minerva Sleep"""
                updated_content = content + new_record + footer
            
            # ファイル保存
            with open(self.minerva_published_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
                
            return True
            
        except Exception as e:
            print(f"公開記録追加エラー: {e}")
            return False
    
    def get_minerva_published_articles(self) -> List[Dict]:
        """公開済みミネルヴスリープ記事一覧を取得"""
        try:
            with open(self.portfolio_articles_path, 'r', encoding='utf-8') as f:
                articles_data = json.load(f)
            
            # Minerva Sleep記事のみ抽出
            minerva_articles = [
                article for article in articles_data.get("seoArticles", [])
                if article.get("client") == "Minerva Sleep"
            ]
            
            return minerva_articles
            
        except Exception as e:
            print(f"記事取得エラー: {e}")
            return []

def main():
    """テスト実行用メイン関数"""
    connector = MinervaPortfolioConnector()
    
    # テストデータ
    test_article = {
        "title": "【テスト記事】快眠のための寝室環境作り｜温度と湿度の最適化ガイド",
        "url": "https://minerva-sleep.jp/blogs/test/20250811",
        "description": "テスト用の記事です。寝室の温度と湿度について解説します。",
        "date": "2025-08-11",
        "tags": ["睡眠", "寝室環境", "温度", "湿度", "快眠"]
    }
    
    # 記事追加テスト
    success = connector.add_minerva_article_to_portfolio(test_article)
    if success:
        print("✅ テスト成功")
    else:
        print("❌ テスト失敗")

if __name__ == "__main__":
    main()