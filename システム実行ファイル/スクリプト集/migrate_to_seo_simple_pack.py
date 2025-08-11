"""
SEO SIMPLE PACKに統一：WordPress抜粋からSEOメタディスクリプションへ移行
最適な方法でメタディスクリプション管理を一元化
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests

def migrate_excerpts_to_seo_simple_pack():
    """WordPress抜粋をSEO SIMPLE PACKのメタディスクリプションに移行"""
    
    wp = WordPressBlogAutomator(
        site_url="https://muffin-blog.com",
        username="muffin1203",
        password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
    )
    
    print("🔄 SEO SIMPLE PACKへの移行開始")
    print("=" * 60)
    
    try:
        # Audible関連記事を取得
        response = requests.get(f"{wp.api_url}/posts?search=Audible&per_page=100", 
                               headers=wp.headers)
        
        if response.status_code == 200:
            posts = response.json()
            
            print(f"📄 {len(posts)}件のAudible関連記事を処理中...")
            
            success_count = 0
            
            for post in posts:
                post_id = post['id']
                title = post['title']['rendered']
                current_excerpt = post['excerpt']['rendered']
                
                # HTMLタグを除去してテキストのみ抽出
                import re
                clean_excerpt = re.sub(r'<[^>]+>', '', current_excerpt).strip()
                
                if clean_excerpt and len(clean_excerpt) > 10:
                    print(f"\n📖 記事: {title}")
                    print(f"移行する内容: {clean_excerpt}")
                    
                    # SEO SIMPLE PACKのメタディスクリプションフィールドに設定
                    update_data = {
                        'meta': {
                            '_ssp_description': clean_excerpt
                        },
                        'excerpt': ''  # WordPress抜粋を空にする
                    }
                    
                    # 記事を更新
                    response = requests.post(f"{wp.api_url}/posts/{post_id}", 
                                           headers=wp.headers, 
                                           json=update_data)
                    
                    if response.status_code == 200:
                        print("✅ SEO SIMPLE PACKに移行完了")
                        success_count += 1
                    else:
                        print(f"❌ 移行失敗: {response.status_code}")
                        print(response.text)
                else:
                    print(f"\n⏭️  スキップ: {title} (抜粋が空または短すぎる)")
            
            print(f"\n🎯 移行完了: {success_count}件の記事を処理しました")
            
        else:
            print(f"❌ 記事取得失敗: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ エラー: {e}")

def verify_migration():
    """移行結果を確認"""
    
    wp = WordPressBlogAutomator(
        site_url="https://muffin-blog.com",
        username="muffin1203",
        password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
    )
    
    print("\n🔍 移行結果の確認")
    print("=" * 40)
    
    try:
        # 移行済み記事を確認
        response = requests.get(f"{wp.api_url}/posts?search=Audible&per_page=10", 
                               headers=wp.headers)
        
        if response.status_code == 200:
            posts = response.json()
            
            for post in posts:
                title = post['title']['rendered']
                excerpt = post['excerpt']['rendered']
                meta = post.get('meta', {})
                ssp_description = meta.get('_ssp_description', '未設定')
                
                print(f"\n📖 {title}")
                print(f"   WordPress抜粋: {'空' if not excerpt.strip() else '設定済み'}")
                print(f"   SEO SIMPLE PACK: {ssp_description[:50]}..." if len(ssp_description) > 50 else f"   SEO SIMPLE PACK: {ssp_description}")
                
        else:
            print(f"❌ 確認失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    print("🚀 SEO SIMPLE PACK統一移行ツール")
    print("WordPress抜粋 → SEO SIMPLE PACKメタディスクリプション")
    print("=" * 70)
    
    # Step 1: 移行実行
    migrate_excerpts_to_seo_simple_pack()
    
    # Step 2: 移行結果確認
    verify_migration()
    
    print("\n✅ 移行処理完了！")
    print("今後はWordPress管理画面の各記事でSEO SIMPLE PACKの")
    print("メタディスクリプション欄でSEO設定を一元管理してください。")