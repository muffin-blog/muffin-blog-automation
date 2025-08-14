#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Master System - 完全統合管理システム
絶対に間違えないシステム構築 - 2025-08-13

【機能】
1. 自動ルール表示・強制実行
2. 1セッション1ファイル強制管理
3. 書籍選定自動化システム
4. メモ作成強制アラート
5. 全作業の自動記録・追跡

【重要】この系統は絶対に守る必要があります
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

class ClaudeMasterSystem:
    """Claude用完全統合管理システム"""
    
    def __init__(self):
        """初期化 - 毎回実行される強制システム"""
        print("🚀 Claude Master System 起動中...")
        
        # 基本パス設定
        self.workspace = "/Users/satoumasamitsu/Desktop/osigoto/CLAUDE_WORKSPACE"
        self.logs_path = os.path.join(self.workspace, "LOGS")
        self.system_path = os.path.join(self.workspace, "SYSTEM")
        self.templates_path = os.path.join(self.workspace, "TEMPLATES")
        
        # 必須ファイル確認
        self.claude_md_path = os.path.join(self.workspace, "CLAUDE.md")
        self.rules_path = os.path.join(self.workspace, "日報ログ保護ルール.md")
        
        # システム状態
        self.session_log_file = None
        self.session_start_time = datetime.now()
        self.rules_violations = []
        
        # 強制初期化実行
        self.force_load_rules()
        self.force_display_critical_rules()
        self.check_session_log_file()
        
    def force_load_rules(self):
        """ルール強制読み込み - 必ず実行"""
        try:
            with open(self.claude_md_path, 'r', encoding='utf-8') as f:
                self.claude_rules = f.read()
            
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                self.protection_rules = f.read()
                
            print("✅ ルールファイル読み込み完了")
            return True
            
        except Exception as e:
            print(f"🚨 【重大エラー】ルールファイルが読み込めません: {e}")
            return False
    
    def force_display_critical_rules(self):
        """重要ルールの強制表示 - 毎回実行"""
        print("\n" + "="*60)
        print("🚨 【絶対遵守ルール】- 毎回確認必須")
        print("="*60)
        print("1️⃣ 1セッション1ファイル - 追記のみ、新規作成禁止")
        print("2️⃣ メモ指示時 - 必ず既存日報に詳細記録")
        print("3️⃣ 書籍選定時 - 5つの基準チェックリスト必須実行")
        print("4️⃣ システム約束 - 「作ります」と言ったら必ず完成まで")
        print("5️⃣ 強制記録 - 重要な学習内容は全て記録")
        print("="*60)
        print("⚠️  これらに違反した場合は自動でアラート表示\n")
    
    def check_session_log_file(self):
        """セッション日報ファイルチェック - 1セッション1ファイル強制"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 今日の既存ログファイル検索
        existing_logs = []
        for file in os.listdir(self.logs_path):
            if file.startswith(today) and file.endswith('.md'):
                existing_logs.append(file)
        
        if existing_logs:
            self.session_log_file = os.path.join(self.logs_path, existing_logs[0])
            print(f"📝 既存日報ファイル検出: {existing_logs[0]}")
            print("✅ 新しい内容は既存ファイルに追記してください")
        else:
            print(f"📝 今日の日報ファイルなし - 必要時に作成します")
            self.session_log_file = None
    
    def force_memo_creation(self, memo_content: str, memo_type: str = "学習内容"):
        """メモ作成強制実行 - メモ指示検出時"""
        print(f"\n🚨 【メモ作成強制実行】- {memo_type}")
        
        if not self.session_log_file:
            # 新規作成
            today = datetime.now().strftime('%Y-%m-%d')
            session_type = memo_type.replace(" ", "_")
            filename = f"{today}_{session_type}_詳細日報.md"
            self.session_log_file = os.path.join(self.logs_path, filename)
            
            # 初期内容作成
            initial_content = f"""# {today} {memo_type} 詳細日報

## セッション概要
- **作業日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
- **セッション種別**: {memo_type}
- **Claude Master System**: 自動記録実行

## 詳細記録

### {datetime.now().strftime('%H:%M:%S')} - {memo_type}
{memo_content}

---
"""
            
            with open(self.session_log_file, 'w', encoding='utf-8') as f:
                f.write(initial_content)
            print(f"📝 新規日報作成: {filename}")
            
        else:
            # 既存ファイルに追記
            append_content = f"""
### {datetime.now().strftime('%H:%M:%S')} - {memo_type}
{memo_content}

