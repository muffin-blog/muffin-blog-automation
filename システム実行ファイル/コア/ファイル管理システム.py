#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
マフィンブログ記事作成における自動ファイル管理システム
- 失敗作・不完全版の自動削除
- バージョン管理
- 品質チェック後のファイル整理
"""

import os
import shutil
import datetime
from pathlib import Path

class FileManagementSystem:
    def __init__(self):
        self.base_path = "/Users/satoumasamitsu/osigoto/ブログ自動化/"
        self.completed_articles_path = f"{self.base_path}マフィンブログ完成記事/"
        self.draft_path = f"{self.base_path}下書き/"
        self.failed_path = f"{self.base_path}失敗作_アーカイブ/"
        
    def clean_failed_articles(self, keyword: str = None):
        """
        失敗した記事ファイルを削除
        
        Args:
            keyword (str): 削除対象のキーワード（例：読書苦手）
        """
        try:
            # 完成記事フォルダから失敗作を検索
            for file_path in Path(self.completed_articles_path).glob("**/*.md"):
                if keyword and keyword in str(file_path):
                    # 失敗作をアーカイブ移動（削除前にバックアップ）
                    if not os.path.exists(self.failed_path):
                        os.makedirs(self.failed_path)
                    
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    archive_name = f"FAILED_{timestamp}_{file_path.name}"
                    shutil.move(str(file_path), f"{self.failed_path}{archive_name}")
                    
            print(f"✅ ファイル整理完了：{keyword}関連の失敗作をアーカイブ移動")
            
        except Exception as e:
            print(f"❌ ファイル整理エラー: {e}")
    
    def validate_article_quality(self, file_path: str) -> dict:
        """
        記事の品質チェック（読者視点ファースト）
        
        Returns:
            dict: 品質チェック結果
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 読者視点チェック項目
            quality_checks = {
                "専門用語過多": self._check_technical_terms(content),
                "情報羅列": self._check_information_dump(content),
                "解決策後回し": self._check_solution_placement(content),
                "マフィンフォーマット": self._check_muffin_format(content),
                "読者共感": self._check_reader_empathy(content)
            }
            
            return quality_checks
            
        except Exception as e:
            return {"error": str(e)}
    
    def _check_technical_terms(self, content: str) -> bool:
        """専門用語の過度使用チェック"""
        technical_terms = [
            "ワーキングメモリ", "海馬", "聴覚学習", "認知負荷", 
            "マルチタスク環境", "神経科学", "脳血流", "併存率"
        ]
        
        term_count = sum(content.count(term) for term in technical_terms)
        return term_count > 5  # 5回以上で警告
    
    def _check_information_dump(self, content: str) -> bool:
        """情報羅列の検出"""
        # 箇条書きや表が多すぎる場合
        bullet_count = content.count("- **") + content.count("* **")
        table_count = content.count("|---|")
        
        return bullet_count > 20 or table_count > 3
    
    def _check_solution_placement(self, content: str) -> bool:
        """解決策の配置チェック"""
        lines = content.split('\n')[:50]  # 最初の50行をチェック
        early_content = '\n'.join(lines)
        
        solution_keywords = ["Audible", "解決", "方法", "始め方"]
        return not any(keyword in early_content for keyword in solution_keywords)
    
    def _check_muffin_format(self, content: str) -> bool:
        """マフィンフォーマットチェック"""
        return "「マフィンさん、" in content and "「" in content and "」" in content
    
    def _check_reader_empathy(self, content: str) -> bool:
        """読者共感チェック"""
        empathy_phrases = [
            "分かる", "気持ち", "悩み", "困って", "大丈夫", 
            "安心", "でも", "実は", "そんな"
        ]
        
        empathy_count = sum(content.count(phrase) for phrase in empathy_phrases)
        return empathy_count < 3  # 3回未満で警告

# システム実行例
if __name__ == "__main__":
    fm = FileManagementSystem()
    
    # 読書苦手関連の失敗作をクリーンアップ
    fm.clean_failed_articles("読書苦手")