"""
実際のブログカテゴリ構造を取得
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests

def get_blog_categories():
    """実際のブログカテゴリを取得"""
    
    wp = WordPressBlogAutomator(
        site_url="https://muffin-blog.com",
        username="muffin1203",
        password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
    )
    
    print("📂 実際のブログカテゴリ構造を取得中...")
    print("=" * 50)
    
    try:
        # カテゴリ一覧を取得
        response = requests.get(f"{wp.api_url}/categories?per_page=100", headers=wp.headers)
        
        if response.status_code == 200:
            categories = response.json()
            
            print(f"✅ 取得成功！カテゴリ数: {len(categories)}")
            print("\n📋 カテゴリ一覧:")
            print("-" * 50)
            
            # 親カテゴリと子カテゴリを分けて整理
            parent_categories = {}
            child_categories = []
            
            for cat in categories:
                if cat['parent'] == 0:
                    parent_categories[cat['id']] = {
                        'name': cat['name'],
                        'slug': cat['slug'],
                        'count': cat['count'],
                        'children': []
                    }
                else:
                    child_categories.append(cat)
            
            # 子カテゴリを親に紐付け
            for child in child_categories:
                parent_id = child['parent']
                if parent_id in parent_categories:
                    parent_categories[parent_id]['children'].append({
                        'name': child['name'],
                        'slug': child['slug'],
                        'count': child['count']
                    })
            
            # 結果を表示
            for parent_id, parent in parent_categories.items():
                print(f"📁 {parent['name']} ({parent['count']}件)")
                print(f"   slug: {parent['slug']}")
                if parent['children']:
                    for child in parent['children']:
                        print(f"   └── {child['name']} ({child['count']}件) [slug: {child['slug']}]")
                print()
            
            return parent_categories
            
        else:
            print(f"❌ カテゴリ取得失敗: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None

if __name__ == "__main__":
    categories = get_blog_categories()
    
    if categories:
        print("\n🎯 LP用カテゴリ設計の提案:")
        print("=" * 50)
        
        # 投稿数の多い順にソート
        sorted_cats = sorted(categories.items(), key=lambda x: x[1]['count'], reverse=True)
        
        print("\n📊 投稿数順:")
        for i, (cat_id, cat_data) in enumerate(sorted_cats[:8], 1):
            print(f"{i}. {cat_data['name']} ({cat_data['count']}件)")
            if cat_data['children']:
                for child in cat_data['children']:
                    print(f"   └── {child['name']} ({child['count']}件)")
        
        print("\n💡 LP用推奨カテゴリセクション構成:")
        print("1. メインカテゴリ4つを選択")
        print("2. 各カテゴリで「左大きく1つ + 右小さく3つ」レイアウト")
        print("3. SWELLの投稿リストブロック活用")
    else:
        print("\n❌ カテゴリ取得に失敗しました")