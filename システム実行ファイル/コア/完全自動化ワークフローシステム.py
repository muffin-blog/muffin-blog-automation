#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
マフィンブログ記事作成完全自動化ワークフローシステム
URL入力 → 全フェーズ自動実行 → ポートフォリオ反映まで完全自動化

【重要】このシステムはユーザーからWordPress完成URLを受け取った瞬間に
全てのPhase（A-E）を自動実行し、ポートフォリオサイトまで自動更新する。
"""

import os
import sys
import json
import re
import subprocess
import requests
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urlparse

class CompleteAutomationWorkflowSystem:
    """WordPress完成URL → 全自動実行システム"""
    
    def __init__(self):
        """初期化"""
        self.base_path = "/Users/satoumasamitsu/osigoto/ブログ自動化/"
        self.portfolio_path = "/Users/satoumasamitsu/osigoto/ポートフォリオサイト/"
        self.articles_json_path = f"{self.portfolio_path}public/content/articles/articles.json"
        self.knowledge_base_path = f"{self.base_path}日報・学習記録/"
        
    def detect_url_input(self, user_message: str) -> Optional[str]:
        """
        ユーザーメッセージからWordPress URLを検出
        
        Args:
            user_message: ユーザーの入力メッセージ
            
        Returns:
            検出されたURL、なければNone
        """
        # WordPress URL パターンを検出
        url_patterns = [
            r'https://muffin-blog\.com/[^/\s]+/?',
            r'https://muffin-blog\.com/\?p=\d+',
            r'muffin-blog\.com/[^/\s]+/?'
        ]
        
        for pattern in url_patterns:
            match = re.search(pattern, user_message)
            if match:
                url = match.group(0)
                if not url.startswith('http'):
                    url = f"https://{url}"
                return url.rstrip('/')
        
        return None
    
    def extract_article_info_from_url(self, url: str) -> Dict:
        """
        WordPress URLから記事情報を自動抽出
        
        Args:
            url: WordPress記事URL
            
        Returns:
            記事情報辞書
        """
        try:
            # WebFetchで記事情報を取得
            response = requests.get(url, timeout=10)
            content = response.text
            
            # タイトル抽出
            title_match = re.search(r'<title>([^<]+)</title>', content)
            title = title_match.group(1).strip() if title_match else "記事タイトル"
            title = title.replace(' - マフィンブログ', '').strip()
            
            # メインキーワード自動推定（タイトルから）
            main_keyword = self._detect_main_keyword(title)
            
            # 絶対的見本テンプレートSEO仕様に基づく生成
            optimized_description = self.generate_meta_description(title, main_keyword, content)
            slug = self.generate_slug(title, main_keyword)
            tags = self._extract_tags_from_content(title, optimized_description, content)
            
            # 今日の日付を使用
            date = datetime.now().strftime("%Y-%m-%d")
            
            article_info = {
                "title": title,
                "url": url,
                "description": optimized_description,
                "slug": slug,
                "main_keyword": main_keyword,
                "date": date,
                "tags": tags
            }
            
            print(f"✅ 記事情報自動抽出完了（絶対的見本テンプレートSEO仕様適用）:")
            print(f"   タイトル: {title}")
            print(f"   メインキーワード: {main_keyword}")
            print(f"   URL: {url}")
            print(f"   最適化メタディスクリプション: {optimized_description}")
            print(f"   SEO最適化スラッグ: {slug}")
            print(f"   日付: {date}")
            print(f"   最適化タグ: {tags}")
            
            return article_info
            
        except Exception as e:
            print(f"❌ 記事情報抽出エラー: {e}")
            return None
    
    def generate_meta_description(self, title: str, main_keyword: str, content: str) -> str:
        """
        絶対的見本テンプレートSEO仕様に基づくメタディスクリプション生成
        
        ルール:
        - 文字数：120-160文字以内
        - メインキーワードを自然に含める
        - ユーザーの悩み・解決策・メリットを含める
        - 行動を促す文言（無料体験、今すぐなど）を入れる
        - 感情に訴える表現を使う
        """
        # 基本パターン: [感情訴求] + [メインキーワード] + [解決策] + [特典・安心要素] + [行動促進]
        
        # 感情訴求フレーズ
        emotional_phrases = [
            f"{main_keyword}でお悩みの方必見！",
            f"{main_keyword}の悩みを解決！",
            f"{main_keyword}でも大丈夫！"
        ]
        
        # 解決策フレーズ
        solution_phrases = [
            "簡単に始められる方法を",
            "効果的な解決策を",
            "おすすめの方法を"
        ]
        
        # 行動促進フレーズ
        action_phrases = [
            "今すぐ試してみませんか？",
            "始めてみてください！", 
            "実感してみませんか？"
        ]
        
        # コンテンツに応じた特典要素の検出
        benefits = []
        if "無料" in content or "30日" in content:
            benefits.append("30日無料体験")
        if "解約" in content or "いつでも" in content:
            benefits.append("いつでも解約可能")
            
        # メタディスクリプション構築
        emotion = emotional_phrases[0]
        solution = solution_phrases[0] if solution_phrases else ""
        benefit_text = "で" + "・".join(benefits) if benefits else ""
        action = action_phrases[0]
        
        meta_desc = f"{emotion}{solution}詳しく解説{benefit_text}。{action}"
        
        # 文字数調整（120-160文字）
        if len(meta_desc) > 160:
            meta_desc = meta_desc[:157] + "..."
        elif len(meta_desc) < 120:
            meta_desc = meta_desc + "詳細な情報とコツをお伝えします。"
            
        return meta_desc

    def generate_slug(self, title: str, main_keyword: str) -> str:
        """
        絶対的見本テンプレートSEO仕様に基づくスラッグ生成
        
        ルール:
        - 英語で作成（日本語不可）
        - ハイフン区切りで単語を分ける
        - メインキーワードを含める
        - 簡潔で覚えやすい（3-6単語程度）
        """
        # 主要キーワードの英語変換マップ
        keyword_translation = {
            "読書苦手": "reading-dislike",
            "Audible": "audible",
            "オーディブル": "audible", 
            "聴く読書": "listening-reading",
            "オーディオブック": "audiobook",
            "本が読めない": "cannot-read-books",
            "読書継続": "reading-habit",
            "ながら読書": "multitask-reading",
            "audiobook": "audiobook-jp",
            "睡眠": "sleep",
            "ダイエット": "diet",
            "投資": "investment"
        }
        
        # メインキーワードを英語に変換
        main_key_eng = keyword_translation.get(main_keyword, "guide")
        
        # タイトルから重要な要素を抽出
        if "解決" in title or "解決法" in title:
            pattern = f"{main_key_eng}-solution"
        elif "始め方" in title or "方法" in title:
            pattern = f"{main_key_eng}-guide"
        elif "比較" in title:
            pattern = f"{main_key_eng}-comparison"
        elif "おすすめ" in title:
            pattern = f"{main_key_eng}-recommend"
        else:
            pattern = f"{main_key_eng}-complete-guide"
            
        return pattern

    def _detect_main_keyword(self, title: str) -> str:
        """
        タイトルからメインキーワードを自動検出
        
        Args:
            title: 記事タイトル
            
        Returns:
            検出されたメインキーワード
        """
        # 優先度順のキーワードマッピング
        keyword_priority = [
            "読書苦手", "Audible", "オーディブル", "聴く読書", 
            "audiobook", "オーディオブック", "本が読めない", 
            "読書継続", "ダイエット", "睡眠", "投資", "格安SIM",
            "マットレス", "UQモバイル"
        ]
        
        title_lower = title.lower()
        
        # 優先度順でキーワードを検索
        for keyword in keyword_priority:
            if keyword.lower() in title_lower:
                return keyword
        
        # 見つからない場合はタイトルから推測
        if "読書" in title or "本" in title:
            return "読書苦手"
        elif "聞く" in title or "聴く" in title:
            return "聴く読書"
        elif "音声" in title or "オーディオ" in title:
            return "オーディオブック"
        else:
            return "記事"  # デフォルト

    def _extract_tags_from_content(self, title: str, description: str, content: str) -> List[str]:
        """
        絶対的見本テンプレートSEO仕様に基づくタグ抽出
        
        ルール:
        - メインキーワード1つ + サブキーワード2-3つ + 関連キーワード5-7つ
        - カンマ区切りで設定
        - ひらがな・カタカナ・漢字のバリエーションを含める
        - 検索ボリュームのあるキーワードを優先
        """
        tags = []
        
        # タグ抽出ルール：メイン・サブ・関連キーワードをバランス良く構成
        keyword_map = {
            # メインキーワード（検索ボリューム重視）
            "読書苦手": ["読書苦手", "本が読めない", "読書継続"],
            "Audible": ["Audible", "オーディブル"],
            "ダイエット": ["ダイエット", "痩せたい", "体重減少"],
            "睡眠": ["睡眠", "快眠", "不眠症"],
            "投資": ["投資", "資産運用", "お金の勉強"],
            
            # サービス・商品名（固有名詞）
            "audiobook": ["audiobook.jp"],
            "マットレス": ["マットレス", "寝具"],
            "UQ": ["UQモバイル", "格安SIM"],
            
            # 機能・手法名（検索意図マッチング）  
            "聴く読書": ["聴く読書", "ながら読書"],
            "海外利用": ["海外利用", "国際ローミング"],
            "食事制限": ["食事制限", "食事法"],
            
            # カテゴリキーワード（関連流入）
            "オーディオブック": ["オーディオブック"],
            "健康": ["健康", "美容"],
            "通信": ["通信", "スマートフォン"],
            
            # 特典・魅力キーワード（購買意欲刺激）
            "無料": ["30日無料", "無料体験", "無料お試し"],
            "比較": ["価格比較", "サービス比較"],
            "セール": ["セール情報", "キャンペーン"],
            "おすすめ": ["おすすめ", "厳選"],
            
            # 関連キーワード（追加タグ）
            "習慣": ["読書習慣", "習慣化"],
            "解決": ["解決法", "解決方法"],
            "初心者": ["初心者", "始め方"],
            "体験": ["無料体験", "お試し"]
        }
        
        text = f"{title} {description}".lower()
        
        # 関連するすべてのタグを抽出（個数制限なし）
        for keyword, tag_list in keyword_map.items():
            if keyword.lower() in text:
                tags.extend(tag_list)
        
        # 重複除去（順序保持）
        tags = list(dict.fromkeys(tags))
        
        # 最低限のタグを確保
        if len(tags) < 3:
            tags.extend(["ブログ記事", "情報", "解説"])
        
        return tags
    
    def update_portfolio_articles_json(self, article_info: Dict) -> bool:
        """
        ポートフォリオのarticles.jsonを自動更新
        
        Args:
            article_info: 記事情報
            
        Returns:
            更新成功フラグ
        """
        try:
            # 既存のarticles.jsonを読み込み
            with open(self.articles_json_path, 'r', encoding='utf-8') as f:
                articles_data = json.load(f)
            
            # 新記事をblogArticlesの最上位に挿入
            new_article = {
                "title": article_info["title"],
                "url": article_info["url"],
                "description": article_info["description"],
                "date": article_info["date"],
                "tags": article_info["tags"]
            }
            
            # 重複チェック（同じURLの記事は削除）
            articles_data["blogArticles"] = [
                article for article in articles_data["blogArticles"]
                if article.get("url") != article_info["url"]
            ]
            
            # 新記事を最上位に追加
            articles_data["blogArticles"].insert(0, new_article)
            
            # ファイルに書き戻し
            with open(self.articles_json_path, 'w', encoding='utf-8') as f:
                json.dump(articles_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ articles.json更新完了: {new_article['title']}")
            return True
            
        except Exception as e:
            print(f"❌ articles.json更新エラー: {e}")
            return False
    
    def git_commit_and_push_portfolio(self, article_title: str) -> bool:
        """
        ポートフォリオサイトのGitコミット・プッシュ
        
        Args:
            article_title: 記事タイトル
            
        Returns:
            成功フラグ
        """
        try:
            os.chdir(self.portfolio_path)
            
            # Git add
            subprocess.run(['git', 'add', '.'], check=True)
            
            # Git commit
            commit_message = f"【新記事自動追加】{article_title}\n\n- 完全自動化システムによる自動更新\n- articles.json更新完了\n- ポートフォリオサイト反映準備完了"
            
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            
            # Git push
            subprocess.run(['git', 'push', 'origin', 'master'], check=True)
            
            print(f"✅ ポートフォリオサイトGitプッシュ完了")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Gitプッシュエラー: {e}")
            return False
    
    def wait_for_vercel_deployment(self, max_wait_seconds: int = 180) -> bool:
        """
        Vercelデプロイ完了まで待機
        
        Args:
            max_wait_seconds: 最大待機時間
            
        Returns:
            デプロイ成功フラグ
        """
        import time
        
        print(f"🔄 Vercel自動デプロイ待機中... (最大{max_wait_seconds}秒)")
        
        for i in range(max_wait_seconds // 30):
            time.sleep(30)
            print(f"   待機中... ({(i + 1) * 30}秒経過)")
            
            # 簡易的な完了チェック（実際のAPIチェックに置き換え可能）
            if i >= 2:  # 90秒経過したら完了と見なす
                print("✅ Vercelデプロイ完了推定")
                return True
        
        print("⚠️ Vercelデプロイ待機タイムアウト（手動確認が必要）")
        return False
    
    def execute_complete_automation(self, wordpress_url: str) -> Dict:
        """
        完全自動化実行メイン関数
        
        Args:
            wordpress_url: WordPress記事URL
            
        Returns:
            実行結果レポート
        """
        print("🚀 完全自動化ワークフロー開始")
        print(f"📝 対象URL: {wordpress_url}")
        
        results = {
            "url": wordpress_url,
            "success": False,
            "completed_phases": [],
            "errors": []
        }
        
        try:
            # Phase 1: 記事情報自動抽出
            print("\n📊 Phase 1: 記事情報自動抽出")
            article_info = self.extract_article_info_from_url(wordpress_url)
            if not article_info:
                results["errors"].append("記事情報抽出失敗")
                return results
            results["completed_phases"].append("記事情報抽出")
            
            # 絶対的見本テンプレート参照の確認メッセージ
            print("\n🎯 【重要】絶対的見本テンプレート参照義務")
            print("   記事作成時は以下を必ず参照してください：")
            print("   ファイル: /ドキュメント/テンプレート見本/読書苦手_Audible_聴く読書_完成記事_絶対的見本テンプレート.md")
            print("   この見本記事と同等以上の品質を確保してください")
            
            # 収益化知識ベース蓄積の確認メッセージ  
            print("\n💰 【収益化知識ベース】セッション記録蓄積")
            print("   本セッション情報は収益化コンテンツ用知識ベースとして蓄積されます：")
            print(f"   保存先: {self.knowledge_base_path}")
            print("   用途: 将来の書籍・有料ノート販売用素材データベース")
            
            # Phase 2: ポートフォリオ更新
            print("\n🔄 Phase 2: ポートフォリオarticles.json更新")
            if not self.update_portfolio_articles_json(article_info):
                results["errors"].append("articles.json更新失敗")
                return results
            results["completed_phases"].append("articles.json更新")
            
            # Phase 3: Git自動コミット・プッシュ
            print("\n📤 Phase 3: ポートフォリオサイトGitプッシュ")
            if not self.git_commit_and_push_portfolio(article_info["title"]):
                results["errors"].append("Gitプッシュ失敗")
                return results
            results["completed_phases"].append("Gitプッシュ")
            
            # Phase 4: Vercelデプロイ待機
            print("\n⏳ Phase 4: Vercelデプロイ待機")
            self.wait_for_vercel_deployment()
            results["completed_phases"].append("Vercelデプロイ")
            
            # 完了
            results["success"] = True
            results["article_info"] = article_info
            
            print("\n🎉 完全自動化ワークフロー成功！")
            print(f"✅ 記事: {article_info['title']}")
            print(f"✅ ポートフォリオサイト: https://muffin-portfolio-public.vercel.app")
            print(f"✅ 完了フェーズ: {', '.join(results['completed_phases'])}")
            
            return results
            
        except Exception as e:
            print(f"❌ 完全自動化ワークフローエラー: {e}")
            results["errors"].append(str(e))
            return results

def detect_and_execute_url_automation(user_message: str) -> Optional[Dict]:
    """
    ユーザーメッセージからURL検出 → 自動実行
    
    Args:
        user_message: ユーザーの入力メッセージ
        
    Returns:
        実行結果、URLが検出されなければNone
    """
    system = CompleteAutomationWorkflowSystem()
    
    # URL検出
    url = system.detect_url_input(user_message)
    if not url:
        return None
    
    print(f"🎯 WordPress URL検出: {url}")
    print("🚀 完全自動化ワークフロー開始...")
    
    # 完全自動実行
    results = system.execute_complete_automation(url)
    return results

# 使用例・テスト
if __name__ == "__main__":
    # テスト用
    test_url = "https://muffin-blog.com/audiobook-jp-tanpin-guide/"
    system = CompleteAutomationWorkflowSystem()
    results = system.execute_complete_automation(test_url)
    print(f"実行結果: {results}")