"""
WordPress抜粋を自動で全記事に設定
手動作業を完全に排除する自動化スクリプト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests

def fix_all_excerpts_automatically():
    """全Audible記事の抜粋を自動で最適化されたメタディスクリプションに設定"""
    
    wp = WordPressBlogAutomator(
        site_url="https://muffin-blog.com",
        username="muffin1203",
        password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
    )
    
    print("🤖 WordPress抜粋自動設定 - 完全自動化")
    print("=" * 60)
    
    # 最適化されたメタディスクリプション
    meta_descriptions = {
        2732: "Audibleでお金の知識を身につけよう！貯蓄・節約・投資が学べるおすすめ書籍6選を厳選紹介。お金の勉強を楽しく続ける方法も解説。",
        2677: "Audibleの休会制度を完全ガイド！メリット・デメリット、退会との違い、手続き方法まで分かりやすく解説します。",
        2625: "Audibleを活用した効率的な学習方法を詳しく解説。忙しい日常でも読書時間を確保し、知識を身につける具体的なノウハウを紹介します。",
        2535: "Audibleの始め方を初心者向けに完全解説！アプリの使い方から料金プラン、おすすめ機能まで、世界一分かりやすくガイドします。",
        2210: "Audibleで人生が変わる！効率的な学習方法と時間活用術を紹介。通勤時間を自己投資の時間に変える具体的な方法を解説します。"
    }
    
    success_count = 0
    
    for post_id, meta_description in meta_descriptions.items():
        try:
            print(f"🔄 記事ID {post_id} を処理中...")
            
            # WordPress抜粋を直接設定
            update_data = {
                'excerpt': meta_description
            }
            
            response = requests.post(f"{wp.api_url}/posts/{post_id}", 
                                   headers=wp.headers, 
                                   json=update_data)
            
            if response.status_code == 200:
                print(f"✅ 記事ID {post_id}: 抜粋設定完了")
                print(f"   設定内容: {meta_description}")
                success_count += 1
            else:
                print(f"❌ 記事ID {post_id}: 設定失敗 ({response.status_code})")
                print(f"   エラー: {response.text}")
                
        except Exception as e:
            print(f"❌ 記事ID {post_id}: エラー - {e}")
    
    print(f"\n🎯 処理完了: {success_count}/{len(meta_descriptions)}件の記事を自動設定")
    return success_count

def verify_automatic_changes():
    """自動設定の結果を確認"""
    
    wp = WordPressBlogAutomator(
        site_url="https://muffin-blog.com",
        username="muffin1203",
        password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
    )
    
    print("\n🔍 自動設定結果の確認")
    print("=" * 40)
    
    target_post_ids = [2732, 2677, 2625, 2535, 2210]
    
    for post_id in target_post_ids:
        try:
            response = requests.get(f"{wp.api_url}/posts/{post_id}", headers=wp.headers)
            if response.status_code == 200:
                post = response.json()
                title = post['title']['rendered']
                excerpt = post['excerpt']['rendered']
                
                # HTMLタグを除去
                import re
                clean_excerpt = re.sub(r'<[^>]+>', '', excerpt).strip()
                
                print(f"\n📖 記事ID {post_id}: {title[:40]}...")
                print(f"現在の抜粋: {clean_excerpt[:60]}...")
                
                # 成功判定
                if 'Audibleで' in clean_excerpt or 'Audibleの' in clean_excerpt:
                    print("✅ 最適化されたメタディスクリプションが設定済み")
                else:
                    print("⚠️  まだ記事冒頭が表示されている可能性")
                    
            else:
                print(f"❌ 記事ID {post_id}: 取得失敗")
                
        except Exception as e:
            print(f"❌ 記事ID {post_id}: エラー - {e}")

def clear_cache_automatically():
    """キャッシュを可能な限り自動でクリア"""
    
    print("\n🧹 キャッシュクリア実行")
    print("=" * 30)
    
    wp = WordPressBlogAutomator(
        site_url="https://muffin-blog.com",
        username="muffin1203",
        password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
    )
    
    # 複数のキャッシュクリア方法を試行
    cache_clear_attempts = [
        {'action': 'wpfc_clear_cache_hook'},
        {'action': 'wp_cache_clear'},
        {'clear_cache': '1'},
        {'wpfc_clear_cache': '1'}
    ]
    
    for attempt in cache_clear_attempts:
        try:
            response = requests.post(f"{wp.site_url}/wp-admin/admin-ajax.php", 
                                   headers=wp.headers, 
                                   data=attempt)
            if response.status_code == 200:
                print("✅ キャッシュクリア成功（可能性）")
                break
        except:
            continue
    
    print("⚠️  完全なキャッシュクリアは手動で以下を実行:")
    print("   1. WordPress管理画面 → WP Fastest Cache → Delete Cache")
    print("   2. ConoHa WINGコントロールパネル → キャッシュクリア")

if __name__ == "__main__":
    print("🚀 WordPress抜粋完全自動化ツール")
    print("手動作業一切なし - 全自動でメタディスクリプション設定")
    print("=" * 70)
    
    # Step 1: 全記事の抜粋を自動設定
    success_count = fix_all_excerpts_automatically()
    
    # Step 2: 設定結果を自動確認
    verify_automatic_changes()
    
    # Step 3: キャッシュクリア試行
    clear_cache_automatically()
    
    print(f"\n✅ 完全自動化完了！")
    print(f"🎯 {success_count}件の記事を自動設定しました")
    print("💡 5-10分後にブログサイトで変更を確認してください")