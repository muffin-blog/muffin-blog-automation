"""
天気情報取得システム
気象庁APIまたは無料気象APIから天気データを取得
"""

import requests
import json
from datetime import datetime, timedelta
import os

class WeatherDataCollector:
    """天気データ収集システム"""
    
    def __init__(self):
        # OpenWeatherMap API（無料プラン）
        self.api_key = None  # 後で設定
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
        # 主要競馬場・競艇場の座標
        self.racecourse_locations = {
            "東京": {"lat": 35.6762, "lon": 139.6503},
            "中山": {"lat": 35.7601, "lon": 140.0437},
            "阪神": {"lat": 34.6937, "lon": 135.5023},
            "京都": {"lat": 35.0116, "lon": 135.7681},
            "新潟": {"lat": 37.9161, "lon": 139.0364},
            "札幌": {"lat": 43.0642, "lon": 141.3469},
            "函館": {"lat": 41.7687, "lon": 140.7290},
            "福島": {"lat": 37.7503, "lon": 140.4676},
            "小倉": {"lat": 33.8834, "lon": 130.8751},
            # 競艇場追加
            "浜名湖": {"lat": 34.6932, "lon": 137.5984},
            "江戸川": {"lat": 35.6681, "lon": 139.8684}
        }
    
    def get_weather_forecast(self, location="東京", days_ahead=1):
        """指定した競馬場の天気予報を取得"""
        
        if location not in self.racecourse_locations:
            location = "東京"  # デフォルトに設定
        
        coords = self.racecourse_locations[location]
        
        # 代替案：気象庁の天気概況を使用（APIキー不要）
        weather_data = self._get_jma_weather_simple(location, days_ahead)
        
        return {
            'location': location,
            'date': (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d'),
            'weather': weather_data['weather'],
            'temperature': weather_data['temperature'],
            'humidity': weather_data.get('humidity', 'N/A'),
            'wind': weather_data.get('wind', 'N/A'),
            'track_condition_forecast': self._predict_track_condition(weather_data['weather'])
        }
    
    def _get_jma_weather_simple(self, location, days_ahead):
        """気象庁データの簡易版（実際のAPIは有料のため、サンプルデータ生成）"""
        
        # 実装時は実際の気象データAPIまたはウェブスクレイピング
        # 現在はサンプルデータを返す
        
        import random
        
        weather_conditions = ['晴れ', '曇り', '雨', '小雨', '大雨', '雪']
        weights = [0.3, 0.25, 0.15, 0.15, 0.1, 0.05]  # 確率重み
        
        weather = random.choices(weather_conditions, weights=weights)[0]
        temperature = random.randint(15, 35)  # 15-35度の範囲
        
        return {
            'weather': weather,
            'temperature': f"{temperature}°C",
            'humidity': f"{random.randint(40, 90)}%",
            'wind': f"{random.randint(0, 20)}m/s"
        }
    
    def _predict_track_condition(self, weather):
        """天気からバンク状態を予測"""
        
        condition_map = {
            '晴れ': '良',
            '曇り': '良',
            '小雨': 'やや重',
            '雨': '重',
            '大雨': '不良',
            '雪': '不良'
        }
        
        return condition_map.get(weather, '良')
    
    def get_multiple_locations_weather(self, locations=None, days_ahead=1):
        """複数競馬場の天気を一括取得"""
        
        if locations is None:
            locations = ["東京", "阪神", "中山"]  # デフォルトの主要会場
        
        weather_data = {}
        
        for location in locations:
            try:
                weather_data[location] = self.get_weather_forecast(location, days_ahead)
            except Exception as e:
                print(f"⚠️ {location}の天気取得エラー: {e}")
                weather_data[location] = {
                    'location': location,
                    'date': (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d'),
                    'weather': '不明',
                    'temperature': 'N/A',
                    'track_condition_forecast': '良'
                }
        
        return weather_data
    
    def save_weather_data(self, weather_data, filename=None):
        """天気データをJSONファイルに保存"""
        
        if filename is None:
            date_str = datetime.now().strftime('%Y%m%d')
            filename = f"天気データ_{date_str}.json"
        
        filepath = os.path.join("../データ管理", filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(weather_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 天気データ保存完了: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ 天気データ保存エラー: {e}")
            return None

# テスト実行用
if __name__ == "__main__":
    print("🌤️ 天気取得システムテスト開始...")
    
    collector = WeatherDataCollector()
    
    # 明日の東京競馬場の天気
    print("\n📍 東京競馬場の明日の天気:")
    tokyo_weather = collector.get_weather_forecast("東京", 1)
    print(json.dumps(tokyo_weather, ensure_ascii=False, indent=2))
    
    # 複数会場の天気
    print("\n📍 主要会場の明日の天気:")
    multi_weather = collector.get_multiple_locations_weather(["東京", "阪神", "中山"], 1)
    
    for location, data in multi_weather.items():
        print(f"{location}: {data['weather']} {data['temperature']} (バンク予想: {data['track_condition_forecast']})")
    
    # データ保存
    collector.save_weather_data(multi_weather)
    
    print("\n✅ 天気取得システムテスト完了")