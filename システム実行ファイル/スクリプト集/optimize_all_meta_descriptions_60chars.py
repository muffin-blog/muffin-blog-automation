"""
全記事のメタディスクリプションをスマホ上限60文字に最適化
完全自動化で手動作業なし
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests

def optimize_all_meta_descriptions_to_60chars():
    """全記事のメタディスクリプションを60文字に最適化"""
    
    wp = WordPressBlogAutomator(
        site_url="https://muffin-blog.com",
        username="muffin1203",
        password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
    )
    
    print("🎯 全記事メタディスクリプション60文字最適化")
    print("=" * 60)
    
    # 60文字に最適化されたメタディスクリプション
    optimized_meta_descriptions = {
        # Audible記事
        2732: "Audibleでお金の知識を身につけよう！貯蓄・節約・投資が学べるおすすめ書籍6選を厳選紹介。",
        2677: "Audibleの休会制度を完全ガイド！メリット・デメリット、退会との違い、手続き方法まで解説。",
        2625: "Audible退会・解約方法を徹底解説。事前チェックポイント7つと安心して始める方法を紹介。",
        2535: "Audibleの始め方を初心者向けに完全解説！アプリの使い方から料金プランまで世界一わかりやすく。",
        2210: "Audibleで人生が変わる！効率的な学習方法と時間活用術で通勤時間を自己投資の時間に変換。",
        
        # コミット車検記事
        649: "コスモ石油のコミっと車検を実際に利用した体験談。料金・サービス・注意点を実体験で詳しく解説。"
    }
    
    success_count = 0
    
    for post_id, meta_description in optimized_meta_descriptions.items():
        try:
            print(f"\\n🔄 記事ID {post_id} を60文字に最適化中...")
            
            # 文字数確認
            char_count = len(meta_description)
            print(f"   文字数: {char_count}文字（目標60文字）")
            
            if char_count > 60:
                print(f"   ⚠️  {char_count - 60}文字オーバー - 調整します")
                # 60文字以内に調整
                meta_description = meta_description[:57] + "..."
                char_count = len(meta_description)
                print(f"   調整後: {char_count}文字")
            
            print(f"   内容: {meta_description}")
            
            # WordPress抜粋を更新
            update_data = {
                'excerpt': meta_description
            }
            
            response = requests.post(f"{wp.api_url}/posts/{post_id}", 
                                   headers=wp.headers, 
                                   json=update_data)
            
            if response.status_code == 200:
                print(f"   ✅ 60文字最適化完了")
                success_count += 1
            else:
                print(f"   ❌ 最適化失敗 ({response.status_code})")
                print(f"   エラー: {response.text}")
                
        except Exception as e:
            print(f"   ❌ 記事ID {post_id}: エラー - {e}")
    
    print(f"\\n🎯 60文字最適化完了: {success_count}/{len(optimized_meta_descriptions)}件")
    return success_count

def verify_60char_optimization():
    """60文字最適化の結果を確認"""
    
    wp = WordPressBlogAutomator(
        site_url="https://muffin-blog.com",
        username="muffin1203",
        password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
    )
    
    print("\\n🔍 60文字最適化結果の確認")
    print("=" * 40)
    
    target_post_ids = [2732, 2677, 2625, 2535, 2210, 649]
    
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
                char_count = len(clean_excerpt)
                
                print(f"\\n📖 記事ID {post_id}: {title[:30]}...")
                print(f"   文字数: {char_count}文字")
                print(f"   内容: {clean_excerpt}")
                
                # 文字数判定
                if char_count <= 60:
                    print("   ✅ 60文字以内で最適化済み")
                else:
                    print(f"   ⚠️  {char_count - 60}文字オーバー")
                    
            else:
                print(f"❌ 記事ID {post_id}: 取得失敗")
                
        except Exception as e:
            print(f"❌ 記事ID {post_id}: エラー - {e}")

if __name__ == "__main__":
    print("🚀 全記事メタディスクリプション60文字最適化ツール")
    print("スマホ検索結果での表示を最大化する完全自動最適化")
    print("=" * 70)
    
    # Step 1: 全記事を60文字に最適化
    success_count = optimize_all_meta_descriptions_to_60chars()
    
    # Step 2: 最適化結果を確認
    verify_60char_optimization()
    
    print(f"\\n✅ 60文字最適化完了！")
    print(f"🎯 {success_count}件の記事をスマホ検索結果に最適化しました")
    print("📱 スマホでの検索結果表示が最大化されます")