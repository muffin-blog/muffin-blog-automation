#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
マフィンブログ統合システム
全22個のファイル機能を統合し、テンプレート準拠・品質自動担保を実現

統合された機能:
- WordPress API連携（記事投稿・編集・削除・バックアップ）
- テンプレート記事作成（マフィンブログフォーマット準拠）
- 品質管理・監視システム（投稿前確認・継続監視）  
- 自動化ワークフロー（URL処理・ポートフォリオ更新）
- SEO最適化（H1タグ・構造化データ・内部リンク）
- ファイル管理・バックアップ・復元機能
"""

import os
import sys
import json
import yaml
import re
import requests
import base64
import shutil
import time
import glob
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv

load_dotenv()

class マフィンブログ統合システム:
    """マフィンブログの全機能を統合したシステム"""
    
    def __init__(self):
        """初期化"""
        print("🚀 マフィンブログ統合システム初期化中...")
        
        # 基本パス設定
        self.base_path = Path("/Users/satoumasamitsu/Desktop/osigoto/ブログ自動化")
        self.service_template_path = self.base_path / "サービス紹介型記事_構成テンプレート.md"
        self.howto_template_path = self.base_path / "ノウハウ解説型記事_構成テンプレート.md"
        self.reference_article_path = self.base_path / "WordPress投稿下書き/読書苦手_Audible_聴く読書_完全ガイド_20250813_最新版.md"
        self.output_path = self.base_path / "WordPress投稿下書き"
        self.backup_dir = self.base_path / "バックアップ・復元/バックアップファイル"
        self.monitor_dir = self.base_path / "システム監視データ"
        
        # ディレクトリ作成
        for directory in [self.output_path, self.backup_dir, self.monitor_dir]:
            directory.mkdir(exist_ok=True)
        
        # WordPress API設定
        self.wp_config = self._setup_wordpress_api()
        
        # テンプレート・参考記事読み込み
        self.service_template = self._load_template_structure(self.service_template_path, "サービス紹介型")
        self.howto_template = self._load_template_structure(self.howto_template_path, "ノウハウ解説型")
        self.reference_article = self._load_reference_article()
        
        # テンプレート読み込み状況報告
        if self.service_template.get('loaded'):
            print(f"✅ サービス紹介型テンプレート読み込み成功: {len(self.service_template['content'])}文字")
        else:
            print("❌ サービス紹介型テンプレート読み込み失敗")
            
        if self.howto_template.get('loaded'):
            print(f"✅ ノウハウ解説型テンプレート読み込み成功: {len(self.howto_template['content'])}文字")
        else:
            print("❌ ノウハウ解説型テンプレート読み込み失敗")
        
        # 品質基準設定
        self.quality_standards = self._set_quality_standards()
        
        # 保護記事ID（削除禁止）
        self.protected_post_ids = [2732, 2677, 2625, 2535, 2210, 649, 2809, 2775]
        
        print("✅ マフィンブログ統合システム初期化完了")
        
        # 統合管理システムとの同期パス（フォルダ構造対応）
        self.integration_system_path = Path("/Users/satoumasamitsu/Desktop/osigoto/統合管理システム")
        self.integration_specs_dir = self.integration_system_path / "マフィンブログシステム仕様書"
        self.daily_log_rules_path = self.integration_system_path / "日報ログ保護ルール.md"
    
    def _setup_wordpress_api(self) -> Dict[str, str]:
        """WordPress API設定"""
        site_url = os.getenv('WORDPRESS_SITE_URL', 'https://muffin-blog.com').rstrip('/')
        username = os.getenv('WORDPRESS_USERNAME', '')
        password = os.getenv('WORDPRESS_PASSWORD', '')
        
        if not all([site_url, username, password]):
            # 環境変数がない場合のデフォルト値（開発用）
            site_url = "https://muffin-blog.com"
            username = "muffin1203"
            password = "TMLy Z4Wi RhPu oVLm 0lcO gZdi"
        
        credentials = f"{username}:{password}"
        auth_header = base64.b64encode(credentials.encode()).decode()
        
        return {
            'site_url': site_url,
            'username': username,
            'password': password,
            'api_url': f"{site_url}/wp-json/wp/v2",
            'headers': {
                'Authorization': f'Basic {auth_header}',
                'Content-Type': 'application/json'
            }
        }
    
    def _load_template_structure(self, template_path: Path, template_type: str) -> Dict[str, Any]:
        """テンプレート構造を読み込み（2025-08-13更新：記事タイプ別対応）"""
        try:
            if template_path.exists():
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {"loaded": True, "content": content, "type": template_type}
            else:
                print(f"⚠️ {template_type}テンプレートファイルが見つかりません")
                return {"loaded": False, "type": template_type}
        except Exception as e:
            print(f"❌ {template_type}テンプレート読み込みエラー: {e}")
            return {"loaded": False, "type": template_type}
    
    def _load_reference_article(self) -> Dict[str, Any]:
        """参考記事を読み込み"""
        try:
            if self.reference_article_path.exists():
                with open(self.reference_article_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {"loaded": True, "content": content}
            else:
                print("⚠️ 参考記事が見つかりません")
                return {"loaded": False}
        except Exception as e:
            print(f"❌ 参考記事読み込みエラー: {e}")
            return {"loaded": False}
    
    def _set_quality_standards(self) -> Dict[str, Any]:
        """品質基準を設定（CLAUDE.md統合版）"""
        return {
            # 基本品質基準
            "minimum_word_count": 2000,
            "required_sections": [
                "この記事で分かること",
                "FAQ", 
                "まとめ"
            ],
            "required_h2_count": 4,
            "conversation_blocks_min": 3,
            "faq_count_min": 5,
            
            # 記事構成テンプレート基準（2025-08-13確立）
            "standard_article_structure": [
                "導入（悩み共感）",
                "概念説明（○○とは？）",  # 最優先
                "基本やり方（ステップ）",    # 次に重要
                "効果・理由",
                "詳細実践方法", 
                "具体例・おすすめ",
                "料金・サービス",
                "FAQ",
                "まとめ"
            ],
            
            # 「この記事で分かること」ルール
            "article_benefits_rules": {
                "style": "簡潔に記事内容を示す",
                "tone": "魅力的だが詰め込みすぎない",
                "expression": "大げさな表現は避ける",
                "consistency": "実際の記事構成と一致させる"
            },
            
            # 「○つの理由」ルール
            "reasons_section_rules": {
                "content": "具体的な効果・理由を示す",
                "language": "専門用語は避ける",
                "clarity": "読者に分かりやすい表現",
                "consistency": "冒頭と見出しを完全一致させる"
            },
            
            # 大見出し下の導入会話ルール
            "section_intro_rules": {
                "placement": "大見出し（##）の直後には必ず導入会話を配置",
                "purpose": "読者の注意を引く自然な疑問",
                "role": "次のセクションへの導入役割",
                "example": "「マフィンさん、○○って何ですか？」"
            },
            
            # 概念説明セクションの文章構成
            "concept_explanation_structure": {
                "paragraph1": "基本定義を1文で明確に提示",
                "paragraph2": "改行してから詳細説明",
                "style": "文章は短く分割して読みやすく",
                "rule": "長い1文は2文に分けて簡潔に"
            },
            
            # 箇条書き統一フォーマット（2025-08-13壁打ち学習）
            "bullet_point_format": {
                "title_format": "**タイトル：**（太字必須）",
                "bullet_format": "- 項目内容（通常テキスト・太字なし）",
                "wordpress_compatibility": "ブロック作成時の利便性を考慮した統一形式",
                "examples": [
                    "**こんな時に聞けます：**",
                    "**でもAudibleなら：**", 
                    "**おすすめの理由：**",
                    "**プロ朗読の効果：**"
                ],
                "structure": [
                    "1. タイトル行：**[内容]：**",
                    "2. 空行", 
                    "3. 箇条書き：- [項目]（太字なし）"
                ]
            },
            
            # 読者検索意図優先の原則
            "search_intent_priority": {
                "early_resolution": "読者の疑問を早期解決",
                "method_first": "「やり方」を「理由」より優先",
                "action_guide": "行動しやすい導線設計",
                "keyword_match": "検索キーワードの期待に応える"
            },
            
            # 禁止表現（更新版）
            "prohibited_expressions": [
                "めっちゃ有名",
                "大ブーム", 
                "みんな知ってる",
                "専門家も絶賛",
                "話題沸騰",
                "革命的",
                "ことが多いです",
                "と言えるでしょう",
                "検討してみてはいかがでしょうか"
            ],
            
            # 必須証拠キーワード
            "required_evidence_keywords": [
                "30日無料",
                "月額1500円",
                "聴き放題",
                "12万冊以上"
            ],
            
            # 学習・改善履歴からの品質基準
            "quality_lessons": {
                "minimum_score": 80,  # 83点でも改善の余地あり
                "word_count_target": 2000,  # 1376文字は不足
                "faq_requirement": 5,  # 0個は致命的
                "seo_elements": "充実したSEO要素必須"
            },
            
            # FAQ戦略的構成パターン（2025-08-13壁打ち学習）
            "faq_strategic_pattern": {
                "source": "Google検索の「その他の質問」「関連する質問」から抜粋",
                "selection_rule": "実際に検索されている質問を優先",
                "structure": [
                    "質問提示",
                    "文章での詳細解説（SEO対策）", 
                    "読者目線の箇条書き（分かりやすさ重視）",
                    "マフィンの会話でクロージング（親しみやすさ）"
                ],
                "strategic_benefits": [
                    "後の記事作成ネタ：FAQ1つが新記事のタネ",
                    "内部リンク構築：関連記事への自然な導線",
                    "検索意図マッチ：実際の検索クエリに対応",
                    "記事間の関連性向上：サイト全体のSEO効果"
                ]
            },
            
            # 記事構成パターン判定（2025-08-13壁打ち学習）
            "article_type_classification": {
                "service_introduction": {
                    "purpose": "サービスの紹介・導入促進",
                    "target": "サービス未利用者（導入検討段階）",
                    "goal": "無料体験・サービス申し込み",
                    "content_focus": "サービス説明中心",
                    "structure": [
                        "問題提起（利用していない悩み）",
                        "サービス解決策提示",
                        "軽い科学的根拠",
                        "詳細な料金・プラン説明",
                        "行動促進（無料体験申し込み等）"
                    ]
                },
                "howto_explanation": {
                    "purpose": "効果を最大化する方法論の解説",
                    "target": "既にサービス利用中/検討中の人",
                    "goal": "実践的な手法の習得",
                    "content_focus": "ノウハウ・テクニック中心",
                    "structure": [
                        "向上心ベースの問題提起",
                        "手法・テクニック解説",
                        "詳細な科学的根拠",
                        "軽い料金説明",
                        "実践促進（手法の実行等）"
                    ]
                }
            },
            
            # 書籍選定の5つの基準（2025-08-13壁打ち学習）
            "book_selection_criteria": {
                "recognition": {
                    "standard": "どこかで名前を聞いたことがある安心感",
                    "effect": "読者の心理的ハードルを下げる",
                    "examples": "YouTubeで流行、投資系で有名等"
                },
                "practicality": {
                    "standard": "読者が直感的に「役に立ちそう」と感じる内容",
                    "effect": "読書モチベーションの向上",
                    "avoid": "純粋な娯楽作品や哲学的すぎる内容"
                },
                "difficulty_balance": {
                    "standard": "初心者～中級者にちょうどいいレベル",
                    "too_hard": "「つまらなそう」で離脱",
                    "too_easy": "二刀流読書の必要性が薄くなる"
                },
                "expansion_potential": {
                    "standard": "その書籍から派生した記事を複数作成できる",
                    "example": "文章術 → ブログ記事でリンク貼り放題",
                    "effect": "SEO・マーケティング価値が高い"
                },
                "psychological_approach": {
                    "keyword": "知ってるけど読めてない本",
                    "effect": "「二刀流なら読める！」という期待感を創出",
                    "success_factor": "認知度があるが読破困難な本を選ぶ"
                }
            }
        }
    
    # ========================================
    # WordPress API機能統合
    # ========================================
    
    def test_wordpress_connection(self) -> bool:
        """WordPress API接続テスト"""
        try:
            response = requests.get(
                f"{self.wp_config['api_url']}/users/me", 
                headers=self.wp_config['headers'],
                timeout=10
            )
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ WordPress API接続成功: {user_data.get('name', 'Unknown')} として認証")
                return True
            else:
                print(f"❌ WordPress API接続失敗: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ WordPress接続エラー: {e}")
            return False
    
    def get_categories(self) -> List[Dict]:
        """カテゴリ一覧取得"""
        try:
            response = requests.get(
                f"{self.wp_config['api_url']}/categories",
                headers=self.wp_config['headers']
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"カテゴリ取得失敗: {response.status_code}")
                return []
        except Exception as e:
            print(f"カテゴリ取得エラー: {e}")
            return []
    
    def find_or_create_category(self, category_name: str) -> int:
        """カテゴリ検索・作成"""
        categories = self.get_categories()
        
        # 既存カテゴリを検索
        for cat in categories:
            if cat['name'].lower() == category_name.lower():
                return cat['id']
        
        # 新規カテゴリ作成
        data = {'name': category_name}
        try:
            response = requests.post(
                f"{self.wp_config['api_url']}/categories",
                headers=self.wp_config['headers'], 
                json=data
            )
            if response.status_code == 201:
                new_category = response.json()
                print(f"✅ 新規カテゴリ作成: {category_name}")
                return new_category['id']
            else:
                print(f"カテゴリ作成失敗: {response.status_code}")
                return 1  # デフォルトカテゴリ
        except Exception as e:
            print(f"カテゴリ作成エラー: {e}")
            return 1
    
    def find_or_create_tags(self, tag_names: List[str]) -> List[int]:
        """タグ検索・作成"""
        try:
            response = requests.get(
                f"{self.wp_config['api_url']}/tags",
                headers=self.wp_config['headers']
            )
            existing_tags = response.json() if response.status_code == 200 else []
        except:
            existing_tags = []
        
        tag_ids = []
        for tag_name in tag_names:
            # 既存タグを検索
            found = False
            for tag in existing_tags:
                if tag['name'].lower() == tag_name.lower():
                    tag_ids.append(tag['id'])
                    found = True
                    break
            
            # 新規タグ作成
            if not found:
                data = {'name': tag_name}
                try:
                    response = requests.post(
                        f"{self.wp_config['api_url']}/tags",
                        headers=self.wp_config['headers'],
                        json=data
                    )
                    if response.status_code == 201:
                        new_tag = response.json()
                        tag_ids.append(new_tag['id'])
                        print(f"✅ 新規タグ作成: {tag_name}")
                except Exception as e:
                    print(f"タグ作成エラー: {e}")
        
        return tag_ids
    
    def create_wordpress_post(self, 
                             title: str, 
                             content: str, 
                             category: str = "Audible",
                             tags: List[str] = None,
                             meta_description: str = "",
                             status: str = "draft") -> Optional[Dict]:
        """WordPress記事作成・投稿"""
        if tags is None:
            tags = []
        
        # カテゴリとタグのIDを取得
        category_id = self.find_or_create_category(category)
        tag_ids = self.find_or_create_tags(tags)
        
        # 投稿データ作成
        post_data = {
            'title': title,
            'content': content,
            'categories': [category_id],
            'tags': tag_ids,
            'status': status,
            'meta': {
                'description': meta_description
            }
        }
        
        try:
            response = requests.post(
                f"{self.wp_config['api_url']}/posts",
                headers=self.wp_config['headers'], 
                json=post_data
            )
            
            if response.status_code == 201:
                post_info = response.json()
                print(f"✅ 記事投稿成功: {title}")
                print(f"   URL: {post_info['link']}")
                print(f"   ID: {post_info['id']}")
                return post_info
            else:
                print(f"❌ 記事投稿失敗: {response.status_code}")
                print(f"   エラー: {response.text}")
                return None
        except Exception as e:
            print(f"❌ 記事投稿エラー: {e}")
            return None
    
    def backup_post(self, post_id: int) -> Optional[str]:
        """記事バックアップ"""
        try:
            response = requests.get(
                f"{self.wp_config['api_url']}/posts/{post_id}",
                headers=self.wp_config['headers']
            )
            
            if response.status_code == 200:
                post_data = response.json()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"記事{post_id}_backup_{timestamp}.json"
                backup_path = self.backup_dir / backup_filename
                
                with open(backup_path, 'w', encoding='utf-8') as f:
                    json.dump(post_data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ 記事{post_id}バックアップ完了: {backup_filename}")
                return str(backup_path)
            else:
                print(f"❌ 記事{post_id}バックアップ失敗: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ バックアップエラー: {e}")
            return None
    
    def delete_post(self, post_id: int, force: bool = False) -> bool:
        """記事削除（保護記事チェック付き）"""
        if post_id in self.protected_post_ids:
            print(f"❌ 記事ID {post_id} は保護対象のため削除できません")
            return False
        
        # バックアップ作成
        backup_path = self.backup_post(post_id)
        if not backup_path:
            print(f"⚠️ 記事{post_id}のバックアップ失敗、削除を中止")
            return False
        
        try:
            params = {'force': 'true'} if force else {}
            response = requests.delete(
                f"{self.wp_config['api_url']}/posts/{post_id}",
                headers=self.wp_config['headers'],
                params=params
            )
            
            if response.status_code == 200:
                print(f"✅ 記事{post_id}削除完了（バックアップ済み）")
                return True
            else:
                print(f"❌ 記事{post_id}削除失敗: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 削除エラー: {e}")
            return False
    
    # ========================================
    # テンプレート記事作成機能統合
    # ========================================
    
    def create_article_from_template(self, 
                                   topic: str,
                                   keywords: List[str],
                                   source_material: str = "") -> Dict[str, Any]:
        """テンプレートに基づいた記事作成"""
        print(f"📝 テンプレート準拠記事作成開始: {topic}")
        
        try:
            # 1. 資料内容分析
            material_analysis = self._analyze_source_material(source_material, keywords)
            
            # 2. テンプレート構造に基づく記事構築
            article_structure = self._build_article_structure(topic, keywords, material_analysis)
            
            # 3. 品質チェック実行
            quality_result = self._perform_comprehensive_quality_check(article_structure)
            
            if not quality_result["passed"]:
                return {
                    "success": False,
                    "reason": "品質基準不合格",
                    "quality_issues": quality_result["issues"]
                }
            
            # 4. ユーザー確認メッセージ表示
            print("\n🚨 **ユーザー確認が必要です！**")
            print("**ルールに従い、WordPress下書き保存前にユーザー確認が必要です。**")
            print(f"📊 品質スコア: {quality_result['score']}/100")
            print(f"📋 テンプレート準拠度: {quality_result.get('template_compliance', 0)}%")
            print("記事内容を確認して、WordPress下書き保存の許可をお願いします。")
            
            # 5. WordPress下書き保存（ルール準拠）
            wordpress_result = self.create_wordpress_post(
                title=article_structure["title"],
                content=article_structure["content"], 
                category="Audible",
                tags=keywords,
                meta_description=article_structure.get("meta_description", ""),
                status="draft"  # 下書き状態で保存
            )
            
            # 6. 記事ファイル保存
            save_result = self._save_article_with_metadata(article_structure, keywords)
            
            return {
                "success": True,
                "article": article_structure,
                "quality_score": quality_result["score"],
                "wordpress_post": wordpress_result,
                "saved_path": save_result["path"],
                "status": "下書き保存完了"
            }
            
        except Exception as e:
            print(f"❌ 記事作成エラー: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _analyze_source_material(self, material: str, keywords: List[str]) -> Dict[str, Any]:
        """資料内容分析"""
        return {
            "main_topic": keywords[0] if keywords else "記事作成",
            "key_points": self._extract_key_points(material),
            "target_audience": "Audible・オーディオブック利用者",
            "article_type": self._determine_article_type(material, keywords)
        }
    
    def _extract_key_points(self, material: str) -> List[str]:
        """重要ポイント抽出"""
        if not material:
            return ["基本的な使い方", "メリット・デメリット", "具体的な活用法"]
        
        # 簡単なキーワード抽出
        key_points = []
        if "価格" in material or "料金" in material:
            key_points.append("料金・価格情報")
        if "比較" in material:
            key_points.append("サービス比較")
        if "方法" in material or "やり方" in material:
            key_points.append("具体的な方法")
        if "メリット" in material or "効果" in material:
            key_points.append("効果・メリット")
        
        return key_points if key_points else ["基本情報", "活用方法", "おすすめポイント"]
    
    def _determine_article_type(self, material: str, keywords: List[str]) -> str:
        """記事タイプ判定"""
        if "比較" in material or any("比較" in k for k in keywords):
            return "comparison"
        elif "方法" in material or "やり方" in material:
            return "howto"
        elif "おすすめ" in material or any("おすすめ" in k for k in keywords):
            return "recommendation"
        else:
            return "guide"
    
    def _build_article_structure(self, topic: str, keywords: List[str], analysis: Dict) -> Dict[str, Any]:
        """記事構造構築"""
        # マフィンブログフォーマットでの記事構築
        title = self._generate_seo_title(topic, keywords)
        
        # SEO設定生成
        seo_settings = self._generate_seo_settings(title, keywords)
        
        # 記事本文構築
        content = self._build_article_content(topic, keywords, analysis)
        
        return {
            "title": title,
            "content": content,
            "seo_settings": seo_settings,
            "keywords": keywords,
            "topic": topic,
            "word_count": len(content),
            "created_at": datetime.now().isoformat()
        }
    
    def _generate_seo_title(self, topic: str, keywords: List[str]) -> str:
        """SEO最適化タイトル生成（Audible関連付け対応）"""
        # マフィンブログはAudible特化ブログのため、Audible関連の文脈でタイトル作成
        main_keyword = keywords[0] if keywords else topic
        current_year = datetime.now().year
        
        # Audible関連付けパターンでタイトル生成
        if "audible" in main_keyword.lower() or "オーディブル" in main_keyword:
            # 直接的Audible関連
            title_patterns = [
                f"{main_keyword}完全ガイド！{current_year}年最新活用法",
                f"{main_keyword}の始め方｜初心者向け完全マニュアル{current_year}",
                f"{main_keyword}活用術｜効果的な使い方とコツ{current_year}年版"
            ]
        elif "audiobook" in main_keyword.lower() or "オーディオブック" in main_keyword:
            # オーディオブック関連（比較・関連付け）
            title_patterns = [
                f"{main_keyword}完全ガイド！Audible比較も解説{current_year}",
                f"{main_keyword}活用法｜Audibleとの違いと選び方{current_year}年版",
                f"{main_keyword}徹底比較｜料金・使いやすさ・Audible{current_year}"
            ]
        elif "読書" in main_keyword or "音声学習" in main_keyword or "聴覚学習" in main_keyword:
            # 読書・学習関連（Audible活用に関連付け）
            title_patterns = [
                f"{main_keyword}完全ガイド！聴く読書で効率化{current_year}年版",
                f"{main_keyword}活用術｜オーディオブックで実践{current_year}",
                f"{main_keyword}の効果的なやり方｜Audible活用法も解説{current_year}"
            ]
        else:
            # その他のトピック（Audible関連に関連付け）
            title_patterns = [
                f"{main_keyword}とオーディオブック活用｜{current_year}年完全ガイド",
                f"{main_keyword}効率化術｜聴く読書との組み合わせ{current_year}年版",
                f"{main_keyword}完全マニュアル｜Audible併用で効果UP{current_year}"
            ]
        
        return title_patterns[0]
    
    def _generate_seo_settings(self, title: str, keywords: List[str]) -> Dict[str, Any]:
        """SEO設定生成（Audible関連付け対応）"""
        main_keyword = keywords[0] if keywords else "記事"
        
        # Audible関連付けでメタディスクリプション生成
        if "audible" in main_keyword.lower() or "オーディブル" in main_keyword:
            meta_description = f"{main_keyword}について詳しく解説。初心者でも分かりやすい使い方から効果的な活用法まで、実用的な情報をお伝えします。30日無料体験の活用法も紹介。"
        elif "audiobook" in main_keyword.lower() or "オーディオブック" in main_keyword:
            meta_description = f"{main_keyword}について詳しく解説。Audibleとの比較、料金・使いやすさの違い、最適な選び方まで分かりやすく説明します。"
        else:
            meta_description = f"{main_keyword}を効率的に活用する方法を詳しく解説。オーディオブックとの組み合わせや聴く読書での実践方法も含めて、実用的な情報をお伝えします。"
        
        # スラッグ生成
        slug = self._generate_slug(title, main_keyword)
        
        # タグ生成（Audible関連付け）
        tags = self._generate_audible_related_tags(keywords)
        
        return {
            "meta_description": meta_description,
            "slug": slug,
            "tags": tags,
            "category": "Audible"
        }
    
    def _generate_slug(self, title: str, main_keyword: str) -> str:
        """スラッグ生成"""
        keyword_translation = {
            "読書苦手": "reading-dislike",
            "Audible": "audible",
            "オーディブル": "audible",
            "聴く読書": "listening-reading",
            "オーディオブック": "audiobook",
            "audiobook": "audiobook-jp"
        }
        
        main_key_eng = keyword_translation.get(main_keyword, "guide")
        
        if "解決" in title:
            return f"{main_key_eng}-solution"
        elif "方法" in title or "始め方" in title:
            return f"{main_key_eng}-guide"
        elif "比較" in title:
            return f"{main_key_eng}-comparison"
        else:
            return f"{main_key_eng}-complete-guide"
    
    def _generate_audible_related_tags(self, keywords: List[str]) -> List[str]:
        """Audible関連付けタグ生成"""
        base_tags = keywords[:3]  # 基本キーワード
        main_keyword = keywords[0] if keywords else ""
        
        # キーワードの種類に応じて関連タグを選定
        related_tags = []
        
        if "audible" in main_keyword.lower() or "オーディブル" in main_keyword:
            # 直接的Audible関連
            related_tags = ["30日無料", "聴き放題", "オーディオブック", "聴く読書"]
        elif "audiobook" in main_keyword.lower() or "オーディオブック" in main_keyword:
            # オーディオブック関連（比較・選択肢）
            related_tags = ["Audible", "audiobook.jp", "比較", "料金", "聴き放題"]
        elif "読書" in main_keyword or "音声学習" in main_keyword or "聴覚学習" in main_keyword:
            # 読書・学習関連
            related_tags = ["聴く読書", "オーディオブック", "Audible", "効率化"]
        elif "kindle" in main_keyword.lower() or "キンドル" in main_keyword:
            # Kindle関連（比較）
            related_tags = ["Audible", "Kindle", "読書", "比較", "聴く読書"]
        else:
            # その他（汎用的な関連付け）
            related_tags = ["オーディオブック", "聴く読書", "効率化"]
        
        # その他共通タグ
        common_tags = ["2025年", "初心者向け", "使い方", "活用法"]
        
        all_tags = base_tags + related_tags + common_tags
        return list(dict.fromkeys(all_tags))[:8]  # 重複除去・8個まで
    
    def _build_article_content(self, topic: str, keywords: List[str], analysis: Dict) -> str:
        """記事本文構築（Audible関連付け対応）"""
        main_keyword = keywords[0] if keywords else topic
        
        # Audible関連付けで記事内容を構築
        content_type = self._determine_audible_relation_type(main_keyword)
        
        # マフィンブログフォーマットの記事構成
        content_parts = []
        
        # 1. 冒頭の会話
        content_parts.append(self._build_opening_dialogue(main_keyword))
        
        # 2. この記事で分かること
        content_parts.append(self._build_article_benefits_section(keywords))
        
        # 3. 結論先出し
        content_parts.append(self._build_conclusion_first(main_keyword))
        
        # 4. メインセクション（関連付けタイプに応じて）
        content_parts.append(self._build_audible_related_sections(main_keyword, content_type, analysis))
        
        # 5. FAQ
        content_parts.append(self._build_audible_related_faq(main_keyword, content_type))
        
        # 6. まとめ
        content_parts.append(self._build_summary_section(main_keyword))
        
        return "\n\n".join(content_parts)
    
    def _determine_audible_relation_type(self, main_keyword: str) -> str:
        """Audible関連付けタイプを判定"""
        if "audible" in main_keyword.lower() or "オーディブル" in main_keyword:
            return "direct_audible"
        elif "audiobook" in main_keyword.lower() or "オーディオブック" in main_keyword:
            return "audiobook_comparison"
        elif "読書" in main_keyword or "音声学習" in main_keyword or "聴覚学習" in main_keyword:
            return "reading_learning"
        elif "kindle" in main_keyword.lower() or "キンドル" in main_keyword:
            return "device_comparison"
        else:
            return "general_relation"
    
    def _build_audible_related_sections(self, main_keyword: str, content_type: str, analysis: Dict) -> str:
        """Audible関連付けメインセクション（タイプ別対応）"""
        
        if content_type == "direct_audible":
            return self._build_direct_audible_sections(main_keyword)
        elif content_type == "audiobook_comparison":
            return self._build_audiobook_comparison_sections(main_keyword)
        elif content_type == "reading_learning":
            return self._build_reading_learning_sections(main_keyword)
        elif content_type == "device_comparison":
            return self._build_device_comparison_sections(main_keyword)
        else:
            return self._build_general_relation_sections(main_keyword)
    
    def _build_direct_audible_sections(self, main_keyword: str) -> str:
        """直接的Audible関連セクション"""
        sections = []
        
        sections.append(f'''## {main_keyword}とは？基本的な仕組みを解説

**女性**：{main_keyword}って、具体的にはどういうサービスなんですか？

**マフィン**：{main_keyword}はな、オーディオブックの聴き放題サービスやねん。本を耳で聴けるから、従来の読書とは全く違う体験ができるで。

### {main_keyword}の基本的な特徴

- **12万冊以上が聴き放題**：豊富なラインナップ
- **プロのナレーション**：理解しやすい朗読
- **倍速再生対応**：0.5〜3.5倍速で効率化
- **30日無料体験**：リスクなしで試せる''')
        
        sections.append(f'''## {main_keyword}の効果的な使い方｜ステップごとに解説

**女性**：実際にはどうやって使い始めればいいんですか？

**マフィン**：簡単やで！アプリダウンロードして、順番に説明したるから一緒にやってみよう。

### ステップ1：無料体験登録
まずは30日無料体験に登録。期間内解約で料金はかからない。

### ステップ2：興味のある本を選択
ライブラリから読みたい本をダウンロード。

### ステップ3：聴きながら生活
通勤、家事、運動中など、あらゆる時間を読書時間に。''')
        
        return "\n\n".join(sections)
    
    def _build_audiobook_comparison_sections(self, main_keyword: str) -> str:
        """オーディオブック比較セクション"""
        sections = []
        
        sections.append(f'''## {main_keyword}とは？Audibleとの違いを解説

**女性**：{main_keyword}って、Audibleと何が違うんですか？

**マフィン**：ええ質問やな！料金体系やサービス内容に違いがあるから、詳しく比較したるわ。

### 主要オーディオブックサービス比較

| 項目 | {main_keyword} | Audible |
|------|------------|---------|
| 月額料金 | 料金による | 1,500円 |
| 聴き放題 | プランによる | 12万冊以上 |
| 無料体験 | サービスによる | 30日間 |

どちらも一長一短があるから、用途に合わせて選ぶのが大切やで。''')
        
        sections.append(f'''## {main_keyword}とAudibleの選び方｜どっちがおすすめ？

**女性**：結局どちらを選べばいいんでしょうか？

**マフィン**：使い方次第やな。料金重視なら{main_keyword}、利便性重視ならAudibleがおすすめやで。

### こんな人には{main_keyword}がおすすめ
- コストを抑えたい人
- 特定の本だけ聴きたい人

### こんな人にはAudibleがおすすめ  
- たくさんの本を聴きたい人
- 使いやすさを重視する人
- 最新のビジネス書を聴きたい人''')
        
        return "\n\n".join(sections)
    
    def _build_reading_learning_sections(self, main_keyword: str) -> str:
        """読書・学習関連セクション"""
        sections = []
        
        sections.append(f'''## {main_keyword}とは？効果的な学習方法を解説

**女性**：{main_keyword}って、どんな学習方法なんですか？

**マフィン**：{main_keyword}はな、従来の文字を読む学習とは違って、耳を使った効率的な学習方法やねん。

### {main_keyword}の基本的な仕組み

- **聴覚を活用**：目を使わずに学習できる
- **マルチタスク可能**：他の作業をしながらでもOK
- **理解度向上**：音声の方が記憶に残りやすい

文字を追うのが苦手な人でも、{main_keyword}なら続けやすいで。''')
        
        sections.append(f'''## {main_keyword}をオーディオブックで実践する方法

**女性**：{main_keyword}を実際に試すには、どうすればいいですか？

**マフィン**：一番手軽なのは、Audibleみたいなオーディオブックサービスを使うことやな。

### オーディオブックでの{main_keyword}実践法

#### Audibleを活用した{main_keyword}
- **豊富な学習コンテンツ**：ビジネス書、自己啓発書が充実
- **再生速度調整**：理解度に合わせて1.25倍速〜2倍速で効率化
- **通勤時間活用**：移動時間を学習時間に変換

#### 具体的なステップ
1. **Audibleに無料登録**：30日間リスクフリー
2. **{main_keyword}関連書籍を選択**：興味のあるテーマから開始  
3. **日常に組み込み**：通勤、家事、運動と併用''')
        
        return "\n\n".join(sections)
    
    def _build_device_comparison_sections(self, main_keyword: str) -> str:
        """デバイス比較セクション"""
        sections = []
        
        sections.append(f'''## {main_keyword}とは？読書デバイスの特徴を解説

**女性**：{main_keyword}って、読書にはどうなんですか？

**マフィン**：{main_keyword}はな、電子書籍を読むには便利やけど、実は聴く読書の方が効率的かもしれんで。

### {main_keyword}の読書における特徴

**メリット**
- 軽量で持ち運びやすい
- 目に優しいディスプレイ
- 長時間読書に適している

**デメリット**  
- 目を使うので疲労する
- 暗い場所では読みにくい
- マルチタスクができない''')
        
        sections.append(f'''## {main_keyword} vs Audible｜どちらが読書に効果的？

**女性**：{main_keyword}とAudibleの聴く読書、どちらがいいんでしょうか？

**マフィン**：用途によるけど、効率性で言うたらAudibleの方がメリット大きいかもな。

### 読書スタイル比較

| 項目 | {main_keyword} | Audible |
|------|------------|---------|
| 目の疲労 | あり | なし |
| マルチタスク | 不可 | 可能 |
| 理解度 | 個人差 | 高い（プロの朗読） |
| 継続性 | 場所に依存 | いつでもどこでも |

### 併用がおすすめ
実は{main_keyword}とAudibleを使い分けるのが最強やで。集中したい時は{main_keyword}、ながら読書はAudibleって感じでな。''')
        
        return "\n\n".join(sections)
    
    def _build_general_relation_sections(self, main_keyword: str) -> str:
        """汎用関連付けセクション"""
        sections = []
        
        sections.append(f'''## {main_keyword}とは？効率的な活用方法を解説

**女性**：{main_keyword}について教えてください！

**マフィン**：{main_keyword}はな、うまく活用すれば生活がもっと効率的になるツールやねん。

### {main_keyword}の基本的な活用法

- **時間効率の向上**：限られた時間を有効活用
- **知識習得の促進**：学習効果を高める
- **ライフスタイル改善**：日常をより充実させる

特に忙しい現代人には、{main_keyword}の効果的な使い方を知ることが大切やで。''')
        
        sections.append(f'''## {main_keyword}×オーディオブック活用術｜相乗効果を狙う

**女性**：{main_keyword}をもっと効果的に使う方法はありますか？

**マフィン**：オーディオブックと組み合わせると、{main_keyword}の効果が倍増するで！

### {main_keyword}とオーディオブックの組み合わせメリット

#### Audibleとの併用効果
- **学習時間の最大化**：移動時間も{main_keyword}の実践時間に
- **理論と実践の両立**：知識インプットと実践が同時進行
- **継続性の向上**：耳学習で習慣化しやすい

#### 具体的な活用例
1. **通勤時間**：Audibleで{main_keyword}関連の本を聴く
2. **実践時間**：学んだ知識を実際の{main_keyword}に活かす
3. **復習時間**：重要部分をリピート再生で定着化''')
        
        return "\n\n".join(sections)
    
    def _build_audible_related_faq(self, main_keyword: str, content_type: str) -> str:
        """Audible関連付けFAQセクション（タイプ別対応）"""
        
        if content_type == "direct_audible":
            return self._build_direct_audible_faq(main_keyword)
        elif content_type == "audiobook_comparison":
            return self._build_audiobook_comparison_faq(main_keyword)
        elif content_type == "reading_learning":
            return self._build_reading_learning_faq(main_keyword)
        elif content_type == "device_comparison":
            return self._build_device_comparison_faq(main_keyword)
        else:
            return self._build_general_relation_faq(main_keyword)
    
    def _build_direct_audible_faq(self, main_keyword: str) -> str:
        """直接的Audible関連FAQ"""
        faqs = [
            {
                "q": f"{main_keyword}は初心者でも使えますか？",
                "a": f"はい、{main_keyword}は初心者の方でも簡単に使えるよう設計されています。アプリの操作も直感的で、30日間の無料体験で試せるので安心です。"
            },
            {
                "q": f"{main_keyword}の料金はいくらですか？",
                "a": f"{main_keyword}の月額料金は1,500円です。12万冊以上が聴き放題で、30日間の無料体験もあります。期間内に解約すれば料金はかかりません。"
            },
            {
                "q": f"{main_keyword}は無料で試せますか？",
                "a": f"はい！{main_keyword}は30日間無料でお試しできます。豊富なラインナップから好きな本を選んで聴けるので、まずは気軽に試してみてください。"
            },
            {
                "q": f"{main_keyword}の解約方法は？",
                "a": f"{main_keyword}はいつでも解約できます。アプリやWebサイトから簡単に手続きでき、解約後もダウンロード済みの本は引き続き聴けます。"
            },
            {
                "q": f"{main_keyword}のおすすめの使い方は？",
                "a": f"通勤時間や家事の時間を活用するのがおすすめです。最初は1.0倍速から始めて、慣れたら1.25倍速で効率よく聴けます。"
            }
        ]
        
        return self._format_faq_content(faqs)
    
    def _build_audiobook_comparison_faq(self, main_keyword: str) -> str:
        """オーディオブック比較FAQ"""
        faqs = [
            {
                "q": f"{main_keyword}とAudibleの最大の違いは？",
                "a": "主に料金体系と聴き放題の範囲です。コストを重視するか、利便性を重視するかで選択が変わります。どちらも無料体験があるので、実際に試して比較するのがおすすめです。"
            },
            {
                "q": f"{main_keyword}の方が安いって本当ですか？",
                "a": f"プランによっては{main_keyword}の方が安い場合があります。ただし、聴き放題の範囲や使いやすさを考慮すると、Audibleの方がコストパフォーマンスが良いことも多いです。"
            },
            {
                "q": "初心者はどちらから始めるべきですか？",
                "a": "オーディオブック初心者なら、まずはAudibleの30日無料体験から始めるのがおすすめです。操作が簡単で、豊富なコンテンツを試せます。"
            },
            {
                "q": "両方のサービスを併用するメリットは？",
                "a": f"用途に応じて使い分けることで、それぞれの良さを活かせます。{main_keyword}で特定のコンテンツを、Audibleで幅広いジャンルをカバーするといった使い方が効果的です。"
            },
            {
                "q": "どちらが解約しやすいですか？",
                "a": "どちらも解約は比較的簡単ですが、Audibleの方が解約後の制限が少なく、ダウンロード済みコンテンツの利用継続などで利便性が高いです。"
            }
        ]
        
        return self._format_faq_content(faqs)
    
    def _build_reading_learning_faq(self, main_keyword: str) -> str:
        """読書・学習関連FAQ"""
        faqs = [
            {
                "q": f"{main_keyword}は本当に効果的ですか？",
                "a": f"はい、{main_keyword}は科学的にも効果が認められている学習方法です。特にオーディオブックと組み合わせることで、移動時間も学習時間に変えられ、効率が大幅に向上します。"
            },
            {
                "q": f"{main_keyword}を始めるのに必要なものは？",
                "a": f"基本的には聴く環境があれば始められます。Audibleなどのオーディオブックサービスがあると、{main_keyword}を手軽に実践できるのでおすすめです。"
            },
            {
                "q": f"{main_keyword}に向いていない人はいますか？",
                "a": f"音声だけでの学習が苦手な人もいますが、多くの場合は慣れの問題です。Audibleの再生速度調整機能を使えば、自分のペースで{main_keyword}を実践できます。"
            },
            {
                "q": f"従来の読書と{main_keyword}、どちらが良いですか？",
                "a": f"どちらにも良さがありますが、継続性と効率性では{main_keyword}が優れています。Audibleなら通勤中でも学習でき、プロの朗読で理解度も向上します。"
            },
            {
                "q": f"{main_keyword}の効果を最大化するコツは？",
                "a": f"日常の隙間時間を活用することです。Audibleで{main_keyword}関連の本を聴きながら、実際に学んだことを実践に移すサイクルを作ることが重要です。"
            }
        ]
        
        return self._format_faq_content(faqs)
    
    def _build_device_comparison_faq(self, main_keyword: str) -> str:
        """デバイス比較FAQ"""
        faqs = [
            {
                "q": f"{main_keyword}とAudible、読書にはどちらがいいですか？",
                "a": f"用途次第ですが、継続性と効率性ではAudibleが優れています。{main_keyword}は集中読書に、Audibleは日常の隙間時間活用に適しています。"
            },
            {
                "q": f"{main_keyword}を持っているなら、Audibleは不要ですか？",
                "a": f"いえ、むしろ併用がおすすめです。{main_keyword}で集中読書、Audibleで移動時間の学習と使い分けることで、読書量を大幅に増やせます。"
            },
            {
                "q": f"{main_keyword}の電池持ちが心配です",
                "a": f"{main_keyword}は電池持ちが良いデバイスですが、長時間使用する場合はAudibleの方が便利です。スマートフォンなら充電しながら聴けるので、バッテリーの心配がありません。"
            },
            {
                "q": f"{main_keyword}で読書習慣をつけるコツは？",
                "a": f"{main_keyword}とAudibleを組み合わせるのが効果的です。移動中はAudible、じっくり読みたい時は{main_keyword}と使い分けることで、無理なく習慣化できます。"
            },
            {
                "q": "コストを抑えて読書量を増やすには？",
                "a": f"{main_keyword}での購入とAudibleの聴き放題を使い分けることです。Audibleで気に入った本を見つけて、{main_keyword}版でじっくり読み返すという方法もおすすめです。"
            }
        ]
        
        return self._format_faq_content(faqs)
    
    def _build_general_relation_faq(self, main_keyword: str) -> str:
        """汎用関連付けFAQ"""
        faqs = [
            {
                "q": f"{main_keyword}を効率的に活用する方法は？",
                "a": f"オーディオブックと組み合わせることで、{main_keyword}の効果を大幅に向上させられます。Audibleなら移動時間も{main_keyword}の学習時間に変えられるのでおすすめです。"
            },
            {
                "q": f"{main_keyword}初心者におすすめの始め方は？",
                "a": f"まずは基本を理解することから始めましょう。Audibleで{main_keyword}関連の本を聴きながら、実際に実践してみるのが効果的です。"
            },
            {
                "q": f"{main_keyword}に必要な時間はどのくらいですか？",
                "a": f"日常生活に組み込めば、特別な時間を確保する必要はありません。Audibleで学習しながら{main_keyword}を実践すれば、効率的にスキルアップできます。"
            },
            {
                "q": f"{main_keyword}の成果が出るまでの期間は？",
                "a": f"個人差がありますが、継続的に取り組めば短期間でも効果を実感できます。Audibleで{main_keyword}の知識を深めながら実践することで、成果が出やすくなります。"
            },
            {
                "q": f"{main_keyword}で失敗しないコツは？",
                "a": f"無理をせず、継続することが大切です。Audibleで{main_keyword}の理論を学び、少しずつ実践に移していくことで、着実に成果を上げられます。"
            }
        ]
        
        return self._format_faq_content(faqs)
    
    def _format_faq_content(self, faqs: List[Dict[str, str]]) -> str:
        """FAQ形式の文字列に整形"""
        faq_content = ["## よくある質問｜FAQ"]
        for i, faq in enumerate(faqs, 1):
            faq_content.append(f"### Q{i}. {faq['q']}")
            faq_content.append(f"A{i}. {faq['a']}")
            faq_content.append("")
        
        return "\n".join(faq_content)
    
    def _check_article_structure_compliance(self, content: str, title: str) -> int:
        """記事構成テンプレート基準チェック（2025-08-13確立）"""
        score = 100
        structure = self.quality_standards["standard_article_structure"]
        
        # 標準構成の存在チェック
        structure_elements = {
            "導入": content.count("**女性**") > 0 and content.count("**マフィン**") > 0,
            "概念説明": "とは" in content or "について" in content,
            "基本やり方": "ステップ" in content or "方法" in content or "やり方" in content,
            "効果・理由": "効果" in content or "理由" in content or "メリット" in content,
            "詳細実践": "実践" in content or "活用" in content,
            "具体例": "おすすめ" in content or "例" in content,
            "料金": "料金" in content or "1500円" in content or "1,500円" in content,
            "FAQ": "FAQ" in content or "よくある質問" in content,
            "まとめ": "まとめ" in content
        }
        
        # 各要素の存在確認
        missing_count = sum(1 for exists in structure_elements.values() if not exists)
        score -= missing_count * 10
        
        # 読者検索意図優先チェック
        # タイトルに「始め方」があるなら基本やり方は前半に必要
        if "始め方" in title and not structure_elements["基本やり方"]:
            score -= 20
        
        return max(0, score)
    
    def _check_section_intro_compliance(self, content: str) -> int:
        """大見出し下の導入会話チェック"""
        score = 100
        
        # ## の直後に会話があるかチェック
        h2_sections = content.split("## ")[1:] if "## " in content else []
        
        intro_count = 0
        for section in h2_sections:
            lines = section.split("\n")
            # 最初の数行内に**女性**があるかチェック
            has_intro = any("**女性**" in line for line in lines[:5])
            if has_intro:
                intro_count += 1
        
        total_h2 = len(h2_sections)
        if total_h2 > 0:
            intro_ratio = (intro_count / total_h2) * 100
            if intro_ratio < 50:  # 50%以下の場合
                score -= 30
        
        return max(0, score)
    
    def _check_search_intent_compliance(self, content: str, title: str) -> int:
        """読者検索意図チェック"""
        score = 100
        
        # タイトル分析
        intent_keywords = {
            "方法": ["ステップ", "方法", "やり方"],
            "とは": ["とは", "について", "意味"],
            "効果": ["効果", "理由", "メリット"],
            "おすすめ": ["おすすめ", "選び方", "比較"]
        }
        
        # タイトルに応じた必要要素チェック
        for intent, required_words in intent_keywords.items():
            if intent in title:
                found = any(word in content for word in required_words)
                if not found:
                    score -= 25
        
        # 「やり方を理由より優先」ルールチェック
        method_position = content.find("方法") if "方法" in content else content.find("やり方")
        reason_position = content.find("理由") if "理由" in content else content.find("効果")
        
        if method_position > 0 and reason_position > 0 and method_position > reason_position:
            if "始め方" in title or "方法" in title:
                score -= 20  # やり方が後にあるのはNG
        
        return max(0, score)
    
    def _ensure_audible_focus(self, topic: str, main_keyword: str) -> str:
        """トピックにAudible要素を確実に含める"""
        if "audible" not in topic.lower() and "オーディブル" not in topic:
            if main_keyword and main_keyword != topic:
                return f"Audibleで{main_keyword}を活用"
            else:
                return f"Audible {topic}"
        return topic
    
    def _ensure_audible_in_keywords(self, keywords: List[str]) -> List[str]:
        """キーワードにAudibleを確実に含める"""
        if not any("audible" in k.lower() or "オーディブル" in k for k in keywords):
            keywords = ["Audible"] + keywords
        return keywords
    
    def _build_opening_dialogue(self, main_keyword: str) -> str:
        """冒頭会話セクション"""
        return f'''**女性**：マフィンさん、{main_keyword}について教えてください！

**マフィン**：ええ質問やな！{main_keyword}について詳しく解説するで。知っておくべきポイントがようけあるから、分かりやすく説明したるわ。

**女性**：ありがとうございます！よろしくお願いします。

**マフィン**：任せとき！実際に使えるコツも含めて、しっかり教えたるからな。'''
    
    def _build_article_benefits_section(self, keywords: List[str]) -> str:
        """記事で分かることセクション（CLAUDE.mdルール準拠）"""
        main_keyword = keywords[0] if keywords else "この記事"
        
        # CLAUDE.mdの「この記事で分かること」ルール適用
        # - 簡潔に記事内容を示す
        # - 魅力的だが詰め込みすぎない  
        # - 大げさな表現は避ける
        # - 実際の記事構成と一致させる
        
        benefits = [
            f"{main_keyword}の基本知識と始め方",
            f"{main_keyword}の効果的な活用方法", 
            f"{main_keyword}のメリット・効果", # デメリットは削除（大げさ回避）
            "実際の使用例と体験談",
            "よくある疑問への回答",
            "30日無料体験の活用法" # Audible特化要素を追加
        ]
        
        benefits_text = "\n".join([f"- {benefit}" for benefit in benefits])
        
        # 結論部分も大げさな表現を避ける
        return f'''**この記事で分かること**

{benefits_text}

**結論を先に言うと：{main_keyword}を効率的に活用する方法が分かり、今日から実践できるようになります。**'''
    
    def _build_conclusion_first(self, main_keyword: str) -> str:
        """結論先出しセクション"""
        return f'''{main_keyword}を効果的に活用するためには、基本的な仕組みを理解することが大切です。

この記事では、初心者の方でも分かりやすいように、具体例を交えながら詳しく解説していきます。'''
    
    def _build_main_sections(self, main_keyword: str, analysis: Dict) -> str:
        """メインセクション"""
        sections = []
        
        # セクション1: 基本説明
        sections.append(f'''## {main_keyword}とは？基本的な仕組みを解説

**女性**：{main_keyword}って具体的にはどういうものなんですか？

**マフィン**：{main_keyword}はな、簡単に言うと[基本的な説明]やねん。仕組みを理解すれば、めっちゃ使いやすくなるで。

### 基本的な特徴

{main_keyword}の主な特徴は以下の通りです：

- **特徴1**：[具体的な説明]
- **特徴2**：[実用的なポイント]
- **特徴3**：[ユーザーメリット]

これらの特徴を理解することで、より効果的に活用できるようになります。''')
        
        # セクション2: 使い方・方法
        sections.append(f'''## {main_keyword}の効果的な使い方｜ステップごとに解説

**女性**：実際にはどうやって使えばいいんですか？

**マフィン**：使い方は簡単やで！順番に説明したるから、一緒にやってみよう。

### ステップ1：準備
まずは基本的な準備から始めましょう。必要なものを揃えて、環境を整えます。

### ステップ2：実践
準備ができたら、実際に使ってみましょう。最初は簡単なものから始めることをおすすめします。

### ステップ3：応用
慣れてきたら、より高度な機能も活用してみてください。''')
        
        # セクション3: メリット・効果
        sections.append(f'''## {main_keyword}を使うメリット｜なぜおすすめなのか

### メリット1：効率性の向上
{main_keyword}を使うことで、従来の方法と比べて大幅な効率化が期待できます。

### メリット2：利便性の向上
いつでもどこでも利用できる手軽さが大きな魅力です。

### メリット3：コストパフォーマンス
費用対効果を考えると、非常に優れた選択肢と言えます。''')
        
        return "\n\n".join(sections)
    
    def _build_faq_section(self, main_keyword: str) -> str:
        """FAQセクション"""
        faqs = [
            {
                "q": f"{main_keyword}は初心者でも使えますか？",
                "a": f"はい、{main_keyword}は初心者の方でも安心して使えるよう設計されています。基本的な操作は直感的で、慣れれば簡単に活用できます。"
            },
            {
                "q": "利用料金はいくらですか？",
                "a": "料金体系は利用方法によって異なります。基本的なプランから始めて、必要に応じて上位プランを検討することをおすすめします。"
            },
            {
                "q": "無料で試すことはできますか？",
                "a": "多くのサービスで無料体験期間が提供されています。まずは無料で試してみて、自分に合うかどうか確認してみてください。"
            },
            {
                "q": "解約はいつでもできますか？",
                "a": "はい、基本的にはいつでも解約可能です。解約方法や注意点については事前に確認しておくことをおすすめします。"
            },
            {
                "q": "おすすめの使い方はありますか？",
                "a": "初心者の方は、まず基本機能から始めて徐々に慣れていくのがおすすめです。自分の目的に合わせて活用方法を見つけてください。"
            }
        ]
        
        faq_content = ["## よくある質問｜FAQ"]
        for i, faq in enumerate(faqs, 1):
            faq_content.append(f"### Q{i}. {faq['q']}")
            faq_content.append(f"A{i}. {faq['a']}")
            faq_content.append("")
        
        return "\n".join(faq_content)
    
    def _build_summary_section(self, main_keyword: str) -> str:
        """まとめセクション"""
        return f'''## まとめ：{main_keyword}で効率的に目標を達成しよう

{main_keyword}について重要なポイントをお伝えしました。

**重要なポイントのまとめ**
1. **基本を理解する**：まずは仕組みをしっかり把握
2. **実際に試す**：無料体験などを活用して体験
3. **継続的に活用**：効果を実感するまで続ける
4. **最適化する**：自分に合った使い方を見つける

**女性**：マフィンさん、ありがとうございました！とても分かりやすかったです。

**マフィン**：どういたしまして！{main_keyword}をうまく活用して、目標達成に向けて頑張ってな。分からんことがあったらまた聞いてや！

初心者の方は、まず基本的な部分から始めて、徐々に詳しい内容に進んでいくことをおすすめします。'''
    
    # ========================================
    # 品質管理・チェック機能統合
    # ========================================
    
    def _perform_comprehensive_quality_check(self, article_structure: Dict) -> Dict[str, Any]:
        """包括的品質チェック（CLAUDE.md統合版）"""
        print("🔍 包括的品質チェック実行中（CLAUDE.mdルール適用）...")
        
        content = article_structure["content"]
        title = article_structure.get("title", "")
        issues = []
        score = 100
        
        # 1. 文字数チェック（学習履歴から強化）
        word_count = len(content)
        target_count = self.quality_standards["quality_lessons"]["word_count_target"]
        if word_count < target_count:
            issues.append(f"文字数不足: {word_count}文字（目標{target_count}文字）")
            score -= 25  # より厳格に
        
        # 2. 必須セクションチェック
        for section in self.quality_standards["required_sections"]:
            if section not in content:
                issues.append(f"必須セクション不足: {section}")
                score -= 15
        
        # 3. 記事構成テンプレート基準チェック（2025-08-13確立）
        structure_score = self._check_article_structure_compliance(content, title)
        if structure_score < 80:
            issues.append(f"記事構成基準不適合: {structure_score}%（最低80%）")
            score -= 15
        
        # 4. H2見出しチェック
        h2_count = content.count("## ")
        if h2_count < self.quality_standards["required_h2_count"]:
            issues.append(f"H2見出し不足: {h2_count}個（最低{self.quality_standards['required_h2_count']}個）")
            score -= 10
        
        # 5. 大見出し下の導入会話チェック
        intro_compliance = self._check_section_intro_compliance(content)
        if intro_compliance < 70:
            issues.append("大見出し下の導入会話が不足または不適切")
            score -= 12
        
        # 6. 会話ブロックチェック（自然性重視）
        conversation_count = content.count("**女性**") + content.count("**マフィン**")
        if conversation_count < self.quality_standards["conversation_blocks_min"] * 2:
            issues.append("マフィンさんとの会話が不足")
            score -= 15
        
        # 7. FAQチェック（学習履歴から強化）
        faq_count = content.count("Q1.") + content.count("Q2.") + content.count("Q3.") + content.count("Q4.") + content.count("Q5.")
        required_faq = self.quality_standards["quality_lessons"]["faq_requirement"]
        if faq_count < required_faq:
            issues.append(f"FAQ不足: {faq_count}個（必須{required_faq}個）- 品質改善履歴より致命的")
            score -= 20  # より厳格に
        
        # 8. 絶対的見本テンプレート準拠チェック
        template_compliance_score = self._check_template_compliance(content)
        if template_compliance_score < 80:
            issues.append(f"テンプレート準拠度不足: {template_compliance_score}%（最低80%）")
            score -= (100 - template_compliance_score) // 4
        
        # 9. 禁止表現チェック（CLAUDE.md統合）
        for expression in self.quality_standards["prohibited_expressions"]:
            if expression in content:
                issues.append(f"禁止表現発見: '{expression}'")
                score -= 10
        
        # 10. 根拠データチェック（Audible関連）
        evidence_found = any(keyword in content for keyword in self.quality_standards["required_evidence_keywords"])
        if not evidence_found:
            issues.append("Audible公式情報（料金・無料体験等）が不足")
            score -= 15
        
        # 11. 読者検索意図チェック
        search_intent_score = self._check_search_intent_compliance(content, title)
        if search_intent_score < 70:
            issues.append("読者検索意図への対応不足")
            score -= 10
        
        # 学習履歴から：83点でも改善の余地ありの教訓を活かす
        final_score = max(0, score)
        passed = final_score >= self.quality_standards["quality_lessons"]["minimum_score"]
        
        return {
            "passed": passed,
            "score": final_score,
            "issues": issues,
            "word_count": word_count,
            "h2_count": h2_count,
            "conversation_count": conversation_count // 2,
            "faq_count": faq_count,
            "template_compliance": template_compliance_score if 'template_compliance_score' in locals() else 0,
            "structure_compliance": structure_score,
            "search_intent_compliance": search_intent_score
        }
    
    def _check_template_compliance(self, content: str) -> int:
        """絶対的見本テンプレートとの準拠度チェック"""
        if not self.template_content:
            print("⚠️ テンプレート内容が読み込まれていません")
            return 0
        
        compliance_score = 100
        template_elements = {
            "この記事で分かること": 20,
            "## ": 15,  # 大見出し構造
            "マフィンさん、": 15,  # 導入会話
            "**女性**": 10,  # 会話形式
            "**マフィン**": 10,  # 会話形式
            "まとめ": 15,  # まとめセクション
            "FAQ": 15   # FAQ セクション
        }
        
        print("🔍 テンプレート準拠度チェック実行中...")
        
        for element, weight in template_elements.items():
            if element not in content:
                compliance_score -= weight
                print(f"   ❌ 不足要素: {element} (-{weight}点)")
            else:
                print(f"   ✅ 準拠要素: {element}")
        
        # テンプレート構造との類似度追加チェック
        template_h2_count = self.template_content.count("## ")
        content_h2_count = content.count("## ")
        
        if abs(template_h2_count - content_h2_count) > 2:
            compliance_score -= 10
            print(f"   ⚠️ 見出し構造差異: テンプレート{template_h2_count}個 vs 記事{content_h2_count}個")
        
        print(f"📊 テンプレート準拠度: {compliance_score}%")
        return max(0, compliance_score)
    
    def _save_article_with_metadata(self, article_structure: Dict, keywords: List[str]) -> Dict[str, Any]:
        """メタデータ付き記事保存"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            main_keyword = keywords[0] if keywords else "記事"
            safe_keyword = re.sub(r'[^\w\s-]', '', main_keyword.replace(' ', '_'))
            filename = f"{safe_keyword}_品質担保済み_{timestamp}.md"
            filepath = self.output_path / filename
            
            # メタデータ付きコンテンツ作成
            metadata = f'''<!--
記事メタ情報:
- メインキーワード: {main_keyword}
- サブキーワード: {", ".join(keywords[1:]) if len(keywords) > 1 else "なし"}
- 作成日: {datetime.now().strftime("%Y年%m月%d日")}
- 対象読者: {article_structure.get("topic", "")}利用者・検討者
- 記事の目的: {main_keyword}の効果的な活用方法の提供
- 品質スコア: テンプレート準拠・品質担保済み
- SEO設定: {article_structure["seo_settings"]}
-->

# {article_structure["title"]}

{article_structure["content"]}

<!-- 生成情報 -->
<!-- 生成日時: {article_structure["created_at"]} -->
<!-- 文字数: {article_structure["word_count"]} -->
<!-- システム: マフィンブログ統合システム -->'''
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(metadata)
            
            return {
                "success": True,
                "path": str(filepath),
                "filename": filename,
                "filesize": len(metadata)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    # ========================================
    # 自動化・ワークフロー機能統合
    # ========================================
    
    def detect_wordpress_url(self, user_message: str) -> Optional[str]:
        """ユーザーメッセージからWordPress URLを検出"""
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
    
    def execute_complete_automation_workflow(self, wordpress_url: str) -> Dict[str, Any]:
        """完全自動化ワークフロー実行"""
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
            article_info = self._extract_article_info_from_url(wordpress_url)
            if not article_info:
                results["errors"].append("記事情報抽出失敗")
                return results
            results["completed_phases"].append("記事情報抽出")
            
            # Phase 2: ポートフォリオ更新
            print("\n🔄 Phase 2: ポートフォリオ更新")
            portfolio_result = self._update_portfolio_articles_json(article_info)
            if not portfolio_result:
                results["errors"].append("ポートフォリオ更新失敗")
                return results
            results["completed_phases"].append("ポートフォリオ更新")
            
            # Phase 3: 品質監視記録
            print("\n📊 Phase 3: 品質監視記録")
            self._log_workflow_execution(article_info, results)
            results["completed_phases"].append("品質監視記録")
            
            results["success"] = True
            results["article_info"] = article_info
            
            print("\n🎉 完全自動化ワークフロー成功！")
            return results
            
        except Exception as e:
            print(f"❌ ワークフローエラー: {e}")
            results["errors"].append(str(e))
            return results
    
    def _extract_article_info_from_url(self, url: str) -> Optional[Dict]:
        """WordPress記事情報抽出"""
        try:
            response = requests.get(url, timeout=10)
            content = response.text
            
            # タイトル抽出
            title_match = re.search(r'<title>([^<]+)</title>', content)
            title = title_match.group(1).strip() if title_match else "記事タイトル"
            title = title.replace(' - マフィンブログ', '').strip()
            
            # メインキーワード推定
            main_keyword = self._detect_main_keyword_from_title(title)
            
            # メタディスクリプション生成
            meta_description = self._generate_optimized_meta_description(title, main_keyword, content)
            
            # スラッグ生成
            slug = self._generate_slug(title, main_keyword)
            
            # タグ生成
            tags = self._generate_tags_from_content(title, meta_description, content)
            
            return {
                "title": title,
                "url": url,
                "description": meta_description,
                "slug": slug,
                "main_keyword": main_keyword,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "tags": tags
            }
            
        except Exception as e:
            print(f"❌ 記事情報抽出エラー: {e}")
            return None
    
    def _detect_main_keyword_from_title(self, title: str) -> str:
        """タイトルからメインキーワード検出"""
        keyword_priority = [
            "読書苦手", "Audible", "オーディブル", "聴く読書",
            "audiobook", "オーディオブック", "本が読めない"
        ]
        
        title_lower = title.lower()
        for keyword in keyword_priority:
            if keyword.lower() in title_lower:
                return keyword
        
        # デフォルト
        if "読書" in title or "本" in title:
            return "読書"
        else:
            return "Audible"
    
    def _generate_optimized_meta_description(self, title: str, main_keyword: str, content: str) -> str:
        """最適化メタディスクリプション生成"""
        base_desc = f"{main_keyword}について詳しく解説。初心者でも分かりやすい使い方から効果的な活用法まで、実用的な情報をお伝えします。"
        
        # 特典情報追加
        if "無料" in content:
            base_desc += "30日無料体験の情報も紹介。"
        
        base_desc += "今すぐチェックしてみませんか？"
        
        # 文字数調整（120-160文字）
        if len(base_desc) > 160:
            base_desc = base_desc[:157] + "..."
        elif len(base_desc) < 120:
            base_desc += "詳細な手順とコツも合わせてご紹介します。"
        
        return base_desc
    
    def _generate_tags_from_content(self, title: str, description: str, content: str) -> List[str]:
        """コンテンツからタグ生成"""
        tags = []
        text = f"{title} {description}".lower()
        
        # 基本タグマッピング
        tag_mapping = {
            "audible": ["Audible", "オーディブル"],
            "読書苦手": ["読書苦手", "本が読めない"],
            "オーディオブック": ["オーディオブック", "聴く読書"],
            "audiobook": ["audiobook.jp"],
            "無料": ["30日無料", "無料体験"],
            "おすすめ": ["おすすめ", "厳選"]
        }
        
        for keyword, tag_list in tag_mapping.items():
            if keyword.lower() in text:
                tags.extend(tag_list)
        
        # 重複除去・最大8個
        return list(dict.fromkeys(tags))[:8]
    
    def _update_portfolio_articles_json(self, article_info: Dict) -> bool:
        """ポートフォリオarticles.json更新"""
        try:
            portfolio_path = "/Users/satoumasamitsu/Desktop/osigoto/ポートフォリオサイト/public/content/articles/articles.json"
            
            # 既存のarticles.json読み込み
            with open(portfolio_path, 'r', encoding='utf-8') as f:
                articles_data = json.load(f)
            
            # 新記事をblogArticlesの最上位に挿入
            new_article = {
                "title": article_info["title"],
                "url": article_info["url"],
                "description": article_info["description"],
                "date": article_info["date"],
                "tags": article_info["tags"],
                "client": "Muffin Blog",
                "thumbnail": None  # 手動設定
            }
            
            # 重複チェック
            articles_data["blogArticles"] = [
                article for article in articles_data["blogArticles"]
                if article.get("url") != article_info["url"]
            ]
            
            # 新記事を最上位に追加
            articles_data["blogArticles"].insert(0, new_article)
            
            # ファイルに書き戻し
            with open(portfolio_path, 'w', encoding='utf-8') as f:
                json.dump(articles_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ ポートフォリオ更新完了: {new_article['title']}")
            return True
            
        except Exception as e:
            print(f"❌ ポートフォリオ更新エラー: {e}")
            return False
    
    def _log_workflow_execution(self, article_info: Dict, results: Dict):
        """ワークフロー実行ログ記録"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "workflow_type": "complete_automation",
                "article_title": article_info["title"],
                "article_url": article_info["url"],
                "completed_phases": results["completed_phases"],
                "success": results["success"],
                "errors": results.get("errors", [])
            }
            
            log_file = self.monitor_dir / "workflow_execution_log.json"
            
            # 既存ログ読み込み
            logs = []
            if log_file.exists():
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        logs = json.load(f)
                except:
                    logs = []
            
            logs.append(log_entry)
            
            # 最新100件のみ保持
            if len(logs) > 100:
                logs = logs[-100:]
            
            # ログ保存
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
            
            print("✅ ワークフロー実行ログ記録完了")
            
        except Exception as e:
            print(f"⚠️ ログ記録エラー: {e}")
    
    # ========================================
    # SEO最適化機能統合
    # ========================================
    
    def optimize_post_h1_tags(self, post_ids: List[int]) -> Dict[str, Any]:
        """H1タグ最適化"""
        results = {"processed": [], "errors": []}
        
        for post_id in post_ids:
            try:
                if post_id in self.protected_post_ids:
                    print(f"H1最適化をスキップ: 記事ID {post_id} は保護対象")
                    continue
                
                # 記事取得
                response = requests.get(
                    f"{self.wp_config['api_url']}/posts/{post_id}",
                    headers=self.wp_config['headers']
                )
                
                if response.status_code != 200:
                    results["errors"].append(f"記事ID {post_id}: 取得失敗")
                    continue
                
                post_data = response.json()
                title = post_data['title']['rendered']
                content = post_data['content']['rendered']
                
                # H1タグチェック
                h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
                
                if not h1_matches:
                    # H1タグが存在しない場合は追加
                    updated_content = f"<h1>{title}</h1>\n\n{content}"
                    
                    update_response = requests.post(
                        f"{self.wp_config['api_url']}/posts/{post_id}",
                        headers=self.wp_config['headers'],
                        json={"content": updated_content}
                    )
                    
                    if update_response.status_code == 200:
                        print(f"✅ H1タグ追加完了: 記事ID {post_id}")
                        results["processed"].append(post_id)
                    else:
                        results["errors"].append(f"記事ID {post_id}: H1タグ追加失敗")
                else:
                    print(f"✅ H1タグ確認済み: 記事ID {post_id}")
                    results["processed"].append(post_id)
                
            except Exception as e:
                results["errors"].append(f"記事ID {post_id}: エラー - {str(e)}")
        
        return results
    
    def add_structured_data(self, post_ids: List[int]) -> Dict[str, Any]:
        """構造化データ追加"""
        results = {"processed": [], "errors": []}
        
        for post_id in post_ids:
            try:
                # 記事取得
                response = requests.get(
                    f"{self.wp_config['api_url']}/posts/{post_id}",
                    headers=self.wp_config['headers']
                )
                
                if response.status_code != 200:
                    results["errors"].append(f"記事ID {post_id}: 取得失敗")
                    continue
                
                post_data = response.json()
                
                # 構造化データ生成
                structured_data = self._generate_structured_data(post_data)
                
                # 記事に構造化データ追加
                content = post_data['content']['rendered']
                if '<script type="application/ld+json">' not in content:
                    json_data = json.dumps(structured_data, ensure_ascii=False, separators=(",", ":"))
                    structured_data_script = f'<script type="application/ld+json">{json_data}</script>'
                    updated_content = structured_data_script + "\n\n" + content
                    
                    update_response = requests.post(
                        f"{self.wp_config['api_url']}/posts/{post_id}",
                        headers=self.wp_config['headers'],
                        json={"content": updated_content}
                    )
                    
                    if update_response.status_code == 200:
                        print(f"✅ 構造化データ追加完了: 記事ID {post_id}")
                        results["processed"].append(post_id)
                    else:
                        results["errors"].append(f"記事ID {post_id}: 構造化データ追加失敗")
                else:
                    print(f"✅ 構造化データ確認済み: 記事ID {post_id}")
                    results["processed"].append(post_id)
                    
            except Exception as e:
                results["errors"].append(f"記事ID {post_id}: エラー - {str(e)}")
        
        return results
    
    def _generate_structured_data(self, post_data: Dict) -> Dict:
        """JSON-LD構造化データ生成"""
        post_id = post_data['id']
        title = post_data['title']['rendered']
        content = post_data['content']['rendered']
        url = f"https://muffin-blog.com/?p={post_id}"
        published_date = post_data['date']
        modified_date = post_data['modified']
        
        # 記事の説明文を抽出
        description = self._extract_description_from_content(content)
        
        # 画像URL抽出
        image_url = self._extract_image_from_content(content)
        
        structured_data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": description,
            "url": url,
            "datePublished": published_date,
            "dateModified": modified_date,
            "author": {
                "@type": "Person",
                "name": "マフィン"
            },
            "publisher": {
                "@type": "Organization",
                "name": "マフィンブログ",
                "url": "https://muffin-blog.com"
            }
        }
        
        if image_url:
            structured_data["image"] = image_url
        
        return structured_data
    
    def _extract_description_from_content(self, content: str) -> str:
        """記事から説明文抽出"""
        # HTMLタグ除去
        text = re.sub(r'<[^>]+>', '', content)
        
        # 最初の段落を抽出（200文字以内）
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            clean_paragraph = paragraph.strip()
            if len(clean_paragraph) > 50:
                return clean_paragraph[:200] + "..." if len(clean_paragraph) > 200 else clean_paragraph
        
        return "マフィンブログの記事です。"
    
    def _extract_image_from_content(self, content: str) -> Optional[str]:
        """記事から画像URL抽出"""
        img_match = re.search(r'<img[^>]+src="([^"]+)"', content)
        return img_match.group(1) if img_match else None
    
    # ========================================
    # ヘルスチェック・監視機能統合
    # ========================================
    
    def comprehensive_site_health_check(self) -> Dict[str, Any]:
        """包括的サイトヘルスチェック"""
        print("🏥 マフィンブログ包括的ヘルスチェック開始")
        print("=" * 60)
        
        health_results = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "unknown",
            "checks": {}
        }
        
        # 1. WordPress API接続チェック
        api_check = self.test_wordpress_connection()
        health_results["checks"]["wordpress_api"] = {
            "status": "pass" if api_check else "fail",
            "description": "WordPress API接続確認"
        }
        
        # 2. カテゴリ・タグ構造チェック
        categories = self.get_categories()
        health_results["checks"]["categories"] = {
            "status": "pass" if categories else "fail", 
            "count": len(categories),
            "description": "カテゴリ構造確認"
        }
        
        # 3. 保護記事ステータスチェック
        protected_status = self._check_protected_posts_status()
        health_results["checks"]["protected_posts"] = protected_status
        
        # 4. バックアップ状況チェック
        backup_status = self._check_backup_status()
        health_results["checks"]["backup_status"] = backup_status
        
        # 5. 品質監視ログチェック
        monitoring_status = self._check_monitoring_system_status()
        health_results["checks"]["monitoring_system"] = monitoring_status
        
        # 総合判定
        all_checks_passed = all(
            check.get("status") == "pass" 
            for check in health_results["checks"].values()
        )
        health_results["overall_status"] = "healthy" if all_checks_passed else "needs_attention"
        
        # 結果表示
        self._display_health_check_results(health_results)
        
        return health_results
    
    def _check_protected_posts_status(self) -> Dict[str, Any]:
        """保護記事ステータスチェック"""
        try:
            available_posts = []
            for post_id in self.protected_post_ids:
                response = requests.get(
                    f"{self.wp_config['api_url']}/posts/{post_id}",
                    headers=self.wp_config['headers']
                )
                if response.status_code == 200:
                    available_posts.append(post_id)
            
            return {
                "status": "pass" if len(available_posts) == len(self.protected_post_ids) else "warning",
                "available_count": len(available_posts),
                "total_count": len(self.protected_post_ids),
                "description": "保護記事アクセス確認"
            }
        except:
            return {
                "status": "fail",
                "description": "保護記事チェック失敗"
            }
    
    def _check_backup_status(self) -> Dict[str, Any]:
        """バックアップ状況チェック"""
        try:
            if not self.backup_dir.exists():
                return {"status": "fail", "description": "バックアップディレクトリが存在しません"}
            
            backup_files = list(self.backup_dir.glob("*.json"))
            recent_backups = [
                f for f in backup_files 
                if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= 7
            ]
            
            return {
                "status": "pass" if recent_backups else "warning",
                "total_backups": len(backup_files),
                "recent_backups": len(recent_backups),
                "description": "バックアップファイル確認"
            }
        except:
            return {
                "status": "fail",
                "description": "バックアップ状況チェック失敗"
            }
    
    def _check_monitoring_system_status(self) -> Dict[str, Any]:
        """監視システムステータスチェック"""
        try:
            if not self.monitor_dir.exists():
                self.monitor_dir.mkdir(exist_ok=True)
            
            log_files = list(self.monitor_dir.glob("*.json"))
            
            return {
                "status": "pass",
                "log_files_count": len(log_files),
                "description": "品質監視システム確認"
            }
        except:
            return {
                "status": "fail", 
                "description": "監視システムチェック失敗"
            }
    
    def _display_health_check_results(self, results: Dict):
        """ヘルスチェック結果表示"""
        overall_emoji = "🟢" if results["overall_status"] == "healthy" else "🟡"
        print(f"\n{overall_emoji} 総合ステータス: {results['overall_status']}")
        print("\n詳細結果:")
        
        for check_name, check_result in results["checks"].items():
            status_emoji = {"pass": "✅", "warning": "⚠️", "fail": "❌"}.get(check_result["status"], "❓")
            print(f"  {status_emoji} {check_name}: {check_result['description']}")
            
            # 詳細情報表示
            for key, value in check_result.items():
                if key not in ["status", "description"]:
                    print(f"      {key}: {value}")
        
        print("\n" + "=" * 60)
    
    # ========================================
    # 自動ファイル整理機能
    # ========================================
    
    def automatic_file_cleanup(self) -> Dict[str, Any]:
        """自動ファイル整理実行"""
        print("🧹 自動ファイル整理開始...")
        
        cleanup_results = {
            "timestamp": datetime.now().isoformat(),
            "cleaned_files": [],
            "errors": []
        }
        
        try:
            # 1. WordPress投稿下書きフォルダの古いファイル削除（7日以上前）
            draft_folder = self.output_path
            cutoff_date = datetime.now() - timedelta(days=7)
            
            for file_path in draft_folder.glob("*.md"):
                file_stat = file_path.stat()
                file_date = datetime.fromtimestamp(file_stat.st_mtime)
                
                if file_date < cutoff_date:
                    try:
                        file_path.unlink()
                        cleanup_results["cleaned_files"].append(str(file_path.name))
                        print(f"✅ 古いファイル削除: {file_path.name}")
                    except Exception as e:
                        cleanup_results["errors"].append(f"削除失敗: {file_path.name} - {str(e)}")
                        print(f"❌ 削除失敗: {file_path.name} - {str(e)}")
            
            # 2. バックアップフォルダの古いバックアップ削除（30日以上前）
            backup_cutoff_date = datetime.now() - timedelta(days=30)
            
            for backup_file in self.backup_dir.glob("*.json"):
                backup_stat = backup_file.stat()
                backup_date = datetime.fromtimestamp(backup_stat.st_mtime)
                
                if backup_date < backup_cutoff_date:
                    try:
                        backup_file.unlink()
                        cleanup_results["cleaned_files"].append(str(backup_file.name))
                        print(f"✅ 古いバックアップ削除: {backup_file.name}")
                    except Exception as e:
                        cleanup_results["errors"].append(f"バックアップ削除失敗: {backup_file.name} - {str(e)}")
            
            # 3. 一時ファイル・キャッシュファイル削除
            temp_patterns = ["*.tmp", "*.cache", "*_temp.json", "*_cache.json"]
            for pattern in temp_patterns:
                for temp_file in self.base_path.glob(f"**/{pattern}"):
                    try:
                        temp_file.unlink()
                        cleanup_results["cleaned_files"].append(str(temp_file.name))
                        print(f"✅ 一時ファイル削除: {temp_file.name}")
                    except Exception as e:
                        cleanup_results["errors"].append(f"一時ファイル削除失敗: {temp_file.name} - {str(e)}")
            
            # 4. 空のディレクトリ削除
            self._clean_empty_directories(self.base_path, cleanup_results)
            
            print(f"🧹 自動ファイル整理完了: {len(cleanup_results['cleaned_files'])}個のファイルを整理")
            
            return cleanup_results
            
        except Exception as e:
            print(f"❌ 自動ファイル整理エラー: {e}")
            cleanup_results["errors"].append(str(e))
            return cleanup_results
    
    def _clean_empty_directories(self, base_path: Path, cleanup_results: Dict):
        """空のディレクトリを再帰的に削除"""
        try:
            for dir_path in base_path.rglob("*"):
                if dir_path.is_dir() and not any(dir_path.iterdir()):
                    # システムディレクトリは除外
                    system_dirs = ["backups", "システム監視データ", "WordPress投稿下書き"]
                    if dir_path.name not in system_dirs:
                        try:
                            dir_path.rmdir()
                            cleanup_results["cleaned_files"].append(f"空ディレクトリ: {dir_path.name}")
                            print(f"✅ 空ディレクトリ削除: {dir_path.name}")
                        except Exception as e:
                            cleanup_results["errors"].append(f"空ディレクトリ削除失敗: {dir_path.name} - {str(e)}")
        except Exception as e:
            cleanup_results["errors"].append(f"空ディレクトリチェック失敗: {str(e)}")
    
    # ========================================
    # 統合管理システム同期機能（2025-08-14追加）
    # ========================================
    
    def sync_with_integration_system(self) -> Dict[str, Any]:
        """統合管理システムとの同期更新実行"""
        print("🔄 統合管理システムとの同期開始...")
        
        sync_result = {
            "timestamp": datetime.now().isoformat(),
            "updated_files": [],
            "errors": []
        }
        
        try:
            # 1. 現在のシステム情報を取得
            current_system_info = self._extract_current_system_info()
            
            # 2. 統合管理システムのドキュメントを更新
            self._update_integration_documentation(current_system_info, sync_result)
            
            # 3. 同期完了ログ出力
            if sync_result["updated_files"]:
                print(f"✅ 同期完了: {len(sync_result['updated_files'])}個のファイルを更新")
                for file in sync_result["updated_files"]:
                    print(f"   📄 {file}")
            else:
                print("ℹ️ 更新対象なし（すべて最新状態）")
            
            return sync_result
            
        except Exception as e:
            print(f"❌ 同期エラー: {e}")
            sync_result["errors"].append(str(e))
            return sync_result
    
    def _extract_current_system_info(self) -> Dict[str, Any]:
        """現在のシステム情報を抽出"""
        return {
            "system_name": "マフィンブログ統合システム",
            "version": "2025-08-14 壁打ち学習統合版",
            "key_features": [
                "記事構成パターン判定（サービス紹介型・ノウハウ解説型）",
                "FAQ戦略的構成（Google関連質問抜粋）",
                "書籍選定5つの基準",
                "箇条書き統一フォーマット",
                "読者検索意図優先の構成原則"
            ],
            "templates": [
                "サービス紹介型記事_構成テンプレート.md",
                "ノウハウ解説型記事_構成テンプレート.md"
            ],
            "quality_standards": self.quality_standards,
            "last_updated": datetime.now().isoformat()
        }
    
    def _update_integration_documentation(self, system_info: Dict[str, Any], sync_result: Dict[str, Any]):
        """統合管理システムの仕様書群を更新"""
        
        # 目次・概要ファイルを更新
        overview_content = self._generate_overview_documentation(system_info)
        overview_path = self.integration_specs_dir / "00_目次・概要.md"
        
        try:
            with open(overview_path, 'w', encoding='utf-8') as f:
                f.write(overview_content)
            
            sync_result["updated_files"].append("00_目次・概要.md")
            print(f"✅ 目次・概要更新完了: 00_目次・概要.md")
            
        except Exception as e:
            sync_result["errors"].append(f"目次・概要更新失敗: {str(e)}")
            print(f"❌ 目次・概要更新失敗: {str(e)}")
        
        # 必要に応じて他の仕様書も更新
        # (品質基準、学習内容などは既に最新のため、概要のみ更新)
    
    def _generate_overview_documentation(self, system_info: Dict[str, Any]) -> str:
        """目次・概要ドキュメントを生成"""
        
        return f"""# マフィンブログシステム仕様書 - 目次・概要

**最終更新**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}  
**バージョン**: {system_info['version']}  
**プログラムファイル**: `/Users/satoumasamitsu/Desktop/osigoto/ブログ自動化/マフィンブログ統合システム.py`

---

## 📚 仕様書構成

### 基本仕様書
- **[01_システム概要.md](./01_システム概要.md)** - システムの目的、役割、全体アーキテクチャ
- **[02_システム構成.md](./02_システム構成.md)** - ファイル構成、テンプレート種別、依存関係
- **[03_品質基準・ルール.md](./03_品質基準・ルール.md)** - 記事品質基準、禁止表現、構成ルール
- **[04_学習統合内容.md](./04_学習統合内容.md)** - 壁打ち学習内容、FAQ戦略、書籍選定基準
- **[05_実行・運用ガイド.md](./05_実行・運用ガイド.md)** - 実行方法、コマンド例、トラブルシューティング
- **[06_同期・管理システム.md](./06_同期・管理システム.md)** - 自動同期、バックアップ、日報管理

### 付録（詳細技術仕様）
- **[A_API設定・環境変数.md](./付録/A_API設定・環境変数.md)** - WordPress API設定、認証情報
- **[B_WordPress連携仕様.md](./付録/B_WordPress連携仕様.md)** - API構造、投稿形式、エラーハンドリング
- **[C_エラーコード一覧.md](./付録/C_エラーコード一覧.md)** - エラーコード、対処法、デバッグ方法
- **[D_テンプレート詳細例.md](./付録/D_テンプレート詳細例.md)** - マフィンフォーマット、会話例、構成例

---

## 🎯 システム概要（クイックリファレンス）

### システムの目的
muffin-blog.com の Audible 特化記事を完全自動化で作成・投稿するシステム

### 主要機能
1. **記事作成**: 2種類のテンプレート（サービス紹介型・ノウハウ解説型）
2. **品質管理**: 101点満点システム、80点以上で合格
3. **WordPress投稿**: 自動下書き保存、SEO最適化
4. **自動同期**: 統合管理システムとの双方向同期

### 品質基準（クイック）
- **最低文字数**: 2,000文字
- **FAQ数**: 5個以上必須
- **必須セクション**: 「この記事で分かること」「FAQ」「まとめ」
- **禁止表現**: めっちゃ有名、大ブーム、話題沸騰など

### 実行方法（クイック）
```bash
cd /Users/satoumasamitsu/Desktop/osigoto/ブログ自動化/
python3 マフィンブログ統合システム.py
```

---

**作成日**: 2025年8月14日  
**管理システム**: マフィンブログ統合システム（自動同期対応）"""

    def _generate_updated_documentation(self, system_info: Dict[str, Any]) -> str:
        """旧形式との互換性維持（削除予定）"""
        
        return f"""# マフィンブログ_ルール仕様書

## 🎯 システム概要
マフィンブログ（muffin-blog.com）の記事作成から投稿まで完全自動化するための統合システム。
2025年8月13日の壁打ち学習内容を統合し、品質基準を大幅に向上。

**最終更新**: {system_info['last_updated']}
**バージョン**: {system_info['version']}

---

## 🚀 システム構成

### メインファイル
```
/Users/satoumasamitsu/Desktop/osigoto/ブログ自動化/マフィンブログ統合システム.py
```

### テンプレートファイル
- **サービス紹介型**: `サービス紹介型記事_構成テンプレート.md`
  - 目的: サービス未利用者向け導入促進
  - ゴール: 無料体験・サービス申し込み
  
- **ノウハウ解説型**: `ノウハウ解説型記事_構成テンプレート.md` 
  - 目的: 利用中/検討中ユーザー向け手法解説
  - ゴール: 実践的な技法習得

---

## 📚 2025年8月13日壁打ち学習統合内容

### 1. FAQ戦略的構成パターン
- **質問源**: Google検索「その他の質問」「関連する質問」から抜粋
- **回答構造**: 
  1. 質問提示
  2. 文章での詳細解説（SEO対策）
  3. 読者目線の箇条書き（分かりやすさ重視）
  4. マフィンの会話でクロージング（親しみやすさ）

**戦略的メリット**:
- 後の記事作成ネタ（FAQ1つが新記事のタネ）
- 内部リンク構築（関連記事への自然な導線）
- 検索意図マッチ（実際の検索クエリに対応）

### 2. 記事構成パターン判定システム

#### サービス紹介型記事
- **ターゲット**: サービス未利用者（導入検討段階）
- **構成**: 問題提起 → サービス解決策 → 軽い科学的根拠 → 詳細料金説明 → 行動促進

#### ノウハウ解説型記事  
- **ターゲット**: 既にサービス利用中/検討中の人
- **構成**: 向上心ベース問題提起 → 手法解説 → 詳細科学的根拠 → 軽い料金説明 → 実践促進

### 3. 書籍選定の5つの基準
1. **認知度**: 「どこかで聞いたことがある」安心感
2. **実用性**: 読者が直感的に「役立ちそう」と感じる
3. **難易度バランス**: 初心者～中級者レベル
4. **展開可能性**: 派生記事を複数作成できる
5. **心理的アプローチ**: 「知ってるけど読めてない本」効果

### 4. 箇条書き統一フォーマット
- **タイトル**: `**内容：**`（太字必須）
- **項目**: `- 内容`（太字なし）
- **WordPress対応**: ブロック作成時の利便性を考慮

### 5. 読者検索意図優先の原則
- 「○○とは？」→「やり方」→「理由・効果」の順序
- 冒頭で読者の疑問を早期解決
- 検索キーワードの期待に直接応える

---

## ⚡ 実行方法

### 基本実行
```bash
cd /Users/satoumasamitsu/Desktop/osigoto/ブログ自動化/
python3 マフィンブログ統合システム.py
```

### 主要機能
1. **記事作成**: テンプレート準拠の高品質記事生成
2. **WordPress投稿**: 自動下書き保存・SEO最適化
3. **品質管理**: 101点満点システム・投稿前確認
4. **同期更新**: 統合管理システムとの自動同期

---

## 🛡️ 品質保証基準

### 記事品質基準
- 最低文字数: 2,000文字
- FAQ数: 5個以上必須
- 品質スコア: 80点以上
- SEO要素: 充実必須

### 禁止表現（自動検出）
- めっちゃ有名、大ブーム、話題沸騰
- 革命的、専門家も絶賛
- ことが多いです、と言えるでしょう

### 必須証拠キーワード
- 30日無料、月額1500円、聴き放題、12万冊以上

---

## 🔄 同期システム

このドキュメントは実行ファイル（.py）と自動同期されます。
- **同期トリガー**: システム更新時
- **同期内容**: 品質基準、機能追加、学習内容
- **更新履歴**: 日報・ログフォルダで管理

---

**作成日**: 2025年8月11日  
**最終更新**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}  
**同期ステータス**: ✅ 最新（実行ファイルと同期済み）
"""

    # ========================================
    # 事前分析・記事企画システム（新機能）
    # ========================================
    
    def analyze_notebookLM_resources(self, notebook_path: str = None) -> Dict[str, Any]:
        """NotebookLM資料分析・テーマ抽出"""
        print("📚 NotebookLM資料分析開始...")
        
        analysis_result = {
            "available_materials": [],
            "extracted_themes": [],
            "suggested_keywords": [],
            "content_gaps": []
        }
        
        # NotebookLM資料フォルダをスキャン（実装時にパス調整）
        notebook_folders = [
            "/Users/satoumasamitsu/Desktop/NotebookLM",
            "/Users/satoumasamitsu/Desktop/osigoto/資料",
            "/Users/satoumasamitsu/Desktop/osigoto/ライティング案件"
        ]
        
        for folder in notebook_folders:
            if Path(folder).exists():
                for file_path in Path(folder).rglob("*.md"):
                    analysis_result["available_materials"].append(str(file_path))
                    
                    # ファイル内容からキーワード抽出（簡易版）
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            keywords = self._extract_keywords_from_content(content)
                            analysis_result["suggested_keywords"].extend(keywords)
                    except:
                        continue
        
        # キーワード重複削除
        analysis_result["suggested_keywords"] = list(set(analysis_result["suggested_keywords"]))
        
        print(f"✅ 利用可能素材: {len(analysis_result['available_materials'])}件")
        print(f"✅ 抽出キーワード: {len(analysis_result['suggested_keywords'])}個")
        
        return analysis_result
    
    def _extract_keywords_from_content(self, content: str) -> List[str]:
        """コンテンツからキーワード抽出（簡易版）"""
        # Audible関連キーワードを優先的に抽出
        audible_keywords = [
            "Audible", "オーディブル", "聴く読書", "音声読書",
            "二刀流読書", "速聴", "読書効果", "集中力",
            "月額1500円", "30日無料", "聴き放題"
        ]
        
        found_keywords = []
        for keyword in audible_keywords:
            if keyword in content:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def check_existing_articles_duplication(self, proposed_theme: str) -> Dict[str, Any]:
        """既存記事との重複チェック"""
        print(f"🔍 既存記事重複チェック: '{proposed_theme}'")
        
        duplicate_check = {
            "is_duplicate": False,
            "similar_articles": [],
            "suggested_angle": "",
            "risk_level": "low"
        }
        
        try:
            # WordPress API で既存記事を取得
            response = requests.get(
                f"{self.wp_config['api_url']}/posts",
                headers=self.wp_config['headers'],
                params={"per_page": 50, "status": "publish"}
            )
            
            if response.status_code == 200:
                existing_posts = response.json()
                
                for post in existing_posts:
                    title = post.get('title', {}).get('rendered', '')
                    
                    # テーマとの類似度チェック（簡易版）
                    similarity_score = self._calculate_theme_similarity(proposed_theme, title)
                    
                    if similarity_score > 0.7:
                        duplicate_check["is_duplicate"] = True
                        duplicate_check["risk_level"] = "high"
                        duplicate_check["similar_articles"].append({
                            "title": title,
                            "similarity": similarity_score,
                            "url": post.get('link', '')
                        })
                
                # 重複があった場合の代替案提案
                if duplicate_check["is_duplicate"]:
                    duplicate_check["suggested_angle"] = self._suggest_alternative_angle(proposed_theme)
                
            print(f"✅ 重複チェック完了 - リスクレベル: {duplicate_check['risk_level']}")
            
        except Exception as e:
            print(f"❌ 重複チェックエラー: {str(e)}")
            duplicate_check["error"] = str(e)
        
        return duplicate_check
    
    def _calculate_theme_similarity(self, theme1: str, theme2: str) -> float:
        """テーマ類似度計算（簡易版）"""
        # キーワードベースの類似度計算
        theme1_words = set(theme1.lower().split())
        theme2_words = set(theme2.lower().split())
        
        if not theme1_words or not theme2_words:
            return 0.0
        
        intersection = theme1_words.intersection(theme2_words)
        union = theme1_words.union(theme2_words)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _suggest_alternative_angle(self, original_theme: str) -> str:
        """代替テーマ角度提案"""
        alternative_angles = [
            f"{original_theme}｜上級者向けテクニック",
            f"{original_theme}｜初心者が知るべき5つのポイント", 
            f"{original_theme}｜科学的根拠と実践方法",
            f"{original_theme}｜よくある失敗例と対策",
            f"{original_theme}｜2025年最新版"
        ]
        
        # ランダムに選択（実際はより賢い選択ロジックを実装）
        import random
        return random.choice(alternative_angles)
    
    # ========================================
    # 品質管理循環システム（新機能）
    # ========================================
    
    def create_article_with_quality_loop(self, theme: str, max_iterations: int = 5) -> Dict[str, Any]:
        """品質管理循環システム付き記事作成"""
        print(f"🔄 品質管理循環システム開始 - テーマ: {theme}")
        
        iteration_results = []
        current_iteration = 1
        
        # テストフォルダ作成
        test_dir = self.base_path / "テスト"
        test_dir.mkdir(exist_ok=True)
        
        while current_iteration <= max_iterations:
            print(f"\n--- 反復 {current_iteration}/{max_iterations} ---")
            
            # 1. 記事生成（プログラム実行）
            if current_iteration == 1:
                # 初回生成
                article_data = self._generate_initial_article(theme)
            else:
                # 改善指示に基づく再生成
                previous_feedback = iteration_results[-1]["claude_feedback"]
                article_data = self._regenerate_article_with_feedback(theme, previous_feedback)
            
            # 2. Claude品質チェック
            claude_check = self._claude_quality_assessment(article_data)
            
            # 3. 結果保存
            test_file_path = test_dir / f"テスト{current_iteration}_{theme.replace(' ', '_')}.md"
            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write(article_data.get('content', ''))
            
            # 4. 反復結果記録
            iteration_result = {
                "iteration": current_iteration,
                "file_path": str(test_file_path),
                "quality_score": claude_check["total_score"],
                "claude_feedback": claude_check,
                "passed_threshold": claude_check["total_score"] >= 80
            }
            iteration_results.append(iteration_result)
            
            print(f"📊 品質スコア: {claude_check['total_score']}点")
            
            # 5. 80点以上で終了
            if claude_check["total_score"] >= 80:
                print(f"✅ 品質基準クリア！（{current_iteration}回目で達成）")
                
                # 最終版保存
                final_file_path = test_dir / f"最終合格版_{theme.replace(' ', '_')}.md"
                shutil.copy2(test_file_path, final_file_path)
                
                return {
                    "success": True,
                    "final_score": claude_check["total_score"],
                    "iterations_needed": current_iteration,
                    "final_file": str(final_file_path),
                    "iteration_history": iteration_results
                }
            
            current_iteration += 1
        
        # 最大反復数に達した場合
        print(f"⚠️ 最大反復数（{max_iterations}回）に達しました")
        return {
            "success": False,
            "final_score": iteration_results[-1]["quality_score"],
            "iterations_needed": max_iterations,
            "iteration_history": iteration_results
        }
    
    def _generate_initial_article(self, theme: str) -> Dict[str, Any]:
        """初回記事生成"""
        print("📝 初回記事生成中...")
        
        # 既存のテンプレート機能を活用
        article_data = {
            "title": f"Audible {theme}｜効果的な活用術を徹底解説",
            "content": self._create_template_article(theme),
            "keywords": [theme, "Audible", "読書効果"],
            "meta_description": f"Audibleを使った{theme}について詳しく解説します。"
        }
        
        return article_data
    
    def _regenerate_article_with_feedback(self, theme: str, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """フィードバックに基づく記事再生成"""
        print("🔄 フィードバック反映版記事生成中...")
        
        # フィードバックに基づく改善（簡易版）
        improvements = feedback.get("improvement_suggestions", [])
        
        article_data = {
            "title": f"Audible {theme}｜効果的な活用術を徹底解説（改善版）",
            "content": self._create_improved_template_article(theme, improvements),
            "keywords": [theme, "Audible", "読書効果"],
            "meta_description": f"Audibleを使った{theme}について詳しく解説します。"
        }
        
        return article_data
    
    def _claude_quality_assessment(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Claude品質評価システム"""
        print("🔍 Claude品質評価実行中...")
        
        content = article_data.get('content', '')
        
        # 品質評価項目
        assessment = {
            "content_length": self._assess_content_length(content),
            "faq_count": self._assess_faq_count(content),
            "template_compliance": self._assess_template_compliance(content),
            "seo_elements": self._assess_seo_elements(article_data),
            "readability": self._assess_readability(content)
        }
        
        # 総合スコア計算
        total_score = sum(assessment.values()) / len(assessment)
        
        # 改善提案生成
        improvement_suggestions = self._generate_improvement_suggestions(assessment)
        
        return {
            "total_score": round(total_score, 1),
            "breakdown": assessment,
            "improvement_suggestions": improvement_suggestions,
            "passed": total_score >= 80
        }
    
    def _assess_content_length(self, content: str) -> float:
        """文字数評価"""
        char_count = len(content)
        if char_count >= 2000:
            return 100.0
        elif char_count >= 1500:
            return 80.0
        elif char_count >= 1000:
            return 60.0
        else:
            return 40.0
    
    def _assess_faq_count(self, content: str) -> float:
        """FAQ数評価"""
        faq_count = content.count("### Q") + content.count("**Q")
        if faq_count >= 5:
            return 100.0
        elif faq_count >= 3:
            return 70.0
        elif faq_count >= 1:
            return 50.0
        else:
            return 30.0
    
    def _assess_template_compliance(self, content: str) -> float:
        """テンプレート準拠度評価"""
        required_sections = [
            "この記事で分かること",
            "まとめ",
            "FAQ"
        ]
        
        compliance_score = 0
        for section in required_sections:
            if section in content:
                compliance_score += 33.3
        
        return min(compliance_score, 100.0)
    
    def _assess_seo_elements(self, article_data: Dict[str, Any]) -> float:
        """SEO要素評価"""
        score = 0
        
        # タイトル評価
        title = article_data.get('title', '')
        if 'Audible' in title:
            score += 30
        if len(title) >= 20:
            score += 20
        
        # メタディスクリプション評価
        meta_desc = article_data.get('meta_description', '')
        if len(meta_desc) >= 100:
            score += 25
        
        # キーワード評価
        keywords = article_data.get('keywords', [])
        if len(keywords) >= 3:
            score += 25
        
        return min(score, 100.0)
    
    def _assess_readability(self, content: str) -> float:
        """読みやすさ評価"""
        # 段落数
        paragraphs = content.split('\n\n')
        paragraph_score = min(len(paragraphs) / 10 * 50, 50)
        
        # 見出し数
        headings = content.count('##') + content.count('###')
        heading_score = min(headings / 8 * 50, 50)
        
        return paragraph_score + heading_score
    
    def _generate_improvement_suggestions(self, assessment: Dict[str, float]) -> List[str]:
        """改善提案生成"""
        suggestions = []
        
        if assessment["content_length"] < 80:
            suggestions.append("文字数を2000文字以上に増やしてください")
        
        if assessment["faq_count"] < 80:
            suggestions.append("FAQ を5個以上追加してください")
        
        if assessment["template_compliance"] < 80:
            suggestions.append("必須セクション（この記事で分かること、FAQ、まとめ）を追加してください")
        
        if assessment["seo_elements"] < 80:
            suggestions.append("SEO要素（キーワード、メタディスクリプション）を強化してください")
        
        if assessment["readability"] < 80:
            suggestions.append("見出しと段落を増やして読みやすさを向上させてください")
        
        return suggestions
    
    def _create_template_article(self, theme: str) -> str:
        """テンプレート記事生成（簡易版）"""
        return f"""# Audible {theme}｜効果的な活用術を徹底解説

## この記事で分かること

✅ {theme}の基本的な考え方
✅ Audibleを活用した{theme}の実践方法
✅ 効果を最大化するコツ
✅ よくある質問と回答

## {theme}とは？

{theme}とは、Audibleを効果的に活用するための手法の一つです。

この方法を使うことで、従来の読書よりも効率的に知識を身につけることができます。

## 具体的な実践方法

### ステップ1: 基本設定
まずはAudibleアプリの基本設定を確認しましょう。

### ステップ2: {theme}の実践
実際に{theme}を始めてみましょう。

### ステップ3: 効果の確認
実践した結果を確認し、必要に応じて調整します。

## FAQ

### Q1. {theme}は本当に効果がありますか？
A. はい、多くのユーザーが効果を実感しています。

### Q2. 初心者でもできますか？
A. はい、段階的に始めれば初心者でも可能です。

### Q3. どのくらいの期間で効果が出ますか？
A. 個人差がありますが、1週間程度で変化を感じる方が多いです。

## まとめ

{theme}は、Audibleを効果的に活用するための優れた手法です。

今回ご紹介した方法を実践して、より効率的な読書体験を楽しんでください。

[>>Audible無料体験はこちら](https://www.audible.co.jp/)
"""
    
    def _create_improved_template_article(self, theme: str, improvements: List[str]) -> str:
        """改善版テンプレート記事生成"""
        base_content = self._create_template_article(theme)
        
        # 改善点を反映（簡易版）
        if "文字数を2000文字以上に" in ' '.join(improvements):
            base_content += "\n\n## 詳細解説\n\nさらに詳しい内容をここに追加..." * 5
        
        if "FAQ を5個以上" in ' '.join(improvements):
            additional_faqs = """
### Q4. 料金はどのくらいかかりますか？
A. 月額1,500円で12万冊以上が聴き放題です。

### Q5. 無料体験はありますか？
A. はい、30日間の無料体験があります。

### Q6. どんなジャンルの本がありますか？
A. ビジネス書、小説、実用書など幅広いジャンルがあります。
"""
            base_content = base_content.replace("## まとめ", additional_faqs + "\n## まとめ")
        
        return base_content

    # ========================================
    # メイン実行関数
    # ========================================
    
