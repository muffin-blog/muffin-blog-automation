"""
日報自動生成システム
毎回のセッション終了時に自動で日報を生成・保存する
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional

class DailyReportAutomation:
    """日報自動生成・管理システム"""
    
    def __init__(self, base_path: str = None):
        self.base_path = base_path or "/Users/satoumasamitsu/osigoto/ブログ自動化/book_publication"
        self.reports_path = os.path.join(self.base_path, "knowledge_base", "daily_reports")
        self.session_data = {}
        
        # ディレクトリ作成
        os.makedirs(self.reports_path, exist_ok=True)
    
    def start_session_tracking(self, theme: str = ""):
        """セッション追跡開始"""
        self.session_data = {
            "start_time": datetime.now(),
            "theme": theme,
            "implementations": [],
            "technical_discoveries": [],
            "challenges_solved": [],
            "workflow_improvements": [],
            "achievements": {},
            "insights": [],
            "next_plans": []
        }
        print(f"📝 セッション追跡開始: {theme}")
    
    def log_implementation(self, feature_name: str, file_path: str, description: str, characteristics: List[str] = None):
        """実装機能の記録"""
        implementation = {
            "feature_name": feature_name,
            "file_path": file_path,
            "description": description,
            "characteristics": characteristics or [],
            "timestamp": datetime.now().isoformat()
        }
        self.session_data["implementations"].append(implementation)
        print(f"🛠 実装記録: {feature_name}")
    
    def log_technical_discovery(self, category: str, discovery: str, details: str):
        """技術的発見の記録"""
        discovery_record = {
            "category": category,
            "discovery": discovery,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.session_data["technical_discoveries"].append(discovery_record)
        print(f"💡 技術発見記録: {discovery}")
    
    def log_challenge_solved(self, challenge: str, problem: str, solution: str, learning: str):
        """課題解決の記録"""
        challenge_record = {
            "challenge": challenge,
            "problem": problem,
            "solution": solution,
            "learning": learning,
            "timestamp": datetime.now().isoformat()
        }
        self.session_data["challenges_solved"].append(challenge_record)
        print(f"🐛 課題解決記録: {challenge}")
    
    def log_workflow_improvement(self, improvement: str, before: str, after: str, effect: str):
        """ワークフロー改善の記録"""
        improvement_record = {
            "improvement": improvement,
            "before": before,
            "after": after,
            "effect": effect,
            "timestamp": datetime.now().isoformat()
        }
        self.session_data["workflow_improvements"].append(improvement_record)
        print(f"🔄 ワークフロー改善記録: {improvement}")
    
    def log_achievement(self, metric_name: str, value: str, description: str = ""):
        """成果の記録"""
        self.session_data["achievements"][metric_name] = {
            "value": value,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        print(f"📈 成果記録: {metric_name} = {value}")
    
    def log_book_insight(self, insight_type: str, content: str):
        """書籍化向け洞察の記録"""
        insight_record = {
            "type": insight_type,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.session_data["insights"].append(insight_record)
        print(f"📚 書籍化洞察記録: {insight_type}")
    
    def log_next_plan(self, plan: str, priority: str = "medium"):
        """次回計画の記録"""
        plan_record = {
            "plan": plan,
            "priority": priority,
            "timestamp": datetime.now().isoformat()
        }
        self.session_data["next_plans"].append(plan_record)
        print(f"🎯 次回計画記録: {plan}")
    
    def generate_daily_report(self) -> str:
        """日報自動生成"""
        
        if not self.session_data:
            return self.generate_template_report()
        
        today = datetime.now().strftime("%Y-%m-%d")
        session_time = self.calculate_session_duration()
        
        report = f"""# 📅 日報 - {today}

## 🎯 セッション概要
**テーマ**: {self.session_data.get('theme', '未記録')}

**作業時間**: {session_time}

**達成状況**: ✅ {len(self.session_data.get('implementations', []))}個の機能実装完了

---

## 🛠 実装・改善した機能
"""
        
        # 実装機能
        for i, impl in enumerate(self.session_data.get('implementations', []), 1):
            report += f"""