---
"""
            
            with open(self.session_log_file, 'a', encoding='utf-8') as f:
                f.write(append_content)
            print(f"📝 既存日報に追記完了")
    
    def book_selection_system(self, article_theme: str, target_readers: str = "初心者～中級者"):
        """書籍選定システム - 5つの基準自動チェック"""
        print(f"\n📚 【書籍選定システム起動】")
        print(f"記事テーマ: {article_theme}")
        print(f"対象読者: {target_readers}")
        
        checklist = {
            "認知度": "YouTubeやSNSで見たことがある程度の知名度",
            "実用性": "読者が「役に立ちそう」と直感的に感じる内容",
            "難易度": "簡単すぎず、難しすぎない適切なレベル",
            "展開性": "関連記事を複数作成できる可能性",
            "心理性": "知ってるけど読めてない本に該当"
        }
        
        print("\n✅ 【必須チェックリスト】")
        for i, (criterion, description) in enumerate(checklist.items(), 1):
            print(f"{i}. {criterion}: {description}")
        
        print("\n🔍 【WebSearch実行手順】")
        print(f"1. 'Audible {article_theme} おすすめ 2025'")
        print(f"2. 'Audible Kindle 両方対応 {article_theme}'")
        print(f"3. '具体的書籍名 両プラットフォーム確認'")
        
        # 自動メモ記録
        memo_content = f"""## 書籍選定システム実行

**記事テーマ**: {article_theme}
**対象読者**: {target_readers}

**チェック項目**:
{chr(10).join([f"- {k}: {v}" for k, v in checklist.items()])}

**検索キーワード**:
1. Audible {article_theme} おすすめ 2025
2. Audible Kindle 両方対応 {article_theme}  
3. 具体的書籍名の両プラットフォーム確認

**重要**: 音声だけでは理解困難で、文字との組み合わせで真価を発揮する書籍を選定
"""
        
        self.force_memo_creation(memo_content, "書籍選定作業")
        return checklist
    
    def detect_violations(self, user_input: str = "", claude_output: str = ""):
        """ルール違反検出システム"""
        violations = []
        
        # 新規ファイル作成違反チェック
        if "新規作成" in claude_output and "日報" in claude_output:
            violations.append("1セッション1ファイルルール違反の可能性")
        
        # メモ指示無視チェック  
        if any(keyword in user_input for keyword in ["メモして", "記録して", "システム化"]):
            violations.append("メモ作成指示検出 - 強制記録実行必要")
        
        # システム約束違反チェック
        if "システム作ります" in claude_output:
            violations.append("システム構築約束 - 完成まで責任を持つ必要")
        
        if violations:
            self.display_violation_alert(violations)
        
        return violations
    
    def display_violation_alert(self, violations: List[str]):
        """ルール違反アラート表示"""
        print("\n" + "🚨"*20)
        print("【重大違反アラート】")
        print("🚨"*20)
        
        for i, violation in enumerate(violations, 1):
            print(f"{i}. {violation}")
        
        print("🚨"*20)
        print("⚠️  これらの違反は必ず修正してください")
        print("🚨"*20 + "\n")
    
    def auto_system_completion_check(self):
        """システム構築完了チェック"""
        if "システム作ります" in str(getattr(self, '_previous_promises', [])):
            print("\n⚠️ 【未完了システム検出】")
            print("前回「システム作ります」と約束した項目があります")
            print("必ず完成させてから新しい作業に進んでください")
    
    def force_session_summary(self):
        """セッション終了時の強制サマリー"""
        if self.session_log_file:
            summary_content = f"""
## セッション完了サマリー ({datetime.now().strftime('%H:%M:%S')})

**セッション時間**: {datetime.now() - self.session_start_time}
**記録されたファイル**: {os.path.basename(self.session_log_file)}
**ルール遵守状況**: {"✅ 良好" if not self.rules_violations else f"⚠️ 違反{len(self.rules_violations)}件"}

**重要学習内容の記録状況**: 記録済み
**次回セッションでの参照**: このファイルを必ず確認

**Claude Master System**: セッション管理完了
"""
            
            with open(self.session_log_file, 'a', encoding='utf-8') as f:
                f.write(summary_content)
            
            print(f"\n📊 セッションサマリー記録完了: {os.path.basename(self.session_log_file)}")

# グローバル実行（このファイルが読み込まれる度に実行）
claude_system = ClaudeMasterSystem()

def memo_now(content: str, memo_type: str = "重要学習"):
    """メモ強制実行関数"""
    return claude_system.force_memo_creation(content, memo_type)

def book_select(theme: str, readers: str = "初心者～中級者"):
    """書籍選定システム実行関数"""
    return claude_system.book_selection_system(theme, readers)

def check_rules():
    """ルール確認関数"""
    claude_system.force_display_critical_rules()

if __name__ == "__main__":
    print("Claude Master System は正常に初期化されました")
    print("このシステムが毎回実行され、違反を防ぎます")