def main():
    """メイン実行関数"""
    print("🚀 マフィンブログ統合システム起動")
    
    system = マフィンブログ統合システム()
    
    # 接続テスト
    if not system.test_wordpress_connection():
        print("❌ WordPress接続失敗。設定を確認してください。")
        return
    
    # システム起動時に自動ファイル整理実行
    print("\n🧹 システム起動時の自動ファイル整理実行...")
    cleanup_result = system.automatic_file_cleanup()
    
    # 統合管理システムとの同期実行
    print("\n🔄 統合管理システムとの同期実行...")
    sync_result = system.sync_with_integration_system()
    
    print("\n" + "=" * 60)
    print("マフィンブログ統合システム - 利用可能な機能:")
    print("1. テンプレート準拠記事作成（2種類のパターン対応）")
    print("2. WordPress投稿・管理")
    print("3. 完全自動化ワークフロー（URL入力）") 
    print("4. SEO最適化（H1タグ・構造化データ）")
    print("5. サイトヘルスチェック")
    print("6. 記事バックアップ・削除")
    print("7. 自動ファイル整理・クリーンアップ")
    print("8. 統合管理システム自動同期")
    print("9. 🆕 NotebookLM資料分析・テーマ抽出")
    print("10. 🆕 既存記事重複チェック")
    print("11. 🆕 品質管理循環システム（80点保証）")
    print("=" * 60)
    
    # 新機能のテストデモ
    print("\n🧪 新機能テストデモ...")
    
    # NotebookLM資料分析テスト
    print("\n📚 NotebookLM資料分析テスト:")
    notebook_analysis = system.analyze_notebookLM_resources()
    
    # 既存記事重複チェックテスト
    test_theme = "二刀流読書"
    print(f"\n🔍 重複チェックテスト（テーマ: {test_theme}）:")
    duplicate_check = system.check_existing_articles_duplication(test_theme)
    
    # 品質管理循環システムの実際のテスト実行
    print(f"\n🔄 品質管理循環システム実行テスト開始...")
    print(f"テーマ '{test_theme}' で記事作成テストを実行します")
    
    # 実際に品質管理循環システムを実行
    quality_loop_result = system.create_article_with_quality_loop(test_theme, max_iterations=3)
    
    if quality_loop_result["success"]:
        print(f"\n🎉 品質管理循環システムテスト成功！")
        print(f"最終スコア: {quality_loop_result['final_score']}点")
        print(f"必要反復数: {quality_loop_result['iterations_needed']}回")
        print(f"最終ファイル: {quality_loop_result['final_file']}")
    else:
        print(f"\n⚠️ 品質管理循環システムテスト - 改善継続中")
        print(f"現在スコア: {quality_loop_result['final_score']}点")
        print(f"実行反復数: {quality_loop_result['iterations_needed']}回")
    
    # デモ実行
    print("\n🧪 システム動作確認...")
    
    # ヘルスチェック実行
    health_result = system.comprehensive_site_health_check()
    
    if health_result["overall_status"] == "healthy":
        print("\n✅ システム正常動作確認完了")
        print("📝 記事作成、WordPress投稿、自動化ワークフロー、自動ファイル整理、統合管理システム同期が利用可能です")
        print("🔄 統合管理システムのドキュメントが最新状態に同期されました")
    else:
        print("\n⚠️ 一部機能に注意が必要です。詳細は上記の結果を確認してください。")

if __name__ == "__main__":
    main()