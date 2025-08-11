"""
ブログの真のSEO課題を包括的に分析
メタディスクリプション以外の根本的SEO問題を特定
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests
import re

def comprehensive_seo_analysis(post_id):
    """記事の包括的SEO分析"""
    
    wp = WordPressBlogAutomator()  # 環境変数から自動読み込み
    
    response = requests.get(f'{wp.api_url}/posts/{post_id}', headers=wp.headers)
    if response.status_code != 200:
        return None
        
    post = response.json()
    title = post['title']['rendered']
    content = post['content']['rendered']
    
    print(f'🔍 包括的SEO分析: {title}')
    print('='*80)
    
    # 1. タイトルタグ戦略分析
    title_length = len(title)
    print(f'📝 タイトル戦略分析:')
    print(f'   文字数: {title_length}文字 (推奨: 28-35文字)')
    
    # キーワード配置分析
    title_words = title.split()
    main_keyword_position = next((i for i, word in enumerate(title_words) if 'Audible' in word), -1)
    print(f'   メインキーワード位置: {main_keyword_position + 1}番目 (推奨: 1-3番目)')
    
    # 感情訴求・クリック誘発要素
    emotional_triggers = ['世界一', '完全', '徹底', '実際', '本当']
    trigger_count = sum(1 for trigger in emotional_triggers if trigger in title)
    print(f'   感情訴求要素: {trigger_count}個含有')
    
    # 2. 見出し構造とSEO最適化分析
    h1_tags = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    h2_tags = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL)
    h3_tags = re.findall(r'<h3[^>]*>(.*?)</h3>', content, re.DOTALL)
    
    print(f'\n🏗️ 見出し構造とキーワード最適化:')
    print(f'   H1: {len(h1_tags)}個 (推奨: 1個)')
    print(f'   H2: {len(h2_tags)}個')
    print(f'   H3: {len(h3_tags)}個')
    
    # H2見出しのキーワード含有率
    if h2_tags:
        keyword_h2_count = 0
        print(f'   H2見出し分析:')
        for i, h2 in enumerate(h2_tags[:5]):
            clean_h2 = re.sub(r'<[^>]+>', '', h2).strip()
            has_keyword = any(kw in clean_h2 for kw in ['Audible', 'お金', '投資', '節約'])
            if has_keyword:
                keyword_h2_count += 1
            print(f'     H{i+1}: {clean_h2} {"✅" if has_keyword else "❌"}')
        
        keyword_ratio = keyword_h2_count / len(h2_tags) * 100
        print(f'   H2キーワード含有率: {keyword_ratio:.1f}% (推奨: 60%以上)')
    
    # 3. キーワード戦略と密度分析
    clean_content = re.sub(r'<[^>]+>', '', content)
    word_count = len(clean_content)
    
    print(f'\n🎯 キーワード戦略分析:')
    
    # メインキーワード群の分析
    primary_keywords = {
        'Audible': ['Audible', 'オーディブル'],
        'お金関連': ['お金', '投資', '節約', '貯金', '資産'],
        'おすすめ': ['おすすめ', '厳選', 'ベスト'],
        '学習': ['勉強', '学習', '知識', 'スキル']
    }
    
    for category, keywords in primary_keywords.items():
        total_count = sum(clean_content.count(kw) for kw in keywords)
        density = (total_count / word_count * 100) if word_count > 0 else 0
        
        # 冒頭1000文字での出現
        early_count = sum(clean_content[:1000].count(kw) for kw in keywords)
        
        print(f'   {category}: {total_count}回 ({density:.2f}%) - 冒頭{early_count}回')
        
        # 推奨密度チェック
        if category == 'Audible' and (density < 0.5 or density > 3.0):
            print(f'     ⚠️ メインキーワード密度要調整 (推奨: 0.5-3.0%)')
    
    # 4. 内部リンク戦略分析
    internal_links = re.findall(r'<a[^>]*href=["\']https://muffin-blog\.com[^"\']*["\']*[^>]*>', content)
    external_links = re.findall(r'<a[^>]*href=["\']https?://(?!muffin-blog\.com)[^"\']*["\']*[^>]*>', content)
    
    print(f'\n🔗 リンク戦略分析:')
    print(f'   内部リンク: {len(internal_links)}個')
    print(f'   外部リンク: {len(external_links)}個')
    
    # Amazon アフィリエイトリンク分析
    amazon_links = len(re.findall(r'amazon\.|amzn\.', content))
    print(f'   Amazonリンク: {amazon_links}個')
    
    # リンクバランス評価
    total_links = len(internal_links) + len(external_links)
    if total_links > 0:
        internal_ratio = len(internal_links) / total_links * 100
        print(f'   内部リンク比率: {internal_ratio:.1f}% (推奨: 70-80%)')
    
    # 5. 画像最適化とメディア戦略
    images = re.findall(r'<img[^>]*>', content)
    alt_attributes = re.findall(r'alt=["\']([^"\']*)["\']', content)
    
    print(f'\n🖼️ 画像・メディア最適化:')
    print(f'   画像数: {len(images)}個')
    print(f'   alt属性設定: {len(alt_attributes)}個')
    
    if images:
        alt_optimization_rate = len(alt_attributes) / len(images) * 100
        print(f'   alt最適化率: {alt_optimization_rate:.1f}% (推奨: 100%)')
        
        # alt属性のキーワード含有チェック
        keyword_alts = sum(1 for alt in alt_attributes if any(kw in alt for kw in ['Audible', 'お金', '投資']))
        if alt_attributes:
            keyword_alt_ratio = keyword_alts / len(alt_attributes) * 100
            print(f'   altキーワード含有率: {keyword_alt_ratio:.1f}%')
    
    # 6. コンテンツ品質とユーザビリティ
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    
    print(f'\n📊 コンテンツ品質分析:')
    print(f'   総文字数: {word_count:,}文字')
    print(f'   段落数: {len(paragraphs)}個')
    
    if paragraphs:
        avg_paragraph_length = sum(len(re.sub(r'<[^>]+>', '', p)) for p in paragraphs) / len(paragraphs)
        print(f'   平均段落長: {avg_paragraph_length:.0f}文字 (推奨: 100-200文字)')
    
    # 読みやすさ指標
    sentence_count = clean_content.count('。') + clean_content.count('！') + clean_content.count('？')
    if sentence_count > 0:
        avg_sentence_length = word_count / sentence_count
        print(f'   平均文長: {avg_sentence_length:.0f}文字 (推奨: 40-60文字)')
    
    # 7. 検索意図適合度分析
    print(f'\n🎯 検索意図適合度:')
    
    # 情報型検索意図
    info_keywords = ['方法', 'やり方', '始め方', 'とは', 'について', '解説']
    info_score = sum(clean_content.count(kw) for kw in info_keywords)
    
    # 商用検索意図
    commercial_keywords = ['おすすめ', '比較', 'レビュー', '口コミ', '評判', '選び方']
    commercial_score = sum(clean_content.count(kw) for kw in commercial_keywords)
    
    # 取引型検索意図
    transactional_keywords = ['購入', '登録', '申込', '無料', 'お試し']
    transactional_score = sum(clean_content.count(kw) for kw in transactional_keywords)
    
    print(f'   情報型スコア: {info_score}点')
    print(f'   商用型スコア: {commercial_score}点')
    print(f'   取引型スコア: {transactional_score}点')
    
    # 主要検索意図の判定
    max_score = max(info_score, commercial_score, transactional_score)
    if max_score == commercial_score:
        print(f'   → 商用検索意図に最適化済み')
    elif max_score == info_score:
        print(f'   → 情報検索意図に最適化済み')
    else:
        print(f'   → 取引検索意図に最適化済み')
    
    # 8. 競合優位性と独自価値
    print(f'\n🏆 競合優位性分析:')
    
    unique_value_indicators = {
        '実体験': ['実際に', '体験', '使ってみた', '試した'],
        '専門性': ['専門', 'プロ', '詳しく', '徹底'],
        '網羅性': ['完全', '全て', '総まとめ', '一覧'],
        '最新性': ['2024', '最新', 'アップデート', '現在'],
        '初心者配慮': ['初心者', 'はじめて', '分かりやすく', '簡単']
    }
    
    for indicator, keywords in unique_value_indicators.items():
        count = sum(clean_content.count(kw) for kw in keywords)
        if count > 0:
            print(f'   ✅ {indicator}: {count}箇所で言及')
    
    # 9. テクニカルSEO課題
    print(f'\n⚙️ テクニカルSEO課題:')
    
    # 構造化データの確認
    json_ld = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>', content)
    print(f'   構造化データ: {len(json_ld)}個')
    
    # 目次の有無
    toc_indicators = ['目次', 'この記事で分かること', 'もくじ']
    has_toc = any(indicator in clean_content for indicator in toc_indicators)
    print(f'   目次設置: {"✅" if has_toc else "❌"}')
    
    return True

if __name__ == "__main__":
    print('🚀 ブログの真のSEO課題 包括分析')
    print('メタディスクリプション以外の根本的問題を特定')
    print('='*80)
    
    # 主要記事を徹底分析
    target_posts = [2732, 2677, 2535]  # お金の勉強、休会制度、始め方
    
    for post_id in target_posts:
        comprehensive_seo_analysis(post_id)
        print('\n' + '='*80 + '\n')
    
    print('📋 分析完了: 真のSEO改善ポイントを特定しました')