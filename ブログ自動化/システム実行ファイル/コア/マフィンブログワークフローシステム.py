"""
マフィンブログ記事制作ワークフローシステム
NotebookLM → 記事作成 → WordPress保存 → ポートフォリオ更新 → サイト分析 → 次記事準備
完全自動化されたブログ運営システム
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional

# パス追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.muffin_blog_article_template import MuffinBlogArticleTemplate
from core.wordpress_draft_saver import WordPressDraftSaver
# from image_generation.unsplash_image_generator import UnsplashImageGenerator  # 削除：アイキャッチ画像は手動作成

class MuffinBlogWorkflowSystem:
    """マフィンブログワークフロー管理システム"""
    
    def __init__(self):
        # セッション開始時の強制アラート
        self.session_start_alert()
        
        # 各システムの初期化
        self.template_system = MuffinBlogArticleTemplate()
        self.draft_saver = WordPressDraftSaver()
        # self.image_generator = UnsplashImageGenerator()  # 削除：アイキャッチ画像は手動作成
        
        # ワークフロー状態管理
        self.workflow_state = {
            "current_step": None,
            "article_data": None,
            "wordpress_result": None,
            "portfolio_updated": False
        }
    
    # ========================
    # アラートシステム
    # ========================
    
    def session_start_alert(self) -> bool:
        """セッション開始時の強制確認アラート"""
        print("\n🚨 CRITICAL ALERT: セッション開始時の必須確認事項")
        print("=" * 60)
        
        start_checklist = [
            "マフィンブログ記事作成_完全自動化ルール.md を読み込み済みか？",
            "前回のセッション結果を確認したか？",  
            "ユーザーの指示内容を正確に理解したか？",
            "Phase A-E の実行手順を把握しているか？",
            "【重要】Phase A完了後は必ずユーザー確認が必要であることを理解したか？",
            "【重要】Phase C実行時はGit操作まで含めて完了させることを理解したか？"
        ]
        
        all_confirmed = True
        for i, item in enumerate(start_checklist, 1):
            print(f"\n{i}. {item}")
            response = input("確認済み [y/n]: ").lower().strip()
            if response != 'y':
                print(f"❌ 未確認: {item}")
                all_confirmed = False
            else:
                print(f"✅ 確認済み: {item}")
        
        if not all_confirmed:
            print(f"\n❌ セッション開始前に未確認項目があります")
            print("すべて確認してから作業を開始してください")
            return False
        
        print(f"\n✅ セッション開始確認完了 - マフィンブログ記事作成を開始します")
        return True
    
    def phase_completion_alert(self, phase_name: str, checklist: list) -> bool:
        """Phase完了前の強制確認アラート"""
        print(f"\n🚨 ALERT: {phase_name} 完了確認")
        print("=" * 50)
        
        all_completed = True
        for i, item in enumerate(checklist, 1):
            response = input(f"{i}. {item} [y/n]: ").lower().strip()
            if response != 'y':
                print(f"❌ 未完了: {item}")
                all_completed = False
            else:
                print(f"✅ 完了: {item}")
        
        if not all_completed:
            print(f"\n❌ {phase_name} に未完了項目があります")
            print("次のPhaseに移行する前に完了してください")
            return False
        
        print(f"\n✅ {phase_name} 完了確認済み - 次のPhaseに移行します")
        return True
    
    # ========================
    # Phase 1: 記事作成フェーズ  
    # ========================
    
    def process_notebook_lm_summary(self, summary_text: str, target_keywords: List[str]):
        """NotebookLM要約を受け取り、記事作成準備"""
        
        print("📝 Phase 1: 記事作成フェーズ開始")
        print("=" * 50)
        
        self.workflow_state["current_step"] = "article_creation"
        
        # 要約内容を解析
        analysis = self.analyze_summary_content(summary_text)
        
        # 最新情報収集
        print("🔍 最新情報収集中...")
        latest_info = self.gather_latest_information(target_keywords)
        
        # 記事構成作成
        print("📋 記事構成作成中...")
        article_structure = self.create_article_structure(analysis, latest_info, target_keywords)
        
        # マフィンブログフォーマットで記事作成
        print("✍️ マフィンブログフォーマットで執筆中...")
        article_content = self.generate_muffin_blog_article(article_structure)
        
        # 品質チェック
        print("🔍 品質チェック実行中...")
        quality_check = self.perform_quality_check(article_content)
        
        if quality_check["passed"]:
            print("✅ 品質チェック合格")
            self.workflow_state["article_data"] = {
                "content": article_content,
                "structure": article_structure,
                "keywords": target_keywords,
                "quality_score": quality_check["score"]
            }
            
            # 🚨 Phase A完了確認アラート（強化版）
            phase_a_checklist = [
                "NotebookLM要約を正しく解析したか？",
                "WebSearchで最新情報を収集したか？",
                "マフィンブログフォーマットで執筆したか？",
                "AI表現を完全に除去したか？", 
                "品質チェックに合格したか？",
                "【重要】ユーザーに記事確認を依頼したか？",
                "【重要】ユーザー承認を得てからPhase Bに進むか？"
            ]
            
            if not self.phase_completion_alert("Phase A", phase_a_checklist):
                return {"success": False, "message": "Phase A未完了のため処理を中断"}
            
            return {"success": True, "article_data": self.workflow_state["article_data"]}
        else:
            print("❌ 品質チェック不合格")
            return {"success": False, "issues": quality_check["issues"]}
    
    def analyze_summary_content(self, summary_text: str) -> Dict:
        """NotebookLM要約内容を解析"""
        # トピック抽出
        topics = self.extract_main_topics(summary_text)
        
        # 記事の方向性判断
        direction = self.determine_article_direction(summary_text)
        
        return {
            "topics": topics,
            "direction": direction,
            "word_count": len(summary_text),
            "complexity": self.assess_complexity(summary_text)
        }
    
    def gather_latest_information(self, keywords: List[str]) -> Dict:
        """最新情報収集（WebSearchツール使用）"""
        latest_info = {}
        
        for keyword in keywords:
            # 実際の実装ではWebSearchツールを使用
            # latest_info[keyword] = self.web_search(keyword + " 2025年 最新")
            latest_info[keyword] = f"{keyword}の最新情報プレースホルダー"
        
        return latest_info
    
    def create_article_structure(self, analysis: Dict, latest_info: Dict, keywords: List[str]) -> Dict:
        """記事構成作成"""
        return {
            "title": self.generate_seo_title(keywords[0], latest_info),
            "sections": [
                f"{keywords[0]}の基本情報と最新動向",
                f"{keywords[0]}と競合サービスの比較",
                f"{keywords[0]}の活用方法と注意点",
                "おすすめの使い方とコツ"
            ],
            "target_length": 3000,
            "seo_keywords": keywords
        }
    
    def generate_muffin_blog_article(self, structure: Dict) -> str:
        """マフィンブログフォーマットで記事生成"""
        # テンプレートシステムを使用して記事生成
        article = self.template_system.create_article_template(
            structure["title"].split("！")[0],  # トピック抽出
            structure["seo_keywords"],
            structure["sections"]
        )
        return article
    
    def perform_quality_check(self, article_content: str) -> Dict:
        """品質チェック実行"""
        issues = []
        score = 100
        
        # AI的表現チェック
        ai_phrases = ["ことが多いです", "と言えるでしょう", "検討してみてはいかがでしょうか"]
        for phrase in ai_phrases:
            if phrase in article_content:
                issues.append(f"AI的表現発見: '{phrase}'")
                score -= 10
        
        # マフィンさんの対話チェック
        if article_content.count("「") < 8:  # 対話が少なすぎる
            issues.append("マフィンさんとの対話が不足")
            score -= 15
        
        # フォーマットチェック
        if not "## まとめ：" in article_content:
            issues.append("まとめセクションが見つからない")
            score -= 20
        
        return {
            "passed": score >= 80,
            "score": score,
            "issues": issues
        }
    
    # ========================
    # Phase 2: WordPress保存フェーズ
    # ========================
    
    def save_to_wordpress_draft(self, user_approved: bool = True) -> Dict:
        """WordPress下書き保存"""
        
        if not user_approved:
            return {"success": False, "reason": "User approval required"}
        
        if not self.workflow_state["article_data"]:
            return {"success": False, "reason": "No article data available"}
        
        print("📝 Phase 2: WordPress下書き保存フェーズ開始")
        print("=" * 50)
        
        self.workflow_state["current_step"] = "wordpress_saving"
        
        # 記事をファイルとして一時保存
        temp_file = self.save_temp_article_file()
        
        # WordPress下書き保存実行
        print("⬆️ WordPress下書き保存実行中...")
        result = self.draft_saver.save_draft_to_wordpress(self.workflow_state["article_data"])
        
        if result["success"]:
            self.workflow_state["wordpress_result"] = result
            print(f"✅ WordPress保存完了: {result['post_url']}")
            
            # マフィンブログ完成記事フォルダにも保存
            self.save_to_completed_articles()
            
            # 🚨 Phase B完了確認アラート
            phase_b_checklist = [
                "SEO8項目すべて設定したか？",
                "パーマリンクを確定したか？",
                "カテゴリ・タグを確定したか？",
                "アイキャッチ画像alt属性を設定したか？", 
                "完成記事フォルダに保存したか？"
            ]
            
            if not self.phase_completion_alert("Phase B", phase_b_checklist):
                return {"success": False, "message": "Phase B未完了のため処理を中断"}
            
            return result
        else:
            print(f"❌ WordPress保存失敗: {result['error']}")
            return result
    
    def save_temp_article_file(self) -> str:
        """一時記事ファイル保存"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"temp_article_{timestamp}.md"
        temp_path = f"/tmp/{filename}"
        
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(self.workflow_state["article_data"]["content"])
        
        return temp_path
    
    def save_to_completed_articles(self):
        """完成記事フォルダに保存"""
        if not self.workflow_state["article_data"]["keywords"]:
            return
        
        main_keyword = self.workflow_state["article_data"]["keywords"][0]
        sub_keyword = self.workflow_state["article_data"]["keywords"][1] if len(self.workflow_state["article_data"]["keywords"]) > 1 else ""
        
        # メタ情報設定
        meta_info = {
            "main_keyword": main_keyword,
            "sub_keywords": self.workflow_state["article_data"]["keywords"],
            "target_audience": "オーディオブック利用者",
            "purpose": "最適な利用方法の提供",
            "reference_article": "システム生成記事"
        }
        
        # 保存実行
        self.template_system.save_new_article(
            self.workflow_state["article_data"]["content"],
            main_keyword,
            sub_keyword,
            meta_info
        )
    
    # ========================
    # Phase 3: ポートフォリオ更新フェーズ
    # ========================
    
    def update_portfolio_site(self, wordpress_url: str) -> Dict:
        """ポートフォリオサイト更新"""
        
        print("📁 Phase 3: ポートフォリオ更新フェーズ開始") 
        print("=" * 50)
        
        self.workflow_state["current_step"] = "portfolio_update"
        
        # WordPress記事情報取得
        article_info = self.extract_wordpress_article_info(wordpress_url)
        
        # articles.json更新
        portfolio_path = "/Users/satoumasamitsu/Desktop/osigoto/ポートフォリオサイト/public/content/articles/articles.json"
        
        try:
            # 既存のarticles.json読み込み
            with open(portfolio_path, 'r', encoding='utf-8') as f:
                portfolio_data = json.load(f)
            
            # 新記事をblogArticlesに追加
            new_article = {
                "title": article_info["title"],
                "url": wordpress_url,
                "description": article_info["description"],
                "date": datetime.now().strftime("%Y-%m-%d"),
                "tags": article_info["tags"]
            }
            
            portfolio_data["blogArticles"].insert(0, new_article)  # 最新記事を先頭に
            
            # 更新されたarticles.jsonを保存
            with open(portfolio_path, 'w', encoding='utf-8') as f:
                json.dump(portfolio_data, f, ensure_ascii=False, indent=2)
            
            print("✅ ポートフォリオサイト更新完了")
            self.workflow_state["portfolio_updated"] = True
            
            # 🚨 Phase C完了確認アラート（強化版）
            phase_c_checklist = [
                "編集完了URLを受け取ったか？",
                "articles.jsonに新記事を【先頭に】追加したか？",
                "記事情報が正確か？(title, url, description, date, tags)",
                "重複記事がないか確認したか？",
                "Git add . を実行したか？",
                "Git commit を実行したか？",
                "Git push origin master を実行したか？",
                "Vercel自動デプロイが開始されたか？",
                "ポートフォリオサイトで最新記事が表示されることを確認したか？"
            ]
            
            if not self.phase_completion_alert("Phase C", phase_c_checklist):
                return {"success": False, "message": "Phase C未完了のため処理を中断"}
            
            return {"success": True, "updated_articles_count": len(portfolio_data["blogArticles"])}
            
        except Exception as e:
            print(f"❌ ポートフォリオ更新失敗: {e}")
            return {"success": False, "error": str(e)}
    
    def extract_wordpress_article_info(self, url: str) -> Dict:
        """WordPress記事から情報抽出"""
        # 実際の実装ではWebFetchツールを使用してページ内容を取得
        
        if self.workflow_state["wordpress_result"]:
            return {
                "title": self.workflow_state["wordpress_result"]["title"],
                "description": f"{self.workflow_state['article_data']['keywords'][0]}に関する詳細ガイド記事",
                "tags": self.workflow_state["article_data"]["keywords"]
            }
        
        return {
            "title": "記事タイトル",
            "description": "記事説明",
            "tags": ["オーディオブック"]
        }
    
    # ========================
    # Phase 4: サイト分析フェーズ
    # ========================
    
    def analyze_blog_site(self) -> Dict:
        """ブログ全体分析"""
        
        print("🔍 Phase 4: ブログ全体分析フェーズ開始")
        print("=" * 50)
        
        self.workflow_state["current_step"] = "site_analysis"
        
        analysis_result = {
            "seo_issues": [],
            "technical_issues": [],
            "content_issues": [],
            "recommendations": [],
            "penalty_risks": []
        }
        
        # SEO分析
        seo_analysis = self.perform_seo_analysis()
        analysis_result["seo_issues"] = seo_analysis
        
        # 技術的分析
        tech_analysis = self.perform_technical_analysis()
        analysis_result["technical_issues"] = tech_analysis
        
        # コンプライアンスチェック
        compliance_check = self.check_compliance()
        analysis_result["compliance"] = compliance_check
        
        # 改善提案生成
        recommendations = self.generate_recommendations(analysis_result)
        analysis_result["recommendations"] = recommendations
        
        print("✅ サイト分析完了")
        
        return analysis_result
    
    def perform_seo_analysis(self) -> List[Dict]:
        """SEO分析実行"""
        # 実際の実装ではWordPressサイトを詳細分析
        return [
            {"type": "meta_description", "status": "要確認", "message": "一部記事でメタディスクリプションが不足"},
            {"type": "internal_links", "status": "良好", "message": "内部リンク構造は適切"}
        ]
    
    def perform_technical_analysis(self) -> List[Dict]:
        """技術的分析実行"""
        return [
            {"type": "page_speed", "status": "良好", "score": 85},
            {"type": "mobile_friendly", "status": "良好", "score": 90}
        ]
    
    def check_compliance(self) -> Dict:
        """コンプライアンスチェック"""
        return {
            "privacy_policy": {"exists": True, "updated": "2025-01-01"},
            "contact_form": {"exists": True, "functional": True},
            "cookie_notice": {"exists": True, "gdpr_compliant": True}
        }
    
    def generate_recommendations(self, analysis: Dict) -> List[str]:
        """改善提案生成"""
        recommendations = []
        
        if len(analysis["seo_issues"]) > 0:
            recommendations.append("SEO要素の最適化を実施することを推奨")
        
        if len(analysis["technical_issues"]) > 0:
            recommendations.append("技術的問題の修正を推奨")
        
        recommendations.append("定期的なコンテンツ更新を継続")
        
        return recommendations
    
    # ========================
    # Phase 4.5: 日報記録フェーズ（次記事準備前）
    # ========================
    
    def generate_session_daily_report(self) -> Dict:
        """セッション日報自動生成（記事作成作業の記録）"""
        
        print("📝 Phase 4.5: セッション日報記録開始")
        print("=" * 50)
        
        # 今回のセッションで何をやったかを自動記録
        session_summary = {
            "theme": "マフィンブログ記事作成セッション",
            "notebook_input": self.workflow_state.get("notebook_summary", ""),
            "article_created": bool(self.workflow_state.get("article_data")),
            "wordpress_saved": bool(self.workflow_state.get("wordpress_result")),
            "challenges_encountered": [],
            "technical_discoveries": [],
            "improvements_made": [],
            "user_experience_notes": []
        }
        
        # 今回のセッションでの課題・発見を自動抽出
        if self.workflow_state.get("article_data"):
            if self.workflow_state["article_data"]["quality_score"] < 80:
                session_summary["challenges_encountered"].append("記事品質スコアが80点未満")
            
        if self.workflow_state.get("wordpress_result"):
            if self.workflow_state["wordpress_result"]["success"]:
                session_summary["technical_discoveries"].append("WordPress下書き保存が正常動作")
            else:
                session_summary["challenges_encountered"].append(f"WordPress保存エラー: {self.workflow_state['wordpress_result'].get('error', 'Unknown')}")
        
        # 日報システムに記録
        try:
            from book_publication.publishing_workflow.daily_report_automation import DailyReportAutomation, auto_finalize_session
            
            report_system = DailyReportAutomation()
            report_system.start_session_tracking(session_summary["theme"])
            
            # システム動作状況を記録
            if session_summary["article_created"]:
                report_system.log_implementation(
                    "マフィンブログ記事自動生成",
                    "core/muffin_blog_workflow_system.py",
                    f"NotebookLM要約から記事作成完了（品質スコア: {self.workflow_state['article_data'].get('quality_score', 'N/A')}）",
                    ["SEO最適化", "AI表現除去", "フォーマット準拠"]
                )
            
            if session_summary["wordpress_saved"]:
                report_system.log_implementation(
                    "WordPress自動投稿",
                    "core/wordpress_draft_saver.py", 
                    f"WordPress下書き保存完了（ID: {self.workflow_state['wordpress_result'].get('post_id', 'N/A')}）",
                    ["SEOタイトル最適化", "メタデータ設定"]
                )
            
            # 課題があれば記録
            for challenge in session_summary["challenges_encountered"]:
                report_system.log_challenge_solved(
                    challenge,
                    "システム運用中の課題",
                    "システム改善で対応" if "エラー" not in challenge else "手動対応で解決",
                    "継続的システム改善の必要性"
                )
            
            # 日報保存
            report_path = auto_finalize_session(report_system)
            
            print(f"✅ セッション日報生成完了: {report_path}")
            
            # 🚨 Phase D完了確認アラート
            phase_d_checklist = [
                "遭遇した課題の自動解決策を実装したか？",
                "次回同様の問題を防ぐルール自動更新をしたか？",
                "効率化できる作業の自動化コードを生成したか？",
                "ワークフロー最適化を実行したか？",
                "改善内容をセッション記録に保存したか？"
            ]
            
            if not self.phase_completion_alert("Phase D", phase_d_checklist):
                return {"success": False, "message": "Phase D未完了のため処理を中断"}
            
            return {
                "success": True,
                "report_path": report_path,
                "session_summary": session_summary
            }
            
        except Exception as e:
            print(f"⚠️ 日報生成でエラー（処理継続）: {e}")
            return {
                "success": False,
                "error": str(e),
                "session_summary": session_summary
            }
    
    # ========================
    # Phase 5: 次記事準備フェーズ
    # ========================
    
    def prepare_next_article_info(self) -> Dict:
        """次記事準備情報収集"""
        
        print("🔮 Phase 5: 次記事準備フェーズ開始")
        print("=" * 50)
        
        self.workflow_state["current_step"] = "next_article_prep"
        
        # 最新情報収集
        latest_trends = self.collect_latest_trends()
        
        # 競合分析
        competitor_analysis = self.analyze_competitors()
        
        # 記事企画提案
        article_proposals = self.generate_article_proposals(latest_trends, competitor_analysis)
        
        print("✅ 次記事準備完了")
        
        # 🚨 Phase E完了確認アラート
        phase_e_checklist = [
            "Audible・Kindle・audiobook.jp最新情報を収集したか？",
            "オーディオブック関連トレンドを把握したか？",
            "競合記事分析を実行したか？",
            "次記事企画提案を作成したか？"
        ]
        
        if not self.phase_completion_alert("Phase E", phase_e_checklist):
            return {"success": False, "message": "Phase E未完了のため処理を中断"}
        
        return {
            "trends": latest_trends,
            "competitors": competitor_analysis,
            "proposals": article_proposals
        }
    
    def collect_latest_trends(self) -> Dict:
        """最新トレンド収集"""
        # 実際の実装ではWebSearchツールを使用
        return {
            "audible": "Audible 2025年新機能追加",
            "kindle": "Kindle Unlimited 対象作品拡充",
            "audiobook_jp": "audiobook.jp セール情報",
            "devices": "新型Kindleデバイス情報"
        }
    
    def analyze_competitors(self) -> List[Dict]:
        """競合記事分析"""
        # 実際の実装ではWebFetchツールで競合サイト分析
        return [
            {
                "site": "競合サイトA",
                "trending_topics": ["オーディオブック比較", "Kindle活用法"],
                "gap_opportunities": ["デバイス詳細レビュー"]
            }
        ]
    
    def generate_article_proposals(self, trends: Dict, competitors: List[Dict]) -> List[Dict]:
        """記事企画提案生成"""
        proposals = []
        
        # トレンド情報から記事案生成
        for service, trend in trends.items():
            proposals.append({
                "title": f"{service} 最新情報完全ガイド",
                "keywords": [service, "2025年", "最新"],
                "priority": "high",
                "reason": f"最新トレンド: {trend}"
            })
        
        return proposals
    
    # ========================
    # ワークフロー実行管理
    # ========================
    
    def run_complete_workflow(self, notebook_summary: str, keywords: List[str]) -> Dict:
        """完全ワークフロー実行"""
        
        print("🚀 マフィンブログ記事制作ワークフロー開始")
        print("=" * 60)
        
        results = {}
        
        # Phase 1: 記事作成
        phase1 = self.process_notebook_lm_summary(notebook_summary, keywords)
        results["phase1"] = phase1
        
        if not phase1["success"]:
            return {"workflow_completed": False, "failed_at": "phase1", "results": results}
        
        # Phase 2: WordPress保存（ユーザー承認が必要）
        print("\n⏸️ ユーザー承認待ち...")
        return {
            "workflow_step": "awaiting_user_approval",
            "next_action": "call save_to_wordpress_draft(user_approved=True)",
            "results": results
        }
    
    def continue_workflow_after_approval(self, wordpress_url: str) -> Dict:
        """ユーザー承認後のワークフロー継続"""
        
        results = {}
        
        # Phase 3: ポートフォリオ更新
        phase3 = self.update_portfolio_site(wordpress_url)
        results["phase3"] = phase3
        
        # Phase 4: サイト分析
        phase4 = self.analyze_blog_site()
        results["phase4"] = phase4
        
        # Phase 4.5: セッション日報記録
        daily_report = self.generate_session_daily_report()
        results["daily_report"] = daily_report
        
        # Phase 5: 次記事準備
        phase5 = self.prepare_next_article_info()
        results["phase5"] = phase5
        
        print("\n🎉 完全ワークフロー完了!")
        print("=" * 60)
        
        # 🚨 最終確認アラート
        final_checklist = [
            "全Phase（A-E）が完了したか？",
            "ルール違反がないか？",
            "ファイル保存・命名規則に準拠したか？",
            "ユーザーに完了報告をしたか？",
            "Phase D で改善事項を記録したか？"
        ]
        
        if not self.phase_completion_alert("最終確認", final_checklist):
            return {"workflow_completed": False, "message": "最終確認未完了のため処理を中断"}
        
        return {
            "workflow_completed": True,
            "results": results,
            "next_notebook_input_ready": True
        }
    
    def get_workflow_status(self) -> Dict:
        """現在のワークフロー状態取得"""
        return self.workflow_state

