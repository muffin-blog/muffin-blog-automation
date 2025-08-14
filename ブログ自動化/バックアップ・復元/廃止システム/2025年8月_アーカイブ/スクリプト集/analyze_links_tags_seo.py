"""
リンクとHTMLタグのSEO最適化状況を包括的に分析
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests
import re

def analyze_link_and_tag_seo(post_id):
    """リンクとタグのSEO最適化状況を詳細分析"""
    
    wp = WordPressBlogAutomator()  # 環境変数から自動読み込み
    
    response = requests.get(f'{wp.api_url}/posts/{post_id}', headers=wp.headers)
    if response.status_code != 200:
        return None
        
    post = response.json()
    title = post['title']['rendered']
    content = post['content']['rendered']
    
    print(f'🔍 リンク・タグSEO分析: {title[:50]}...')
    print('='*80)
    
    # 1. リンクのアンカーテキスト分析
    print('🔗 リンクのSEO最適化状況:')
    
    # 内部リンクのアンカーテキスト分析
    internal_links = re.findall(r'<a[^>]*href=["\']https://muffin-blog\.com[^"\']*["\']*[^>]*>(.*?)</a>', content, re.DOTALL)
    print(f'   内部リンク総数: {len(internal_links)}個')
    
    if internal_links:
        print('   内部リンクアンカーテキスト分析:')
        keyword_internal_count = 0
        for i, anchor in enumerate(internal_links[:5]):
            clean_anchor = re.sub(r'<[^>]+>', '', anchor).strip()
            # キーワード含有チェック
            has_keyword = any(kw in clean_anchor for kw in ['Audible', 'お金', '投資', '節約', '始め方'])
            if has_keyword:
                keyword_internal_count += 1
            keyword_status = '✅' if has_keyword else '❌'
            print(f'     {i+1}. "{clean_anchor}" {keyword_status}')
        
        if internal_links:
            keyword_internal_ratio = keyword_internal_count / min(len(internal_links), 5) * 100
            print(f'   内部リンクキーワード含有率: {keyword_internal_ratio:.1f}% (推奨: 80%以上)')
    
    # 外部リンクのアンカーテキスト分析
    external_links = re.findall(r'<a[^>]*href=["\']https?://(?!muffin-blog\.com)[^"\']*["\']*[^>]*>(.*?)</a>', content, re.DOTALL)
    print(f'   外部リンク総数: {len(external_links)}個')
    
    if external_links:
        print('   外部リンクアンカーテキスト分析:')
        generic_anchors = 0
        for i, anchor in enumerate(external_links[:5]):
            clean_anchor = re.sub(r'<[^>]+>', '', anchor).strip()
            # 汎用的なアンカーテキストチェック
            is_generic = clean_anchor in ['こちら', 'ここ', 'クリック', 'リンク', '詳細', '公式サイト']
            if is_generic:
                generic_anchors += 1
            generic_status = '❌ 汎用的' if is_generic else '✅ 具体的'
            print(f'     {i+1}. "{clean_anchor}" {generic_status}')
        
        if external_links:
            generic_ratio = generic_anchors / min(len(external_links), 5) * 100
            print(f'   汎用的アンカーテキスト率: {generic_ratio:.1f}% (推奨: 0%)')
    
    # 2. リンクのrel属性分析
    print(f'\n🏷️ リンク属性のSEO最適化:')
    
    # nofollow属性の分析
    nofollow_links = len(re.findall(r'rel=["\'][^"\']*nofollow[^"\']*["\']', content))
    external_links_count = len(re.findall(r'href=["\']https?://(?!muffin-blog\.com)', content))
    
    print(f'   nofollow設定済みリンク: {nofollow_links}個')
    if external_links_count > 0:
        nofollow_ratio = nofollow_links / external_links_count * 100
        print(f'   外部リンクnofollow率: {nofollow_ratio:.1f}%')
    
    # target='_blank'の分析
    blank_links = len(re.findall(r'target=["\']_blank["\']', content))
    print(f'   新しいタブで開くリンク: {blank_links}個')
    
    # sponsored属性の分析（アフィリエイトリンク用）
    sponsored_links = len(re.findall(r'rel=["\'][^"\']*sponsored[^"\']*["\']', content))
    amazon_links = len(re.findall(r'amazon\.|amzn\.', content))
    print(f'   sponsored属性設定: {sponsored_links}個')
    print(f'   Amazonリンク数: {amazon_links}個')
    
    if amazon_links > 0 and sponsored_links == 0:
        print('   ⚠️ Amazonリンクにsponsored属性未設定（Google推奨違反）')
    
    # 3. 画像のalt属性とSEO最適化
    print(f'\n🖼️ 画像タグのSEO最適化:')
    
    images = re.findall(r'<img[^>]*>', content)
    alt_texts = re.findall(r'alt=["\']([^"\']*)["\']', content)
    title_attrs = re.findall(r'<img[^>]*title=["\']([^"\']*)["\'][^>]*>', content)
    
    print(f'   画像総数: {len(images)}個')
    print(f'   alt属性設定: {len(alt_texts)}個 ({len(alt_texts)/len(images)*100 if images else 0:.1f}%)')
    print(f'   title属性設定: {len(title_attrs)}個')
    
    # alt属性のSEO品質分析
    if alt_texts:
        keyword_alts = 0
        descriptive_alts = 0
        empty_alts = 0
        
        print('   alt属性の品質分析:')
        for i, alt in enumerate(alt_texts[:5]):
            if not alt.strip():
                empty_alts += 1
                continue
                
            has_keyword = any(kw in alt for kw in ['Audible', 'お金', '投資', '節約'])
            is_descriptive = len(alt) > 10 and alt not in ['画像', 'image', 'img']
            
            if has_keyword:
                keyword_alts += 1
            if is_descriptive:
                descriptive_alts += 1
                
            keyword_status = '✅' if has_keyword else '❌'
            descriptive_status = '✅' if is_descriptive else '❌'
            print(f'     {i+1}. "{alt}" キーワード:{keyword_status} 説明的:{descriptive_status}')
        
        total_analyzed = min(len(alt_texts), 5)
        keyword_alt_ratio = keyword_alts / total_analyzed * 100 if total_analyzed > 0 else 0
        descriptive_ratio = descriptive_alts / total_analyzed * 100 if total_analyzed > 0 else 0
        empty_ratio = empty_alts / len(alt_texts) * 100 if alt_texts else 0
        
        print(f'   キーワード含有率: {keyword_alt_ratio:.1f}% (推奨: 50%以上)')
        print(f'   説明的alt率: {descriptive_ratio:.1f}% (推奨: 90%以上)')
        print(f'   空のalt率: {empty_ratio:.1f}% (推奨: 0%)')
    
    # 4. HTMLタグの意味構造（セマンティック）分析
    print(f'\n📝 HTMLセマンティック構造:')
    
    # 強調タグの使用状況
    strong_tags = re.findall(r'<strong[^>]*>(.*?)</strong>', content, re.DOTALL)
    em_tags = re.findall(r'<em[^>]*>(.*?)</em>', content, re.DOTALL)
    b_tags = re.findall(r'<b[^>]*>(.*?)</b>', content, re.DOTALL)
    i_tags = re.findall(r'<i[^>]*>(.*?)</i>', content, re.DOTALL)
    
    print(f'   <strong>タグ: {len(strong_tags)}個 (SEO推奨)')
    print(f'   <em>タグ: {len(em_tags)}個 (SEO推奨)')
    print(f'   <b>タグ: {len(b_tags)}個 (非推奨)')
    print(f'   <i>タグ: {len(i_tags)}個 (非推奨)')
    
    if len(b_tags) > 0 or len(i_tags) > 0:
        print('   ⚠️ <b><i>タグの代わりに<strong><em>タグ使用を推奨')
    
    # 強調タグ内のキーワード分析
    if strong_tags:
        keyword_strong = sum(1 for strong in strong_tags if any(kw in re.sub(r'<[^>]+>', '', strong) for kw in ['Audible', 'お金', '投資']))
        keyword_strong_ratio = keyword_strong / len(strong_tags) * 100
        print(f'   強調タグ内キーワード率: {keyword_strong_ratio:.1f}% (推奨: 30%以上)')
    
    # 5. リスト構造の最適化
    print(f'\n📋 リスト構造の最適化:')
    
    ul_tags = re.findall(r'<ul[^>]*>', content)
    ol_tags = re.findall(r'<ol[^>]*>', content)
    li_tags = re.findall(r'<li[^>]*>', content)
    
    print(f'   箇条書きリスト: {len(ul_tags)}個')
    print(f'   番号付きリスト: {len(ol_tags)}個')
    print(f'   リスト項目総数: {len(li_tags)}個')
    
    if len(ul_tags) + len(ol_tags) == 0:
        print('   ⚠️ リスト構造未使用（読みやすさとSEOに不利）')
    
    # 6. テーブル構造の最適化
    table_tags = re.findall(r'<table[^>]*>', content)
    th_tags = re.findall(r'<th[^>]*>', content)
    td_tags = re.findall(r'<td[^>]*>', content)
    
    print(f'\n📊 テーブル構造:')
    print(f'   テーブル数: {len(table_tags)}個')
    print(f'   ヘッダーセル数: {len(th_tags)}個')
    print(f'   データセル数: {len(td_tags)}個')
    
    if len(table_tags) > 0 and len(th_tags) == 0:
        print('   ⚠️ テーブルにヘッダー行（<th>）が未設定')
    
    # 7. 構造化マークアップの確認
    print(f'\n🏗️ 構造化マークアップ:')
    
    # Schema.org構造化データ
    json_ld = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', content, re.DOTALL)
    microdata = re.findall(r'itemtype=["\'][^"\']*["\']', content)
    
    print(f'   JSON-LD構造化データ: {len(json_ld)}個')
    print(f'   Microdata属性: {len(microdata)}個')
    
    if len(json_ld) == 0 and len(microdata) == 0:
        print('   ⚠️ 構造化データ未実装（リッチスニペット表示不可）')
    
    # 8. アクセシビリティとSEO
    print(f'\n♿ アクセシビリティ関連:')
    
    # aria属性の使用
    aria_labels = re.findall(r'aria-label=["\'][^"\']*["\']', content)
    aria_described = re.findall(r'aria-describedby=["\'][^"\']*["\']', content)
    
    print(f'   aria-label属性: {len(aria_labels)}個')
    print(f'   aria-describedby属性: {len(aria_described)}個')
    
    return True

if __name__ == "__main__":
    print('🚀 全記事のリンク・タグSEO最適化状況分析')
    print('='*80)
    
    target_posts = [2732, 2677, 2625, 2535, 2210, 649]
    
    for post_id in target_posts:
        analyze_link_and_tag_seo(post_id)
        print('\n' + '='*80 + '\n')
    
    print('📋 分析完了: リンクとタグの最適化状況を確認しました')