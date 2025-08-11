"""
学習アルゴリズムシステム
1週間のデータを基に予想精度を向上させる機械学習システム
"""

import json
import os
from datetime import datetime, timedelta
# import numpy as np  # numpyなしで実装

class LearningAlgorithm:
    """軽量学習アルゴリズム（1週間データベース）"""
    
    def __init__(self):
        self.data_dir = "../データ管理"
        self.learning_history = []
        self.weight_adjustments = {
            'odds_weight': 0.0,
            'form_weight': 0.0,
            'weather_weight': 0.0,
            'jockey_weight': 0.0
        }
        
        # 学習パラメータ
        self.learning_rate = 0.1
        self.min_accuracy_threshold = 0.25  # 25%以下なら大幅調整
        self.target_accuracy = 0.45  # 目標45%
    
    def load_recent_data(self, days=7):
        """直近N日間のデータを読み込み"""
        
        recent_data = {
            'predictions': [],
            'results': [],
            'verifications': []
        }
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i+1)
            date_str = date.strftime('%Y%m%d')
            
            # 予想データ読み込み
            prediction_file = os.path.join(self.data_dir, f"予想データ_競馬_{date_str}.json")
            if os.path.exists(prediction_file):
                with open(prediction_file, 'r', encoding='utf-8') as f:
                    pred_data = json.load(f)
                    recent_data['predictions'].append(pred_data)
            
            # 検証結果読み込み
            verification_file = os.path.join(self.data_dir, f"検証結果_競馬_{date_str}.json")
            if os.path.exists(verification_file):
                with open(verification_file, 'r', encoding='utf-8') as f:
                    verify_data = json.load(f)
                    recent_data['verifications'].append(verify_data)
        
        return recent_data
    
    def analyze_prediction_patterns(self, recent_data):
        """予想パターンの分析"""
        
        analysis = {
            'total_predictions': 0,
            'total_correct': 0,
            'overall_accuracy': 0.0,
            'accuracy_by_odds_range': {},
            'accuracy_by_venue': {},
            'successful_factors': [],
            'failed_factors': []
        }
        
        odds_ranges = {
            'favorite': (0, 3.0),      # 人気馬
            'mid_range': (3.1, 8.0),   # 中位人気
            'longshot': (8.1, 99.9)    # 穴馬
        }
        
        venue_stats = {}
        odds_stats = {range_name: {'total': 0, 'correct': 0} for range_name in odds_ranges}
        
        # 検証データから統計取得
        for verification in recent_data['verifications']:
            analysis['total_predictions'] += verification['total_races']
            analysis['total_correct'] += verification['correct_predictions']
            
            # 詳細分析
            for detail in verification['accuracy_details']:
                venue = detail['venue']
                odds = detail['winning_odds']
                is_correct = detail['is_correct']
                
                # 会場別統計
                if venue not in venue_stats:
                    venue_stats[venue] = {'total': 0, 'correct': 0}
                venue_stats[venue]['total'] += 1
                if is_correct:
                    venue_stats[venue]['correct'] += 1
                
                # オッズ範囲別統計
                for range_name, (min_odds, max_odds) in odds_ranges.items():
                    if min_odds <= odds <= max_odds:
                        odds_stats[range_name]['total'] += 1
                        if is_correct:
                            odds_stats[range_name]['correct'] += 1
                        break
        
        # 精度計算
        if analysis['total_predictions'] > 0:
            analysis['overall_accuracy'] = analysis['total_correct'] / analysis['total_predictions']
        
        # 会場別精度
        for venue, stats in venue_stats.items():
            if stats['total'] > 0:
                accuracy = stats['correct'] / stats['total']
                analysis['accuracy_by_venue'][venue] = {
                    'accuracy': accuracy,
                    'total_races': stats['total']
                }
        
        # オッズ範囲別精度
        for range_name, stats in odds_stats.items():
            if stats['total'] > 0:
                accuracy = stats['correct'] / stats['total']
                analysis['accuracy_by_odds_range'][range_name] = {
                    'accuracy': accuracy,
                    'total_predictions': stats['total']
                }
        
        return analysis
    
    def identify_improvement_areas(self, analysis):
        """改善すべき領域を特定"""
        
        improvements = []
        
        overall_acc = analysis['overall_accuracy']
        
        # 全体的中率に基づく改善提案
        if overall_acc < self.min_accuracy_threshold:
            improvements.append({
                'area': 'overall_strategy',
                'priority': 'critical',
                'suggestion': '予想ロジック全体の見直しが必要',
                'action': 'major_weight_adjustment'
            })
        elif overall_acc < self.target_accuracy:
            improvements.append({
                'area': 'weight_tuning',
                'priority': 'high',
                'suggestion': '重み付けの微調整が必要',
                'action': 'minor_weight_adjustment'
            })
        
        # オッズ範囲別分析
        odds_analysis = analysis['accuracy_by_odds_range']
        
        if 'favorite' in odds_analysis:
            fav_acc = odds_analysis['favorite']['accuracy']
            if fav_acc < 0.6:  # 人気馬的中率が60%未満
                improvements.append({
                    'area': 'favorite_selection',
                    'priority': 'high',
                    'suggestion': '人気馬の選別精度向上が必要',
                    'action': 'increase_odds_weight'
                })
        
        if 'longshot' in odds_analysis:
            long_acc = odds_analysis['longshot']['accuracy']
            if long_acc > 0.3:  # 穴馬的中率が30%超
                improvements.append({
                    'area': 'longshot_strategy',
                    'priority': 'medium',
                    'suggestion': '穴馬選別が良好、戦略維持',
                    'action': 'maintain_current_weights'
                })
        
        # 会場別分析
        venue_analysis = analysis['accuracy_by_venue']
        poor_venues = []
        
        for venue, stats in venue_analysis.items():
            if stats['accuracy'] < 0.3 and stats['total_races'] >= 3:
                poor_venues.append(venue)
        
        if poor_venues:
            improvements.append({
                'area': 'venue_specific',
                'priority': 'medium',
                'suggestion': f'特定会場({", ".join(poor_venues)})の対策必要',
                'action': 'venue_specific_adjustment'
            })
        
        return improvements
    
    def adjust_weights(self, improvements, current_weights):
        """重み調整実行"""
        
        new_weights = current_weights.copy()
        adjustments_made = []
        
        for improvement in improvements:
            action = improvement['action']
            
            if action == 'major_weight_adjustment':
                # 大幅調整（全体的中率が低い場合）
                new_weights['odds_weight'] = min(0.6, new_weights['odds_weight'] + 0.15)
                new_weights['form_weight'] = max(0.1, new_weights['form_weight'] - 0.1)
                adjustments_made.append('大幅調整: オッズ重視度上昇')
                
            elif action == 'minor_weight_adjustment':
                # 微調整
                new_weights['odds_weight'] += 0.05
                new_weights['form_weight'] -= 0.02
                new_weights['weather_weight'] -= 0.02
                adjustments_made.append('微調整: バランス調整')
                
            elif action == 'increase_odds_weight':
                # 人気重視強化
                new_weights['odds_weight'] = min(0.7, new_weights['odds_weight'] + 0.1)
                new_weights['form_weight'] = max(0.1, new_weights['form_weight'] - 0.05)
                adjustments_made.append('調整: 人気重視強化')
        
        # 重みの合計を1.0に正規化
        total_weight = sum(new_weights.values())
        if total_weight > 0:
            for key in new_weights:
                new_weights[key] = new_weights[key] / total_weight
        
        return new_weights, adjustments_made
    
    def generate_learning_report(self, analysis, improvements, weight_changes):
        """学習レポート生成"""
        
        report = {
            'date': datetime.now().isoformat(),
            'learning_summary': {
                'data_period': '直近7日間',
                'total_predictions': analysis['total_predictions'],
                'total_correct': analysis['total_correct'],
                'overall_accuracy': round(analysis['overall_accuracy'] * 100, 2)
            },
            'performance_analysis': {
                'accuracy_by_venue': analysis['accuracy_by_venue'],
                'accuracy_by_odds': analysis['accuracy_by_odds_range']
            },
            'identified_improvements': improvements,
            'weight_adjustments': weight_changes,
            'next_actions': self._generate_next_actions(analysis, improvements)
        }
        
        return report
    
    def _generate_next_actions(self, analysis, improvements):
        """次のアクション提案"""
        
        actions = []
        
        accuracy = analysis['overall_accuracy']
        
        if accuracy < 0.3:
            actions.append('予想アルゴリズムの根本的見直し')
            actions.append('データ収集方法の改善検討')
        elif accuracy < 0.4:
            actions.append('重み付け調整の継続')
            actions.append('新たな評価要素の追加検討')
        else:
            actions.append('現在の戦略継続')
            actions.append('微調整によるさらなる向上')
        
        return actions
    
    def execute_learning_cycle(self, prediction_engine):
        """学習サイクル実行"""
        
        print("📚 学習サイクル開始...")
        
        # 1. 直近データ読み込み
        recent_data = self.load_recent_data(7)
        print(f"📊 直近7日間のデータ読み込み完了")
        
        # 2. パターン分析
        analysis = self.analyze_prediction_patterns(recent_data)
        print(f"🔍 分析完了 - 全体的中率: {analysis['overall_accuracy']*100:.1f}%")
        
        # 3. 改善領域特定
        improvements = self.identify_improvement_areas(analysis)
        print(f"📋 改善点 {len(improvements)} 項目特定")
        
        # 4. 重み調整
        current_weights = prediction_engine.weights
        new_weights, adjustments = self.adjust_weights(improvements, current_weights)
        
        # 5. 予想エンジンに新しい重みを適用
        prediction_engine.weights = new_weights
        
        # 6. レポート生成
        learning_report = self.generate_learning_report(analysis, improvements, adjustments)
        
        # 7. レポート保存
        self.save_learning_report(learning_report)
        
        print("✅ 学習サイクル完了")
        return learning_report
    
    def save_learning_report(self, report):
        """学習レポート保存"""
        
        date_str = datetime.now().strftime('%Y%m%d')
        filename = f"学習レポート_{date_str}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            print(f"📄 学習レポート保存: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ レポート保存エラー: {e}")
            return None

