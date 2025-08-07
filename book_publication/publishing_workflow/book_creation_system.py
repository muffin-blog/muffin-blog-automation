"""
書籍・有料ノート自動生成システム
日々の知識蓄積から書籍化までの完全自動化ワークフロー
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import markdown
from pathlib import Path

class BookPublishingSystem:
    """書籍出版ワークフロー管理システム"""
    
    def __init__(self, base_path: str = None):
        self.base_path = base_path or "/Users/satoumasamitsu/osigoto/ブログ自動化/book_publication"
        self.knowledge_base_path = os.path.join(self.base_path, "knowledge_base")
        self.manuscript_path = os.path.join(self.base_path, "manuscript_drafts")
        
        # ディレクトリ作成
        os.makedirs(self.manuscript_path, exist_ok=True)
        
    def collect_daily_reports(self) -> List[Dict]:
        """日報ファイルを収集・解析"""
        reports_path = os.path.join(self.knowledge_base_path, "daily_reports")
        reports = []
        
        if not os.path.exists(reports_path):
            return reports
            
        for filename in os.listdir(reports_path):
            if filename.endswith('.md'):
                file_path = os.path.join(reports_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                reports.append({
                    'date': self.extract_date_from_filename(filename),
                    'filename': filename,
                    'content': content,
                    'sections': self.parse_report_sections(content)
                })
        
        return sorted(reports, key=lambda x: x['date'])
    
    def extract_date_from_filename(self, filename: str) -> str:
        """ファイル名から日付抽出"""
        # 例: 2025-08-07_session_complete.md -> 2025-08-07
        return filename.split('_')[0]
    
    def parse_report_sections(self, content: str) -> Dict:
        """日報内容をセクション別に解析"""
        sections = {}
        current_section = None
        current_content = []
        
        lines = content.split('\n')
        for line in lines:
            if line.startswith('## '):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line[3:].strip()
                current_content = []
            else:
                current_content.append(line)
        
        if current_section:
            sections[current_section] = '\n'.join(current_content)
            
        return sections
    
    def generate_chapter_outline(self, reports: List[Dict]) -> Dict:
        """日報から章立て自動生成"""
        
        chapter_outline = {
            "title": "AI協働ブログ自動化の実践 - Claude Code と共に構築する完全自動化システム",
            "subtitle": "NotebookLMからWordPressまで、5分で記事投稿する技術",
            "chapters": [
                {
                    "number": 1,
                    "title": "AI協働の新時代 - なぜClaude Codeなのか",
                    "sections": [
                        "従来のブログ運営の課題",
                        "Claude Codeとの出会い",
                        "AI協働による可能性の発見"
                    ],
                    "key_insights": self.extract_insights_by_theme(reports, "ai_collaboration")
                },
                {
                    "number": 2, 
                    "title": "段階的システム構築の実践",
                    "sections": [
                        "小さく始める重要性",
                        "WordPress API統合の第一歩",
                        "テスト・検証・改善のサイクル"
                    ],
                    "key_insights": self.extract_insights_by_theme(reports, "system_building")
                },
                {
                    "number": 3,
                    "title": "WordPress統合とSEO最適化",
                    "sections": [
                        "REST API の効果的活用",
                        "28-32文字タイトル最適化の実装",
                        "メタデータ自動生成システム"
                    ],
                    "key_insights": self.extract_insights_by_theme(reports, "wordpress_seo")
                },
                {
                    "number": 4,
                    "title": "画像システムの自動化",
                    "sections": [
                        "Unsplash API統合の実践",
                        "SEO最適化alt属性の自動生成",
                        "スコアリングシステムによる品質確保"
                    ],
                    "key_insights": self.extract_insights_by_theme(reports, "image_system")
                },
                {
                    "number": 5,
                    "title": "品質保証システムの構築", 
                    "sections": [
                        "AI表現検出・修正の実装",
                        "マフィンブログフォーマット準拠チェック",
                        "スコアリングによる品質担保"
                    ],
                    "key_insights": self.extract_insights_by_theme(reports, "quality_assurance")
                },
                {
                    "number": 6,
                    "title": "完全自動化への道",
                    "sections": [
                        "5フェーズワークフローの設計",
                        "NotebookLM要約からの自動実行",
                        "ユーザー体験の最適化"
                    ],
                    "key_insights": self.extract_insights_by_theme(reports, "automation")
                },
                {
                    "number": 7,
                    "title": "システム保存と継続可能性",
                    "sections": [
                        "GitHubによるバージョン管理",
                        "セキュリティ考慮事項",
                        "拡張性・汎用性の確保"
                    ],
                    "key_insights": self.extract_insights_by_theme(reports, "system_management")
                },
                {
                    "number": 8,
                    "title": "未来展望とビジネス応用",
                    "sections": [
                        "ROI分析と効果測定",
                        "他業界への応用可能性", 
                        "次世代AI協働システムの展望"
                    ],
                    "key_insights": self.extract_insights_by_theme(reports, "future_prospects")
                }
            ],
            "appendix": [
                "完全なソースコード",
                "API設定・環境構築手順",
                "トラブルシューティングガイド",
                "参考資料・リンク集"
            ]
        }
        
        return chapter_outline
    
    def extract_insights_by_theme(self, reports: List[Dict], theme: str) -> List[str]:
        """テーマ別の洞察抽出"""
        insights = []
        
        theme_keywords = {
            "ai_collaboration": ["AI協働", "Claude Code", "協働パターン", "AI活用"],
            "system_building": ["段階的", "システム構築", "テスト", "検証"],
            "wordpress_seo": ["WordPress", "SEO", "タイトル", "メタデータ"],
            "image_system": ["Unsplash", "画像", "alt属性", "アイキャッチ"],
            "quality_assurance": ["品質保証", "AI表現", "スコア", "チェック"],
            "automation": ["自動化", "ワークフロー", "NotebookLM", "フェーズ"],
            "system_management": ["GitHub", "保存", "セキュリティ", "管理"],
            "future_prospects": ["未来", "展望", "ビジネス", "ROI", "効果"]
        }
        
        keywords = theme_keywords.get(theme, [])
        
        for report in reports:
            if 'sections' in report:
                for section_name, section_content in report['sections'].items():
                    if any(keyword in section_content for keyword in keywords):
                        # キーワードに関連する重要な洞察を抽出
                        lines = section_content.split('\n')
                        for line in lines:
                            if ('###' in line or '**' in line) and any(keyword in line for keyword in keywords):
                                insights.append(line.strip())
        
        return insights[:5]  # 上位5つの洞察
    
    def generate_manuscript_draft(self, outline: Dict) -> str:
        """章立てから原稿ドラフト生成"""
        
        manuscript = f"""# {outline['title']}

