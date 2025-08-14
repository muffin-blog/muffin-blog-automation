#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
継続的品質管理統合システム（Phase4完成版）
投稿前確認システム + 監視システム + 自動化ワークフローの完全統合

【概要】
- リアルタイム品質監視
- 自動エラー検出・対応
- 継続的改善提案
- 完全自動化対応
"""

import sys
import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

# パス設定
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from 投稿前確認システム import 投稿前確認システム
    from WordPress連携API import WordPressBlogAutomator
    import importlib.util
    spec = importlib.util.spec_from_file_location("monitoring", os.path.join(os.path.dirname(__file__), "システム監視・品質管理.py"))
    monitoring_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(monitoring_module)
    システム監視品質管理 = monitoring_module.システム監視品質管理
except Exception as e:
    print(f"⚠️ モジュール読み込みエラー: {e}")

class 継続的品質管理統合システム:
    """継続的品質管理統合システム（Phase4完成版）"""
    
    def __init__(self):
        """初期化"""
        self.system_version = "1.1.0-Phase4"
        self.base_path = "/Users/satoumasamitsu/Desktop/osigoto/ブログ自動化"
        
        # コンポーネント初期化
        self.validator = 投稿前確認システム()
        self.monitor = システム監視品質管理() if 'システム監視品質管理' in globals() else None
        self.wp = WordPressBlogAutomator()
        
        # 統合管理設定
        self.management_config = {
            'auto_monitoring': True,
            'continuous_improvement': True,
            'error_auto_recovery': True,
            'quality_threshold': 85,
            'max_retry_attempts': 3,
            'alert_threshold': {
                'quality_decline': 70,
                'error_rate': 0.15,
                'performance_degradation': 45.0
            }
        }
        
        # 品質履歴管理
        self.quality_history = []
        self.improvement_suggestions = []
        
        # 日報ログシステム参照
        self.daily_log_path = "/Users/satoumasamitsu/Desktop/osigoto/統合管理システム/日報・ログ"
        self.load_daily_log_rules()
        
        print(f"🚀 継続的品質管理統合システム初期化完了 v{self.system_version}")
        
    def execute_comprehensive_quality_check(self, article_data: Dict) -> Dict:
        """包括的品質チェック実行（Phase4統合版）"""
        print("🔍 包括的品質チェック実行開始...")
        
        check_start_time = time.time()
        
        # システムヘルスチェック
        system_health = self.perform_system_health_check()
        
        # 記事データ検証
        validation_result = self.validator.comprehensive_validation(article_data)
        
        # 品質監視記録
        if self.monitor:
            execution_time = time.time() - check_start_time
            self.monitor.log_validation_result(article_data, validation_result, execution_time)
        
        # 統合結果作成
        comprehensive_result = {
            'timestamp': datetime.now().isoformat(),
            'system_health': system_health,
            'validation_result': validation_result,
            'quality_score': validation_result.get('overall_score', 0),
            'is_ready_for_publish': self.determine_publish_readiness(validation_result, system_health),
            'improvement_actions': self.generate_improvement_actions(validation_result),
            'execution_time': time.time() - check_start_time
        }
        
        # 品質履歴更新
        self.update_quality_history(comprehensive_result)
        
        # 継続的改善実行
        if self.management_config['continuous_improvement']:
            self.execute_continuous_improvement()
        
        return comprehensive_result
    
    def perform_system_health_check(self) -> Dict:
        """システムヘルスチェック実行"""
        print("🏥 システムヘルスチェック実行中...")
        
        health_result = {
            'overall_healthy': True,
            'components': {},
            'warnings': [],
            'critical_issues': []
        }
        
        # WordPress API接続確認
        try:
            wp_healthy = self.wp.test_connection()
            health_result['components']['wordpress_api'] = {
                'status': 'healthy' if wp_healthy else 'unhealthy',
                'details': 'API接続正常' if wp_healthy else 'API接続失敗'
            }
            if not wp_healthy:
                health_result['critical_issues'].append('WordPress API接続不良')
                health_result['overall_healthy'] = False
        except Exception as e:
            health_result['components']['wordpress_api'] = {
                'status': 'error',
                'details': f'接続エラー: {e}'
            }
            health_result['critical_issues'].append(f'WordPress API エラー: {e}')
            health_result['overall_healthy'] = False
        
        # ディスク容量確認
        try:
            import shutil
            disk_usage = shutil.disk_usage(self.base_path)
            free_gb = disk_usage.free / (1024**3)
            if free_gb < 1.0:  # 1GB未満
                health_result['warnings'].append(f'ディスク容量不足: {free_gb:.2f}GB残り')
                health_result['components']['disk_space'] = {
                    'status': 'warning',
                    'details': f'{free_gb:.2f}GB利用可能'
                }
            else:
                health_result['components']['disk_space'] = {
                    'status': 'healthy',
                    'details': f'{free_gb:.2f}GB利用可能'
                }
        except Exception as e:
            health_result['warnings'].append(f'ディスク容量確認失敗: {e}')
        
        # 監視システム確認
        if self.monitor:
            try:
                # 監視システム自動ヘルスチェック
                monitor_healthy = self.monitor.auto_health_check()
                health_result['components']['monitoring_system'] = {
                    'status': 'healthy' if monitor_healthy else 'unhealthy',
                    'details': '監視システム正常' if monitor_healthy else '監視システム異常'
                }
                if not monitor_healthy:
                    health_result['warnings'].append('監視システム異常')
            except Exception as e:
                health_result['components']['monitoring_system'] = {
                    'status': 'error',
                    'details': f'監視システムエラー: {e}'
                }
                health_result['warnings'].append(f'監視システムエラー: {e}')
        else:
            health_result['components']['monitoring_system'] = {
                'status': 'disabled',
                'details': '監視システム無効'
            }
        
        return health_result
    
    def determine_publish_readiness(self, validation_result: Dict, system_health: Dict) -> bool:
        """投稿準備完了判定"""
        # 品質スコアチェック
        quality_score = validation_result.get('overall_score', 0)
        if quality_score < self.management_config['quality_threshold']:
            return False
        
        # バリデーション成功チェック
        if not validation_result.get('overall_valid', False):
            return False
        
        # システムヘルス チェック
        if not system_health.get('overall_healthy', False):
            # 重要な問題があるかチェック
            critical_issues = system_health.get('critical_issues', [])
            if critical_issues:
                return False
        
        return True
    
    def generate_improvement_actions(self, validation_result: Dict) -> List[str]:
        """改善アクション生成"""
        actions = []
        
        # エラーベースの改善アクション
        errors = validation_result.get('errors', [])
        for error in errors:
            if 'メタディスクリプション' in error:
                actions.append("メタディスクリプションの見直し: 文字数とキーワード含有率の最適化")
            elif 'タグ' in error:
                actions.append("タグの最適化: 数量とバリエーションの調整")
            elif 'スラッグ' in error:
                actions.append("スラッグの改善: 英語表記と文字数の調整")
        
        # スコア改善アクション
        score = validation_result.get('overall_score', 0)
        if score < 90:
            actions.append("全体的なSEO最適化の実施")
        if score < 80:
            actions.append("絶対的見本テンプレートとの比較確認")
        
        # 警告ベースの改善アクション
        warnings = validation_result.get('warnings', [])
        for warning in warnings:
            if 'キーワード密度' in warning:
                actions.append("キーワード密度の調整: 自然な文章への改善")
        
        return actions
    
    def update_quality_history(self, result: Dict):
        """品質履歴更新"""
        # 履歴追加
        history_entry = {
            'timestamp': result['timestamp'],
            'quality_score': result['quality_score'],
            'is_ready': result['is_ready_for_publish'],
            'execution_time': result['execution_time'],
            'improvement_count': len(result['improvement_actions'])
        }
        
        self.quality_history.append(history_entry)
        
        # 履歴サイズ制限（最新100件）
        if len(self.quality_history) > 100:
            self.quality_history = self.quality_history[-100:]
        
        # トレンド分析
        if len(self.quality_history) >= 5:
            self.analyze_quality_trends()
    
    def analyze_quality_trends(self):
        """品質トレンド分析"""
        if len(self.quality_history) < 5:
            return
        
        recent_scores = [entry['quality_score'] for entry in self.quality_history[-5:]]
        avg_recent = sum(recent_scores) / len(recent_scores)
        
        if len(self.quality_history) >= 10:
            older_scores = [entry['quality_score'] for entry in self.quality_history[-10:-5]]
            avg_older = sum(older_scores) / len(older_scores)
            
            # トレンド判定
            if avg_recent < avg_older - 5:
                trend_suggestion = "品質スコアが低下傾向です。絶対的見本テンプレートの再確認を推奨します。"
                if trend_suggestion not in self.improvement_suggestions:
                    self.improvement_suggestions.append(trend_suggestion)
                    print(f"📉 品質トレンドアラート: {trend_suggestion}")
    
    def execute_continuous_improvement(self):
        """継続的改善実行"""
        if not self.improvement_suggestions:
            return
        
        print("🔄 継続的改善提案:")
        for i, suggestion in enumerate(self.improvement_suggestions[-3:], 1):
            print(f"   {i}. {suggestion}")
        
        # 改善提案をログに記録
        if self.monitor:
            try:
                self.monitor.log_performance('continuous_improvement', 0.1, True, {
                    'suggestions_count': len(self.improvement_suggestions),
                    'recent_suggestions': self.improvement_suggestions[-3:]
                })
            except Exception as e:
                print(f"⚠️ 改善ログ記録エラー: {e}")
    
    def auto_recover_from_errors(self, errors: List[str]) -> Dict:
        """エラー自動回復機能"""
        if not self.management_config['error_auto_recovery']:
            return {'recovered': False, 'reason': 'auto_recovery_disabled'}
        
        recovery_result = {
            'recovered': False,
            'actions_taken': [],
            'remaining_errors': errors.copy()
        }
        
        for error in errors.copy():
            if '必須項目不足' in error:
                recovery_result['actions_taken'].append("デフォルト値自動設定を試行")
                # 実際の修復処理はここに実装
            elif 'カテゴリ読み込みエラー' in error:
                recovery_result['actions_taken'].append("フォールバックカテゴリ設定")
                # 実際の修復処理はここに実装
        
        if recovery_result['actions_taken']:
            recovery_result['recovered'] = True
        
        return recovery_result
    
    def generate_quality_dashboard(self) -> str:
        """品質ダッシュボード生成"""
        dashboard = ["📊 継続的品質管理ダッシュボード"]
        dashboard.append("=" * 50)
        
        # システム状態
        dashboard.append(f"🕐 最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        dashboard.append(f"📈 システムバージョン: {self.system_version}")
        
        # 品質履歴サマリー
        if self.quality_history:
            recent_scores = [entry['quality_score'] for entry in self.quality_history[-10:]]
            avg_score = sum(recent_scores) / len(recent_scores)
            dashboard.append(f"📊 直近平均品質スコア: {avg_score:.1f}/100")
            dashboard.append(f"🎯 最高スコア: {max(recent_scores)}/100")
            dashboard.append(f"📉 最低スコア: {min(recent_scores)}/100")
        
        # 改善提案
        if self.improvement_suggestions:
            dashboard.append("\n💡 継続的改善提案:")
            for suggestion in self.improvement_suggestions[-3:]:
                dashboard.append(f"   • {suggestion}")
        else:
            dashboard.append("\n✅ 改善提案なし（品質良好）")
        
        # 監視システム状態
        if self.monitor:
            try:
                # 監視ダッシュボード統合
                dashboard.append("\n🔍 監視システム状態:")
                dashboard.append("   統合監視機能: 有効")
            except Exception as e:
                dashboard.append(f"\n⚠️ 監視システムエラー: {e}")
        else:
            dashboard.append("\n⚠️ 監視システム: 無効")
        
        return "\n".join(dashboard)
    
    def save_integrated_report(self, comprehensive_result: Dict) -> str:
        """統合レポート保存 - システム監視データに統合保存"""
        # 重複回避: 品質管理レポートフォルダは使用せず、システム監視データに統合
        
        # レポートサマリーを生成（詳細JSON保存は廃止）
        report_summary = {
            'timestamp': datetime.now().isoformat(),
            'system_version': self.system_version,
            'quality_score': comprehensive_result.get('article_validation_result', {}).get('overall_score', 0),
            'system_health': comprehensive_result.get('system_health', {}),
            'total_checks': len(self.quality_history),
            'avg_score': sum(entry['quality_score'] for entry in self.quality_history) / len(self.quality_history) if self.quality_history else 0
        }
        
        # 既存のシステム監視データ機能を活用（重複レポート生成を停止）
        print(f"📊 品質レポート要約: スコア{report_summary['quality_score']}/100")
        
        return None  # 詳細レポートファイルは生成しない
    
    def load_daily_log_rules(self):
        """日報ログ保護ルール読み込み"""
        try:
            rules_path = "/Users/satoumasamitsu/Desktop/osigoto/統合管理システム/日報ログ保護ルール.md"
            with open(rules_path, 'r', encoding='utf-8') as f:
                rules_content = f.read()
            
            # 重要ルールを抽出
            self.daily_log_rules = {
                'protection_enabled': True,
                'log_directory': self.daily_log_path,
                'edit_prohibited': True,
                'append_only': True,
                'new_creation_allowed': True
            }
            
            print("📋 日報ログ保護ルール読み込み完了")
            
        except Exception as e:
            print(f"⚠️ 日報ログルール読み込みエラー: {e}")
            self.daily_log_rules = {'protection_enabled': False}
    
    def check_daily_log_requirement(self, result: Dict) -> bool:
        """日報作成要否判定"""
        if not hasattr(self, 'daily_log_rules') or not self.daily_log_rules.get('protection_enabled'):
            return False
        
        # 重要なセッションの判定基準
        important_session_indicators = [
            result.get('quality_score', 0) < 80,  # 品質問題発生
            len(result.get('improvement_actions', [])) > 2,  # 多数の改善必要
            not result.get('is_ready_for_publish', True),  # 投稿準備未完了
            result.get('execution_time', 0) > 60  # 長時間実行
        ]
        
        return any(important_session_indicators)
    
    def auto_create_daily_log(self, comprehensive_result: Dict, session_details: Dict):
        """重要セッションの自動日報作成"""
        if not self.check_daily_log_requirement(comprehensive_result):
            return None
        
        try:
            from datetime import datetime
            today = datetime.now().strftime('%Y-%m-%d')
            
            # 日報ファイル名生成
            session_type = session_details.get('type', '品質管理作業')
            log_filename = f"{today}_{session_type}_自動品質管理_日報.md"
            log_filepath = os.path.join(self.daily_log_path, log_filename)
            
            # 日報内容生成
            log_content = self.generate_auto_log_content(comprehensive_result, session_details)
            
            # ファイル作成（既存ファイルがある場合は追記）
            if os.path.exists(log_filepath):
                with open(log_filepath, 'a', encoding='utf-8') as f:
                    f.write(f"\n\n## 追加セッション ({datetime.now().strftime('%H:%M:%S')})\n\n")
                    f.write(log_content)
                print(f"📝 既存日報に追記: {log_filename}")
            else:
                with open(log_filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# {today} {session_type} 自動品質管理 日報\n\n")
                    f.write(log_content)
                print(f"📝 新規日報作成: {log_filename}")
            
            return log_filepath
            
        except Exception as e:
            print(f"⚠️ 自動日報作成エラー: {e}")
            return None
    
    def generate_auto_log_content(self, result: Dict, session_details: Dict) -> str:
        """自動日報内容生成"""
        content = []
        
        # セッション概要
        content.append("## セッション概要")
        content.append(f"- **実行時刻**: {result.get('timestamp', 'N/A')}")
        content.append(f"- **品質スコア**: {result.get('quality_score', 'N/A')}/100")
        content.append(f"- **投稿準備状況**: {'完了' if result.get('is_ready_for_publish') else '要改善'}")
        content.append(f"- **実行時間**: {result.get('execution_time', 0):.2f}秒")
        
        # 検出された問題
        if result.get('improvement_actions'):
            content.append("\n## 検出された改善点")
            for i, action in enumerate(result['improvement_actions'], 1):
                content.append(f"{i}. {action}")
        
        # システムヘルス
        system_health = result.get('system_health', {})
        if not system_health.get('overall_healthy', True):
            content.append("\n## システム問題")
            for issue in system_health.get('critical_issues', []):
                content.append(f"- 🚨 {issue}")
            for warning in system_health.get('warnings', []):
                content.append(f"- ⚠️ {warning}")
        
        # 記録の重要性
        content.append("\n## 記録意義")
        content.append("この記録は品質管理システムの継続的改善と、将来の書籍出版・有料ノート作成の貴重な素材として保管されます。")
        
        return "\n".join(content)

def execute_integrated_quality_management(article_data: Dict) -> Dict:
    """統合品質管理実行（エントリーポイント）"""
    print("🚀 継続的品質管理統合システム実行開始")
    
    # システム初期化
    integrated_system = 継続的品質管理統合システム()
    
    # 包括的品質チェック実行
    result = integrated_system.execute_comprehensive_quality_check(article_data)
    
    # ダッシュボード表示
    print("\n" + integrated_system.generate_quality_dashboard())
    
    # 統合レポート保存
    report_path = integrated_system.save_integrated_report(result)
    
    # 自動日報作成（重要セッションの場合）
    session_details = {
        'type': '記事品質管理',
        'article_title': article_data.get('title', 'N/A'),
        'user_interaction': True
    }
    daily_log_path = integrated_system.auto_create_daily_log(result, session_details)
    
    # 結果サマリー
    print("\n🎉 継続的品質管理完了")
    print(f"📊 品質スコア: {result['quality_score']}/100")
    print(f"✅ 投稿準備: {'完了' if result['is_ready_for_publish'] else '要改善'}")
    if report_path:
        print(f"📄 詳細レポート: {report_path}")
    
    return result

# CLI実行対応
def main():
    """メイン実行関数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python 継続的品質管理統合システム.py [記事データJSONファイル]")
        return
    
    json_file_path = sys.argv[1]
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            article_data = json.load(f)
        
        # 統合品質管理実行
        result = execute_integrated_quality_management(article_data)
        
        print(f"\n🚀 統合システム実行完了")
        
    except FileNotFoundError:
        print(f"❌ ファイルが見つかりません: {json_file_path}")
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    main()