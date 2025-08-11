"""
システム監視・品質管理システム
投稿前確認システムの品質監視と継続的改善
"""

import sys
import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class システム監視品質管理:
    """投稿前確認システムの監視・品質管理"""
    
    def __init__(self):
        # ログ・データ保存パス
        self.monitor_dir = Path("/Users/satoumasamitsu/Desktop/osigoto/ブログ自動化/システム監視データ")
        self.monitor_dir.mkdir(exist_ok=True)
        
        self.quality_log_path = self.monitor_dir / "品質監視ログ.json"
        self.error_log_path = self.monitor_dir / "エラー監視ログ.json"
        self.performance_log_path = self.monitor_dir / "パフォーマンス監視ログ.json"
        
        # 監視基準設定
        self.quality_standards = {
            'score_threshold': 80,  # 品質スコア基準
            'error_rate_threshold': 0.1,  # エラー率基準（10%以下）
            'response_time_threshold': 30.0,  # 応答時間基準（30秒以下）
            'validation_coverage': 5  # 必須検証項目数
        }
        
        # アラート設定
        self.alerts = {
            'enabled': True,
            'quality_decline': True,  # 品質低下アラート
            'error_spike': True,      # エラー急増アラート
            'performance_issue': True # パフォーマンス問題アラート
        }
    
    def log_validation_result(self, article_data: Dict, validation_result: Dict, execution_time: float):
        """検証結果のログ記録"""
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            'timestamp': timestamp,
            'article_id': self._generate_article_id(article_data),
            'title': article_data.get('title', 'Unknown'),
            'overall_score': validation_result.get('overall_score', 0),
            'overall_valid': validation_result.get('overall_valid', False),
            'execution_time': execution_time,
            'validation_details': validation_result.get('validations', {}),
            'issues_count': self._count_issues(validation_result),
            'suggestions_count': self._count_suggestions(validation_result)
        }
        
        # 品質ログに記録
        self._append_to_log(self.quality_log_path, log_entry)
        
        # リアルタイム品質監視
        self._monitor_quality_trends(log_entry)
        
        print(f"📊 品質ログ記録完了: スコア{log_entry['overall_score']}/100")
    
    def log_error(self, error_type: str, error_message: str, context: Dict = None):
        """エラーログの記録"""
        timestamp = datetime.now().isoformat()
        
        error_entry = {
            'timestamp': timestamp,
            'error_type': error_type,
            'error_message': str(error_message),
            'context': context or {},
            'severity': self._classify_error_severity(error_type, error_message)
        }
        
        # エラーログに記録
        self._append_to_log(self.error_log_path, error_entry)
        
        # エラー傾向監視
        self._monitor_error_trends(error_entry)
        
        print(f"🚨 エラーログ記録: {error_type} - {error_entry['severity']}")
    
    def log_performance(self, operation: str, duration: float, success: bool, details: Dict = None):
        """パフォーマンスログの記録"""
        timestamp = datetime.now().isoformat()
        
        perf_entry = {
            'timestamp': timestamp,
            'operation': operation,
            'duration': duration,
            'success': success,
            'details': details or {},
            'performance_grade': self._grade_performance(duration, success)
        }
        
        # パフォーマンスログに記録
        self._append_to_log(self.performance_log_path, perf_entry)
        
        # パフォーマンス監視
        self._monitor_performance_trends(perf_entry)
    
    def generate_quality_report(self, days: int = 7) -> Dict:
        """品質レポート生成"""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        # データ収集
        quality_data = self._load_log_data(self.quality_log_path, start_time, end_time)
        error_data = self._load_log_data(self.error_log_path, start_time, end_time)
        performance_data = self._load_log_data(self.performance_log_path, start_time, end_time)
        
        report = {
            'report_period': f'{days}日間',
            'generated_at': end_time.isoformat(),
            'summary': {
                'total_validations': len(quality_data),
                'average_score': self._calculate_average_score(quality_data),
                'success_rate': self._calculate_success_rate(quality_data),
                'total_errors': len(error_data),
                'error_rate': len(error_data) / max(len(quality_data), 1),
                'average_response_time': self._calculate_average_response_time(performance_data)
            },
            'quality_trends': self._analyze_quality_trends(quality_data),
            'error_analysis': self._analyze_error_patterns(error_data),
            'performance_analysis': self._analyze_performance_trends(performance_data),
            'recommendations': self._generate_recommendations(quality_data, error_data, performance_data),
            'alerts': self._check_alert_conditions(quality_data, error_data, performance_data)
        }
        
        # レポート保存
        report_path = self.monitor_dir / f"品質レポート_{end_time.strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report
    
    def display_dashboard(self):
        """リアルタイム監視ダッシュボード表示"""
        print("📊 システム監視ダッシュボード")
        print("=" * 60)
        
        # 過去24時間のデータ取得
        report = self.generate_quality_report(1)
        summary = report['summary']
        
        # メトリクス表示
        print(f"📈 過去24時間の統計:")
        print(f"   検証実行回数: {summary['total_validations']}回")
        print(f"   平均品質スコア: {summary['average_score']:.1f}/100")
        print(f"   成功率: {summary['success_rate']:.1%}")
        print(f"   エラー発生率: {summary['error_rate']:.1%}")
        print(f"   平均応答時間: {summary['average_response_time']:.2f}秒")
        print()
        
        # 品質状態判定
        overall_health = self._assess_system_health(summary)
        health_emoji = "🟢" if overall_health == "良好" else "🟡" if overall_health == "注意" else "🔴"
        print(f"{health_emoji} システム状態: {overall_health}")
        print()
        
        # アラート表示
        alerts = report['alerts']
        if alerts:
            print("🚨 アラート:")
            for alert in alerts:
                print(f"   ⚠️ {alert}")
            print()
        else:
            print("✅ アラートなし")
            print()
        
        # 推奨事項表示
        recommendations = report['recommendations']
        if recommendations:
            print("💡 推奨改善事項:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"   {i}. {rec}")
        else:
            print("✅ 改善事項なし")
    
    def auto_health_check(self) -> bool:
        """自動ヘルスチェック"""
        print("🔍 システム自動ヘルスチェック実行中...")
        
        try:
            # WordPress API接続確認
            from WordPress連携API import WordPressBlogAutomator
            wp = WordPressBlogAutomator()
            api_healthy = wp.test_connection()
            
            # カテゴリデータ確認
            categories = wp.get_categories()
            categories_healthy = len(categories) > 0
            
            # ファイルシステム確認
            dirs_to_check = [
                "/Users/satoumasamitsu/Desktop/osigoto/ブログ自動化/WordPress投稿下書き/記事データ保存_JSON",
                "/Users/satoumasamitsu/Desktop/osigoto/ブログ自動化/システム監視データ"
            ]
            filesystem_healthy = all(os.path.exists(dir_path) for dir_path in dirs_to_check)
            
            # 総合判定
            overall_healthy = api_healthy and categories_healthy and filesystem_healthy
            
            # 結果記録
            health_status = {
                'wordpress_api': api_healthy,
                'categories_data': categories_healthy,
                'filesystem': filesystem_healthy,
                'overall': overall_healthy
            }
            
            self.log_performance(
                'health_check', 
                time.time(), 
                overall_healthy, 
                health_status
            )
            
            # 結果表示
            status_emoji = "✅" if overall_healthy else "❌"
            print(f"{status_emoji} ヘルスチェック結果: {'正常' if overall_healthy else '異常'}")
            
            if not overall_healthy:
                if not api_healthy:
                    print("   ⚠️ WordPress API接続に問題があります")
                if not categories_healthy:
                    print("   ⚠️ カテゴリデータ取得に問題があります")
                if not filesystem_healthy:
                    print("   ⚠️ ファイルシステムに問題があります")
            
            return overall_healthy
            
        except Exception as e:
            self.log_error('health_check_failed', str(e))
            print(f"❌ ヘルスチェック失敗: {e}")
            return False
    
    # プライベートメソッド
    def _generate_article_id(self, article_data: Dict) -> str:
        """記事ID生成"""
        import hashlib
        content = f"{article_data.get('title', '')}{article_data.get('main_keyword', '')}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def _count_issues(self, validation_result: Dict) -> int:
        """問題数カウント"""
        count = 0
        validations = validation_result.get('validations', {})
        for field_validation in validations.values():
            count += len(field_validation.get('issues', []))
        return count
    
    def _count_suggestions(self, validation_result: Dict) -> int:
        """提案数カウント"""
        count = 0
        validations = validation_result.get('validations', {})
        for field_validation in validations.values():
            count += len(field_validation.get('suggestions', []))
        return count
    
    def _append_to_log(self, log_path: Path, entry: Dict):
        """ログファイルに追記"""
        logs = []
        if log_path.exists():
            try:
                with open(log_path, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        logs.append(entry)
        
        # 最新1000件のみ保持
        if len(logs) > 1000:
            logs = logs[-1000:]
        
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    
    def _classify_error_severity(self, error_type: str, error_message: str) -> str:
        """エラー重要度分類"""
        critical_keywords = ['connection', 'api', 'authentication', 'file']
        warning_keywords = ['validation', 'format', 'timeout']
        
        error_text = f"{error_type} {error_message}".lower()
        
        if any(keyword in error_text for keyword in critical_keywords):
            return 'critical'
        elif any(keyword in error_text for keyword in warning_keywords):
            return 'warning'
        else:
            return 'info'
    
    def _grade_performance(self, duration: float, success: bool) -> str:
        """パフォーマンス評価"""
        if not success:
            return 'F'
        elif duration < 5:
            return 'A'
        elif duration < 15:
            return 'B'
        elif duration < 30:
            return 'C'
        else:
            return 'D'
    
    def _monitor_quality_trends(self, log_entry: Dict):
        """品質傾向監視"""
        score = log_entry['overall_score']
        if score < self.quality_standards['score_threshold']:
            if self.alerts['quality_decline']:
                print(f"🟡 品質低下アラート: スコア{score}/100 (基準: {self.quality_standards['score_threshold']}以上)")
    
    def _monitor_error_trends(self, error_entry: Dict):
        """エラー傾向監視"""
        if error_entry['severity'] == 'critical':
            if self.alerts['error_spike']:
                print(f"🔴 重要エラーアラート: {error_entry['error_type']}")
    
    def _monitor_performance_trends(self, perf_entry: Dict):
        """パフォーマンス監視"""
        if perf_entry['duration'] > self.quality_standards['response_time_threshold']:
            if self.alerts['performance_issue']:
                print(f"🟡 パフォーマンス警告: 応答時間{perf_entry['duration']:.2f}秒")
    
    def _load_log_data(self, log_path: Path, start_time: datetime, end_time: datetime) -> List[Dict]:
        """ログデータ読み込み（期間指定）"""
        if not log_path.exists():
            return []
        
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                all_logs = json.load(f)
            
            filtered_logs = []
            for log in all_logs:
                log_time = datetime.fromisoformat(log['timestamp'])
                if start_time <= log_time <= end_time:
                    filtered_logs.append(log)
            
            return filtered_logs
        except:
            return []
    
    def _calculate_average_score(self, quality_data: List[Dict]) -> float:
        """平均スコア計算"""
        if not quality_data:
            return 0.0
        
        total_score = sum(log.get('overall_score', 0) for log in quality_data)
        return total_score / len(quality_data)
    
    def _calculate_success_rate(self, quality_data: List[Dict]) -> float:
        """成功率計算"""
        if not quality_data:
            return 0.0
        
        success_count = sum(1 for log in quality_data if log.get('overall_valid', False))
        return success_count / len(quality_data)
    
    def _calculate_average_response_time(self, performance_data: List[Dict]) -> float:
        """平均応答時間計算"""
        if not performance_data:
            return 0.0
        
        total_time = sum(log.get('duration', 0) for log in performance_data)
        return total_time / len(performance_data)
    
    def _analyze_quality_trends(self, quality_data: List[Dict]) -> Dict:
        """品質傾向分析"""
        if not quality_data:
            return {'trend': 'no_data'}
        
        scores = [log.get('overall_score', 0) for log in quality_data]
        recent_scores = scores[-5:] if len(scores) >= 5 else scores
        
        if len(recent_scores) >= 2:
            trend = 'improving' if recent_scores[-1] > recent_scores[0] else 'declining'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'min_score': min(scores),
            'max_score': max(scores),
            'recent_average': sum(recent_scores) / len(recent_scores)
        }
    
    def _analyze_error_patterns(self, error_data: List[Dict]) -> Dict:
        """エラーパターン分析"""
        if not error_data:
            return {'most_common': 'none'}
        
        error_types = {}
        for error in error_data:
            error_type = error.get('error_type', 'unknown')
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        most_common = max(error_types.items(), key=lambda x: x[1])
        
        return {
            'most_common': most_common[0],
            'most_common_count': most_common[1],
            'unique_error_types': len(error_types)
        }
    
    def _analyze_performance_trends(self, performance_data: List[Dict]) -> Dict:
        """パフォーマンス傾向分析"""
        if not performance_data:
            return {'trend': 'no_data'}
        
        durations = [log.get('duration', 0) for log in performance_data]
        recent_durations = durations[-5:] if len(durations) >= 5 else durations
        
        return {
            'average_duration': sum(durations) / len(durations),
            'recent_average': sum(recent_durations) / len(recent_durations),
            'performance_grade_distribution': self._calculate_grade_distribution(performance_data)
        }
    
    def _calculate_grade_distribution(self, performance_data: List[Dict]) -> Dict:
        """パフォーマンス評価分布計算"""
        grades = {}
        for log in performance_data:
            grade = log.get('performance_grade', 'F')
            grades[grade] = grades.get(grade, 0) + 1
        return grades
    
    def _generate_recommendations(self, quality_data: List[Dict], error_data: List[Dict], performance_data: List[Dict]) -> List[str]:
        """改善推奨事項生成"""
        recommendations = []
        
        # 品質分析
        if quality_data:
            avg_score = self._calculate_average_score(quality_data)
            if avg_score < 85:
                recommendations.append("品質スコア向上のため、SEO基準の見直しを推奨")
        
        # エラー分析
        if len(error_data) > 5:
            recommendations.append("エラー発生頻度が高いため、システムの安定性改善を推奨")
        
        # パフォーマンス分析
        if performance_data:
            avg_time = self._calculate_average_response_time(performance_data)
            if avg_time > 20:
                recommendations.append("応答時間改善のため、処理最適化を推奨")
        
        return recommendations
    
    def _check_alert_conditions(self, quality_data: List[Dict], error_data: List[Dict], performance_data: List[Dict]) -> List[str]:
        """アラート条件チェック"""
        alerts = []
        
        # 品質アラート
        if quality_data:
            recent_scores = [log.get('overall_score', 0) for log in quality_data[-3:]]
            if all(score < 70 for score in recent_scores):
                alerts.append("品質スコアの継続的低下を検出")
        
        # エラーアラート
        if len(error_data) > 10:
            alerts.append("エラー発生率が基準を超過")
        
        # パフォーマンスアラート
        if performance_data:
            recent_times = [log.get('duration', 0) for log in performance_data[-3:]]
            if all(time > 30 for time in recent_times):
                alerts.append("応答時間の継続的悪化を検出")
        
        return alerts
    
    def _assess_system_health(self, summary: Dict) -> str:
        """システム健全性評価"""
        score = summary['average_score']
        success_rate = summary['success_rate']
        error_rate = summary['error_rate']
        
        if score >= 85 and success_rate >= 0.9 and error_rate <= 0.05:
            return "良好"
        elif score >= 70 and success_rate >= 0.8 and error_rate <= 0.1:
            return "注意"
        else:
            return "要改善"

# CLI実行対応
def main():
    """メイン実行関数"""
    monitor = システム監視品質管理()
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python システム監視・品質管理.py [dashboard|health-check|report]")
        return
    
    command = sys.argv[1]
    
    if command == 'dashboard':
        monitor.display_dashboard()
    elif command == 'health-check':
        monitor.auto_health_check()
    elif command == 'report':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        report = monitor.generate_quality_report(days)
        print(f"📊 {days}日間の品質レポートを生成しました")
    else:
        print("❌ 不正なコマンドです")

if __name__ == "__main__":
    main()