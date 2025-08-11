"""
レース結果確認システム
前日の予想的中率を確認し、学習用データとして保存
"""

import json
import os
from datetime import datetime, timedelta
import random

class ResultVerificationSystem:
    """レース結果確認・分析システム"""
    
    def __init__(self):
        self.data_dir = "../データ管理"
        self.prediction_accuracy = {
            'total_predictions': 0,
            'correct_predictions': 0,
            'accuracy_rate': 0.0
        }
    
    def get_previous_day_results(self, race_type='競馬'):
        """前日のレース結果を取得"""
        
        yesterday = datetime.now() - timedelta(days=1)
        date_str = yesterday.strftime('%Y-%m-%d')
        
        # 実際の実装では公式サイトやAPIから結果取得
        # 現在はサンプルデータ生成
        results = self._generate_sample_results(date_str, race_type)
        
        return {
            'date': date_str,
            'race_type': race_type,
            'results': results
        }
    
    def _generate_sample_results(self, date_str, race_type):
        """サンプル結果データ生成"""
        
        if race_type == '競馬':
            return self._generate_horse_racing_results()
        elif race_type == '競艇':
            return self._generate_boat_racing_results()
        elif race_type == '競輪':
            return self._generate_bicycle_racing_results()
        elif race_type == 'オートレース':
            return self._generate_auto_racing_results()
        
        return []
    
    def _generate_horse_racing_results(self):
        """競馬結果生成"""
        
        results = []
        venues = ['東京', '阪神', '中山']
        
        for venue in venues:
            race_count = random.randint(8, 12)
            
            for race_num in range(1, race_count + 1):
                horse_count = random.randint(12, 18)
                
                # 1着-3着を決定
                winners = random.sample(range(1, horse_count + 1), 3)
                
                result = {
                    'venue': venue,
                    'race_number': race_num,
                    'finish_order': {
                        '1st': winners[0],
                        '2nd': winners[1],
                        '3rd': winners[2]
                    },
                    'winning_odds': round(random.uniform(1.5, 50.0), 1),
                    'track_condition': random.choice(['良', 'やや重', '重', '不良'])
                }
                results.append(result)
        
        return results
    
    def _generate_boat_racing_results(self):
        """競艇結果生成"""
        
        results = []
        venues = ['桐生', '戸田', '江戸川']
        
        for venue in venues:
            for race_num in range(1, 13):  # 12レース
                
                # 1-3着を決定
                winners = random.sample(range(1, 7), 3)
                
                result = {
                    'venue': venue,
                    'race_number': race_num,
                    'finish_order': {
                        '1st': winners[0],
                        '2nd': winners[1],
                        '3rd': winners[2]
                    },
                    'winning_odds': round(random.uniform(1.5, 30.0), 1)
                }
                results.append(result)
        
        return results
    
    def _generate_bicycle_racing_results(self):
        """競輪結果生成"""
        
        results = []
        venue = '立川'
        
        for race_num in range(1, 12):
            winners = random.sample(range(1, 10), 3)
            
            result = {
                'venue': venue,
                'race_number': race_num,
                'finish_order': {
                    '1st': winners[0],
                    '2nd': winners[1],
                    '3rd': winners[2]
                },
                'winning_odds': round(random.uniform(1.8, 25.0), 1)
            }
            results.append(result)
        
        return results
    
    def _generate_auto_racing_results(self):
        """オートレース結果生成"""
        
        results = []
        venue = '川口'
        
        for race_num in range(1, 11):
            winners = random.sample(range(1, 9), 3)
            
            result = {
                'venue': venue,
                'race_number': race_num,
                'finish_order': {
                    '1st': winners[0],
                    '2nd': winners[1],
                    '3rd': winners[2]
                },
                'winning_odds': round(random.uniform(2.0, 20.0), 1)
            }
            results.append(result)
        
        return results
    
    def verify_predictions(self, prediction_data, result_data):
        """予想と結果を照合して的中率を計算"""
        
        verification_results = {
            'date': result_data['date'],
            'race_type': result_data['race_type'],
            'total_races': len(result_data['results']),
            'correct_predictions': 0,
            'accuracy_details': [],
            'learning_factors': []
        }
        
        # 各レースの予想と結果を比較
        for result_race in result_data['results']:
            venue = result_race['venue']
            race_num = result_race['race_number']
            
            # 対応する予想を見つける
            prediction_race = self._find_matching_prediction(
                prediction_data, venue, race_num
            )
            
            if prediction_race:
                is_correct = self._check_prediction_accuracy(
                    prediction_race, result_race
                )
                
                accuracy_detail = {
                    'venue': venue,
                    'race_number': race_num,
                    'predicted': prediction_race.get('predicted_winner', 'N/A'),
                    'actual_winner': result_race['finish_order']['1st'],
                    'is_correct': is_correct,
                    'winning_odds': result_race['winning_odds']
                }
                
                verification_results['accuracy_details'].append(accuracy_detail)
                
                if is_correct:
                    verification_results['correct_predictions'] += 1
                
                # 学習要因を分析
                learning_factor = self._analyze_learning_factors(
                    prediction_race, result_race, is_correct
                )
                verification_results['learning_factors'].append(learning_factor)
        
        # 的中率計算
        if verification_results['total_races'] > 0:
            accuracy_rate = verification_results['correct_predictions'] / verification_results['total_races']
            verification_results['accuracy_rate'] = round(accuracy_rate * 100, 2)
        
        return verification_results
    
    def _find_matching_prediction(self, prediction_data, venue, race_num):
        """予想データから対応するレースを見つける"""
        
        if not prediction_data or 'predictions' not in prediction_data:
            return None
        
        for pred_race in prediction_data['predictions']:
            if (pred_race.get('venue') == venue and 
                pred_race.get('race_number') == race_num):
                return pred_race
        
        return None
    
    def _check_prediction_accuracy(self, prediction_race, result_race):
        """予想的中チェック"""
        
        predicted_winner = prediction_race.get('predicted_winner')
        actual_winner = result_race['finish_order']['1st']
        
        return predicted_winner == actual_winner
    
    def _analyze_learning_factors(self, prediction_race, result_race, is_correct):
        """学習要因分析"""
        
        factors = {
            'venue': result_race['venue'],
            'race_number': result_race['race_number'],
            'is_correct': is_correct,
            'predicted_winner': prediction_race.get('predicted_winner'),
            'actual_winner': result_race['finish_order']['1st'],
            'winning_odds': result_race['winning_odds'],
            'factors': []
        }
        
        # 的中/外れの要因を分析
        if is_correct:
            factors['factors'].append('予想ロジック適切')
            if result_race['winning_odds'] <= 3.0:
                factors['factors'].append('人気馬的中')
            else:
                factors['factors'].append('穴馬的中')
        else:
            factors['factors'].append('予想ミス')
            if result_race['winning_odds'] >= 10.0:
                factors['factors'].append('大穴決着')
            
            # 競馬特有の要因
            if 'track_condition' in result_race:
                track = result_race['track_condition']
                if track in ['重', '不良']:
                    factors['factors'].append('馬場状態悪化影響')
        
        return factors
    
    def generate_learning_summary(self, verification_results):
        """学習サマリー生成"""
        
        summary = {
            'date': verification_results['date'],
            'overall_accuracy': verification_results['accuracy_rate'],
            'total_races': verification_results['total_races'],
            'correct_count': verification_results['correct_predictions'],
            'key_learnings': [],
            'improvement_suggestions': []
        }
        
        # 学習ポイント抽出
        correct_factors = []
        incorrect_factors = []
        
        for factor in verification_results['learning_factors']:
            if factor['is_correct']:
                correct_factors.extend(factor['factors'])
            else:
                incorrect_factors.extend(factor['factors'])
        
        # 成功要因
        if correct_factors:
            summary['key_learnings'].append({
                'type': '成功要因',
                'factors': list(set(correct_factors))
            })
        
        # 失敗要因
        if incorrect_factors:
            summary['key_learnings'].append({
                'type': '失敗要因', 
                'factors': list(set(incorrect_factors))
            })
        
        # 改善提案
        accuracy_rate = verification_results['accuracy_rate']
        
        if accuracy_rate < 30:
            summary['improvement_suggestions'].append('予想ロジックの基本見直しが必要')
        elif accuracy_rate < 50:
            summary['improvement_suggestions'].append('重み付けの調整を検討')
        else:
            summary['improvement_suggestions'].append('現在のロジックを維持')
        
        return summary
    
    def save_verification_results(self, verification_results):
        """検証結果を保存"""
        
        date_str = datetime.now().strftime('%Y%m%d')
        filename = f"検証結果_{verification_results['race_type']}_{date_str}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(verification_results, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 検証結果保存完了: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ 検証結果保存エラー: {e}")
            return None

# テスト実行用
if __name__ == "__main__":
    print("🔍 結果確認システムテスト開始...")
    
    verifier = ResultVerificationSystem()
    
    # サンプル結果データ取得
    print("\n📊 前日の競馬結果取得:")
    results = verifier.get_previous_day_results('競馬')
    print(f"結果レース数: {len(results['results'])}")
    
    # サンプル予想データ（実際は保存された予想データを読み込み）
    sample_predictions = {
        'predictions': [
            {
                'venue': '東京',
                'race_number': 1,
                'predicted_winner': random.randint(1, 15)
            }
        ]
    }
    
    # 予想検証
    verification = verifier.verify_predictions(sample_predictions, results)
    print(f"\n🎯 検証結果:")
    print(f"的中率: {verification['accuracy_rate']}%")
    print(f"的中数: {verification['correct_predictions']}/{verification['total_races']}")
    
    # 学習サマリー生成
    learning_summary = verifier.generate_learning_summary(verification)
    print(f"\n📈 学習サマリー:")
    print(f"全体的中率: {learning_summary['overall_accuracy']}%")
    
    # 結果保存
    verifier.save_verification_results(verification)
    
    print("\n✅ 結果確認システムテスト完了")