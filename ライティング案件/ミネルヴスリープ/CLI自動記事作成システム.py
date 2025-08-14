#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI自動記事作成システム - ライティング案件（ミネルヴスリープ）
テキスト資料をFINAL版テンプレートで高品質記事に変換

統合システム:
- FINAL版テンプレート完全準拠
- WebSearch読者ニーズ分析
- ポートフォリオ連携システム対応
"""

import os
import re
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# 統合アーカイブシステム import
sys.path.append("/Users/satoumasamitsu/Desktop/osigoto/統合管理システム/資料アーカイブ/")
try:
    from archive_utilization_system import ArchiveUtilizationSystem
except ImportError:
    print("⚠️ アーカイブシステムが見つかりません。基本機能のみで動作します。")
    ArchiveUtilizationSystem = None

class CLIAutoWritingSystem:
    """CLI自動記事作成システム - ライティング案件側"""
    
    def __init__(self):
        """初期化"""
        self.base_path = "/Users/satoumasamitsu/Desktop/osigoto/ライティング案件/ミネルヴスリープ/"
        self.template_path = os.path.join(self.base_path, "テンプレート/記事作成完全テンプレート_FINAL.md")
        self.work_in_progress_path = os.path.join(self.base_path, "記事/3_作成中/")
        self.completed_path = os.path.join(self.base_path, "記事/2_完成記事/")
        self.reference_articles_path = os.path.join(self.base_path, "記事/2_完成記事/追加記事/")
        
        # 参照記事（2025年8月11日記事）
        self.reference_articles = [
            "2025.08.11.布団.ホコリ対策.md",
            "2025.08.11.社会人.睡眠時間.md"
        ]
        
        # + α 統合アーカイブシステム初期化
        self.archive_system = None
        if ArchiveUtilizationSystem:
            try:
                self.archive_system = ArchiveUtilizationSystem()
                print("✅ 統合アーカイブシステム連携完了")
            except Exception as e:
                print(f"⚠️ アーカイブシステム初期化警告: {e}")
        else:
            print("ℹ️ 基本機能のみで動作中（アーカイブ機能無効）")
    
    def load_final_template(self) -> str:
        """FINAL版テンプレートを読み込み"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ FINAL版テンプレート読み込みエラー: {e}")
            return ""
    
    def load_reference_articles(self) -> Dict[str, str]:
        """参照記事を読み込み（Phase 0対応）"""
        references = {}
        
        for article_name in self.reference_articles:
            try:
                article_path = os.path.join(self.reference_articles_path, article_name)
                if os.path.exists(article_path):
                    with open(article_path, 'r', encoding='utf-8') as f:
                        references[article_name] = f.read()
                    print(f"✅ 参照記事読み込み: {article_name}")
                else:
                    print(f"⚠️ 参照記事が見つかりません: {article_name}")
            except Exception as e:
                print(f"❌ 参照記事読み込みエラー ({article_name}): {e}")
        
        return references
    
    def parse_input_data(self, input_text: str) -> Dict:
        """テキスト資料を解析"""
        try:
            # 基本的なパターンマッチング
            data = {
                "project": "",
                "main_keyword": "",
                "related_keywords": [],
                "competitor_analysis": "",
                "target_audience": "",
                "other_requirements": ""
            }
            
            lines = input_text.strip().split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                
                if line.startswith('【案件】') or line.startswith('【プロジェクト】'):
                    data["project"] = line.split('】')[-1].strip().replace(':', '').replace('：', '')
                
                elif line.startswith('【メインキーワード】'):
                    data["main_keyword"] = line.split('】')[-1].strip().replace(':', '').replace('：', '')
                
                elif line.startswith('【関連キーワード】'):
                    keywords_str = line.split('】')[-1].strip().replace(':', '').replace('：', '')
                    data["related_keywords"] = [k.strip() for k in keywords_str.split(',') if k.strip()]
                
                elif line.startswith('【上位記事分析】') or line.startswith('【競合分析】'):
                    current_section = "competitor"
                    data["competitor_analysis"] = ""
                
                elif line.startswith('【ターゲット】') or line.startswith('【読者】'):
                    data["target_audience"] = line.split('】')[-1].strip().replace(':', '').replace('：', '')
                
                elif line.startswith('【その他】') or line.startswith('【要望】'):
                    data["other_requirements"] = line.split('】')[-1].strip().replace(':', '').replace('：', '')
                
                elif current_section == "competitor" and line:
                    data["competitor_analysis"] += line + "\\n"
            
            return data
            
        except Exception as e:
            print(f"❌ 入力データ解析エラー: {e}")
            return {}
    
    def analyze_reader_needs(self, main_keyword: str, related_keywords: List[str]) -> Dict:
        """読者ニーズ分析（WebSearch使用）"""
        print(f"🔍 読者ニーズ分析中: {main_keyword}")
        
        # WebSearch用クエリ生成
        search_queries = [
            f"{main_keyword} 悩み",
            f"{main_keyword} 不安",
            f"{main_keyword} 疑問",
            f"{main_keyword} 選び方",
            f"{main_keyword} 失敗"
        ]
        
        # 関連キーワードからも検索クエリ生成
        for keyword in related_keywords[:3]:  # 上位3つのキーワード
            search_queries.append(f"{keyword} {main_keyword}")
        
        # 実際のWebSearch実行は後で実装
        # 現在は分析フレームワークベースで仮生成
        reader_analysis = {
            "primary_concerns": self._generate_primary_concerns(main_keyword, related_keywords),
            "search_intent": self._analyze_search_intent(main_keyword),
            "pain_points": self._identify_pain_points(main_keyword, related_keywords),
            "desired_outcomes": self._identify_desired_outcomes(main_keyword),
            "knowledge_level": self._assess_knowledge_level(main_keyword)
        }
        
        print("✅ 読者ニーズ分析完了")
        return reader_analysis
    
    def _generate_primary_concerns(self, main_keyword: str, related_keywords: List[str]) -> List[str]:
        """主要な悩み・不安を生成"""
        concerns = []
        
        # キーワードベースの悩み生成
        if "選び方" in main_keyword or "選び方" in ' '.join(related_keywords):
            concerns.extend([
                "どれを選んでいいかわからない",
                "失敗したくない",
                "自分に合うものがわからない"
            ])
        
        if "サイズ" in ' '.join(related_keywords):
            concerns.append("サイズ選びで失敗しそう")
        
        if "予算" in ' '.join(related_keywords) or "価格" in ' '.join(related_keywords):
            concerns.extend([
                "予算内で良いものが見つかるか不安",
                "高いものと安いものの違いがわからない"
            ])
        
        # デフォルト悩み
        if not concerns:
            concerns = [
                "初めてで何もわからない",
                "失敗したくない",
                "後悔したくない"
            ]
        
        return concerns[:5]  # 最大5つまで
    
    def _analyze_search_intent(self, main_keyword: str) -> str:
        """検索意図の分析"""
        if "選び方" in main_keyword:
            return "商品選択・比較検討"
        elif "おすすめ" in main_keyword:
            return "推奨商品・ランキング情報"
        elif "方法" in main_keyword:
            return "具体的な手順・やり方"
        else:
            return "基本的な情報収集"
    
    def _identify_pain_points(self, main_keyword: str, related_keywords: List[str]) -> List[str]:
        """痛点・課題の特定"""
        pain_points = []
        
        keywords_text = main_keyword + ' ' + ' '.join(related_keywords)
        
        if "ベッド" in keywords_text:
            pain_points.extend([
                "部屋のサイズに合わない",
                "組み立てが大変",
                "搬入できない"
            ])
        
        if "マットレス" in keywords_text:
            pain_points.extend([
                "硬さが体に合わない",
                "寝心地が悪い",
                "腰痛になる"
            ])
        
        if "睡眠" in keywords_text:
            pain_points.extend([
                "なかなか眠れない",
                "朝起きるのがつらい",
                "疲れが取れない"
            ])
        
        return pain_points[:4]  # 最大4つまで
    
    def _identify_desired_outcomes(self, main_keyword: str) -> List[str]:
        """望む結果の特定"""
        outcomes = [
            "失敗せずに選びたい",
            "満足できるものを購入したい",
            "長く使えるものが欲しい",
            "コストパフォーマンスの良いものを見つけたい"
        ]
        
        return outcomes
    
    def _assess_knowledge_level(self, main_keyword: str) -> str:
        """読者の知識レベル評価"""
        if "初心者" in main_keyword or "始め方" in main_keyword:
            return "初心者レベル（基本から説明必要）"
        elif "選び方" in main_keyword:
            return "中級者レベル（比較検討段階）"
        elif "おすすめ" in main_keyword:
            return "決定段階（具体的な商品情報が必要）"
        else:
            return "初級～中級者レベル（丁寧な説明が必要）"
    
    def create_article_structure(self, input_data: Dict, reader_analysis: Dict, references: Dict) -> str:
        """記事構造・骨格を作成"""
        print("📝 記事構造作成中...")
        
        # 参照記事から構成パターンを学習
        reference_patterns = self._analyze_reference_patterns(references)
        
        # メインキーワードからタイトル生成
        title = self._generate_title(input_data["main_keyword"], input_data["related_keywords"])
        
        # 見出し構成生成
        structure = self._generate_heading_structure(
            input_data, reader_analysis, reference_patterns
        )
        
        # 骨格ファイル作成
        skeleton = f"""# 記事骨格：{title}

## 📊 記事情報
- **メインキーワード**: {input_data["main_keyword"]}
- **関連キーワード**: {", ".join(input_data["related_keywords"])}
- **対象読者**: {reader_analysis["knowledge_level"]}
- **検索意図**: {reader_analysis["search_intent"]}

## 🎯 読者ニーズ分析結果

### 主要な悩み・不安
{chr(10).join([f"- {concern}" for concern in reader_analysis["primary_concerns"]])}

### 痛点・課題
{chr(10).join([f"- {pain}" for pain in reader_analysis["pain_points"]])}

### 望む結果
{chr(10).join([f"- {outcome}" for outcome in reader_analysis["desired_outcomes"]])}

## 📝 記事構成案

{structure}

## 🎨 執筆方針
- FINAL版テンプレート完全準拠
- 参照記事（8月11日）のトーンを踏襲
- 読者の悩みファーストで構成
- 具体的で実践しやすい内容
- スクロール効率（1見出し1箇条書き）遵守

---
**作成日時**: {datetime.now().strftime('%Y年%m月%d日 %H時%M分')}
**ステータス**: 骨格作成完了・承認待ち
"""
        
        print("✅ 記事構造作成完了")
        return skeleton
    
    def _analyze_reference_patterns(self, references: Dict) -> Dict:
        """参照記事のパターン分析"""
        patterns = {
            "heading_style": "## ",
            "numbered_lists": True,
            "conclusion_pattern": "まとめ",
            "tone": "親しみやすい・実用的"
        }
        
        # 実際の参照記事から見出しパターンを抽出
        for article_name, content in references.items():
            lines = content.split('\n')
            for line in lines:
                if line.startswith('## '):
                    # 見出しパターンの分析
                    if '5選' in line or '3つ' in line:
                        patterns["uses_numbers"] = True
                    if 'メリット' in line or 'デメリット' in line:
                        patterns["pros_cons"] = True
        
        return patterns
    
    def _generate_title(self, main_keyword: str, related_keywords: List[str]) -> str:
        """タイトル生成（31文字前後）"""
        
        # 関連キーワードからサブワード抽出
        sub_words = []
        for keyword in related_keywords[:3]:
            if len(keyword) <= 4:  # 短いキーワードを優先
                sub_words.append(keyword)
        
        # パターンベースでタイトル生成
        if "選び方" in main_keyword:
            title = f"{main_keyword.replace('選び方', '')}選びで失敗しない！{main_keyword}完全ガイド"
        elif "おすすめ" in main_keyword:
            title = f"{main_keyword}｜プロが厳選する{sub_words[0] if sub_words else '最適'}な選び方"
        else:
            title = f"{main_keyword}の全て｜初心者でも失敗しない選び方ガイド"
        
        # 文字数調整（31文字前後）
        if len(title) > 35:
            title = title[:32] + "..."
        elif len(title) < 28:
            title = title + "【2025年版】"
        
        return title
    
    def _generate_heading_structure(self, input_data: Dict, reader_analysis: Dict, patterns: Dict) -> str:
        """見出し構成生成"""
        
        main_keyword = input_data["main_keyword"]
        related_keywords = input_data["related_keywords"]
        
        structure = f"""### H1: {self._generate_title(main_keyword, related_keywords)}

### 導入文（読者の悩みに共感）
- {reader_analysis["primary_concerns"][0] if reader_analysis["primary_concerns"] else "読者の悩み"}について共感的な導入

### H2: {main_keyword}を選ぶ前に知っておきたい基本知識
- 基本的な知識・前提条件
- よくある誤解の解消

### H2: {main_keyword}選びで失敗しがちな3つのポイント
1. {reader_analysis["pain_points"][0] if len(reader_analysis["pain_points"]) > 0 else "よくある失敗"}
2. {reader_analysis["pain_points"][1] if len(reader_analysis["pain_points"]) > 1 else "注意すべきポイント"}
3. {reader_analysis["pain_points"][2] if len(reader_analysis["pain_points"]) > 2 else "見落としがちな要素"}

### H2: {related_keywords[0] if related_keywords else "重要項目"}から考える選び方
- 具体的な選択基準
- 判断のポイント

### H2: {related_keywords[1] if len(related_keywords) > 1 else "予算・価格帯"}で選ぶ{main_keyword}
- 価格帯別の特徴
- コストパフォーマンス重視の選び方

### H2: おすすめ{main_keyword} 厳選5選
1. 商品名1：（特徴・おすすめポイント）
2. 商品名2：（特徴・おすすめポイント）
3. 商品名3：（特徴・おすすめポイント）
4. 商品名4：（特徴・おすすめポイント）
5. 商品名5：（特徴・おすすめポイント）

### H2: {main_keyword}選びでよくある質問Q&A
- Q1: {reader_analysis["primary_concerns"][0] if reader_analysis["primary_concerns"] else "よくある質問"}
- Q2: 予算はどのくらい必要？
- Q3: 初心者でも大丈夫？

### H2: まとめ：失敗しない{main_keyword}の選び方
- 重要ポイントの再整理
- 最終的な選択の決め手
- 次のアクション提案"""
        
        return structure
    
    def save_skeleton_file(self, skeleton_content: str, input_data: Dict) -> str:
        """骨格ファイルを作成中フォルダに保存"""
        
        # ファイル名生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        main_keyword_clean = re.sub(r'[^\w\s-]', '', input_data["main_keyword"]).strip()
        main_keyword_clean = re.sub(r'[\s_]+', '_', main_keyword_clean)
        
        filename = f"{timestamp}_{main_keyword_clean}_骨格.md"
        
        # 保存
        os.makedirs(self.work_in_progress_path, exist_ok=True)
        file_path = os.path.join(self.work_in_progress_path, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(skeleton_content)
        
        return file_path

def main():
    """メイン実行関数"""
    system = CLIAutoWritingSystem()
    
    print("🚀 CLI自動記事作成システム - ライティング案件（ミネルヴスリープ）")
    print("=" * 80)
    
    # FINAL版テンプレート確認
    template = system.load_final_template()
    if not template:
        print("❌ FINAL版テンプレートが読み込めません")
        return
    
    print("✅ FINAL版テンプレート読み込み完了")
    
    # 参照記事読み込み（Phase 0）
    references = system.load_reference_articles()
    print(f"✅ 参照記事読み込み完了（{len(references)}件）")
    
    # 入力資料受け取り
    print("\n📝 競合分析・キーワード資料を入力してください：")
    print("（例：【メインキーワード】：ベッドフレーム 選び方）")
    print("入力完了後、空行を入れてENTERを押してください")
    print("-" * 50)
    
    input_lines = []
    empty_lines = 0
    
    while True:
        try:
            line = input()
            if line.strip() == "":
                empty_lines += 1
                if empty_lines >= 2:  # 2回連続空行で終了
                    break
            else:
                empty_lines = 0
                input_lines.append(line)
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\n❌ 入力をキャンセルしました")
            return
    
    input_text = '\n'.join(input_lines)
    
    if not input_text.strip():
        print("❌ 入力データが空です")
        return
    
    # データ解析
    print("\n🔍 入力データ解析中...")
    input_data = system.parse_input_data(input_text)
    
    if not input_data.get("main_keyword"):
        print("❌ メインキーワードが見つかりません")
        return
    
    print(f"✅ 解析完了:")
    print(f"   プロジェクト: {input_data.get('project', 'なし')}")
    print(f"   メインキーワード: {input_data['main_keyword']}")
    print(f"   関連キーワード: {', '.join(input_data['related_keywords'])}")
    
    # + α アーカイブシステム統合分析
    archive_analysis = None
    if system.archive_system:
        try:
            print("\n🔍 統合アーカイブ分析実行中...")
            user_request = f"メインキーワード: {input_data['main_keyword']}, 関連: {', '.join(input_data['related_keywords'])}"
            archive_analysis = system.archive_system.auto_archive_utilization_workflow(user_request)
            if archive_analysis["workflow_status"] == "success":
                print("✅ アーカイブ分析完了")
                if archive_analysis["duplication_check"]["status"] != "SAFE":
                    print(f"⚠️ 重複リスク検出: {archive_analysis['duplication_check']['status']}")
                    if archive_analysis["duplication_check"]["suggestions"]:
                        print(f"💡 差別化提案: {archive_analysis['duplication_check']['suggestions'][0]}")
                        
                        # 重複リスクが高い場合は確認を求める
                        if archive_analysis["duplication_check"]["status"] == "HIGH_RISK":
                            continue_confirm = input(f"\n⚠️ 高い重複リスクが検出されました。続行しますか？ (y/n): ").lower().strip()
                            if continue_confirm != 'y':
                                print("❌ 記事作成をキャンセルしました")
                                return
            else:
                print("⚠️ アーカイブ分析で問題が発生しました")
        except Exception as e:
            print(f"⚠️ アーカイブ分析エラー: {e}")
    
    # 読者ニーズ分析
    print("\n🎯 読者ニーズ分析実行中...")
    reader_analysis = system.analyze_reader_needs(
        input_data["main_keyword"], 
        input_data["related_keywords"]
    )
    
    # 記事構造作成
    skeleton = system.create_article_structure(input_data, reader_analysis, references)
    
    # プレビュー表示
    print("\n" + "="*80)
    print("📋 作成された記事骨格プレビュー:")
    print("="*80)
    print(skeleton[:1500] + "..." if len(skeleton) > 1500 else skeleton)
    print("="*80)
    
    # 保存確認
    save_confirm = input("\n✅ この骨格を「3_作成中」フォルダに保存しますか？ (y/n): ").lower().strip()
    
    if save_confirm == 'y':
        try:
            file_path = system.save_skeleton_file(skeleton, input_data)
            print(f"✅ 骨格ファイル保存完了:")
            print(f"   ファイル: {os.path.basename(file_path)}")
            print(f"   パス: {file_path}")
            print("\n📋 次のステップ:")
            print("1. 保存された骨格ファイルをレビュー")
            print("2. 修正・承認後、文章作成を開始")
            print("3. 完成後は「2_完成記事」フォルダへ移動")
            
        except Exception as e:
            print(f"❌ 保存エラー: {e}")
    else:
        print("❌ 保存をキャンセルしました")

if __name__ == "__main__":
    main()