# テスト実行用
if __name__ == "__main__":
    print("🧠 学習アルゴリズムテスト開始...")
    
    learner = LearningAlgorithm()
    
    # サンプル分析データ
    sample_analysis = {
        'total_predictions': 50,
        'total_correct': 18,
        'overall_accuracy': 0.36,
        'accuracy_by_odds_range': {
            'favorite': {'accuracy': 0.55, 'total_predictions': 20},
            'mid_range': {'accuracy': 0.28, 'total_predictions': 25},
            'longshot': {'accuracy': 0.2, 'total_predictions': 5}
        },
        'accuracy_by_venue': {
            '東京': {'accuracy': 0.42, 'total_races': 12},
            '阪神': {'accuracy': 0.31, 'total_races': 13}
        }
    }
    
    # 改善領域特定テスト
    improvements = learner.identify_improvement_areas(sample_analysis)
    print(f"\n📋 特定された改善点: {len(improvements)}件")
    
    for imp in improvements:
        print(f"- {imp['area']}: {imp['suggestion']}")
    
    # 重み調整テスト
    sample_weights = {
        'odds_weight': 0.4,
        'form_weight': 0.3,
        'weather_weight': 0.2,
        'jockey_weight': 0.1
    }
    
    new_weights, adjustments = learner.adjust_weights(improvements, sample_weights)
    
    print(f"\n⚖️ 重み調整結果:")
    for key, value in new_weights.items():
        print(f"- {key}: {value:.3f}")
    
    print(f"\n📝 調整内容:")
    for adj in adjustments:
        print(f"- {adj}")
    
    print("\n✅ 学習アルゴリズムテスト完了")