"""
note記事生成システム
有料記事（100円）用の競馬・競艇予想記事を自動生成
"""

import json
from datetime import datetime, timedelta
import os

class NoteArticleGenerator:
    """note記事自動生成システム"""
    
    def __init__(self):
        self.price = 100  # 有料note価格
        self.target_length = 1500  # 目標文字数
        
        # 記事テンプレート
        self.article_templates = {
            '競馬': {
                'title_format': '🏇【{date}】{venue}重賞完全予想！的中率向上の秘密とは？',
                'intro_template': self._get_horse_racing_intro(),
                'analysis_template': self._get_horse_racing_analysis(),
                'conclusion_template': self._get_horse_racing_conclusion()
            },
            '競艇': {
                'title_format': '🚤【{date}】{venue}G1予想！水面を制する勝利の法則',
                'intro_template': self._get_boat_racing_intro(),
                'analysis_template': self._get_boat_racing_analysis(),
                'conclusion_template': self._get_boat_racing_conclusion()
            }
        }
    
    def generate_full_article(self, prediction_data, weather_data=None, race_type='競馬'):
        """完全なnote記事を生成"""
        
        # 記事の各部分を生成
        title = self._generate_title(prediction_data, race_type)
        intro = self._generate_introduction(prediction_data, weather_data, race_type)
        main_content = self._generate_main_analysis(prediction_data, race_type)
        predictions_section = self._generate_predictions_section(prediction_data, race_type)
        conclusion = self._generate_conclusion(prediction_data, race_type)
        
        # 記事統合
        full_article = f"""{title}

{intro}

{main_content}

{predictions_section}

{conclusion}

---
💰 この記事は100円の有料記事です
🎯 予想的中で投資回収を目指しましょう！
📊 毎日更新で継続的な利益を追求

#競馬予想 #競艇予想 #投資 #ギャンブル #note有料記事
"""
        
        # 記事情報をまとめて返す
        article_info = {
            'title': title,
            'content': full_article,
            'price': self.price,
            'word_count': len(full_article),
            'date': prediction_data.get('date', datetime.now().strftime('%Y-%m-%d')),
            'race_type': race_type,
            'main_races_count': len(self._get_main_races(prediction_data)),
            'tags': self._generate_tags(race_type)
        }
        
        return article_info
    
    def _generate_title(self, prediction_data, race_type):
        """記事タイトル生成"""
        
        date = prediction_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%m月%d日')
        
        # メイン会場抽出
        main_venues = []
        for prediction in prediction_data.get('predictions', []):
            venue = prediction.get('venue')
            if venue and venue not in main_venues:
                main_venues.append(venue)
        
        venue_str = '・'.join(main_venues[:2]) if main_venues else '全会場'
        
        if race_type == '競馬':
            return f"🏇【{formatted_date}】{venue_str}重賞完全予想！AI分析で的中率向上"
        elif race_type == '競艇':
            return f"🚤【{formatted_date}】{venue_str}G1予想！勝利の波に乗る必勝法"
        else:
            return f"🎯【{formatted_date}】{venue_str}完全予想！データ分析の真骨頂"
    
    def _generate_introduction(self, prediction_data, weather_data, race_type):
        """導入部分生成"""
        
        date = prediction_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        tomorrow = datetime.strptime(date, '%Y-%m-%d')
        formatted_date = tomorrow.strftime('%m月%d日（%a）')
        
        total_races = len(prediction_data.get('predictions', []))
        main_races = self._get_main_races(prediction_data)
        
        # 天気情報の組み込み
        weather_info = ""
        if weather_data:
            weather_summary = self._summarize_weather(weather_data)
            weather_info = f"\n\n🌤️ **明日の天気予報**\n{weather_summary}"
        
        intro = f"""こんにちは！毎日の{race_type}予想をお届けしています。

📅 **{formatted_date}の{race_type}予想**

明日は全{total_races}レース、その中でも注目の{len(main_races)}レースを厳選して予想いたします。

✨ **今回の特徴**
・AI分析による客観的予想
・過去データに基づく的確な根拠
・初心者でも分かりやすい解説
・リスクを抑えた堅実な買い目

{weather_info}

💡 この予想記事は、過去の実績データを基に独自のアルゴリズムで分析しています。投資は自己責任でお願いします。"""
        
        return intro
    
    def _generate_main_analysis(self, prediction_data, race_type):
        """メイン分析セクション生成"""
        
        main_races = self._get_main_races(prediction_data)
        
        if race_type == '競馬':
            analysis_intro = """## 🏇 本日の競馬分析ポイント

### 📊 分析方法について
今回の予想は以下の要素を総合的に分析しています：

1. **オッズ分析** - 市場の評価と実力のギャップを検証
2. **調子分析** - 最近5走の成績から現在の調子を判定
3. **コース適性** - 距離・馬場状態での過去成績を重視
4. **騎手評価** - 勝率・連対率の高い騎手を高評価

### 🎯 注目ポイント"""
        
        elif race_type == '競艇':
            analysis_intro = """## 🚤 本日の競艇分析ポイント

### 📊 分析方法について
競艇予想では以下の要素を重点的にチェック：

1. **スタート力** - 平均スタートタイムとフライング率
2. **モーター性能** - 出足・行足・伸び足の総合評価
3. **コース取り** - 1コース進入率と決まり手分析
4. **選手実力** - 勝率・2連率の安定性を重視

### 🎯 注目ポイント"""
        
        else:
            analysis_intro = f"""## 🎯 本日の{race_type}分析ポイント

### 📊 分析方法について
データに基づく客観的分析を実施：

1. **実力評価** - 過去実績とランクを総合判定
2. **調子分析** - 直近成績から現在の状態を評価
3. **オッズ分析** - 人気と実力のバランスを検証

### 🎯 注目ポイント"""
        
        # レース別の簡易分析
        race_highlights = []
        for i, race in enumerate(main_races[:3], 1):
            venue = race.get('venue', '会場名')
            race_num = race.get('race_number', i)
            race_name = race.get('race_name', f'{race_num}R')
            
            highlight = f"""
**{i}. {venue} {race_num}R {race_name}**
- 予想本命: {race.get('predicted_winner', '?')}番
- 注目理由: {race.get('prediction_reason', 'データ分析により選出')[:50]}...
- オッズ: {race.get('winning_odds', '?')}倍
"""
            race_highlights.append(highlight)
        
        return analysis_intro + '\n'.join(race_highlights)
    
    def _generate_predictions_section(self, prediction_data, race_type):
        """予想セクション生成"""
        
        main_races = self._get_main_races(prediction_data)
        
        predictions_content = """## 🎯 本命予想詳細

### 💎 厳選レース予想

"""
        
        for i, race in enumerate(main_races, 1):
            venue = race.get('venue', '会場')
            race_num = race.get('race_number', i)
            race_name = race.get('race_name', f'{race_num}R')
            predicted_winner = race.get('predicted_winner', '?')
            confidence_score = race.get('confidence_score', 0)
            winning_odds = race.get('winning_odds', '?')
            reason = race.get('prediction_reason', 'データ分析により選出')
            
            # トップ3予想があれば追加
            top3 = race.get('top3_predictions', [])
            top3_text = ""
            if len(top3) >= 3:
                top3_text = f"""
**予想順位**
1. {top3[0].get('number', '?')}番 (スコア: {top3[0].get('score', 0):.1f})
2. {top3[1].get('number', '?')}番 (スコア: {top3[1].get('score', 0):.1f})  
3. {top3[2].get('number', '?')}番 (スコア: {top3[2].get('score', 0):.1f})
"""
            
            race_prediction = f"""
### 📍 {venue} {race_num}R - {race_name}

🎯 **本命予想: {predicted_winner}番**
💰 **オッズ: {winning_odds}倍**
📊 **信頼度: {confidence_score:.1f}/100**

**📝 予想根拠**
{reason}

{top3_text}

**💡 投資戦略**
- 本命単勝: {predicted_winner}番
- 安全策: {predicted_winner}番軸の複勝・ワイド
- 期待収支: プラス想定（オッズ{winning_odds}倍×的中率考慮）

---
"""
            
            predictions_content += race_prediction
        
        return predictions_content
    
    def _generate_conclusion(self, prediction_data, race_type):
        """結論セクション生成"""
        
        main_races_count = len(self._get_main_races(prediction_data))
        total_races = len(prediction_data.get('predictions', []))
        
        conclusion = f"""## 📈 まとめ

### 🎯 本日の予想サマリー
- **対象レース**: 全{total_races}レース中、厳選{main_races_count}レース
- **予想方針**: データ重視の堅実路線
- **リスクレベル**: 中程度（安定性重視）

### 💰 投資のポイント
1. **資金管理**: 1日の投資額は余裕資金の範囲で
2. **分散投資**: 複数レースに分けてリスク分散
3. **冷静な判断**: 熱くならずデータに基づく判断を

### 🔄 継続購読のメリット
- 毎日の継続的な予想提供
- 学習アルゴリズムによる精度向上
- 長期的な利益追求が可能

### ⚠️ 免責事項
競馬・競艇は農林水産大臣・国土交通大臣許可の公営競技です。予想は参考情報であり、投資は自己責任でお願いします。20歳未満の方の馬券・舟券購入は法律で禁止されています。

### 📞 お問い合わせ
ご質問やリクエストがあればコメント欄にお寄せください！

**明日の予想もお楽しみに！** 🚀

---
**この記事が参考になったら「スキ」👍とフォローをお願いします！**"""
        
        return conclusion
    
    def _get_main_races(self, prediction_data):
        """メインレースを抽出"""
        
        all_predictions = prediction_data.get('predictions', [])
        main_races = []
        
        for prediction in all_predictions:
            race_number = prediction.get('race_number', 0)
            # 10R以降、またはGrade表示があるものをメインレースとして扱う
            if (race_number >= 10 or 
                'G1' in str(prediction.get('race_name', '')) or
                'G2' in str(prediction.get('race_name', '')) or
                'G3' in str(prediction.get('race_name', '')) or
                'メイン' in str(prediction.get('race_name', ''))):
                main_races.append(prediction)
        
        # メインレースが少ない場合は後半レースを追加
        if len(main_races) < 3:
            for prediction in all_predictions:
                if prediction not in main_races and prediction.get('race_number', 0) >= 8:
                    main_races.append(prediction)
                    if len(main_races) >= 3:
                        break
        
        return main_races[:5]  # 最大5レース
    
    def _summarize_weather(self, weather_data):
        """天気情報要約"""
        
        weather_summary = []
        
        for venue, data in weather_data.items():
            weather = data.get('weather', '不明')
            temp = data.get('temperature', '?')
            track_condition = data.get('track_condition_forecast', '良')
            
            weather_summary.append(f"・**{venue}**: {weather} {temp} (バンク予想: {track_condition})")
        
        return '\n'.join(weather_summary[:3])  # 最大3会場
    
    def _generate_tags(self, race_type):
        """記事タグ生成"""
        
        base_tags = [f'{race_type}予想', '有料記事', 'ギャンブル', '投資']
        
        if race_type == '競馬':
            specific_tags = ['競馬', '馬券', '単勝', '複勝', 'JRA']
        elif race_type == '競艇':
            specific_tags = ['競艇', '舟券', '1号艇', 'ボートレース']
        else:
            specific_tags = ['予想', 'データ分析']
        
        return base_tags + specific_tags
    
    def save_article(self, article_info, filename=None):
        """記事をファイルに保存"""
        
        if filename is None:
            date_str = datetime.now().strftime('%Y%m%d')
            filename = f"note記事_{article_info['race_type']}_{date_str}.md"
        
        filepath = os.path.join("../記事生成", filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(article_info['content'])
            
            print(f"✅ note記事保存完了: {filepath}")
            print(f"📊 文字数: {article_info['word_count']}文字")
            return filepath
            
        except Exception as e:
            print(f"❌ 記事保存エラー: {e}")
            return None
    
    # テンプレート定義メソッド群
    def _get_horse_racing_intro(self):
        return "競馬予想記事の導入テンプレート"
    
    def _get_horse_racing_analysis(self):
        return "競馬分析テンプレート"
    
    def _get_horse_racing_conclusion(self):
        return "競馬記事結論テンプレート"
    
    def _get_boat_racing_intro(self):
        return "競艇予想記事の導入テンプレート"
    
    def _get_boat_racing_analysis(self):
        return "競艇分析テンプレート"
    
    def _get_boat_racing_conclusion(self):
        return "競艇記事結論テンプレート"

# テスト実行用
if __name__ == "__main__":
    print("📝 note記事生成システムテスト開始...")
    
    generator = NoteArticleGenerator()
    
    # サンプル予想データ
    sample_prediction = {
        'date': '2025-08-08',
        'race_type': '競馬',
        'predictions': [
            {
                'venue': '東京',
                'race_number': 11,
                'race_name': 'メインレース',
                'predicted_winner': 3,
                'predicted_horse_name': 'テスト馬03',
                'confidence_score': 75.5,
                'winning_odds': 4.2,
                'prediction_reason': 'オッズと実力のバランスが良好、調子も上昇中',
                'top3_predictions': [
                    {'number': 3, 'score': 75.5},
                    {'number': 1, 'score': 72.1},
                    {'number': 7, 'score': 68.9}
                ]
            }
        ]
    }
    
    # サンプル天気データ  
    sample_weather = {
        '東京': {
            'weather': '晴れ',
            'temperature': '25°C',
            'track_condition_forecast': '良'
        }
    }
    
    # 記事生成
    article = generator.generate_full_article(
        sample_prediction, 
        sample_weather, 
        '競馬'
    )
    
    print(f"\n📰 生成記事情報:")
    print(f"タイトル: {article['title']}")
    print(f"文字数: {article['word_count']}文字")
    print(f"価格: {article['price']}円")
    print(f"メインレース数: {article['main_races_count']}レース")
    
    # 記事保存
    generator.save_article(article)
    
    print("\n✅ note記事生成システムテスト完了")