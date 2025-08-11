"""
レース情報取得システム
競馬・競艇・オートレース・競輪の情報を取得
"""

import requests
import json
from datetime import datetime, timedelta
import re
import random
import os

class RaceDataCollector:
    """レース情報収集システム"""
    
    def __init__(self):
        self.race_types = ['競馬', '競艇', '競輪', 'オートレース']
        
        # 競馬場リスト
        self.horse_racing_venues = [
            '東京', '中山', '阪神', '京都', '新潟', '札幌', '函館', '福島', '小倉'
        ]
        
        # 競艇場リスト  
        self.boat_racing_venues = [
            '桐生', '戸田', '江戸川', '平和島', '多摩川', '浜名湖', '蒲郡', '常滑', 
            '津', '三国', '琵琶湖', '住之江', '尼崎', '鳴門', '丸亀', '児島', 
            '宮島', '徳山', '下関', '若松', '芦屋', '福岡', '唐津', '大村'
        ]
    
    def get_tomorrow_races(self, race_type='競馬'):
        """明日のレース情報を取得"""
        
        tomorrow = datetime.now() + timedelta(days=1)
        date_str = tomorrow.strftime('%Y-%m-%d')
        
        if race_type == '競馬':
            races = self._generate_horse_racing_data(date_str)
        elif race_type == '競艇':
            races = self._generate_boat_racing_data(date_str, venues=['浜名湖', '江戸川'])
        elif race_type == '競輪':
            races = self._generate_bicycle_racing_data(date_str)
        elif race_type == 'オートレース':
            races = self._generate_auto_racing_data(date_str)
        else:
            races = self._generate_horse_racing_data(date_str)
        
        return {
            'date': date_str,
            'race_type': race_type,
            'races': races,
            'total_races': len(races)
        }
    
    def _generate_horse_racing_data(self, date_str):
        """競馬データ生成（実際の実装時は本物のAPIまたはスクレイピング）"""
        
        races = []
        venues = random.sample(self.horse_racing_venues, random.randint(2, 4))
        
        for venue in venues:
            race_count = random.randint(8, 12)  # 通常8-12レース
            
            for race_num in range(1, race_count + 1):
                race = {
                    'venue': venue,
                    'race_number': race_num,
                    'race_name': self._generate_race_name(race_num),
                    'distance': random.choice([1200, 1400, 1600, 1800, 2000, 2400]),
                    'track_type': random.choice(['芝', 'ダート']),
                    'grade': self._determine_grade(race_num),
                    'horses': self._generate_horse_entries(),
                    'start_time': f"{9 + (race_num - 1) // 2}:{15 + (race_num % 2) * 25:02d}",
                    'prize_money': self._calculate_prize_money(race_num)
                }
                races.append(race)
        
        return races
    
    def _generate_boat_racing_data(self, date_str, venues=None):
        """競艇データ生成"""
        
        races = []
        if venues:
            venues_to_use = venues
        else:
            venues_to_use = random.sample(self.boat_racing_venues, random.randint(3, 6))
        
        for venue in venues_to_use:
            race_count = 12  # 競艇は通常12レース
            
            for race_num in range(1, race_count + 1):
                # 特別レース名設定
                if venue == '浜名湖':
                    if race_num >= 10:
                        race_name = f"第39回レディースチャンピオン {race_num}R (PGI)"
                    else:
                        race_name = f"レディースチャンピオン {race_num}R"
                elif venue == '江戸川':
                    if race_num >= 10:
                        race_name = f"アサヒビールカップ {race_num}R (GIII)"
                    else:
                        race_name = f"アサヒビールカップ {race_num}R"
                else:
                    race_name = f"{venue} {race_num}R"
                    
                race = {
                    'venue': venue,
                    'race_number': race_num,
                    'race_name': race_name,
                    'boats': self._generate_boat_entries(),
                    'start_time': f"{10 + (race_num - 1) // 2}:{30 + (race_num % 2) * 25:02d}",
                    'water_condition': random.choice(['良', 'やや荒れ', '荒れ'])
                }
                races.append(race)
        
        return races
    
    def _generate_bicycle_racing_data(self, date_str):
        """競輪データ生成"""
        
        races = []
        venues = ['松戸', '立川', '川崎', '平塚', '小田原']
        venue = random.choice(venues)
        
        race_count = random.randint(9, 12)
        
        for race_num in range(1, race_count + 1):
            race = {
                'venue': venue,
                'race_number': race_num,
                'race_name': f"{venue} {race_num}R",
                'distance': 2000,  # 競輪は通常2000m
                'riders': self._generate_rider_entries(),
                'start_time': f"{10 + race_num // 2}:{(race_num % 2) * 30:02d}"
            }
            races.append(race)
        
        return races
    
    def _generate_auto_racing_data(self, date_str):
        """オートレースデータ生成"""
        
        races = []
        venues = ['川口', '伊勢崎', '浜松', '飯塚', '山陽']
        venue = random.choice(venues)
        
        race_count = random.randint(10, 12)
        
        for race_num in range(1, race_count + 1):
            race = {
                'venue': venue,
                'race_number': race_num,
                'race_name': f"{venue} {race_num}R",
                'distance': random.choice([1000, 1500]),
                'riders': self._generate_auto_rider_entries(),
                'start_time': f"{11 + race_num // 2}:{(race_num % 2) * 30:02d}"
            }
            races.append(race)
        
        return races
    
    def _generate_race_name(self, race_num):
        """競馬のレース名生成"""
        
        if race_num <= 6:
            return f"{race_num}R 一般戦"
        elif race_num <= 10:
            return f"{race_num}R 特別戦"
        else:
            special_names = ['メインレース', '重賞', 'ステークス']
            return f"{race_num}R {random.choice(special_names)}"
    
    def _determine_grade(self, race_num):
        """レースグレード決定"""
        
        if race_num >= 11:
            return random.choice(['G3', 'G2', 'G1']) if random.random() < 0.3 else 'L'
        elif race_num >= 8:
            return 'L' if random.random() < 0.2 else '一般'
        else:
            return '一般'
    
    def _generate_horse_entries(self):
        """競馬の出走馬生成"""
        
        horse_count = random.randint(12, 18)
        horses = []
        
        for i in range(1, horse_count + 1):
            horse = {
                'number': i,
                'name': f"サンプル馬{i:02d}",
                'jockey': f"騎手{i:02d}",
                'weight': random.randint(52, 60),
                'odds': round(random.uniform(1.5, 50.0), 1),
                'recent_form': ''.join(random.choices(['○', '△', '×', '-'], k=5))
            }
            horses.append(horse)
        
        return horses
    
    def _generate_boat_entries(self):
        """競艇の出走艇生成"""
        
        boats = []
        
        for i in range(1, 7):  # 競艇は6艇
            boat = {
                'number': i,
                'racer': f"選手{i:02d}",
                'motor_number': random.randint(1, 60),
                'boat_number': random.randint(1, 60),
                'odds': round(random.uniform(1.5, 30.0), 1),
                'recent_form': ''.join(random.choices(['1', '2', '3', '4', '5', '6'], k=5))
            }
            boats.append(boat)
        
        return boats
    
    def _generate_rider_entries(self):
        """競輪選手生成"""
        
        riders = []
        
        for i in range(1, 10):  # 競輪は通常9人
            rider = {
                'number': i,
                'name': f"選手{i:02d}",
                'rank': random.choice(['S1', 'S2', 'A1', 'A2', 'A3']),
                'odds': round(random.uniform(1.8, 25.0), 1)
            }
            riders.append(rider)
        
        return riders
    
    def _generate_auto_rider_entries(self):
        """オートレース選手生成"""
        
        riders = []
        
        for i in range(1, 9):  # オートレースは8人
            rider = {
                'number': i,
                'name': f"選手{i:02d}",
                'grade': random.choice(['S1', 'S2', 'A1', 'A2']),
                'odds': round(random.uniform(2.0, 20.0), 1)
            }
            riders.append(rider)
        
        return riders
    
    def _calculate_prize_money(self, race_num):
        """賞金計算"""
        
        base_money = 500  # 50万円
        
        if race_num >= 11:
            return base_money * random.randint(20, 100)  # 1000万-5000万
        elif race_num >= 8:
            return base_money * random.randint(5, 20)   # 250万-1000万
        else:
            return base_money * random.randint(1, 5)    # 50万-250万
    
    def get_main_races(self, race_data):
        """メインレースを抽出"""
        
        main_races = []
        
        for race in race_data['races']:
            # 競馬の場合
            if race_data['race_type'] == '競馬':
                if race['race_number'] >= 10 or race['grade'] in ['G1', 'G2', 'G3']:
                    main_races.append(race)
            
            # 競艇の場合
            elif race_data['race_type'] == '競艇':
                if race['race_number'] >= 10:
                    main_races.append(race)
            
            # その他も最終数レースをメインとして扱う
            else:
                if race['race_number'] >= 9:
                    main_races.append(race)
        
        return main_races[:3]  # 最大3レース
    
    def save_race_data(self, race_data, filename=None):
        """レースデータを保存"""
        
        if filename is None:
            date_str = datetime.now().strftime('%Y%m%d')
            filename = f"レースデータ_{race_data['race_type']}_{date_str}.json"
        
        filepath = os.path.join("../データ管理", filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(race_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ レースデータ保存完了: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ レースデータ保存エラー: {e}")
            return None

# テスト実行用
if __name__ == "__main__":
    print("🏇 レース情報取得システムテスト開始...")
    
    collector = RaceDataCollector()
    
    # 競馬データ取得
    print("\n📍 明日の競馬レース:")
    horse_races = collector.get_tomorrow_races('競馬')
    print(f"合計レース数: {horse_races['total_races']}")
    
    # メインレース抽出
    main_races = collector.get_main_races(horse_races)
    print(f"\n🎯 メインレース ({len(main_races)}レース):")
    
    for race in main_races:
        print(f"- {race['venue']} {race['race_number']}R: {race['race_name']}")
        print(f"  {race['distance']}m {race['track_type']} ({race['grade']})")
    
    # データ保存
    collector.save_race_data(horse_races)
    
    print("\n✅ レース情報取得システムテスト完了")