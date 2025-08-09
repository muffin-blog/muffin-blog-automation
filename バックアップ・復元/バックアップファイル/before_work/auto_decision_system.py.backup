"""
自立判断システム - 何をすべきか自動決定
マスタープランに基づく優先度判定
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests
import json
from datetime import datetime

class AutoDecisionSystem:
    """自立判断システム"""
    
    def __init__(self):
        self.wp = WordPressBlogAutomator(
            site_url="https://muffin-blog.com",
            username="muffin1203",
            password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
        )
        
        # 優先度ルール
        self.priority_rules = {
            "seo_foundation": {
                "priority": 1,
                "description": "SEO基礎設定（H1、内部リンク、構造化データ）未完了",
                "required_completion": 100
            },
            "technical_issues": {
                "priority": 2, 
                "description": "技術的問題（リンク切れ、エラー）が存在",
                "required_completion": 95
            },
            "content_optimization": {
                "priority": 3,
                "description": "既存コンテンツの最適化が必要",
                "required_completion": 80
            },
            "new_content": {
                "priority": 4,
                "description": "新規コンテンツ作成",
                "required_completion": 0
            }
        }
        
        # 既存記事情報
        self.existing_posts = {
            2732: {
                "title": "Audibleでお金の勉強！これから貯金・節約・投資を学びたい人におすすめの書籍6選",
                "keywords": ["Audible", "お金", "勉強", "書籍"],
                "seo_status": {
                    "h1_tag": False,
                    "internal_links": 5,  # 推奨20以上
                    "structured_data": False,
                    "alt_attributes": 30  # 推奨50%以上
                }
            },
            2677: {
                "title": "Audibleの休会制度を完全ガイド！メリットや注意点、退会との違いを丁寧に解説",
                "keywords": ["Audible", "休会", "退会"],
                "seo_status": {
                    "h1_tag": False,
                    "internal_links": 3,
                    "structured_data": False,
                    "alt_attributes": 20
                }
            },
            2625: {
                "title": "安心してAudibleを始めるために事前にチェック！退会・解約方法を徹底解説",
                "keywords": ["Audible", "退会", "解約"],
                "seo_status": {
                    "h1_tag": False,
                    "internal_links": 4,
                    "structured_data": False,
                    "alt_attributes": 25
                }
            },
            2535: {
                "title": "世界一分かりやすいAudible（オーディブル）の始め方！アプリの使い方を完全ガイド",
                "keywords": ["Audible", "始め方", "使い方"],
                "seo_status": {
                    "h1_tag": False,
                    "internal_links": 8,
                    "structured_data": False,
                    "alt_attributes": 40
                }
            },
            2210: {
                "title": "「耳活で人生は変わる！」1年後の自分が楽になるたった一つの習慣",
                "keywords": ["耳活", "習慣", "Audible"],
                "seo_status": {
                    "h1_tag": False,
                    "internal_links": 6,
                    "structured_data": False,
                    "alt_attributes": 35
                }
            }
        }
    
    def analyze_current_status(self):
        """現在の状況を分析して優先タスクを決定"""
        
        print("🧠 自立判断システム - 現状分析開始")
        print("=" * 60)
        
        analysis_result = {
            "seo_foundation_completion": 0,
            "technical_health_score": 0,
            "content_optimization_score": 0,
            "priority_tasks": [],
            "next_actions": []
        }
        
        # 1. SEO基礎完了率の算出
        seo_completion = self._calculate_seo_completion()
        analysis_result["seo_foundation_completion"] = seo_completion
        
        print(f"📊 SEO基礎完了率: {seo_completion}%")
        
        # 2. 技術的健全性スコア
        tech_score = self._calculate_technical_health()
        analysis_result["technical_health_score"] = tech_score
        
        print(f"⚙️ 技術的健全性: {tech_score}%")
        
        # 3. コンテンツ最適化スコア
        content_score = self._calculate_content_optimization()
        analysis_result["content_optimization_score"] = content_score
        
        print(f"📝 コンテンツ最適化: {content_score}%")
        
        # 4. 優先タスクの決定
        priority_tasks = self._determine_priority_tasks(
            seo_completion, tech_score, content_score
        )
        analysis_result["priority_tasks"] = priority_tasks
        
        # 5. 次のアクションを決定
        next_actions = self._determine_next_actions(priority_tasks)
        analysis_result["next_actions"] = next_actions
        
        return analysis_result
    
    def _calculate_seo_completion(self):
        """SEO基礎設定の完了率を計算"""
        
        total_posts = len(self.existing_posts)
        total_seo_items = total_posts * 4  # H1, 内部リンク, 構造化データ, alt属性
        
        completed_items = 0
        
        for post_id, post_data in self.existing_posts.items():
            seo_status = post_data["seo_status"]
            
            # H1タグ
            if seo_status["h1_tag"]:
                completed_items += 1
                
            # 内部リンク（20本以上で完了とみなす）
            if seo_status["internal_links"] >= 20:
                completed_items += 1
                
            # 構造化データ
            if seo_status["structured_data"]:
                completed_items += 1
                
            # alt属性（50%以上で完了とみなす）
            if seo_status["alt_attributes"] >= 50:
                completed_items += 1
        
        completion_rate = (completed_items / total_seo_items) * 100
        return round(completion_rate, 1)
    
    def _calculate_technical_health(self):
        """技術的健全性スコアを計算"""
        
        # 前回のサイトヘルス診断結果を参考
        # 実際の実装では、site_health_monitor.pyの結果を読み込む
        
        health_factors = {
            "api_connection": 100,  # WordPress API正常
            "site_speed": 100,      # 0.12秒（優秀）
            "broken_links": 60,     # 71件→31件修正で改善
            "seo_basics": 90        # robots.txt, sitemap等は正常
        }
        
        # 重み付き平均
        weights = {
            "api_connection": 0.2,
            "site_speed": 0.2,
            "broken_links": 0.4,
            "seo_basics": 0.2
        }
        
        weighted_score = sum(
            health_factors[factor] * weights[factor] 
            for factor in health_factors
        )
        
        return round(weighted_score, 1)
    
    def _calculate_content_optimization(self):
        """コンテンツ最適化スコアを計算"""
        
        optimization_factors = {
            "content_quality": 70,    # 一定の品質はあるが改善余地あり
            "keyword_targeting": 75,  # キーワードは設定済み
            "user_engagement": 60,    # 内部リンク不足で回遊率低い
            "competitive_advantage": 50  # 競合比較で劣位
        }
        
        average_score = sum(optimization_factors.values()) / len(optimization_factors)
        return round(average_score, 1)
    
    def _determine_priority_tasks(self, seo_completion, tech_score, content_score):
        """優先タスクを決定"""
        
        priority_tasks = []
        
        # Rule 1: SEO基礎設定優先
        if seo_completion < self.priority_rules["seo_foundation"]["required_completion"]:
            priority_tasks.append({
                "category": "seo_foundation",
                "priority": 1,
                "description": f"SEO基礎設定完了率: {seo_completion}% → 100%必要",
                "tasks": [
                    "H1タグ設定（全記事）",
                    "内部リンク追加（各記事20本以上）", 
                    "構造化データ実装",
                    "alt属性最適化"
                ]
            })
        
        # Rule 2: 技術的問題修正
        if tech_score < self.priority_rules["technical_issues"]["required_completion"]:
            priority_tasks.append({
                "category": "technical_issues",
                "priority": 2,
                "description": f"技術的健全性: {tech_score}% → 95%以上必要",
                "tasks": [
                    "残存リンク切れの修正",
                    "サイト監視システム稼働",
                    "パフォーマンス最適化"
                ]
            })
        
        # Rule 3: コンテンツ最適化
        if content_score < self.priority_rules["content_optimization"]["required_completion"]:
            priority_tasks.append({
                "category": "content_optimization", 
                "priority": 3,
                "description": f"コンテンツ最適化: {content_score}% → 80%以上必要",
                "tasks": [
                    "既存記事の品質向上",
                    "競合分析に基づく差別化",
                    "アイキャッチ画像作成"
                ]
            })
        
        return sorted(priority_tasks, key=lambda x: x["priority"])
    
    def _determine_next_actions(self, priority_tasks):
        """次に実行すべきアクションを決定"""
        
        if not priority_tasks:
            return [{
                "action": "new_content_creation",
                "description": "基礎設定完了済み。新規コンテンツ作成を開始。",
                "steps": [
                    "競合分析実行",
                    "キーワードギャップ分析", 
                    "新記事戦略策定"
                ]
            }]
        
        # 最優先タスクに基づくアクション決定
        top_priority = priority_tasks[0]
        
        if top_priority["category"] == "seo_foundation":
            return [{
                "action": "seo_foundation_setup",
                "description": "SEO基礎設定を完了させる",
                "steps": [
                    "SEO修正ツール群の開発",
                    "記事ID 2732から順次SEO修正実行",
                    "修正結果の検証"
                ],
                "tools_needed": [
                    "seo_optimizer.py",
                    "internal_link_builder.py", 
                    "structured_data_injector.py"
                ]
            }]
        
        elif top_priority["category"] == "technical_issues":
            return [{
                "action": "technical_fixes",
                "description": "技術的問題を修正",
                "steps": [
                    "詳細サイト診断実行",
                    "問題箇所の特定・修正",
                    "監視システム稼働"
                ]
            }]
        
        elif top_priority["category"] == "content_optimization":
            return [{
                "action": "content_improvement",
                "description": "既存コンテンツの品質向上",
                "steps": [
                    "競合記事詳細分析",
                    "既存記事の改善点特定",
                    "段階的な品質向上実行"
                ]
            }]
    
    def check_duplicate_content_risk(self, proposed_title, proposed_keywords):
        """重複コンテンツリスクをチェック"""
        
        print(f"\n🔍 重複コンテンツチェック: {proposed_title}")
        
        risks = []
        
        for post_id, post_data in self.existing_posts.items():
            existing_keywords = set(post_data["keywords"])
            proposed_keywords_set = set(proposed_keywords)
            
            # キーワード重複率を計算
            overlap = existing_keywords.intersection(proposed_keywords_set)
            overlap_rate = len(overlap) / len(existing_keywords.union(proposed_keywords_set)) * 100
            
            if overlap_rate > 50:  # 50%以上の重複で警告
                risks.append({
                    "post_id": post_id,
                    "existing_title": post_data["title"],
                    "overlap_keywords": list(overlap),
                    "overlap_rate": round(overlap_rate, 1),
                    "recommendation": "既存記事の改善を推奨" if overlap_rate > 80 else "差別化要素の追加が必要"
                })
        
        return risks
    
    def generate_decision_report(self):
        """判断結果をレポート形式で出力"""
        
        analysis = self.analyze_current_status()
        
        print("\n" + "="*60)
        print("🎯 自立判断システム - 決定レポート")
        print("="*60)
        
        print(f"\n📊 現状分析結果:")
        print(f"   SEO基礎完了率: {analysis['seo_foundation_completion']}%")
        print(f"   技術的健全性: {analysis['technical_health_score']}%") 
        print(f"   コンテンツ最適化: {analysis['content_optimization_score']}%")
        
        print(f"\n🎯 優先タスク:")
        if analysis['priority_tasks']:
            for i, task in enumerate(analysis['priority_tasks'], 1):
                print(f"   {i}. {task['description']}")
                for subtask in task['tasks']:
                    print(f"      - {subtask}")
        else:
            print("   基礎設定完了済み。新規コンテンツ作成フェーズ。")
        
        print(f"\n🚀 次のアクション:")
        for action in analysis['next_actions']:
            print(f"   アクション: {action['description']}")
            for i, step in enumerate(action['steps'], 1):
                print(f"      {i}. {step}")
            
            if 'tools_needed' in action:
                print(f"   必要ツール:")
                for tool in action['tools_needed']:
                    print(f"      - {tool}")
        
        print(f"\n📅 推奨実行順序:")
        if analysis['seo_foundation_completion'] < 100:
            print("   1. SEO基礎設定完了（最優先）")
            print("   2. 技術的問題修正")
            print("   3. コンテンツ品質向上")
            print("   4. 新規コンテンツ作成")
        else:
            print("   1. 競合分析実行")
            print("   2. 新記事戦略策定")
            print("   3. 差別化コンテンツ作成")
        
        return analysis

if __name__ == "__main__":
    print("🧠 自立判断システム起動")
    print("="*60)
    
    decision_system = AutoDecisionSystem()
    report = decision_system.generate_decision_report()
    
    # 重複コンテンツチェックの例
    print("\n" + "="*60)
    print("🔍 重複コンテンツリスク例")
    print("="*60)
    
    risks = decision_system.check_duplicate_content_risk(
        "Audibleでお金の勉強！投資初心者おすすめ書籍10選",
        ["Audible", "お金", "勉強", "投資", "初心者"]
    )
    
    if risks:
        print("⚠️ 重複リスク検出:")
        for risk in risks:
            print(f"   既存記事ID {risk['post_id']}: {risk['overlap_rate']}%重複")
            print(f"   推奨: {risk['recommendation']}")
    else:
        print("✅ 重複リスクなし - 新規作成可能")
    
    print(f"\n✅ 判断システム完了")
    print("決定に従って次のアクションを実行してください。")