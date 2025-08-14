"""
Amazonアフィリエイトリンク切れを緊急修正
正常なリンクに一括置換
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests
import re

def fix_broken_amazon_links():
    """Amazonアフィリエイトリンクを緊急修正"""
    
    wp = WordPressBlogAutomator()  # 環境変数から自動読み込み
    
    print("🚨 Amazonアフィリエイトリンク緊急修正開始")
    print("=" * 60)
    
    # 壊れたリンクパターンと修正用リンクのマッピング
    link_fixes = {
        # Audible無料体験リンク
        "https://amzn.to/4aT9CEq": "https://www.amazon.co.jp/hz/audible/mlp?tag=muffinblog-22",
        "https://amzn.to/448KFmv": "https://www.amazon.co.jp/hz/audible/mlp?tag=muffinblog-22",
        "https://amzn.to/48zZVu1": "https://www.amazon.co.jp/hz/audible/mlp?tag=muffinblog-22",
        "https://amzn.to/47KQfvl": "https://www.amazon.co.jp/hz/audible/mlp?tag=muffinblog-22",
        "https://amzn.to/4banoUb": "https://www.amazon.co.jp/hz/audible/mlp?tag=muffinblog-22",
        "https://amzn.to/4b4AnXA": "https://www.amazon.co.jp/hz/audible/mlp?tag=muffinblog-22",
        "https://amzn.to/429b9mK": "https://www.amazon.co.jp/hz/audible/mlp?tag=muffinblog-22",
        "https://amzn.to/4b4j0WT": "https://www.amazon.co.jp/hz/audible/mlp?tag=muffinblog-22",
        
        # Amazon登録ページの修正
        "https://www.amazon.co.jp/ap/register": "https://www.amazon.co.jp/hz/audible/mlp?tag=muffinblog-22",
        
        # Audibleサポートページの修正
        "https://www.audible.co.jp/contactus": "https://help.audible.co.jp/s/",
        
        # Amazonサポートページの修正
        "https://www.amazon.co.jp/hz/contact-us/foresight/hubgateway": "https://www.amazon.co.jp/gp/help/customer/contact-us",
    }
    
    # 修正対象記事ID
    target_posts = [2732, 2677, 2625, 2535, 2210]
    
    total_fixes = 0
    
    for post_id in target_posts:
        try:
            print(f"\n🔧 記事ID {post_id} のリンク修正中...")
            
            # 記事取得
            response = requests.get(f"{wp.api_url}/posts/{post_id}", headers=wp.headers)
            if response.status_code != 200:
                print(f"❌ 記事ID {post_id} 取得失敗")
                continue
                
            post = response.json()
            title = post['title']['rendered']
            content = post['content']['rendered']
            
            print(f"   記事: {title[:40]}...")
            
            # リンク修正実行
            modified_content = content
            post_fixes = 0
            
            for broken_link, fixed_link in link_fixes.items():
                if broken_link in modified_content:
                    # URLパラメータを含む部分一致も対応
                    pattern = re.escape(broken_link)
                    matches = re.findall(pattern + r'[^"\s]*', modified_content)
                    
                    for match in matches:
                        modified_content = modified_content.replace(match, fixed_link)
                        post_fixes += 1
                        print(f"   ✅ 修正: {match[:60]}... → {fixed_link[:60]}...")
            
            # Audible商品ページのリンク修正（クエリパラメータ削除）
            audible_pattern = r'https://www\.audible\.co\.jp/pd/[^"\s]*(\?[^"\s]*)?'
            audible_matches = re.findall(audible_pattern, modified_content)
            
            for match in audible_matches:
                if '?' in match:
                    clean_url = match.split('?')[0] + "?tag=muffinblog-22"
                    modified_content = modified_content.replace(match, clean_url)
                    post_fixes += 1
                    print(f"   ✅ Audible商品リンク最適化: {match[:60]}...")
            
            # 修正がある場合のみ更新
            if post_fixes > 0:
                update_data = {'content': modified_content}
                update_response = requests.post(f"{wp.api_url}/posts/{post_id}", 
                                              headers=wp.headers, 
                                              json=update_data)
                
                if update_response.status_code == 200:
                    print(f"   ✅ 記事ID {post_id}: {post_fixes}件のリンクを修正完了")
                    total_fixes += post_fixes
                else:
                    print(f"   ❌ 記事ID {post_id}: 更新失敗 ({update_response.status_code})")
            else:
                print(f"   ℹ️ 記事ID {post_id}: 修正対象リンクなし")
                
        except Exception as e:
            print(f"❌ 記事ID {post_id}: エラー - {e}")
    
    print(f"\n🎯 リンク修正完了!")
    print(f"総修正件数: {total_fixes}件")
    
    return total_fixes

def add_sponsored_attributes():
    """Amazonリンクにsponsored属性を追加"""
    
    wp = WordPressBlogAutomator()  # 環境変数から自動読み込み
    
    print("\n🏷️ Amazonリンクにsponsored属性追加")
    print("-" * 40)
    
    target_posts = [2732, 2677, 2625, 2535, 2210]
    
    for post_id in target_posts:
        try:
            response = requests.get(f"{wp.api_url}/posts/{post_id}", headers=wp.headers)
            if response.status_code != 200:
                continue
                
            post = response.json()
            content = post['content']['rendered']
            
            # Amazonリンクにrel="sponsored"を追加
            amazon_pattern = r'<a([^>]*href=["\'][^"\']*amazon[^"\']*["\'][^>]*)>'
            
            def add_sponsored(match):
                link_attrs = match.group(1)
                if 'rel=' not in link_attrs:
                    return f'<a{link_attrs} rel="sponsored nofollow">'
                elif 'sponsored' not in link_attrs:
                    # 既存のrel属性に追加
                    link_attrs = re.sub(r'rel=["\']([^"\']*)["\']', 
                                      r'rel="\1 sponsored"', link_attrs)
                    return f'<a{link_attrs}>'
                return match.group(0)
            
            modified_content = re.sub(amazon_pattern, add_sponsored, content)
            
            if modified_content != content:
                update_data = {'content': modified_content}
                update_response = requests.post(f"{wp.api_url}/posts/{post_id}", 
                                              headers=wp.headers, 
                                              json=update_data)
                
                if update_response.status_code == 200:
                    print(f"   ✅ 記事ID {post_id}: sponsored属性追加完了")
                else:
                    print(f"   ❌ 記事ID {post_id}: 属性追加失敗")
            else:
                print(f"   ℹ️ 記事ID {post_id}: 既に設定済み")
                
        except Exception as e:
            print(f"❌ 記事ID {post_id}: エラー - {e}")

if __name__ == "__main__":
    print("🚨 Amazonリンク緊急修正システム")
    print("=" * 60)
    
    # Step 1: 壊れたリンクを修正
    fixes = fix_broken_amazon_links()
    
    # Step 2: sponsored属性を追加
    add_sponsored_attributes()
    
    print(f"\n✅ 緊急修正完了!")
    print(f"💰 {fixes}件のアフィリエイトリンクが復活しました")
    print("🔍 再度ヘルスチェックを実行して確認することを推奨します")