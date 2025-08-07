"""
記事のメタディスクリプション更新スクリプト
ブログカードで表示される文章を記事冒頭からメタディスクリプションに変更
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests

def update_post_meta_description(post_id, meta_description):
    """特定の記事のメタディスクリプションを更新"""
    
    wp = WordPressBlogAutomator(
        site_url="https://muffin-blog.com",
        username="muffin1203",
        password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
    )
    
    try:
        # 記事の更新データ
        update_data = {
            'excerpt': meta_description  # WordPressではexcerptがメタディスクリプションとして使用される
        }
        
        # 記事を更新
        response = requests.post(f"{wp.api_url}/posts/{post_id}", 
                               headers=wp.headers, 
                               json=update_data)
        
        if response.status_code == 200:
            print(f"✅ 記事ID {post_id} のメタディスクリプションを更新しました")
            return True
        else:
            print(f"❌ 更新失敗: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def update_audible_post_meta():
    """Audible記事のメタディスクリプションを更新"""
    
    wp = WordPressBlogAutomator(
        site_url="https://muffin-blog.com",
        username="muffin1203",
        password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
    )
    
    print("🔍 Audible記事を検索中...")
    
    try:
        # Audible関連記事を検索
        response = requests.get(f"{wp.api_url}/posts?search=Audible&per_page=100", 
                               headers=wp.headers)
        
        if response.status_code == 200:
            posts = response.json()
            
            print(f"📄 {len(posts)}件のAudible関連記事が見つかりました")
            
            for post in posts:
                post_id = post['id']
                title = post['title']['rendered']
                current_excerpt = post['excerpt']['rendered']
                
                print(f"\n📖 記事: {title}")
                print(f"現在の抜粋: {current_excerpt[:100]}...")
                
                # Audible記事用の最適化されたメタディスクリプション
                if "始め方" in title:
                    new_meta = "Audibleの始め方を初心者向けに完全解説！アプリの使い方から料金プラン、おすすめ機能まで、世界一分かりやすくガイドします。"
                elif "活用" in title or "人生" in title:
                    new_meta = "Audibleで人生が変わる！効率的な学習方法と時間活用術を紹介。通勤時間を自己投資の時間に変える具体的な方法を解説します。"
                elif "貯蓄" in title or "節約" in title:
                    new_meta = "Audibleでお金の知識を身につけよう！貯蓄・節約・投資が学べるおすすめ書籍6選を厳選紹介。お金の勉強を楽しく続ける方法も解説。"
                elif "休会" in title:
                    new_meta = "Audibleの休会制度を完全ガイド！メリット・デメリット、退会との違い、手続き方法まで分かりやすく解説します。"
                else:
                    # 汎用的なAudible記事用メタディスクリプション
                    new_meta = "Audibleを活用した効率的な学習方法を詳しく解説。忙しい日常でも読書時間を確保し、知識を身につける具体的なノウハウを紹介します。"
                
                print(f"新しいメタディスクリプション: {new_meta}")
                
                # 自動更新実行
                print("🔄 更新中...")
                success = update_post_meta_description(post_id, new_meta)
                if success:
                    print("✅ 更新完了")
                else:
                    print("❌ 更新失敗")
                
        else:
            print(f"❌ 記事検索失敗: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ エラー: {e}")

def update_specific_post_meta():
    """特定記事のメタディスクリプションを手動更新"""
    
    print("📝 特定記事のメタディスクリプション更新")
    print("=" * 50)
    
    post_id = input("記事ID を入力してください: ")
    meta_description = input("新しいメタディスクリプションを入力してください: ")
    
    if post_id and meta_description:
        success = update_post_meta_description(post_id, meta_description)
        if success:
            print("✅ メタディスクリプションの更新が完了しました")
        else:
            print("❌ 更新に失敗しました")
    else:
        print("❌ 記事IDとメタディスクリプションの両方を入力してください")

def get_all_posts_with_excerpts():
    """全記事の現在の抜粋を確認"""
    
    wp = WordPressBlogAutomator(
        site_url="https://muffin-blog.com",
        username="muffin1203",
        password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
    )
    
    try:
        response = requests.get(f"{wp.api_url}/posts?per_page=100", 
                               headers=wp.headers)
        
        if response.status_code == 200:
            posts = response.json()
            
            print("📋 全記事の抜粋一覧:")
            print("=" * 80)
            
            for post in posts:
                title = post['title']['rendered']
                excerpt = post['excerpt']['rendered']
                post_id = post['id']
                
                print(f"\n🆔 ID: {post_id}")
                print(f"📖 タイトル: {title}")
                print(f"📄 現在の抜粋: {excerpt.strip()[:150]}...")
                print("-" * 80)
                
        else:
            print(f"❌ 記事取得失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    print("🔧 メタディスクリプション更新ツール")
    print("=" * 50)
    
    # ユーザーからの明示的なリクエストによりAudible記事の一括更新を実行
    print("\n🎯 Audible記事のメタディスクリプション一括更新を開始します...")
    update_audible_post_meta()
    print("\n✅ 処理完了しました")