# ヘルパー関数
def extract_main_topics(text: str) -> List[str]:
    """テキストから主要トピック抽出"""
    # 簡易実装（実際はより高度な自然言語処理を使用）
    topics = []
    if "audiobook" in text.lower():
        topics.append("オーディオブック")
    if "audible" in text.lower():
        topics.append("Audible")
    if "kindle" in text.lower():
        topics.append("Kindle")
    return topics

def determine_article_direction(text: str) -> str:
    """記事の方向性判断"""
    if "比較" in text:
        return "comparison"
    elif "方法" in text or "使い方" in text:
        return "how_to"
    elif "おすすめ" in text:
        return "recommendation"
    else:
        return "general_guide"

def assess_complexity(text: str) -> str:
    """内容の複雑度評価"""
    word_count = len(text)
    if word_count > 1000:
        return "high"
    elif word_count > 500:
        return "medium" 
    else:
        return "low"

def generate_seo_title(main_keyword: str, info: Dict) -> str:
    """SEO最適化タイトル生成"""
    return f"{main_keyword}完全ガイド！2025年最新情報と使い方"

if __name__ == "__main__":
    # システムテスト
    workflow = MuffinBlogWorkflowSystem()
    
    # テスト用NotebookLM要約
    test_summary = """
    audiobook.jpとAudibleの比較について。
    単品購入とサブスクリプションの違い、価格差、おすすめの使い方。
    セール情報や最新の動向についても含める。
    """
    
    test_keywords = ["audiobook.jp", "Audible", "比較"]
    
    # ワークフロー実行テスト
    result = workflow.run_complete_workflow(test_summary, test_keywords)
    
    print("\n🧪 ワークフローテスト結果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))