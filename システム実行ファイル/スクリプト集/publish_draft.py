"""
下書き記事を公開してアイキャッチを確認
"""

import requests
from wordpress_api import WordPressBlogAutomator

def publish_latest_draft():
    """最新の下書きを公開"""
    
    SITE_URL = "https://muffin-blog.com"
    USERNAME = "muffin1203"
    PASSWORD = "TMLy Z4Wi RhPu oVLm 0lcO gZdi"
    
    blog_automator = WordPressBlogAutomator(SITE_URL, USERNAME, PASSWORD)
    
    print("🔍 下書き記事を確認中...")
    
    try:
        # 下書き記事を取得
        response = requests.get(
            f"{SITE_URL}/wp-json/wp/v2/posts",
            headers=blog_automator.headers,
            params={'status': 'draft', 'per_page': 5, 'order': 'desc'}
        )
        
        if response.status_code == 200:
            drafts = response.json()
            
            if drafts:
                latest_draft = drafts[0]
                post_id = latest_draft['id']
                title = latest_draft['title']['rendered']
                featured_media = latest_draft.get('featured_media', 0)
                
                print(f"📝 最新下書き: {title}")
                print(f"   ID: {post_id}")
                print(f"   アイキャッチ画像ID: {featured_media}")
                
                if featured_media > 0:
                    print("✅ アイキャッチ画像が設定されています")
                    
                    # 記事を公開
                    publish_data = {'status': 'publish'}
                    publish_response = requests.post(
                        f"{SITE_URL}/wp-json/wp/v2/posts/{post_id}",
                        headers=blog_automator.headers,
                        json=publish_data
                    )
                    
                    if publish_response.status_code == 200:
                        published_post = publish_response.json()
                        print(f"🎉 記事公開成功!")
                        print(f"   URL: {published_post['link']}")
                        
                        # メディア詳細を取得して確認
                        media_response = requests.get(
                            f"{SITE_URL}/wp-json/wp/v2/media/{featured_media}",
                            headers=blog_automator.headers
                        )
                        
                        if media_response.status_code == 200:
                            media_data = media_response.json()
                            print(f"   🖼️ アイキャッチURL: {media_data['source_url']}")
                        
                        return published_post
                    else:
                        print(f"❌ 公開失敗: {publish_response.status_code}")
                else:
                    print("❌ アイキャッチ画像が設定されていません")
            else:
                print("下書き記事が見つかりません")
        else:
            print(f"❌ 下書き取得失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    return None

if __name__ == "__main__":
    print("=" * 50)
    print("下書き記事の公開とアイキャッチ確認")
    print("=" * 50)
    
    result = publish_latest_draft()
    
    if result:
        print(f"\n🎊 記事が正常に公開されました!")
        print(f"アイキャッチ画像の表示を確認してください: {result['link']}")
    else:
        print(f"\n❌ 公開に失敗しました")