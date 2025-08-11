"""
毎日自動実行システム
365日継続的に競馬予想記事を生成・学習するメインシステム
"""

import sys
import os
from datetime import datetime, timedelta
import json
import traceback

# パス追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 各システムをインポート
from データ収集.天気取得システム import WeatherDataCollector
from データ収集.レース情報取得 import RaceDataCollector
from データ収集.結果確認システム import ResultVerificationSystem
from 予想エンジン.基本予想ロジック import BasicPredictionEngine
from 予想エンジン.学習アルゴリズム import LearningAlgorithm
from 記事生成.note記事生成 import NoteArticleGenerator
from 記事生成.X投稿文生成 import TwitterPostGenerator
from データ管理.1週間データ保持 import WeeklyDataManager

class DailyAutomationSystem:
    """毎日自動実行システム"""
    
    def __init__(self):
        # 各システムコンポーネントを初期化
        self.weather_collector = WeatherDataCollector()
        self.race_collector = RaceDataCollector()
        self.result_verifier = ResultVerificationSystem()
        self.prediction_engine = BasicPredictionEngine()
        self.learning_system = LearningAlgorithm()
        self.note_generator = NoteArticleGenerator()
        self.twitter_generator = TwitterPostGenerator()
        self.data_manager = WeeklyDataManager("../データ管理")
        
        # 実行ログ
        self.execution_log = []
        
        # 対象競技
        self.race_types = ['競馬']  # 後で競艇等も追加可能
    
    def execute_daily_workflow(self, race_type='競馬'):
        """毎日のワークフロー実行"""
        
        start_time = datetime.now()
        self.log_message("🚀 毎日自動実行開始", "info")
        
        try:
            # 1. 前日結果の確認と学習
            self.log_message("📊 前日結果確認・学習フェーズ", "info")
            learning_result = self._execute_learning_phase(race_type)
            
            # 2. 翌日データ収集
            self.log_message("📡 翌日データ収集フェーズ", "info")
            data_collection_result = self._execute_data_collection(race_type)
            
            # 3. 予想生成
            self.log_message("🤖 予想生成フェーズ", "info")
            prediction_result = self._execute_prediction_phase(
                data_collection_result, race_type
            )
            
            # 4. 記事・投稿文生成
            self.log_message("📝 コンテンツ生成フェーズ", "info")
            content_result = self._execute_content_generation(
                prediction_result, data_collection_result, race_type
            )
            
            # 5. データ管理・クリーンアップ
            self.log_message("🧹 データ管理フェーズ", "info")
            cleanup_result = self._execute_data_management()
            
            # 6. 実行結果サマリー
            execution_time = (datetime.now() - start_time).total_seconds()
            summary = self._generate_execution_summary(
                learning_result, data_collection_result, prediction_result,
                content_result, cleanup_result, execution_time
            )
            
            self.log_message("✅ 毎日自動実行完了", "success")
            return summary
            
        except Exception as e:
            self.log_message(f"❌ 実行エラー: {str(e)}", "error")
            self.log_message(f"詳細: {traceback.format_exc()}", "error")
            return self._generate_error_summary(str(e), start_time)
    
    def _execute_learning_phase(self, race_type):
        """学習フェーズ実行"""
        
        try:
            # 前日結果取得
            results = self.result_verifier.get_previous_day_results(race_type)
            self.log_message(f"前日結果取得: {len(results['results'])}レース", "info")
            
            # 学習実行（予想エンジンの重み調整）
            learning_report = self.learning_system.execute_learning_cycle(
                self.prediction_engine
            )
            self.log_message(f"学習完了: 的中率 {learning_report['learning_summary']['overall_accuracy']}%", "info")
            
            return {
                'status': 'success',
                'results_count': len(results['results']),
                'accuracy_rate': learning_report['learning_summary']['overall_accuracy'],
                'weight_adjustments': len(learning_report['weight_adjustments'])
            }
            
        except Exception as e:
            self.log_message(f"学習フェーズエラー: {e}", "error")
            return {
                'status': 'error',
                'error': str(e),
                'results_count': 0,
                'accuracy_rate': 0
            }
    
    def _execute_data_collection(self, race_type):
        """データ収集フェーズ実行"""
        
        try:
            # 天気データ取得
            weather_data = self.weather_collector.get_multiple_locations_weather(
                ["東京", "阪神", "中山"], 1  # 明日の天気
            )
            self.log_message(f"天気データ取得: {len(weather_data)}会場", "info")
            
            # レースデータ取得
            race_data = self.race_collector.get_tomorrow_races(race_type)
            self.log_message(f"レースデータ取得: {race_data['total_races']}レース", "info")
            
            # データ保存
            weather_file = self.weather_collector.save_weather_data(weather_data)
            race_file = self.race_collector.save_race_data(race_data)
            
            return {
                'status': 'success',
                'weather_data': weather_data,
                'race_data': race_data,
                'weather_venues': len(weather_data),
                'total_races': race_data['total_races'],
                'saved_files': [weather_file, race_file]
            }
            
        except Exception as e:
            self.log_message(f"データ収集エラー: {e}", "error")
            return {
                'status': 'error',
                'error': str(e),
                'weather_venues': 0,
                'total_races': 0
            }
    
    def _execute_prediction_phase(self, data_collection_result, race_type):
        """予想フェーズ実行"""
        
        try:
            if data_collection_result['status'] != 'success':
                raise Exception("データ収集に失敗したため予想を中断")
            
            # 予想実行
            race_data = data_collection_result['race_data']
            weather_data = data_collection_result['weather_data']
            
            predictions = self.prediction_engine.predict_race_winners(
                race_data, weather_data
            )
            self.log_message(f"予想生成: {predictions['total_predictions']}レース", "info")
            
            # 予想データ保存
            date_str = datetime.now().strftime('%Y%m%d')
            prediction_file = f"../データ管理/予想データ_{race_type}_{date_str}.json"
            
            with open(prediction_file, 'w', encoding='utf-8') as f:
                json.dump(predictions, f, ensure_ascii=False, indent=2)
            
            self.log_message(f"予想データ保存: {prediction_file}", "info")
            
            return {
                'status': 'success',
                'predictions': predictions,
                'prediction_count': predictions['total_predictions'],
                'main_races': len([p for p in predictions['predictions'] 
                                 if p.get('race_number', 0) >= 10]),
                'saved_file': prediction_file
            }
            
        except Exception as e:
            self.log_message(f"予想フェーズエラー: {e}", "error")
            return {
                'status': 'error',
                'error': str(e),
                'prediction_count': 0
            }
    
    def _execute_content_generation(self, prediction_result, data_collection_result, race_type):
        """コンテンツ生成フェーズ実行"""
        
        try:
            if prediction_result['status'] != 'success':
                raise Exception("予想生成に失敗したためコンテンツ生成を中断")
            
            predictions = prediction_result['predictions']
            weather_data = data_collection_result.get('weather_data')
            
            # note記事生成
            note_article = self.note_generator.generate_full_article(
                predictions, weather_data, race_type
            )
            
            # note記事保存
            note_file = self.note_generator.save_article(note_article)
            self.log_message(f"note記事生成: {note_article['word_count']}文字", "info")
            
            # Twitter投稿文生成
            twitter_posts = self.twitter_generator.generate_multiple_posts(
                predictions, "[note記事URL]", race_type
            )
            
            # Twitter投稿文保存
            twitter_file = self.twitter_generator.save_posts(twitter_posts)
            self.log_message(f"X投稿文生成: {twitter_posts['total_posts']}投稿", "info")
            
            return {
                'status': 'success',
                'note_article': {
                    'title': note_article['title'],
                    'word_count': note_article['word_count'],
                    'price': note_article['price'],
                    'file': note_file
                },
                'twitter_posts': {
                    'total_posts': twitter_posts['total_posts'],
                    'file': twitter_file
                }
            }
            
        except Exception as e:
            self.log_message(f"コンテンツ生成エラー: {e}", "error")
            return {
                'status': 'error',
                'error': str(e),
                'note_article': None,
                'twitter_posts': None
            }
    
    def _execute_data_management(self):
        """データ管理フェーズ実行"""
        
        try:
            # 古いファイル削除
            cleanup_result = self.data_manager.schedule_daily_cleanup()
            
            self.log_message(
                f"データクリーンアップ: {cleanup_result['deleted_count']}ファイル削除", 
                "info"
            )
            
            return {
                'status': 'success',
                'deleted_files': cleanup_result['deleted_count'],
                'space_freed': cleanup_result['space_freed']
            }
            
        except Exception as e:
            self.log_message(f"データ管理エラー: {e}", "error")
            return {
                'status': 'error',
                'error': str(e),
                'deleted_files': 0
            }
    
    def _generate_execution_summary(self, learning_result, data_result, 
                                  prediction_result, content_result, 
                                  cleanup_result, execution_time):
        """実行サマリー生成"""
        
        summary = {
            'execution_date': datetime.now().isoformat(),
            'execution_time_seconds': execution_time,
            'overall_status': 'success',
            'phases': {
                'learning': learning_result,
                'data_collection': data_result,
                'prediction': prediction_result,
                'content_generation': content_result,
                'data_management': cleanup_result
            },
            'key_metrics': {
                'races_analyzed': prediction_result.get('prediction_count', 0),
                'articles_generated': 1 if content_result.get('note_article') else 0,
                'posts_generated': content_result.get('twitter_posts', {}).get('total_posts', 0),
                'files_cleaned': cleanup_result.get('deleted_files', 0)
            }
        }
        
        # エラーチェック
        error_phases = []
        for phase_name, result in summary['phases'].items():
            if result.get('status') == 'error':
                error_phases.append(phase_name)
        
        if error_phases:
            summary['overall_status'] = 'partial_success'
            summary['error_phases'] = error_phases
        
        return summary
    
    def _generate_error_summary(self, error_message, start_time):
        """エラーサマリー生成"""
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return {
            'execution_date': datetime.now().isoformat(),
            'execution_time_seconds': execution_time,
            'overall_status': 'error',
            'error_message': error_message,
            'phases': {},
            'key_metrics': {
                'races_analyzed': 0,
                'articles_generated': 0,
                'posts_generated': 0,
                'files_cleaned': 0
            }
        }
    
    def log_message(self, message, level="info"):
        """ログメッセージ記録"""
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message
        }
        
        self.execution_log.append(log_entry)
        
        # コンソール出力
        level_emoji = {
            'info': 'ℹ️',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌'
        }
        
        print(f"{level_emoji.get(level, 'ℹ️')} {message}")
    
    def save_execution_log(self, summary):
        """実行ログ保存"""
        
        log_data = {
            'summary': summary,
            'detailed_log': self.execution_log
        }
        
        date_str = datetime.now().strftime('%Y%m%d')
        log_file = f"../データ管理/実行ログ_{date_str}.json"
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2)
            
            self.log_message(f"実行ログ保存: {log_file}", "success")
            return log_file
            
        except Exception as e:
            self.log_message(f"ログ保存エラー: {e}", "error")
            return None
    
    def run_test_mode(self):
        """テストモード実行"""
        
        self.log_message("🧪 テストモード実行", "info")
        
        # 簡易テスト実行
        test_summary = {
            'test_date': datetime.now().isoformat(),
            'test_results': {
                'weather_system': self._test_weather_system(),
                'race_system': self._test_race_system(),
                'prediction_system': self._test_prediction_system(),
                'content_system': self._test_content_system()
            }
        }
        
        return test_summary
    
    def _test_weather_system(self):
        try:
            weather = self.weather_collector.get_weather_forecast("東京", 1)
            return {'status': 'ok', 'location': weather['location']}
        except:
            return {'status': 'error'}
    
    def _test_race_system(self):
        try:
            races = self.race_collector.get_tomorrow_races('競馬')
            return {'status': 'ok', 'race_count': races['total_races']}
        except:
            return {'status': 'error'}
    
    def _test_prediction_system(self):
        try:
            # ダミーデータでテスト
            dummy_data = {
                'date': '2025-08-08',
                'race_type': '競馬',
                'races': [{'venue': 'テスト', 'race_number': 1, 'horses': []}]
            }
            predictions = self.prediction_engine.predict_race_winners(dummy_data)
            return {'status': 'ok', 'prediction_count': predictions['total_predictions']}
        except:
            return {'status': 'error'}
    
    def _test_content_system(self):
        try:
            # ダミーデータでテスト
            dummy_predictions = {
                'date': '2025-08-08',
                'predictions': [{'venue': 'テスト', 'race_number': 11}]
            }
            article = self.note_generator.generate_full_article(dummy_predictions)
            return {'status': 'ok', 'word_count': article['word_count']}
        except:
            return {'status': 'error'}