## {outline['subtitle']}

---

## 📖 目次

"""
        
        # 目次生成
        for chapter in outline['chapters']:
            manuscript += f"{chapter['number']}. **{chapter['title']}**\n"
            for section in chapter['sections']:
                manuscript += f"   - {section}\n"
            manuscript += "\n"
        
        manuscript += "\n---\n\n"
        
        # 各章の詳細
        for chapter in outline['chapters']:
            manuscript += f"""## 第{chapter['number']}章: {chapter['title']}

### 概要
この章では、{chapter['sections'][0]}について詳しく解説します。

"""
            
            # セクション詳細
            for i, section in enumerate(chapter['sections'], 1):
                manuscript += f"""### {chapter['number']}.{i} {section}

（この部分は日報からの具体的な体験・技術的詳細で充実させる）

"""
            
            # 重要な洞察
            if chapter['key_insights']:
                manuscript += "### 💡 重要な洞察\n\n"
                for insight in chapter['key_insights']:
                    manuscript += f"- {insight}\n"
                manuscript += "\n"
            
            manuscript += "---\n\n"
        
        # 付録
        manuscript += "## 📚 付録\n\n"
        for item in outline['appendix']:
            manuscript += f"### {item}\n（詳細内容を記載）\n\n"
        
        return manuscript
    
    def create_publishing_package(self) -> Dict:
        """出版パッケージ作成"""
        
        print("📚 書籍化プロセス開始...")
        
        # 1. 日報収集
        reports = self.collect_daily_reports()
        print(f"📋 日報収集完了: {len(reports)}件")
        
        # 2. 章立て生成
        outline = self.generate_chapter_outline(reports)
        print("📝 章立て生成完了")
        
        # 3. 原稿ドラフト生成
        manuscript = self.generate_manuscript_draft(outline)
        print("✍️ 原稿ドラフト生成完了")
        
        # 4. ファイル保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 章立てJSON保存
        outline_path = os.path.join(self.manuscript_path, f"outline_{timestamp}.json")
        with open(outline_path, 'w', encoding='utf-8') as f:
            json.dump(outline, f, ensure_ascii=False, indent=2)
        
        # 原稿Markdown保存
        manuscript_path = os.path.join(self.manuscript_path, f"manuscript_draft_{timestamp}.md")
        with open(manuscript_path, 'w', encoding='utf-8') as f:
            f.write(manuscript)
        
        # HTMLバージョン生成
        html_content = markdown.markdown(manuscript, extensions=['toc', 'tables', 'fenced_code'])
        html_path = os.path.join(self.manuscript_path, f"manuscript_draft_{timestamp}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{outline['title']}</title>
    <style>
        body {{ font-family: 'Hiragino Kaku Gothic Pro', sans-serif; line-height: 1.6; margin: 40px; }}
        h1, h2, h3 {{ color: #333; }}
        code {{ background: #f4f4f4; padding: 2px 4px; }}
        pre {{ background: #f4f4f4; padding: 15px; overflow-x: auto; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
            """)
        
        print(f"💾 ファイル保存完了:")
        print(f"   章立て: {outline_path}")
        print(f"   原稿: {manuscript_path}")
        print(f"   HTML: {html_path}")
        
        return {
            "success": True,
            "reports_count": len(reports),
            "outline_path": outline_path,
            "manuscript_path": manuscript_path,
            "html_path": html_path,
            "word_count": len(manuscript.split()),
            "chapter_count": len(outline['chapters'])
        }