### {i}. **{impl['feature_name']}**
- **ファイル**: `{impl['file_path']}`
- **機能**: {impl['description']}
- **特徴**: {', '.join(impl['characteristics'])}
"""
        
        report += "\n---\n\n## 💡 技術的発見\n"
        
        # 技術的発見
        discoveries_by_category = {}
        for discovery in self.session_data.get('technical_discoveries', []):
            category = discovery['category']
            if category not in discoveries_by_category:
                discoveries_by_category[category] = []
            discoveries_by_category[category].append(discovery)
        
        for category, discoveries in discoveries_by_category.items():
            report += f"\n### {category}\n"
            for discovery in discoveries:
                report += f"""
1. **{discovery['discovery']}**
   - {discovery['details']}
"""
        
        report += "\n---\n\n## 🐛 課題と解決\n"
        
        # 課題解決
        for i, challenge in enumerate(self.session_data.get('challenges_solved', []), 1):
            report += f"""
### 課題{i}: {challenge['challenge']}
**問題**: {challenge['problem']}
**解決**: {challenge['solution']}
**学習**: {challenge['learning']}
"""
        
        report += "\n---\n\n## 🔄 ワークフロー改善\n"
        
        # ワークフロー改善
        for i, improvement in enumerate(self.session_data.get('workflow_improvements', []), 1):
            report += f"""
### 改善{i}: {improvement['improvement']}
**Before**: {improvement['before']}
**After**: {improvement['after']}
**効果**: {improvement['effect']}
"""
        
        report += "\n---\n\n## 📈 成果・インパクト\n"
        
        # 成果
        achievements = self.session_data.get('achievements', {})
        if achievements:
            report += "\n### 定量的成果\n"
            for metric, data in achievements.items():
                report += f"- **{metric}**: {data['value']}\n"
                if data['description']:
                    report += f"  - {data['description']}\n"
        
        report += "\n---\n\n## 📚 書籍化に向けた今日の洞察\n"
        
        # 書籍化洞察
        insights_by_type = {}
        for insight in self.session_data.get('insights', []):
            insight_type = insight['type']
            if insight_type not in insights_by_type:
                insights_by_type[insight_type] = []
            insights_by_type[insight_type].append(insight['content'])
        
        for insight_type, contents in insights_by_type.items():
            report += f"\n### {insight_type}\n"
            for content in contents:
                report += f"- {content}\n"
        
        report += "\n---\n\n## 🎯 次回セッション予定\n"
        
        # 次回計画
        plans = self.session_data.get('next_plans', [])
        high_priority = [p for p in plans if p['priority'] == 'high']
        medium_priority = [p for p in plans if p['priority'] == 'medium']
        low_priority = [p for p in plans if p['priority'] == 'low']
        
        if high_priority:
            report += "\n### 優先事項\n"
            for plan in high_priority:
                report += f"1. **{plan['plan']}**\n"
        
        if medium_priority:
            report += "\n### 継続課題\n"
            for plan in medium_priority:
                report += f"- {plan['plan']}\n"
        
        if low_priority:
            report += "\n### 検討事項\n"
            for plan in low_priority:
                report += f"- {plan['plan']}\n"
        
        report += f"""
---

**記録者**: Claude Code  
**確認者**: ユーザー  
**次回更新予定**: 次回作業セッション後
**セッション時間**: {session_time}
"""
        
        return report
    
    def calculate_session_duration(self) -> str:
        """セッション時間計算"""
        if 'start_time' not in self.session_data:
            return "未記録"
        
        duration = datetime.now() - self.session_data['start_time']
        hours = int(duration.total_seconds() // 3600)
        minutes = int((duration.total_seconds() % 3600) // 60)
        
        if hours > 0:
            return f"{hours}時間{minutes}分"
        else:
            return f"{minutes}分"
    
    def generate_template_report(self) -> str:
        """テンプレート日報生成"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        return f"""# 📅 日報 - {today}

## 🎯 セッション概要
**テーマ**: [作業テーマを記入]

**作業時間**: [作業時間を記入]

**達成状況**: [達成状況を記入]

---

## 🛠 実装・改善した機能

### 1. **[機能名]**
- **ファイル**: `[ファイルパス]`
- **機能**: [機能説明]
- **特徴**: [特徴・特色]

---

## 💡 技術的発見

### [発見カテゴリ]

1. **[具体的発見]**
   - [詳細説明]

---

