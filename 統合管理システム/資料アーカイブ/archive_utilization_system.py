#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動検索・活用システム - 統合資料アーカイブ連携
信頼できるソース情報の自動発見・活用・循環システム

統合機能:
- アーカイブ自動検索
- 重複チェック・防止
- 差別化提案自動生成
- 品質向上要素自動抽出
- 新知識自動蓄積
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import difflib

class ArchiveUtilizationSystem:
    """統合資料アーカイブ自動検索・活用システム"""
    
    def __init__(self):
        """初期化"""
        self.base_path = "/Users/satoumasamitsu/Desktop/osigoto/"
        self.archive_path = os.path.join(self.base_path, "統合管理システム/資料アーカイブ/")
        self.notebook_path = os.path.join(self.base_path, "ブログ自動化/NotebookLM資料/")
        self.duplication_db_path = os.path.join(self.archive_path, "作成済み記事・キーワード重複管理.md")
        
        # キーワードマッピングデータベース
        self.keyword_categories = {
            "audible": {
                "primary": ["Audible", "オーディブル", "聴く読書"],
                "secondary": ["料金", "プラン", "集中力", "読解力", "効果"],
                "tertiary": ["使い方", "活用法", "メリット", "デメリット", "比較"]
            },
            "audiobook": {
                "primary": ["オーディオブック", "audiobook.jp", "聴き放題"],
                "secondary": ["読書術", "効果", "方法", "比較", "料金"],
                "tertiary": ["初心者", "始め方", "おすすめ", "選び方"]
            },
            "sleep_furniture": {
                "primary": ["睡眠", "ベッド", "マットレス", "布団"],
                "secondary": ["選び方", "おすすめ", "対策", "改善", "快適"],
                "tertiary": ["一人暮らし", "社会人", "健康", "サイズ", "素材"]
            }
        }
        
        # 既知の作成済み記事データ（初期データ）
        self.created_articles = {
            "blog": [
                {
                    "main_keyword": "Audible 集中力 読解力",
                    "related_keywords": ["オーディブル", "聴く読書", "読書苦手", "効果", "方法"],
                    "target_audience": "読書苦手な人",
                    "angle": "集中力・読解力向上効果",
                    "created_date": "2025-08-11"
                }
            ],
            "writing_project": [
                {
                    "main_keyword": "ベッドフレーム 選び方",
                    "related_keywords": ["サイズ", "素材", "価格", "おすすめ"],
                    "target_audience": "一人暮らし開始予定の社会人",
                    "angle": "失敗しない選び方ガイド",
                    "created_date": "2025-08-12"
                },
                {
                    "main_keyword": "布団 ホコリ対策",
                    "related_keywords": ["掃除", "アレルギー", "対策", "方法"],
                    "target_audience": "アレルギーで困っている人",
                    "angle": "効果的なホコリ対策方法",
                    "created_date": "2025-08-11"
                },
                {
                    "main_keyword": "社会人 睡眠時間",
                    "related_keywords": ["忙しい", "時間管理", "健康", "改善"],
                    "target_audience": "忙しい社会人",
                    "angle": "効率的な睡眠時間確保方法",
                    "created_date": "2025-08-11"
                }
            ]
        }
    
    def extract_keywords_from_request(self, user_request: str) -> Dict[str, Any]:
        """ユーザーリクエストからキーワードを自動抽出"""
        
        # 基本的なキーワード抽出
        extracted_keywords = {
            "main_keywords": [],
            "category": "unknown",
            "detected_keywords": [],
            "inferred_intent": ""
        }
        
        request_lower = user_request.lower()
        
        # カテゴリ判定とキーワード抽出
        for category, keywords in self.keyword_categories.items():
            category_score = 0
            found_keywords = []
            
            # Primary keywordsチェック
            for keyword in keywords["primary"]:
                if keyword.lower() in request_lower or keyword in user_request:
                    category_score += 3
                    found_keywords.append(keyword)
                    if keyword not in extracted_keywords["main_keywords"]:
                        extracted_keywords["main_keywords"].append(keyword)
            
            # Secondary keywordsチェック
            for keyword in keywords["secondary"]:
                if keyword.lower() in request_lower or keyword in user_request:
                    category_score += 2
                    found_keywords.append(keyword)
            
            # Tertiary keywordsチェック
            for keyword in keywords["tertiary"]:
                if keyword.lower() in request_lower or keyword in user_request:
                    category_score += 1
                    found_keywords.append(keyword)
            
            if category_score > 0:
                extracted_keywords["detected_keywords"].extend(found_keywords)
                if category_score > 3 and extracted_keywords["category"] == "unknown":
                    extracted_keywords["category"] = category
        
        # Intent推定
        if "記事" in user_request and "作成" in user_request:
            extracted_keywords["inferred_intent"] = "article_creation"
        elif "記事" in user_request and "書" in user_request:
            extracted_keywords["inferred_intent"] = "article_creation"
        
        return extracted_keywords
    
    def search_relevant_archives(self, keywords: Dict[str, Any]) -> List[Dict]:
        """キーワードに基づく関連アーカイブ資料の自動検索"""
        
        relevant_materials = []
        
        try:
            # NotebookLM資料フォルダをスキャン
            for file_path in Path(self.notebook_path).glob("*.md"):
                file_name = file_path.name
                relevance_score = 0
                matched_keywords = []
                
                # ファイル名でのキーワードマッチング
                for keyword in keywords["main_keywords"] + keywords["detected_keywords"]:
                    if keyword.lower() in file_name.lower():
                        relevance_score += 3
                        matched_keywords.append(keyword)
                
                # ファイル内容での詳細マッチング（最初の500文字）
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content_preview = f.read(500)
                        
                        for keyword in keywords["detected_keywords"]:
                            if keyword in content_preview:
                                relevance_score += 1
                                if keyword not in matched_keywords:
                                    matched_keywords.append(keyword)
                
                except Exception as e:
                    print(f"⚠️ ファイル読み込み警告 ({file_name}): {e}")
                
                # 関連性があるファイルを結果に追加
                if relevance_score > 0:
                    relevant_materials.append({
                        "file_name": file_name,
                        "file_path": str(file_path),
                        "relevance_score": relevance_score,
                        "matched_keywords": matched_keywords,
                        "category": keywords["category"]
                    })
            
            # 関連度順でソート
            relevant_materials.sort(key=lambda x: x["relevance_score"], reverse=True)
            
        except Exception as e:
            print(f"❌ アーカイブ検索エラー: {e}")
        
        return relevant_materials
    
    def check_duplication_risk(self, keywords: Dict[str, Any]) -> Dict[str, Any]:
        """記事重複リスクの自動チェック"""
        
        duplication_result = {
            "status": "SAFE",
            "risk_level": 0,
            "conflicting_articles": [],
            "suggestions": []
        }
        
        try:
            new_main_keywords = set(keywords["main_keywords"])
            new_detected = set(keywords["detected_keywords"])
            
            # 既存記事との比較
            all_articles = self.created_articles["blog"] + self.created_articles["writing_project"]
            
            for article in all_articles:
                existing_main = set([article["main_keyword"]])
                existing_related = set(article["related_keywords"])
                
                # メインキーワード完全一致チェック
                main_overlap = len(new_main_keywords.intersection(existing_main))
                if main_overlap > 0:
                    overlap_ratio = main_overlap / len(new_main_keywords) if new_main_keywords else 0
                    if overlap_ratio > 0.8:
                        duplication_result["status"] = "HIGH_RISK"
                        duplication_result["risk_level"] = 9
                        duplication_result["conflicting_articles"].append({
                            "article": article["main_keyword"],
                            "overlap_type": "main_keyword_exact_match",
                            "created_date": article["created_date"]
                        })
                
                # 関連キーワード類似度チェック
                related_overlap = len(new_detected.intersection(existing_related))
                if related_overlap > 2:
                    similarity_ratio = related_overlap / len(new_detected) if new_detected else 0
                    if similarity_ratio > 0.6:
                        current_risk = min(8, int(similarity_ratio * 10))
                        if current_risk > duplication_result["risk_level"]:
                            duplication_result["risk_level"] = current_risk
                            duplication_result["status"] = "MODERATE_RISK" if current_risk < 7 else "HIGH_RISK"
                            duplication_result["conflicting_articles"].append({
                                "article": article["main_keyword"],
                                "overlap_type": "related_keywords_similar",
                                "similarity_ratio": similarity_ratio,
                                "created_date": article["created_date"]
                            })
            
            # 差別化提案生成
            if duplication_result["risk_level"] > 3:
                duplication_result["suggestions"] = self._generate_differentiation_suggestions(
                    keywords, duplication_result["conflicting_articles"]
                )
        
        except Exception as e:
            print(f"❌ 重複チェックエラー: {e}")
        
        return duplication_result
    
    def _generate_differentiation_suggestions(self, keywords: Dict, conflicts: List[Dict]) -> List[str]:
        """差別化提案の自動生成"""
        
        suggestions = []
        
        # 基本的な差別化戦略
        base_strategies = [
            "ターゲット読者層の変更（初心者→上級者、学生→社会人など）",
            "記事の深さレベル変更（入門編→実践編→応用編）",
            "アプローチ角度変更（方法論→効果検証→比較分析）",
            "具体的用途・シチュエーション特化",
            "失敗例・注意点にフォーカスした逆説的アプローチ"
        ]
        
        # キーワードベースの特化提案
        if keywords["category"] == "audible":
            suggestions.extend([
                "特定デバイス特化（スマホ→Alexa→Car Play）",
                "特定ジャンル特化（ビジネス書→小説→学習書）",
                "利用シーン特化（通勤→運動→就寝前）"
            ])
        elif keywords["category"] == "audiobook":
            suggestions.extend([
                "サービス比較特化（Audible vs audiobook.jp）",
                "料金・コスパ分析特化",
                "機能・使いやすさ比較特化"
            ])
        elif keywords["category"] == "sleep_furniture":
            suggestions.extend([
                "予算帯別特化（1万円以下→3万円以下→高級品）",
                "住環境別特化（一人暮らし→ファミリー→高齢者）",
                "体型・体質別特化（身長別→体重別→腰痛対策）"
            ])
        
        # 競合記事との差別化ポイント
        if conflicts:
            suggestions.extend([
                f"既存記事（{conflicts[0]['article']}）との明確な差別化ポイント設定",
                "新しいデータ・エビデンスの追加",
                "より実践的・具体的な内容に特化"
            ])
        
        suggestions.extend(base_strategies)
        
        return suggestions[:8]  # 最大8個まで
    
    def extract_quality_elements(self, relevant_materials: List[Dict]) -> Dict[str, Any]:
        """関連資料から品質向上要素を自動抽出"""
        
        quality_elements = {
            "proven_structures": [],
            "effective_phrases": [],
            "reliable_data_sources": [],
            "successful_keywords": [],
            "engagement_patterns": []
        }
        
        try:
            for material in relevant_materials[:3]:  # 上位3つの関連資料を分析
                file_path = material["file_path"]
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 構造パターン抽出（見出し構造）
                headings = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
                if headings:
                    structure_pattern = [f"H{len(h[0])}:{h[1][:30]}..." for h in headings[:5]]
                    quality_elements["proven_structures"].append({
                        "source": material["file_name"],
                        "structure": structure_pattern
                    })
                
                # 効果的なフレーズ抽出（強調表現）
                effective_phrases = re.findall(r'\*\*(.+?)\*\*', content)
                if effective_phrases:
                    quality_elements["effective_phrases"].extend(effective_phrases[:5])
                
                # データソース抽出（具体的な数値・研究結果）
                data_patterns = re.findall(r'(\d+%|\d+人|\d+倍|\d+円|\d+冊)', content)
                if data_patterns:
                    quality_elements["reliable_data_sources"].extend(data_patterns[:5])
                
                # キーワード使用パターン抽出
                for keyword in material["matched_keywords"]:
                    if keyword not in quality_elements["successful_keywords"]:
                        quality_elements["successful_keywords"].append(keyword)
        
        except Exception as e:
            print(f"❌ 品質要素抽出エラー: {e}")
        
        return quality_elements
    
    def generate_enhanced_suggestions(self, keywords: Dict, relevant_materials: List[Dict], 
                                    duplication_check: Dict, quality_elements: Dict) -> Dict[str, Any]:
        """統合情報に基づく記事作成提案の生成"""
        
        suggestions = {
            "recommended_approach": "",
            "content_structure_suggestions": [],
            "keyword_optimization": [],
            "quality_enhancement_tips": [],
            "differentiation_strategy": "",
            "risk_mitigation": []
        }
        
        try:
            # 推奨アプローチ決定
            if duplication_check["status"] == "SAFE":
                suggestions["recommended_approach"] = "通常のアプローチで高品質記事作成"
            elif duplication_check["status"] == "MODERATE_RISK":
                suggestions["recommended_approach"] = "差別化ポイントを明確にした特化型アプローチ"
            else:
                suggestions["recommended_approach"] = "大幅な角度変更または企画見直し推奨"
            
            # コンテンツ構造提案（関連資料の成功パターン活用）
            if quality_elements["proven_structures"]:
                suggestions["content_structure_suggestions"] = [
                    f"参考構造: {struct['source']} - {struct['structure']}"
                    for struct in quality_elements["proven_structures"][:2]
                ]
            
            # キーワード最適化提案
            successful_keywords = quality_elements["successful_keywords"][:5]
            suggestions["keyword_optimization"] = [
                f"高効果キーワード活用: {', '.join(successful_keywords)}",
                f"カテゴリ特化: {keywords['category']}系キーワード強化推奨"
            ]
            
            # 品質向上のヒント
            if quality_elements["effective_phrases"]:
                suggestions["quality_enhancement_tips"] = [
                    f"効果的な表現活用: {phrase}" for phrase in quality_elements["effective_phrases"][:3]
                ]
            
            if quality_elements["reliable_data_sources"]:
                suggestions["quality_enhancement_tips"].append(
                    f"具体的データ活用: {', '.join(quality_elements['reliable_data_sources'][:3])}"
                )
            
            # 差別化戦略
            if duplication_check["suggestions"]:
                suggestions["differentiation_strategy"] = duplication_check["suggestions"][0]
            
            # リスク緩和策
            if duplication_check["status"] != "SAFE":
                suggestions["risk_mitigation"] = [
                    "既存記事との明確な差別化ポイント設定",
                    "ターゲット読者層の特化",
                    "新しい情報・角度の追加"
                ]
        
        except Exception as e:
            print(f"❌ 提案生成エラー: {e}")
        
        return suggestions
    
    def auto_archive_utilization_workflow(self, user_request: str) -> Dict[str, Any]:
        """統合自動活用ワークフロー - メイン実行関数"""
        
        print("🔍 統合資料アーカイブ自動活用システム起動...")
        
        workflow_result = {
            "keywords": {},
            "relevant_materials": [],
            "duplication_check": {},
            "quality_elements": {},
            "suggestions": {},
            "workflow_status": "success"
        }
        
        try:
            # Step 1: キーワード自動抽出
            print("⚙️ Step 1: キーワード自動抽出...")
            workflow_result["keywords"] = self.extract_keywords_from_request(user_request)
            print(f"✅ 抽出完了: カテゴリ={workflow_result['keywords']['category']}, "
                  f"キーワード数={len(workflow_result['keywords']['detected_keywords'])}")
            
            # Step 2: 関連資料自動検索
            print("⚙️ Step 2: 関連資料自動検索...")
            workflow_result["relevant_materials"] = self.search_relevant_archives(workflow_result["keywords"])
            print(f"✅ 検索完了: 関連資料{len(workflow_result['relevant_materials'])}件発見")
            
            # Step 3: 重複リスク自動チェック
            print("⚙️ Step 3: 重複リスク自動チェック...")
            workflow_result["duplication_check"] = self.check_duplication_risk(workflow_result["keywords"])
            print(f"✅ チェック完了: リスクレベル={workflow_result['duplication_check']['status']}")
            
            # Step 4: 品質要素自動抽出
            print("⚙️ Step 4: 品質向上要素自動抽出...")
            workflow_result["quality_elements"] = self.extract_quality_elements(workflow_result["relevant_materials"])
            print(f"✅ 抽出完了: 品質要素{len(workflow_result['quality_elements']['successful_keywords'])}個特定")
            
            # Step 5: 統合提案生成
            print("⚙️ Step 5: 統合提案自動生成...")
            workflow_result["suggestions"] = self.generate_enhanced_suggestions(
                workflow_result["keywords"],
                workflow_result["relevant_materials"],
                workflow_result["duplication_check"],
                workflow_result["quality_elements"]
            )
            print("✅ 提案生成完了")
            
            print("🎉 統合資料アーカイブ活用ワークフロー完了！")
            
        except Exception as e:
            print(f"❌ ワークフローエラー: {e}")
            workflow_result["workflow_status"] = "error"
            workflow_result["error_message"] = str(e)
        
        return workflow_result
    
    def generate_workflow_report(self, workflow_result: Dict[str, Any]) -> str:
        """ワークフロー結果レポート生成"""
        
        if workflow_result["workflow_status"] == "error":
            return f"❌ ワークフローエラー: {workflow_result.get('error_message', '不明なエラー')}"
        
        report = f"""
📊 統合資料アーカイブ活用レポート
{'='*50}

🔍 キーワード分析結果:
- 検出カテゴリ: {workflow_result['keywords']['category']}
- メインキーワード: {', '.join(workflow_result['keywords']['main_keywords'])}
- 関連キーワード: {len(workflow_result['keywords']['detected_keywords'])}個検出

📚 関連資料発見状況:
- 発見資料数: {len(workflow_result['relevant_materials'])}件
- 高関連度資料: {len([m for m in workflow_result['relevant_materials'] if m['relevance_score'] > 5])}件

🚫 重複リスク分析:
- リスクステータス: {workflow_result['duplication_check']['status']}
- リスクレベル: {workflow_result['duplication_check']['risk_level']}/10
- 競合記事: {len(workflow_result['duplication_check']['conflicting_articles'])}件

💡 品質向上要素:
- 成功実績キーワード: {len(workflow_result['quality_elements']['successful_keywords'])}個
- 効果的フレーズ: {len(workflow_result['quality_elements']['effective_phrases'])}個
- 参考構造パターン: {len(workflow_result['quality_elements']['proven_structures'])}個

🎯 推奨アプローチ:
{workflow_result['suggestions']['recommended_approach']}

{'='*50}
✅ アーカイブ活用システム分析完了
"""
        
        return report


def main():
    """テスト実行用メイン関数"""
    system = ArchiveUtilizationSystem()
    
    # テスト用リクエスト
    test_requests = [
        "Audibleの使い方について記事を作成したい",
        "オーディオブックの効果について詳しく書きたい",
        "ベッドの選び方について記事を書いて"
    ]
    
    for request in test_requests:
        print(f"\n🧪 テスト: {request}")
        result = system.auto_archive_utilization_workflow(request)
        report = system.generate_workflow_report(result)
        print(report)


if __name__ == "__main__":
    main()