def auto_generate_daily_report_template() -> str:
    """日報テンプレート自動生成"""
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    template = f"""# 📅 日報 - {today}

## 🎯 セッション概要
**テーマ**: 

**作業時間**: 

**達成状況**: 

---

## 🛠 実装・改善した機能

### 1. **[機能名]**
- **ファイル**: 
- **機能**: 
- **特徴**: 

---

## 💡 技術的発見

### [発見のカテゴリ]

1. **[具体的な発見]**
   - 詳細説明

---

## 🐛 課題と解決

### 課題1: [課題名]
**問題**: 
**解決**: 
**学習**: 

---

## 🔄 ワークフロー改善

### 改善1: [改善内容]
**Before**: 
**After**: 
**効果**: 

---

## 📈 成果・インパクト

### 定量的成果
- **[指標名]**: [数値]

### 定性的成果
- **[成果名]**: [説明]

---

## 📚 書籍化に向けた今日の洞察

### 章立てのヒント
1. **第X章**: [タイトル] - [概要]

### 読者への価値提案
- **[価値1]**: [説明]

---

## 🎯 次回セッション予定

### 優先事項
1. **[項目1]**

### 継続課題
- [課題1]

---

## 📝 メモ・アイデア

### [カテゴリ]
- [アイデア1]

---

**記録者**: Claude Code  
**確認者**: ユーザー  
**次回更新予定**: 次回作業セッション後
"""
    
    return template

# 使用例
if __name__ == "__main__":
    # 書籍化システムテスト
    book_system = BookPublishingSystem()
    result = book_system.create_publishing_package()
    
    print(f"\n🎉 書籍化パッケージ生成完了!")
    print(f"章数: {result['chapter_count']}")
    print(f"単語数: {result['word_count']:,}")
    print(f"日報数: {result['reports_count']}")