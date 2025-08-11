"""
基本予想ロジックシステム
競馬・競艇などの基本的な予想アルゴリズム
"""

import json
import random
from datetime import datetime
import os

class BasicPredictionEngine:
    """基本予想エンジン"""
    
    def __init__(self):
        # 予想重み設定（学習により調整される）
        self.weights = {
            'odds_weight': 0.4,      # オッズ重視度
            'form_weight': 0.3,      # 調子重視度
            'weather_weight': 0.2,   # 天気影響度
            'jockey_weight': 0.1     # 騎手重視度（競馬のみ）
        }
        
        # 競技別特別重み
        self.sport_specific_weights = {
            '競馬': {
                'distance_weight': 0.15,
                'track_condition_weight': 0.25,
                'jockey_experience_weight': 0.2
            },
            '競艇': {
                'motor_performance_weight': 0.3,
                'start_timing_weight': 0.25,
                'water_condition_weight': 0.2
            },
            '競輪': {
                'rank_weight': 0.35,
                'recent_performance_weight': 0.3,
                'course_compatibility_weight': 0.15
            },
            'オートレース': {
                'grade_weight': 0.3,
                'machine_condition_weight': 0.25,
                'experience_weight': 0.2
            }
        }
    
    def predict_race_winners(self, race_data, weather_data=None):
        """レースの勝者予想"""
        
        race_type = race_data.get('race_type', '競馬')
        predictions = []
        
        for race in race_data['races']:
            prediction = self._predict_single_race(race, race_type, weather_data)
            predictions.append(prediction)
        
        return {
            'date': race_data['date'],
            'race_type': race_type,
            'predictions': predictions,
            'total_predictions': len(predictions)
        }
    
    def _predict_single_race(self, race, race_type, weather_data):
        """個別レース予想"""
        
        if race_type == '競馬':
            return self._predict_horse_race(race, weather_data)
        elif race_type == '競艇':
            return self._predict_boat_race(race, weather_data)
        elif race_type == '競輪':
            return self._predict_bicycle_race(race)
        elif race_type == 'オートレース':
            return self._predict_auto_race(race)
        else:
            return self._predict_horse_race(race, weather_data)
    
    def _predict_horse_race(self, race, weather_data):
        """競馬予想ロジック"""
        
        venue = race['venue']
        horses = race['horses']
        
        # 天気情報取得
        weather_info = self._get_weather_for_venue(venue, weather_data)
        track_condition = weather_info.get('track_condition_forecast', '良') if weather_info else '良'
        
        # 各馬のスコア計算
        horse_scores = []
        
        for horse in horses:
            score = self._calculate_horse_score(horse, race, track_condition)
            horse_scores.append({
                'number': horse['number'],
                'name': horse['name'],
                'score': score,
                'odds': horse['odds']
            })
        
        # スコア順ソート
        horse_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # 予想理由生成
        top_horse = horse_scores[0]
        reason = self._generate_horse_prediction_reason(top_horse, race, track_condition)
        
        return {
            'venue': venue,
            'race_number': race['race_number'],
            'race_name': race['race_name'],
            'predicted_winner': top_horse['number'],
            'predicted_horse_name': top_horse['name'],
            'confidence_score': round(top_horse['score'], 2),
            'winning_odds': top_horse['odds'],
            'prediction_reason': reason,
            'top3_predictions': horse_scores[:3],
            'track_condition': track_condition
        }
    
    def _calculate_horse_score(self, horse, race, track_condition):
        """競馬スコア計算"""
        
        score = 0.0
        
        # オッズベース評価（人気度）
        odds_score = max(0, (20 - horse['odds']) / 20) * 100
        score += odds_score * self.weights['odds_weight']
        
        # 調子評価（最近の成績）
        recent_form = horse.get('recent_form', '△△△△△')
        form_score = self._evaluate_form(recent_form) * 100
        score += form_score * self.weights['form_weight']
        
        # 騎手評価
        jockey_score = self._evaluate_jockey(horse.get('jockey', '')) * 100
        score += jockey_score * self.weights['jockey_weight']
        
        # 馬場状態適性
        track_score = self._evaluate_track_compatibility(track_condition) * 100
        score += track_score * self.sport_specific_weights['競馬']['track_condition_weight']
        
        # 距離適性
        distance_score = self._evaluate_distance_compatibility(race.get('distance', 1600)) * 100
        score += distance_score * self.sport_specific_weights['競馬']['distance_weight']
        
        return score
    
    def _predict_boat_race(self, race, weather_data):
        """競艇予想ロジック"""
        
        boats = race['boats']
        venue = race['venue']
        
        # 各艇のスコア計算
        boat_scores = []
        
        for boat in boats:
            score = self._calculate_boat_score(boat, race)
            boat_scores.append({
                'number': boat['number'],
                'racer': boat['racer'],
                'score': score,
                'odds': boat['odds']
            })
        
        # スコア順ソート
        boat_scores.sort(key=lambda x: x['score'], reverse=True)
        
        top_boat = boat_scores[0]
        reason = self._generate_boat_prediction_reason(top_boat, race)
        
        return {
            'venue': venue,
            'race_number': race['race_number'],
            'predicted_winner': top_boat['number'],
            'predicted_racer': top_boat['racer'],
            'confidence_score': round(top_boat['score'], 2),
            'winning_odds': top_boat['odds'],
            'prediction_reason': reason,
            'top3_predictions': boat_scores[:3]
        }
    
    def _calculate_boat_score(self, boat, race):
        """競艇スコア計算"""
        
        score = 0.0
        
        # オッズ評価
        odds_score = max(0, (15 - boat['odds']) / 15) * 100
        score += odds_score * self.weights['odds_weight']
        
        # 最近の成績評価
        recent_form = boat.get('recent_form', '333333')
        form_score = self._evaluate_boat_form(recent_form) * 100
        score += form_score * self.weights['form_weight']
        
        # モーター評価
        motor_score = self._evaluate_motor_performance(boat.get('motor_number', 30)) * 100
        score += motor_score * self.sport_specific_weights['競艇']['motor_performance_weight']
        
        # スタート評価（艇番による傾向）
        start_score = self._evaluate_start_position(boat['number']) * 100
        score += start_score * self.sport_specific_weights['競艇']['start_timing_weight']
        
        return score
    
    def _predict_bicycle_race(self, race):
        """競輪予想ロジック"""
        
        riders = race['riders']
        venue = race['venue']
        
        rider_scores = []
        
        for rider in riders:
            score = self._calculate_bicycle_score(rider, race)
            rider_scores.append({
                'number': rider['number'],
                'name': rider['name'],
                'score': score,
                'odds': rider['odds']
            })
        
        rider_scores.sort(key=lambda x: x['score'], reverse=True)
        
        top_rider = rider_scores[0]
        reason = self._generate_bicycle_prediction_reason(top_rider, race)
        
        return {
            'venue': venue,
            'race_number': race['race_number'],
            'predicted_winner': top_rider['number'],
            'predicted_rider': top_rider['name'],
            'confidence_score': round(top_rider['score'], 2),
            'winning_odds': top_rider['odds'],
            'prediction_reason': reason,
            'top3_predictions': rider_scores[:3]
        }
    
    def _calculate_bicycle_score(self, rider, race):
        """競輪スコア計算"""
        
        score = 0.0
        
        # オッズ評価
        odds_score = max(0, (12 - rider['odds']) / 12) * 100
        score += odds_score * self.weights['odds_weight']
        
        # ランク評価
        rank_score = self._evaluate_bicycle_rank(rider.get('rank', 'A3')) * 100
        score += rank_score * self.sport_specific_weights['競輪']['rank_weight']
        
        # 車番評価（位置による有利不利）
        position_score = self._evaluate_bicycle_position(rider['number']) * 100
        score += position_score * 0.2
        
        return score
    
    def _predict_auto_race(self, race):
        """オートレース予想ロジック"""
        
        riders = race['riders']
        venue = race['venue']
        
        rider_scores = []
        
        for rider in riders:
            score = self._calculate_auto_score(rider, race)
            rider_scores.append({
                'number': rider['number'],
                'name': rider['name'],
                'score': score,
                'odds': rider['odds']
            })
        
        rider_scores.sort(key=lambda x: x['score'], reverse=True)
        
        top_rider = rider_scores[0]
        reason = self._generate_auto_prediction_reason(top_rider, race)
        
        return {
            'venue': venue,
            'race_number': race['race_number'],
            'predicted_winner': top_rider['number'],
            'predicted_rider': top_rider['name'],
            'confidence_score': round(top_rider['score'], 2),
            'winning_odds': top_rider['odds'],
            'prediction_reason': reason,
            'top3_predictions': rider_scores[:3]
        }
    
    def _calculate_auto_score(self, rider, race):
        """オートレーススコア計算"""
        
        score = 0.0
        
        # オッズ評価
        odds_score = max(0, (10 - rider['odds']) / 10) * 100
        score += odds_score * self.weights['odds_weight']
        
        # グレード評価
        grade_score = self._evaluate_auto_grade(rider.get('grade', 'A2')) * 100
        score += grade_score * self.sport_specific_weights['オートレース']['grade_weight']
        
        return score
    
    # 評価用メソッド群
    def _get_weather_for_venue(self, venue, weather_data):
        """会場の天気情報取得"""
        if not weather_data:
            return None
        return weather_data.get(venue)
    
    def _evaluate_form(self, recent_form):
        """調子評価（競馬）"""
        if not recent_form:
            return 0.5
        
        good_results = recent_form.count('○')
        total_races = len(recent_form)
        
        return good_results / total_races if total_races > 0 else 0.5
    
    def _evaluate_jockey(self, jockey_name):
        """騎手評価（簡易版）"""
        # 実装時は実際の騎手データベースを使用
        return random.uniform(0.3, 0.9)
    
    def _evaluate_track_compatibility(self, track_condition):
        """馬場適性評価"""
        condition_scores = {
            '良': 0.8,
            'やや重': 0.6,
            '重': 0.4,
            '不良': 0.3
        }
        return condition_scores.get(track_condition, 0.6)
    
    def _evaluate_distance_compatibility(self, distance):
        """距離適性評価"""
        # 短距離(1200m以下): 0.7, 中距離(1400-1800m): 0.8, 長距離(2000m以上): 0.6
        if distance <= 1200:
            return 0.7
        elif distance <= 1800:
            return 0.8
        else:
            return 0.6
    
    def _evaluate_boat_form(self, recent_form):
        """競艇調子評価"""
        if not recent_form:
            return 0.5
        
        # 1着の回数を評価
        first_places = recent_form.count('1')
        return min(first_places / 3, 1.0)  # 最大3回の1着で満点
    
    def _evaluate_motor_performance(self, motor_number):
        """モーター性能評価（簡易版）"""
        # 実装時は実際のモーター成績データを使用
        return random.uniform(0.4, 0.9)
    
    def _evaluate_start_position(self, boat_number):
        """スタート位置評価"""
        # インが有利
        position_scores = {1: 0.9, 2: 0.8, 3: 0.7, 4: 0.6, 5: 0.5, 6: 0.4}
        return position_scores.get(boat_number, 0.5)
    
    def _evaluate_bicycle_rank(self, rank):
        """競輪ランク評価"""
        rank_scores = {'S1': 1.0, 'S2': 0.9, 'A1': 0.8, 'A2': 0.6, 'A3': 0.4}
        return rank_scores.get(rank, 0.5)
    
    def _evaluate_bicycle_position(self, position):
        """競輪車番評価"""
        # 中団が有利
        if position in [4, 5, 6]:
            return 0.8
        elif position in [3, 7]:
            return 0.7
        else:
            return 0.6
    
    def _evaluate_auto_grade(self, grade):
        """オートレースグレード評価"""
        grade_scores = {'S1': 1.0, 'S2': 0.8, 'A1': 0.6, 'A2': 0.4}
        return grade_scores.get(grade, 0.5)
    
    # 理由生成メソッド群
    def _generate_horse_prediction_reason(self, top_horse, race, track_condition):
        """競馬予想理由生成"""
        
        reasons = []
        
        if top_horse['odds'] <= 3.0:
            reasons.append(f"人気上位（{top_horse['odds']}倍）で安定感あり")
        elif top_horse['odds'] >= 10.0:
            reasons.append(f"穴狙い（{top_horse['odds']}倍）で高配当期待")
        
        if track_condition != '良':
            reasons.append(f"馬場状態（{track_condition}）に対応可能")
        
        distance = race.get('distance', 1600)
        if distance <= 1200:
            reasons.append("短距離適性を評価")
        elif distance >= 2000:
            reasons.append("長距離適性を評価")
        
        reasons.append(f"総合評価スコア {top_horse['score']:.1f}点で選出")
        
        return "、".join(reasons) + "。"
    
    def _generate_boat_prediction_reason(self, top_boat, race):
        """競艇予想理由生成"""
        
        reasons = []
        
        if top_boat['number'] == 1:
            reasons.append("1コースの有利さ")
        elif top_boat['number'] <= 3:
            reasons.append("内枠からの展開を期待")
        
        if top_boat['odds'] <= 2.5:
            reasons.append("圧倒的人気で信頼度高")
        
        reasons.append(f"総合スコア {top_boat['score']:.1f}点で選出")
        
        return "、".join(reasons) + "。"
    
    def _generate_bicycle_prediction_reason(self, top_rider, race):
        """競輪予想理由生成"""
        
        reasons = []
        
        if top_rider['odds'] <= 3.0:
            reasons.append("実力上位で期待値高")
        
        reasons.append(f"総合評価 {top_rider['score']:.1f}点")
        
        return "、".join(reasons) + "。"
    
    def _generate_auto_prediction_reason(self, top_rider, race):
        """オートレース予想理由生成"""
        
        reasons = []
        
        if top_rider['odds'] <= 4.0:
            reasons.append("人気実力ともに上位")
        
        reasons.append(f"総合スコア {top_rider['score']:.1f}点")
        
        return "、".join(reasons) + "。"