# メイン実行
def main():
    """メイン関数"""
    
    print("🎯 競馬予想システム - 毎日自動実行")
    print("=" * 50)
    
    # システム初期化
    automation = DailyAutomationSystem()
    
    # 実行モード選択（実際の運用では自動実行）
    mode = "production"  # or "test"
    
    if mode == "test":
        # テストモード
        test_result = automation.run_test_mode()
        print(f"\n🧪 テスト結果: {json.dumps(test_result, ensure_ascii=False, indent=2)}")
    
    else:
        # 本番実行
        summary = automation.execute_daily_workflow('競馬')
        
        # ログ保存
        log_file = automation.save_execution_log(summary)
        
        # 結果表示
        print(f"\n📊 実行結果サマリー:")
        print(f"- 実行状況: {summary['overall_status']}")
        print(f"- 実行時間: {summary['execution_time_seconds']:.1f}秒")
        print(f"- 分析レース数: {summary['key_metrics']['races_analyzed']}")
        print(f"- 生成記事数: {summary['key_metrics']['articles_generated']}")
        print(f"- 生成投稿数: {summary['key_metrics']['posts_generated']}")
        print(f"- 削除ファイル数: {summary['key_metrics']['files_cleaned']}")
        
        if summary['overall_status'] == 'success':
            print("\n🎉 全フェーズ正常完了！")
        else:
            print(f"\n⚠️ 一部フェーズでエラー発生")

if __name__ == "__main__":
    main()