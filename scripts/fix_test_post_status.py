"""
テスト投稿を下書きに変更
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests

def fix_test_post_status():
    """公開済みのテスト投稿を下書きに変更"""
    
    wp = WordPressBlogAutomator(
        site_url="https://muffin-blog.com",
        username="muffin1203",
        password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
    )
    
    print("🔧 テスト投稿のステータス修正")
    print("=" * 40)
    
    # 問題のあるテスト投稿ID
    test_post_id = 2819
    
    try:
        # 現在のステータス確認
        response = requests.get(f"{wp.api_url}/posts/{test_post_id}", headers=wp.headers)
        if response.status_code == 200:
            post_data = response.json()
            current_status = post_data['status']
            title = post_data['title']['rendered']
            
            print(f"📄 投稿ID: {test_post_id}")
            print(f"📝 タイトル: {title}")
            print(f"📊 現在のステータス: {current_status}")
            
            if current_status == 'publish':
                print("⚠️  公開状態です！下書きに変更します...")
                
                # 下書きに変更
                update_data = {'status': 'draft'}
                response = requests.post(f"{wp.api_url}/posts/{test_post_id}", 
                                       headers=wp.headers, 
                                       json=update_data)
                
                if response.status_code == 200:
                    print("✅ 下書きに変更完了！")
                    updated_post = response.json()
                    print(f"📊 新しいステータス: {updated_post['status']}")
                else:
                    print(f"❌ 変更失敗: {response.status_code}")
                    print(response.text)
            else:
                print(f"✅ 既に {current_status} 状態です")
                
        else:
            print(f"❌ 投稿取得失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ エラー: {e}")

def check_all_test_posts():
    """すべてのテスト関連投稿をチェック"""
    
    wp = WordPressBlogAutomator(
        site_url="https://muffin-blog.com",
        username="muffin1203",
        password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
    )
    
    print("\n🔍 全投稿のステータス確認")
    print("=" * 40)
    
    try:
        # 最近の投稿を取得
        response = requests.get(f"{wp.api_url}/posts?per_page=10&status=publish,draft", 
                              headers=wp.headers)
        if response.status_code == 200:
            posts = response.json()
            
            test_posts = []
            for post in posts:
                title = post['title']['rendered']
                if 'テスト' in title or 'test' in title.lower() or 'audible' in title.lower():
                    test_posts.append({
                        'id': post['id'],
                        'title': title,
                        'status': post['status'],
                        'date': post['date'][:10]
                    })
            
            if test_posts:
                print("⚠️  テスト関連の投稿:")
                for post in test_posts:
                    status_emoji = "🟢" if post['status'] == 'publish' else "🟡"
                    print(f"   {status_emoji} ID:{post['id']} [{post['status']}] {post['title']} ({post['date']})")
            else:
                print("✅ テスト関連の公開投稿は見つかりませんでした")
        else:
            print(f"❌ 投稿一覧取得失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    print("🚨 テスト投稿ステータス修正ツール")
    print("=" * 50)
    
    # 特定のテスト投稿を下書きに変更
    fix_test_post_status()
    
    # 全体確認
    check_all_test_posts()
    
    print("\n✅ 修正完了！今後のテスト投稿は必ず'draft'ステータスにします。")