# テスト実行用
if __name__ == "__main__":
    print("🤖 基本予想ロジックテスト開始...")
    
    engine = BasicPredictionEngine()
    
    # サンプル競馬データ
    sample_race_data = {
        'date': '2025-08-08',
        'race_type': '競馬',
        'races': [{
            'venue': '東京',
            'race_number': 11,
            'race_name': 'メインレース',
            'distance': 1600,
            'horses': [
                {'number': 1, 'name': 'テスト馬01', 'odds': 2.5, 'recent_form': '○○△○×'},
                {'number': 2, 'name': 'テスト馬02', 'odds': 5.2, 'recent_form': '○△○○△'},
                {'number': 3, 'name': 'テスト馬03', 'odds': 12.8, 'recent_form': '×△○×○'}
            ]
        }]
    }
    
    # 予想実行
    predictions = engine.predict_race_winners(sample_race_data)
    
    print("\n🎯 予想結果:")
    for pred in predictions['predictions']:
        print(f"📍 {pred['venue']} {pred['race_number']}R")
        print(f"予想: {pred['predicted_winner']}番 {pred['predicted_horse_name']}")
        print(f"オッズ: {pred['winning_odds']}倍")
        print(f"理由: {pred['prediction_reason']}")
        print()
    
    print("✅ 基本予想ロジックテスト完了")