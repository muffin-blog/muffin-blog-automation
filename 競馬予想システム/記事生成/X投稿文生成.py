"""
X(Twitter)投稿文生成システム
140文字制限内でnote記事への誘導とメインレース予想を配信
"""

import json
from datetime import datetime
import os

class TwitterPostGenerator:
    """X(Twitter)投稿文自動生成システム"""
    
    def __init__(self):
        self.character_limit = 140
        self.hashtag_sets = {
            '競馬': ['#競馬', '#競馬予想', '#馬券', '#JRA'],
            '競艇': ['#競艇', '#ボートレース', '#舟券', '#競艇予想'],
            '競輪': ['#競輪', '#競輪予想'],
            'オートレース': ['#オートレース', '#オート予想']
        }
        
        # 投稿パターンテンプレート
        self.post_patterns = {
            'main_prediction': {
                '競馬': '🏇{date} {venue}{race_num}R本命{winner}番({odds}倍)\n{reason}\n📝詳細note↓\n{url}',
                '競艇': '🚤{date} {venue}{race_num}R本命{winner}番({odds}倍)\n{reason}\n📝詳細note↓\n{url}',
                'default': '🎯{date} {venue}{race_num}R本命{winner}番({odds}倍)\n{reason}\n📝詳細note↓\n{url}'
            },
            'daily_summary': {
                '競馬': '🏇{date}の競馬予想\n✅厳選{count}レース\n💰堅実路線で利益追求\n📊AI分析完了\n📝note記事↓\n{url}',
                '競艇': '🚤{date}の競艇予想\n✅厳選{count}レース\n💰本命狙いで着実に\n📊データ分析済み\n📝note記事↓\n{url}',
                'default': '🎯{date}の{race_type}予想\n✅厳選{count}レース\n💰データ重視の予想\n📝note記事↓\n{url}'
            }
        }
    
    def generate_main_race_post(self, main_race, note_url=None, race_type='競馬'):
        """メインレース予想投稿生成"""
        
        # 基本情報抽出
        venue = main_race.get('venue', '会場')
        race_num = main_race.get('race_number', '?')
        winner = main_race.get('predicted_winner', '?')
        odds = main_race.get('winning_odds', '?')
        reason = main_race.get('prediction_reason', '予想根拠あり')
        
        # 日付フォーマット
        date = datetime.now().strftime('%m/%d')
        
        # URLプレースホルダー
        url = note_url if note_url else '[note記事URL]'
        
        # 理由を短縮
        short_reason = self._shorten_reason(reason, 30)
        
        # パターン選択
        pattern = self.post_patterns['main_prediction'].get(race_type, 
                                                           self.post_patterns['main_prediction']['default'])
        
        # 投稿文作成
        post_text = pattern.format(
            date=date,
            venue=venue,
            race_num=race_num,
            winner=winner,
            odds=odds,
            reason=short_reason,
            url=url
        )
        
        # ハッシュタグ追加
        hashtags = self._select_hashtags(race_type, 2)
        if hashtags:
            post_text += f" {' '.join(hashtags)}"
        
        # 文字数調整
        final_post = self._adjust_character_count(post_text)
        
        return {
            'type': 'main_race_prediction',
            'content': final_post,
            'character_count': len(final_post),
            'race_info': {
                'venue': venue,
                'race_number': race_num,
                'predicted_winner': winner,
                'odds': odds
            },
            'hashtags': hashtags
        }
    
    def generate_daily_summary_post(self, prediction_data, note_url=None, race_type='競馬'):
        """日次サマリー投稿生成"""
        
        # 基本情報
        date = datetime.now().strftime('%m/%d')
        predictions = prediction_data.get('predictions', [])
        main_races = self._get_main_races(predictions)
        count = len(main_races)
        
        # URLプレースホルダー
        url = note_url if note_url else '[note記事URL]'
        
        # パターン選択
        pattern = self.post_patterns['daily_summary'].get(race_type,
                                                         self.post_patterns['daily_summary']['default'])
        
        # 投稿文作成
        post_text = pattern.format(
            date=date,
            race_type=race_type,
            count=count,
            url=url
        )
        
        # ハッシュタグ追加
        hashtags = self._select_hashtags(race_type, 3)
        if hashtags:
            post_text += f" {' '.join(hashtags)}"
        
        # 文字数調整
        final_post = self._adjust_character_count(post_text)
        
        return {
            'type': 'daily_summary',
            'content': final_post,
            'character_count': len(final_post),
            'races_count': count,
            'hashtags': hashtags
        }
    
    def generate_result_report_post(self, verification_data, race_type='競馬'):
        """結果報告投稿生成"""
        
        # 結果データ抽出
        total_races = verification_data.get('total_races', 0)
        correct_predictions = verification_data.get('correct_predictions', 0)
        accuracy_rate = verification_data.get('accuracy_rate', 0)
        
        # 日付
        date = datetime.now().strftime('%m/%d')
        
        # 結果投稿パターン
        if accuracy_rate >= 50:
            emoji = '🎉'
            comment = '好調継続中'
        elif accuracy_rate >= 30:
            emoji = '✅'
            comment = '堅実に的中'
        else:
            emoji = '📊'
            comment = '分析継続'
        
        post_text = f"{emoji}{date}結果報告\n{correct_predictions}/{total_races}的中({accuracy_rate:.1f}%)\n{comment}\n📈明日も期待"
        
        # ハッシュタグ追加
        hashtags = self._select_hashtags(race_type, 2)
        if hashtags:
            post_text += f" {' '.join(hashtags)}"
        
        # 文字数調整
        final_post = self._adjust_character_count(post_text)
        
        return {
            'type': 'result_report',
            'content': final_post,
            'character_count': len(final_post),
            'accuracy_rate': accuracy_rate,
            'results': f"{correct_predictions}/{total_races}",
            'hashtags': hashtags
        }
    
    def generate_teaser_post(self, race_type='競馬', note_url=None):
        """予告投稿生成"""
        
        date = datetime.now().strftime('%m/%d')
        url = note_url if note_url else '[note記事URL]'
        
        teaser_patterns = {
            '競馬': f"🏇{date}の予想準備中\n📊データ分析進行中\n💎穴馬候補も発見\n🕐午前中に公開予定\n📝note↓\n{url}",
            '競艇': f"🚤{date}の予想作業中\n📊モーター情報確認済み\n💰本命候補絞り込み完了\n🕐午前中公開\n📝note↓\n{url}",
            'default': f"🎯{date}の{race_type}予想\n📊分析作業中\n💡注目レース選定済み\n📝soon公開\n{url}"
        }
        
        post_text = teaser_patterns.get(race_type, teaser_patterns['default'])
        
        # ハッシュタグ追加
        hashtags = self._select_hashtags(race_type, 2)
        if hashtags:
            post_text += f" {' '.join(hashtags)}"
        
        # 文字数調整
        final_post = self._adjust_character_count(post_text)
        
        return {
            'type': 'teaser',
            'content': final_post,
            'character_count': len(final_post),
            'hashtags': hashtags
        }
    
    def generate_multiple_posts(self, prediction_data, note_url=None, race_type='競馬'):
        """複数投稿パターン生成"""
        
        posts = []
        main_races = self._get_main_races(prediction_data.get('predictions', []))
        
        # 1. 日次サマリー投稿
        summary_post = self.generate_daily_summary_post(prediction_data, note_url, race_type)
        posts.append(summary_post)
        
        # 2. メインレース投稿（最大2つ）
        for i, main_race in enumerate(main_races[:2]):
            main_post = self.generate_main_race_post(main_race, note_url, race_type)
            posts.append(main_post)
        
        # 3. 予告投稿（オプション）
        teaser_post = self.generate_teaser_post(race_type, note_url)
        posts.append(teaser_post)
        
        return {
            'posts': posts,
            'total_posts': len(posts),
            'recommended_schedule': self._generate_posting_schedule(len(posts))
        }
    
    def _get_main_races(self, predictions):
        """メインレース抽出"""
        
        main_races = []
        for prediction in predictions:
            race_number = prediction.get('race_number', 0)
            race_name = prediction.get('race_name', '')
            
            if (race_number >= 10 or 
                any(grade in race_name for grade in ['G1', 'G2', 'G3', 'メイン', '重賞'])):
                main_races.append(prediction)
        
        return main_races[:3]  # 最大3レース
    
    def _shorten_reason(self, reason, max_length):
        """予想理由を短縮"""
        
        if len(reason) <= max_length:
            return reason
        
        # キーワードを抽出して短縮
        keywords = ['人気', '調子', '実力', '適性', 'オッズ', '期待', '安定']
        
        for keyword in keywords:
            if keyword in reason:
                return f"{keyword}良好"
        
        return reason[:max_length-1] + "…"
    
    def _select_hashtags(self, race_type, count=2):
        """ハッシュタグ選択"""
        
        available_tags = self.hashtag_sets.get(race_type, ['#予想'])
        return available_tags[:count] if available_tags else []
    
    def _adjust_character_count(self, text):
        """文字数調整"""
        
        if len(text) <= self.character_limit:
            return text
        
        # 文字数オーバーの場合は調整
        # URL部分を除いて調整
        if '[note記事URL]' in text:
            url_placeholder = '[note記事URL]'
            text_without_url = text.replace(url_placeholder, '')
            available_chars = self.character_limit - len(url_placeholder)
            
            if len(text_without_url) > available_chars:
                shortened = text_without_url[:available_chars-3] + "..."
                return shortened + url_placeholder
        
        # 通常の短縮
        return text[:self.character_limit-3] + "..."
    
    def _generate_posting_schedule(self, post_count):
        """投稿スケジュール提案"""
        
        schedule = []
        base_times = ['09:00', '10:30', '12:00', '14:00']
        
        for i in range(min(post_count, len(base_times))):
            schedule.append({
                'time': base_times[i],
                'post_index': i,
                'description': f'{i+1}番目の投稿推奨時刻'
            })
        
        return schedule
    
    def save_posts(self, posts_data, filename=None):
        """投稿データを保存"""
        
        if filename is None:
            date_str = datetime.now().strftime('%Y%m%d')
            filename = f"X投稿文_{date_str}.json"
        
        filepath = os.path.join("../記事生成", filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(posts_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ X投稿文保存完了: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ 投稿文保存エラー: {e}")
            return None
    
    def preview_posts(self, posts_data):
        """投稿プレビュー表示"""
        
        print("📱 X投稿文プレビュー\n" + "="*50)
        
        for i, post in enumerate(posts_data.get('posts', []), 1):
            print(f"\n【投稿 {i}】({post['type']})")
            print(f"文字数: {post['character_count']}/{self.character_limit}")
            print("-" * 30)
            print(post['content'])
            print("-" * 30)
        
        schedule = posts_data.get('recommended_schedule', [])
        if schedule:
            print(f"\n📅 推奨投稿スケジュール:")
            for item in schedule:
                print(f"- {item['time']}: {item['description']}")

# テスト実行用
if __name__ == "__main__":
    print("📱 X投稿文生成システムテスト開始...")
    
    generator = TwitterPostGenerator()
    
    # サンプル予想データ
    sample_prediction_data = {
        'date': '2025-08-08',
        'race_type': '競馬',
        'predictions': [
            {
                'venue': '東京',
                'race_number': 11,
                'race_name': 'メインレース',
                'predicted_winner': 3,
                'winning_odds': 4.2,
                'prediction_reason': 'オッズと実力のバランスが良好で、最近の調子も上昇傾向'
            }
        ]
    }
    
    # 複数投稿生成
    posts_data = generator.generate_multiple_posts(
        sample_prediction_data,
        note_url="https://note.com/sample/n/abc123",
        race_type='競馬'
    )
    
    # プレビュー表示
    generator.preview_posts(posts_data)
    
    # 投稿データ保存
    generator.save_posts(posts_data)
    
    print("\n✅ X投稿文生成システムテスト完了")