## 🐛 課題と解決

### 課題1: [課題名]
**問題**: [問題内容]
**解決**: [解決方法]
**学習**: [学習内容]

---

## 🔄 ワークフロー改善

### 改善1: [改善名]
**Before**: [改善前]
**After**: [改善後] 
**効果**: [効果・結果]

---

## 📈 成果・インパクト

### 定量的成果
- **[指標名]**: [数値・結果]

### 定性的成果
- **[成果名]**: [説明]

---

## 📚 書籍化に向けた今日の洞察

### 章立てのヒント
1. **第X章**: [章タイトル] - [章概要]

### 読者への価値提案
- **[価値名]**: [価値説明]

---

## 🎯 次回セッション予定

### 優先事項
1. **[優先項目1]**

### 継続課題
- [継続課題1]

---

## 📝 メモ・アイデア

### [メモカテゴリ]
- [アイデア・メモ]

---

**記録者**: Claude Code  
**確認者**: ユーザー  
**次回更新予定**: 次回作業セッション後
"""
    
    def save_daily_report(self) -> str:
        """日報保存"""
        report_content = self.generate_daily_report()
        
        today = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H%M%S")
        
        # ファイル名生成
        if self.session_data.get('theme'):
            safe_theme = "".join(c for c in self.session_data['theme'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_theme = safe_theme.replace(' ', '_')
            filename = f"{today}_{safe_theme}_{timestamp}.md"
        else:
            filename = f"{today}_session_{timestamp}.md"
        
        file_path = os.path.join(self.reports_path, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"💾 日報保存完了: {filename}")
        return file_path
    
    def get_report_summary(self) -> Dict:
        """セッションサマリー生成"""
        return {
            "theme": self.session_data.get('theme', ''),
            "duration": self.calculate_session_duration(),
            "implementations_count": len(self.session_data.get('implementations', [])),
            "discoveries_count": len(self.session_data.get('technical_discoveries', [])),
            "challenges_solved": len(self.session_data.get('challenges_solved', [])),
            "improvements_count": len(self.session_data.get('workflow_improvements', [])),
            "achievements_count": len(self.session_data.get('achievements', {})),
            "insights_count": len(self.session_data.get('insights', [])),
            "next_plans_count": len(self.session_data.get('next_plans', []))
        }

# セッション終了時の自動実行関数
def auto_finalize_session(report_system: DailyReportAutomation):
    """セッション自動終了処理"""
    
    print("\n" + "="*60)
    print("📝 セッション終了 - 日報自動生成中...")
    print("="*60)
    
    # サマリー表示
    summary = report_system.get_report_summary()
    print(f"📊 セッションサマリー:")
    print(f"   テーマ: {summary['theme']}")
    print(f"   作業時間: {summary['duration']}")
    print(f"   実装機能: {summary['implementations_count']}件")
    print(f"   技術発見: {summary['discoveries_count']}件")
    print(f"   課題解決: {summary['challenges_solved']}件")
    print(f"   改善項目: {summary['improvements_count']}件")
    print(f"   成果記録: {summary['achievements_count']}件")
    print(f"   書籍洞察: {summary['insights_count']}件")
    print(f"   次回計画: {summary['next_plans_count']}件")
    
    # 日報保存
    report_path = report_system.save_daily_report()
    
    print(f"\n✅ 日報生成完了: {os.path.basename(report_path)}")
    print("📚 書籍化知識ベースに蓄積されました")
    print("="*60 + "\n")
    
    return report_path

# 使用例
if __name__ == "__main__":
    # 日報システムテスト
    report_system = DailyReportAutomation()
    
    # サンプルセッション
    report_system.start_session_tracking("書籍化システム構築")
    
    # サンプルログ
    report_system.log_implementation(
        "書籍出版システム",
        "book_publication/publishing_workflow/book_creation_system.py", 
        "日報から自動で書籍原稿を生成するシステム",
        ["章立て自動生成", "原稿ドラフト作成", "HTML出力対応"]
    )
    
    report_system.log_technical_discovery(
        "AI協働パターン",
        "知識蓄積の自動化",
        "日々の作業を自動記録し、書籍化につなげる仕組みの重要性"
    )
    
    # 日報生成・保存
    auto_finalize_session(report_system)