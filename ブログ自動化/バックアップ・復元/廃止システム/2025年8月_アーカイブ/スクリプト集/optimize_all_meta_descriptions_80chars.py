"""
全記事のメタディスクリプションを80文字上限に最適化
PC・スマホ両対応での完全自動最適化
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests

def optimize_all_meta_descriptions_to_80chars():
    """全記事のメタディスクリプションを80文字上限に最適化"""
    
    wp = WordPressBlogAutomator()  # 環境変数から自動読み込み
    
    print("🎯 全記事メタディスクリプション80文字上限最適化")
    print("=" * 60)
    
    # 80文字上限に最適化されたメタディスクリプション
    optimized_meta_descriptions = {
        # Audible記事
        2732: "Audibleでお金の知識を身につけよう！貯蓄・節約・投資が学べるおすすめ書籍6選を厳選紹介。お金の勉強を楽しく続ける方法も詳しく解説します。",
        2677: "Audibleの休会制度を完全ガイド！メリット・デメリット、退会との違い、手続き方法まで分かりやすく解説。忙しい時期の活用法も紹介します。",
        2625: "Audible退会・解約方法を徹底解説。事前チェックポイント7つと安心して始める方法を紹介。解約前の重要な確認事項もまとめました。",
        2535: "Audibleの始め方を初心者向けに完全解説！アプリの使い方から料金プラン、おすすめ機能まで世界一分かりやすくガイドします。",
        2210: "Audibleで人生が変わる！効率的な学習方法と時間活用術で通勤時間を自己投資の時間に変換。1年後の自分を楽にする習慣術を紹介。",
        
        # コミット車検記事
        649: "コスモ石油のコミっと車検を実際に利用した体験談。料金・サービス・注意点を実体験で詳しく解説。車検選びの参考にどうぞ。"
    }
    
    success_count = 0
    
    for post_id, meta_description in optimized_meta_descriptions.items():
        try:
            print(f"\\n🔄 記事ID {post_id} を80文字上限に最適化中...")
            
            # 文字数確認
            char_count = len(meta_description)
            print(f"   文字数: {char_count}文字（上限80文字）")
            
            if char_count > 80:
                print(f"   ⚠️  {char_count - 80}文字オーバー - 調整します")
                # 80文字以内に調整
                meta_description = meta_description[:77] + "..."
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
                print(f"   ✅ 80文字上限最適化完了")
                success_count += 1
            else:
                print(f"   ❌ 最適化失敗 ({response.status_code})")
                print(f"   エラー: {response.text}")
                
        except Exception as e:
            print(f"   ❌ 記事ID {post_id}: エラー - {e}")
    
    print(f"\\n🎯 80文字上限最適化完了: {success_count}/{len(optimized_meta_descriptions)}件")
    return success_count

def verify_80char_optimization():
    """80文字上限最適化の結果を確認"""
    
    wp = WordPressBlogAutomator()  # 環境変数から自動読み込み
    
    print("\\n🔍 80文字上限最適化結果の確認")
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
                if char_count <= 80:
                    if char_count >= 70:
                        print("   ✅ 70-80文字の最適範囲で設定済み")
                    else:
                        print("   ✅ 80文字以内で設定済み")
                else:
                    print(f"   ⚠️  {char_count - 80}文字オーバー")
                    
            else:
                print(f"❌ 記事ID {post_id}: 取得失敗")
                
        except Exception as e:
            print(f"❌ 記事ID {post_id}: エラー - {e}")

if __name__ == "__main__":
    print("🚀 全記事メタディスクリプション80文字上限最適化ツール")
    print("PC・スマホ両デバイス対応の完全自動最適化")
    print("=" * 70)
    
    # Step 1: 全記事を80文字上限に最適化
    success_count = optimize_all_meta_descriptions_to_80chars()
    
    # Step 2: 最適化結果を確認
    verify_80char_optimization()
    
    print(f"\\n✅ 80文字上限最適化完了！")
    print(f"🎯 {success_count}件の記事をPC・スマホ両対応に最適化しました")
    print("💻📱 PC・スマホでの検索結果表示が最大化されます")