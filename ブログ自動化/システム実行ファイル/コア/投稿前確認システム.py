"""
投稿前確認システム（SEO仕様統合版）
絶対的見本テンプレートの仕様に基づく包括的な投稿前確認
"""

import sys
import os
import re
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from WordPress連携API import WordPressBlogAutomator

try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("monitoring", os.path.join(os.path.dirname(__file__), "システム監視・品質管理.py"))
    monitoring_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(monitoring_module)
    システム監視品質管理 = monitoring_module.システム監視品質管理
except Exception as e:
    print(f"⚠️ 監視システム読み込みエラー: {e}")
    システム監視品質管理 = None

class 投稿前確認システム:
    """投稿前の包括的確認システム（絶対的見本テンプレート仕様準拠）"""
    
    def __init__(self):
        self.wp = WordPressBlogAutomator()
        self.monitor = システム監視品質管理() if システム監視品質管理 else None
        
        # SEO仕様（絶対的見本テンプレートより）- Phase4強化版
        self.seo_specs = {
            'meta_description': {
                'min_length': 120,
                'max_length': 160,
                'required_elements': ['メインキーワード', 'ユーザーの悩み', '解決策', 'メリット', '行動促進'],
                'action_words': ['無料体験', '今すぐ', 'お試し', '始める', '解決', '改善'],
                'prohibited_words': ['絶対', '確実', '100%', '必ず'],  # 薬事法対策
                'emotion_patterns': ['！', '？', 'ませんか', 'してみませんか', '解決', '安心', '簡単']
            },
            'tags': {
                'main_keywords': 1,
                'sub_keywords': {'min': 2, 'max': 3},
                'related_keywords': {'min': 5, 'max': 7},
                'total_max': 11,
                'total_min': 8,  # 最低限のタグ数
                'variations': ['ひらがな', 'カタカナ', '漢字'],
                'prohibited_tags': ['SEO', 'アフィリエイト', '稼ぐ'],  # スパム回避
                'max_tag_length': 20  # タグの最大文字数
            },
            'slug': {
                'language': 'english',
                'separator': '-',
                'word_count': {'min': 3, 'max': 6},
                'required': 'main_keyword_included',
                'examples': ['audible-reading-solution', 'book-listening-beginner'],
                'prohibited_chars': ['_', ' ', '/', '?', '#', '&'],  # 禁止文字
                'max_length': 50  # スラッグの最大文字数
            },
            'title': {
                'length': {'min': 28, 'max': 32},
                'structure': ['問題提起', 'メリット/解決策', 'ブランド名'],
                'examples': ['本が読めない悩み解決！Audibleで始める聴く読書の魅力とは'],
                'prohibited_words': ['最強', '裏技', '秘密'],  # 煽り文句制限
                'required_punctuation': ['！', '？', 'とは', 'なら'],  # 感情表現必須
                'keyword_density_max': 0.3  # キーワード密度上限
            },
            'content_quality': {
                'min_word_count': 2000,  # 最低文字数
                'max_keyword_density': 0.05,  # キーワード密度上限
                'required_sections': ['導入', '本文', '結論'],
                'external_link_min': 1,  # 最低外部リンク数
                'internal_link_min': 2   # 最低内部リンク数
            }
        }
        
        # カテゴリ管理
        self.existing_categories = []
        self.load_existing_categories()
    
    def load_existing_categories(self):
        """既存カテゴリの読み込み"""
        try:
            categories = self.wp.get_categories()
            self.existing_categories = [cat['name'] for cat in categories]
            print(f"📂 既存カテゴリ読み込み完了: {len(self.existing_categories)}個")
            
            # 成功ログ記録
            if self.monitor:
                self.monitor.log_performance('category_load', 0.1, True, {
                    'category_count': len(self.existing_categories),
                    'categories': self.existing_categories[:5]  # 最初の5個のみログ
                })
                
        except Exception as e:
            error_msg = f"カテゴリ読み込みエラー: {e}"
            print(f"⚠️ {error_msg}")
            self.existing_categories = ['Audible', 'その他']
            
            # エラーログ記録
            if self.monitor:
                self.monitor.log_error('category_load_failed', error_msg, {
                    'fallback_categories': self.existing_categories
                })
    
    def validate_prohibited_content(self, text: str, content_type: str) -> List[str]:
        """禁止コンテンツチェック（Phase4強化機能）"""
        issues = []
        
        if content_type == 'meta_description':
            prohibited = self.seo_specs['meta_description']['prohibited_words']
        elif content_type == 'title':
            prohibited = self.seo_specs['title']['prohibited_words']
        else:
            prohibited = []
        
        for word in prohibited:
            if word in text:
                issues.append(f"禁止語句「{word}」が含まれています")
        
        return issues
    
    def validate_meta_description(self, meta_desc: str, main_keyword: str) -> Dict:
        """メタディスクリプション検証（Phase4強化版）"""
        result = {
            'valid': True,
            'issues': [],
            'suggestions': [],
            'score': 0
        }
        
        # 禁止コンテンツチェック
        prohibited_issues = self.validate_prohibited_content(meta_desc, 'meta_description')
        if prohibited_issues:
            result['issues'].extend(prohibited_issues)
            result['valid'] = False
        else:
            result['score'] += 15
        
        # 文字数チェック
        length = len(meta_desc)
        if length < self.seo_specs['meta_description']['min_length']:
            result['issues'].append(f"文字数不足: {length}文字（推奨: 120-160文字）")
            result['valid'] = False
        elif length > self.seo_specs['meta_description']['max_length']:
            result['issues'].append(f"文字数過多: {length}文字（推奨: 120-160文字）")
            result['valid'] = False
        else:
            result['score'] += 20
        
        # メインキーワード含有チェック
        if main_keyword.lower() not in meta_desc.lower():
            result['issues'].append(f"メインキーワード「{main_keyword}」が含まれていません")
            result['valid'] = False
        else:
            result['score'] += 20
        
        # キーワード密度チェック（Phase4新機能）
        keyword_count = meta_desc.lower().count(main_keyword.lower())
        keyword_density = keyword_count / len(meta_desc.split())
        if keyword_density > 0.1:  # 10%以上は過度
            result['issues'].append(f"キーワード密度過多: {keyword_density:.1%}（推奨: 10%以下）")
            result['suggestions'].append("キーワード使用回数を調整してください")
        else:
            result['score'] += 15
        
        # 行動促進ワードチェック
        action_found = any(word in meta_desc for word in self.seo_specs['meta_description']['action_words'])
        if action_found:
            result['score'] += 15
        else:
            result['suggestions'].append("行動促進ワード（無料体験、今すぐ等）の追加を検討")
        
        # 感情表現チェック
        emotion_patterns = self.seo_specs['meta_description']['emotion_patterns']
        emotion_found = any(pattern in meta_desc for pattern in emotion_patterns)
        if emotion_found:
            result['score'] += 15
        else:
            result['suggestions'].append("感情に訴える表現の追加を検討")
        
        return result
    
    def validate_tags(self, tags: List[str]) -> Dict:
        """タグ検証（Phase4強化版）"""
        result = {
            'valid': True,
            'issues': [],
            'suggestions': [],
            'score': 0,
            'analysis': {
                'total_count': len(tags),
                'variations': {'hiragana': 0, 'katakana': 0, 'kanji': 0, 'english': 0},
                'avg_length': sum(len(tag) for tag in tags) / len(tags) if tags else 0,
                'longest_tag': max(tags, key=len) if tags else '',
                'prohibited_found': []
            }
        }
        
        # 禁止タグチェック（Phase4新機能）
        prohibited_tags = self.seo_specs['tags']['prohibited_tags']
        for tag in tags:
            if tag in prohibited_tags:
                result['issues'].append(f"禁止タグ「{tag}」が含まれています")
                result['analysis']['prohibited_found'].append(tag)
                result['valid'] = False
        
        if not result['analysis']['prohibited_found']:
            result['score'] += 15
        
        # タグ文字数チェック（Phase4新機能）
        max_tag_length = self.seo_specs['tags']['max_tag_length']
        long_tags = [tag for tag in tags if len(tag) > max_tag_length]
        if long_tags:
            result['issues'].append(f"長すぎるタグ: {', '.join(long_tags)} (最大{max_tag_length}文字)")
            result['suggestions'].append("タグを短縮してください")
        else:
            result['score'] += 10
        
        # タグ数チェック
        total_min = self.seo_specs['tags']['total_min']
        total_max = self.seo_specs['tags']['total_max']
        
        if len(tags) > total_max:
            result['issues'].append(f"タグ数過多: {len(tags)}個（推奨: {total_min}-{total_max}個）")
            result['valid'] = False
        elif len(tags) < total_min:
            result['issues'].append(f"タグ数不足: {len(tags)}個（推奨: {total_min}-{total_max}個）")
            result['suggestions'].append("関連キーワードの追加を検討")
        else:
            result['score'] += 25
        
        # バリエーションチェック
        for tag in tags:
            if re.search(r'[ひ-ろ]', tag):
                result['analysis']['variations']['hiragana'] += 1
            if re.search(r'[ア-ヶ]', tag):
                result['analysis']['variations']['katakana'] += 1
            if re.search(r'[一-龯]', tag):
                result['analysis']['variations']['kanji'] += 1
            if re.search(r'[a-zA-Z]', tag):
                result['analysis']['variations']['english'] += 1
        
        # バリエーション評価
        variation_types = sum(1 for count in result['analysis']['variations'].values() if count > 0)
        if variation_types >= 3:
            result['score'] += 40
        elif variation_types >= 2:
            result['score'] += 20
            result['suggestions'].append("文字種バリエーション（ひらがな・カタカナ・漢字）の追加を検討")
        else:
            result['suggestions'].append("文字種バリエーション不足です")
        
        # 重複チェック
        if len(tags) != len(set(tags)):
            result['issues'].append("重複タグがあります")
            result['valid'] = False
        else:
            result['score'] += 30
        
        return result
    
    def validate_slug(self, slug: str, main_keyword: str) -> Dict:
        """スラッグ検証"""
        result = {
            'valid': True,
            'issues': [],
            'suggestions': [],
            'score': 0
        }
        
        # 先頭スラッシュの処理
        clean_slug = slug.lstrip('/')
        
        # 英語チェック
        if not re.match(r'^[a-z0-9\-]+$', clean_slug):
            result['issues'].append("英語・数字・ハイフンのみ使用可能です（日本語不可）")
            result['valid'] = False
        else:
            result['score'] += 25
        
        # 単語数チェック
        words = clean_slug.split('-')
        word_count = len(words)
        if word_count < self.seo_specs['slug']['word_count']['min']:
            result['issues'].append(f"単語数不足: {word_count}単語（推奨: 3-6単語）")
            result['valid'] = False
        elif word_count > self.seo_specs['slug']['word_count']['max']:
            result['issues'].append(f"単語数過多: {word_count}単語（推奨: 3-6単語）")
            result['suggestions'].append("より簡潔な表現を検討")
        else:
            result['score'] += 25
        
        # メインキーワード含有チェック（英語変換）
        keyword_mapping = {
            'Audible': 'audible',
            'audible': 'audible', 
            '読書': 'reading',
            '本': 'book',
            '聴く': 'listening',
            '学習': 'learning',
            '解決': 'solution'
        }
        
        main_keyword_en = keyword_mapping.get(main_keyword, main_keyword.lower())
        if main_keyword_en in clean_slug:
            result['score'] += 25
        else:
            result['suggestions'].append(f"メインキーワード「{main_keyword}」の英語表現を含めることを推奨")
        
        # スラッグ形式チェック
        if clean_slug.startswith('-') or clean_slug.endswith('-') or '--' in clean_slug:
            result['issues'].append("ハイフンの使用方法が不正です")
            result['valid'] = False
        else:
            result['score'] += 25
        
        return result
    
    def validate_title(self, title: str, main_keyword: str) -> Dict:
        """タイトル検証"""
        result = {
            'valid': True,
            'issues': [],
            'suggestions': [],
            'score': 0
        }
        
        # 文字数チェック
        length = len(title)
        if length < self.seo_specs['title']['length']['min']:
            result['issues'].append(f"タイトル文字数不足: {length}文字（推奨: 28-32文字）")
            result['valid'] = False
        elif length > self.seo_specs['title']['length']['max']:
            result['issues'].append(f"タイトル文字数過多: {length}文字（推奨: 28-32文字）")
            result['valid'] = False
        else:
            result['score'] += 30
        
        # メインキーワード含有チェック
        if main_keyword in title:
            result['score'] += 30
        else:
            result['issues'].append(f"メインキーワード「{main_keyword}」がタイトルに含まれていません")
            result['valid'] = False
        
        # 構造チェック（問題提起・解決策・感情表現）
        structure_elements = {
            '問題提起': ['悩み', '困った', '苦手', 'できない', '分からない', '迷う'],
            '解決策': ['解決', '方法', '改善', 'コツ', 'テクニック', '攻略'],
            '感情表現': ['！', '？', 'とは', 'なら', 'でも']
        }
        
        found_elements = []
        for element, patterns in structure_elements.items():
            if any(pattern in title for pattern in patterns):
                found_elements.append(element)
        
        if len(found_elements) >= 2:
            result['score'] += 40
        else:
            result['suggestions'].append(f"タイトル構造の改善を検討（問題提起・解決策・感情表現）")
        
        return result
    
    def validate_category(self, category: str) -> Dict:
        """カテゴリ検証"""
        result = {
            'valid': True,
            'issues': [],
            'suggestions': [],
            'score': 0
        }
        
        if category in self.existing_categories:
            result['score'] = 100
            result['suggestions'].append(f"✅ 既存カテゴリ「{category}」を使用")
        else:
            result['issues'].append(f"カテゴリ「{category}」は存在しません")
            result['valid'] = False
            result['suggestions'].append(f"利用可能カテゴリ: {', '.join(self.existing_categories)}")
        
        return result
    
    def comprehensive_validation(self, article_data: Dict) -> Dict:
        """包括的記事データ検証"""
        print("🔍 投稿前包括的検証開始...")
        print("=" * 60)
        
        start_time = time.time()
        
        validation_results = {
            'overall_valid': True,
            'overall_score': 0,
            'validations': {},
            'errors': [],
            'warnings': []
        }
        
        # 入力データ検証
        try:
            if not isinstance(article_data, dict):
                raise ValueError("記事データが辞書形式ではありません")
        except Exception as e:
            error_msg = f"入力データ検証エラー: {e}"
            validation_results['errors'].append(error_msg)
            if self.monitor:
                self.monitor.log_error('input_validation_failed', error_msg, {
                    'data_type': type(article_data).__name__
                })
            return validation_results
        
        # 必須項目チェック
        required_fields = ['title', 'meta_description', 'tags', 'slug', 'category', 'main_keyword']
        missing_fields = [field for field in required_fields if not article_data.get(field)]
        
        if missing_fields:
            validation_results['overall_valid'] = False
            validation_results['missing_fields'] = missing_fields
            error_msg = f"必須項目不足: {', '.join(missing_fields)}"
            validation_results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            
            # エラーログ記録
            if self.monitor:
                self.monitor.log_error('missing_required_fields', error_msg, {
                    'missing_fields': missing_fields,
                    'provided_fields': list(article_data.keys())
                })
            
            return validation_results
        
        # 各項目の検証実行
        validations = [
            ('title', self.validate_title(article_data['title'], article_data['main_keyword'])),
            ('meta_description', self.validate_meta_description(article_data['meta_description'], article_data['main_keyword'])),
            ('tags', self.validate_tags(article_data['tags'])),
            ('slug', self.validate_slug(article_data['slug'], article_data['main_keyword'])),
            ('category', self.validate_category(article_data['category']))
        ]
        
        total_score = 0
        max_score = 0
        validation_errors = []
        validation_warnings = []
        
        for field_name, validation in validations:
            try:
                validation_results['validations'][field_name] = validation
                total_score += validation['score']
                max_score += 100
                
                if not validation['valid']:
                    validation_results['overall_valid'] = False
                
                # エラーと警告の収集
                if validation['issues']:
                    validation_errors.extend([f"{field_name}: {issue}" for issue in validation['issues']])
                
                if validation['suggestions']:
                    validation_warnings.extend([f"{field_name}: {suggestion}" for suggestion in validation['suggestions']])
                
                # 結果表示
                status = "✅" if validation['valid'] else "❌"
                score_display = f"{validation['score']}/100"
                print(f"{status} {field_name.upper()}: {score_display}")
                
                if validation['issues']:
                    for issue in validation['issues']:
                        print(f"   ⚠️ {issue}")
                
                if validation['suggestions']:
                    for suggestion in validation['suggestions']:
                        print(f"   💡 {suggestion}")
                print()
                
            except Exception as e:
                error_msg = f"検証エラー ({field_name}): {e}"
                validation_errors.append(error_msg)
                print(f"❌ {error_msg}")
                
                # 個別検証エラーログ
                if self.monitor:
                    self.monitor.log_error('field_validation_error', error_msg, {
                        'field_name': field_name,
                        'field_value': article_data.get(field_name, 'N/A')
                    })
        
        # エラーと警告をresultに追加
        validation_results['errors'].extend(validation_errors)
        validation_results['warnings'].extend(validation_warnings)
        
        # 総合スコア計算
        validation_results['overall_score'] = int((total_score / max_score) * 100)
        
        # 総合評価表示
        print("=" * 60)
        print(f"📊 総合評価: {validation_results['overall_score']}/100")
        
        # 実行時間記録
        execution_time = time.time() - start_time
        print(f"⏱️ 実行時間: {execution_time:.2f}秒")
        
        # 監視システムへの記録
        if self.monitor:
            try:
                self.monitor.log_validation_result(article_data, validation_results, execution_time)
            except Exception as e:
                print(f"⚠️ 監視ログ記録エラー: {e}")
        else:
            print("ℹ️ 監視システム無効（スタンドアローン実行）")
        
        if validation_results['overall_valid'] and validation_results['overall_score'] >= 80:
            print("🎉 投稿準備完了！高品質なSEO設定です")
        elif validation_results['overall_valid']:
            print("✅ 投稿可能ですが、改善余地があります")
        else:
            print("❌ 修正が必要です。上記の問題を解決してから再実行してください")
        
        return validation_results
    
    def interactive_confirmation(self, article_data: Dict) -> bool:
        """対話式最終確認"""
        print("\n" + "=" * 60)
        print("📝 投稿前最終確認")
        print("=" * 60)
        
        # 記事情報表示
        print("🎯 記事情報:")
        print(f"   タイトル: {article_data['title']}")
        print(f"   カテゴリ: {article_data['category']}")
        print(f"   メインキーワード: {article_data['main_keyword']}")
        print(f"   スラッグ: {article_data['slug']}")
        print()
        print(f"📝 メタディスクリプション ({len(article_data['meta_description'])}文字):")
        print(f"   {article_data['meta_description']}")
        print()
        print(f"🏷️  タグ ({len(article_data['tags'])}個):")
        print(f"   {', '.join(article_data['tags'])}")
        print()
        
        # 確認プロンプト
        while True:
            print("この内容で投稿を実行しますか？")
            print("  [y] はい（投稿実行）")
            print("  [e] 編集する")
            print("  [n] いいえ（中止）")
            
            choice = input("選択してください (y/e/n): ").lower().strip()
            
            if choice == 'y':
                print("✅ 投稿実行が承認されました")
                return True
            elif choice == 'n':
                print("❌ 投稿がキャンセルされました")
                return False
            elif choice == 'e':
                print("✏️ 編集モードに入ります...")
                return self.edit_mode(article_data)
            else:
                print("⚠️ y, e, n のいずれかを入力してください")
    
    def edit_mode(self, article_data: Dict) -> bool:
        """編集モード"""
        editable_fields = {
            '1': ('title', 'タイトル'),
            '2': ('meta_description', 'メタディスクリプション'),
            '3': ('tags', 'タグ'),
            '4': ('slug', 'スラッグ'),
            '5': ('category', 'カテゴリ')
        }
        
        while True:
            print("\n編集したい項目を選択してください:")
            for key, (field, name) in editable_fields.items():
                current_value = article_data[field]
                if isinstance(current_value, list):
                    current_value = ', '.join(current_value)
                print(f"  [{key}] {name}: {current_value}")
            print("  [0] 編集完了")
            
            choice = input("番号を入力: ").strip()
            
            if choice == '0':
                # 再検証
                validation_result = self.comprehensive_validation(article_data)
                if validation_result['overall_valid']:
                    return self.interactive_confirmation(article_data)
                else:
                    continue
            elif choice in editable_fields:
                field, name = editable_fields[choice]
                current_value = article_data[field]
                
                if field == 'tags':
                    current_value = ', '.join(current_value)
                
                print(f"\n現在の{name}: {current_value}")
                new_value = input(f"新しい{name}を入力: ").strip()
                
                if new_value:
                    if field == 'tags':
                        article_data[field] = [tag.strip() for tag in new_value.split(',')]
                    else:
                        article_data[field] = new_value
                    print(f"✅ {name}を更新しました")
            else:
                print("⚠️ 正しい番号を入力してください")
    
    def save_article_data_json(self, article_data: Dict, file_path: str = None) -> str:
        """記事データをJSON形式で保存（エラーハンドリング強化版）"""
        save_start_time = time.time()
        
        try:
            if not file_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_path = f"/Users/satoumasamitsu/Desktop/osigoto/ブログ自動化/WordPress投稿下書き/記事データ保存_JSON/{timestamp}_記事データ.json"
            
            # ディレクトリ作成（権限チェック付き）
            dir_path = os.path.dirname(file_path)
            try:
                os.makedirs(dir_path, exist_ok=True)
                if not os.access(dir_path, os.W_OK):
                    raise PermissionError(f"ディレクトリへの書き込み権限がありません: {dir_path}")
            except Exception as e:
                error_msg = f"ディレクトリ作成エラー: {e}"
                if self.monitor:
                    self.monitor.log_error('directory_creation_failed', error_msg, {
                        'directory_path': dir_path
                    })
                print(f"❌ {error_msg}")
                return None
            
            # 保存用データ準備（バリデーション付き）
            try:
                save_data = {
                    'created_at': datetime.now().isoformat(),
                    'article_data': article_data,
                    'validation_completed': True,
                    'system_version': '1.1',
                    'file_size_bytes': 0,  # 後で設定
                    'checksum': None  # 後で設定
                }
                
                # JSON変換テスト
                json_str = json.dumps(save_data, ensure_ascii=False, indent=2)
                save_data['file_size_bytes'] = len(json_str.encode('utf-8'))
                
            except Exception as e:
                error_msg = f"データ準備エラー: {e}"
                if self.monitor:
                    self.monitor.log_error('data_preparation_failed', error_msg, {
                        'article_title': article_data.get('title', 'N/A')
                    })
                print(f"❌ {error_msg}")
                return None
            
            # ファイル書き込み
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(save_data, f, ensure_ascii=False, indent=2)
                
                # ファイル検証
                if not os.path.exists(file_path):
                    raise FileNotFoundError("保存されたファイルが見つかりません")
                
                file_size = os.path.getsize(file_path)
                if file_size == 0:
                    raise ValueError("保存されたファイルが空です")
                
            except Exception as e:
                error_msg = f"ファイル書き込みエラー: {e}"
                if self.monitor:
                    self.monitor.log_error('file_write_failed', error_msg, {
                        'file_path': file_path,
                        'data_size': len(str(article_data))
                    })
                print(f"❌ {error_msg}")
                return None
            
            # 成功ログ記録
            save_time = time.time() - save_start_time
            if self.monitor:
                self.monitor.log_performance('article_data_save', save_time, True, {
                    'file_path': file_path,
                    'file_size': file_size,
                    'article_title': article_data.get('title', 'N/A')
                })
            
            print(f"💾 記事データ保存完了: {file_path} ({file_size:,} bytes)")
            return file_path
            
        except Exception as e:
            error_msg = f"記事データ保存エラー: {e}"
            if self.monitor:
                self.monitor.log_error('article_save_failed', error_msg, {
                    'file_path': file_path,
                    'execution_time': time.time() - save_start_time
                })
            print(f"❌ {error_msg}")
            return None

# CLI実行対応
def main():
    """メイン実行関数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python 投稿前確認システム.py [記事データJSONファイル]")
        return
    
    json_file_path = sys.argv[1]
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            article_data = json.load(f)
        
        checker = 投稿前確認システム()
        
        # 包括的検証
        validation_result = checker.comprehensive_validation(article_data)
        
        # 対話式確認
        if validation_result['overall_valid'] or validation_result['overall_score'] >= 60:
            confirmed = checker.interactive_confirmation(article_data)
            
            if confirmed:
                # JSON保存
                saved_path = checker.save_article_data_json(article_data)
                print(f"🚀 投稿承認完了。記事データ: {saved_path}")
            else:
                print("📝 投稿がキャンセルされました")
        else:
            print("❌ 品質基準に達していません。修正が必要です。")
            
    except FileNotFoundError:
        print(f"❌ ファイルが見つかりません: {json_file_path}")
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    main()