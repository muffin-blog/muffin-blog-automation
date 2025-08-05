"""
カテゴリ管理システム
カテゴリの追加・編集・削除を自動化
"""

import sys
import os
sys.path.append('/Users/satoumasamitsu/osigoto/ブログ自動化')

from wordpress_api import WordPressBlogAutomator
import requests

class CategoryManager:
    """カテゴリ管理クラス"""
    
    def __init__(self):
        self.wp = WordPressBlogAutomator(
            site_url="https://muffin-blog.com",
            username="muffin1203",
            password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
        )
    
    def list_categories(self):
        """現在のカテゴリ一覧を表示"""
        print("📂 現在のカテゴリ一覧:")
        print("-" * 40)
        
        categories = self.wp.get_categories()
        for cat in categories:
            print(f"   ID: {cat['id']} | {cat['name']} (投稿数: {cat['count']})")
            if cat.get('description'):
                print(f"      説明: {cat['description']}")
        
        return categories
    
    def add_category(self, name, description="", parent_id=0):
        """新しいカテゴリを追加"""
        try:
            data = {
                'name': name,
                'description': description
            }
            
            if parent_id > 0:
                data['parent'] = parent_id
                
            response = requests.post(f"{self.wp.api_url}/categories", 
                                   headers=self.wp.headers, 
                                   json=data)
            
            if response.status_code == 201:
                new_cat = response.json()
                print(f"✅ カテゴリ追加成功: '{name}' (ID: {new_cat['id']})")
                return new_cat['id']
            else:
                print(f"❌ カテゴリ追加失敗: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"❌ エラー: {e}")
            return None
    
    def update_category(self, category_id, name=None, description=None):
        """既存カテゴリを更新"""
        try:
            data = {}
            if name:
                data['name'] = name
            if description is not None:
                data['description'] = description
                
            response = requests.post(f"{self.wp.api_url}/categories/{category_id}", 
                                   headers=self.wp.headers, 
                                   json=data)
            
            if response.status_code == 200:
                updated_cat = response.json()
                print(f"✅ カテゴリ更新成功: '{updated_cat['name']}'")
                return True
            else:
                print(f"❌ カテゴリ更新失敗: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ エラー: {e}")
            return False
    
    def delete_category(self, category_id):
        """カテゴリを削除"""
        try:
            response = requests.delete(f"{self.wp.api_url}/categories/{category_id}", 
                                     headers=self.wp.headers)
            
            if response.status_code == 200:
                print(f"✅ カテゴリ削除成功: ID {category_id}")
                return True
            else:
                print(f"❌ カテゴリ削除失敗: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ エラー: {e}")
            return False
    
    def setup_recommended_categories(self):
        """おすすめカテゴリセットアップ"""
        print("🚀 おすすめカテゴリセットアップ開始")
        print("=" * 50)
        
        recommended_categories = [
            {
                'name': 'Audible活用術',
                'description': 'Audibleの効果的な使い方、おすすめ作品、活用テクニック'
            },
            {
                'name': '読書術・速読',
                'description': '効率的な読書方法、速読テクニック、読書習慣の作り方'
            },
            {
                'name': '学習・自己啓発',
                'description': '継続的な学習方法、スキルアップ、成長マインドセット'
            },
            {
                'name': '時間管理術',
                'description': '効率的な時間の使い方、生産性向上、ライフハック'
            },
            {
                'name': 'Kindle・電子書籍',
                'description': 'Kindle端末、電子書籍の活用法、読み放題サービス'
            },
            {
                'name': 'おすすめ本',
                'description': '厳選したおすすめ書籍、ジャンル別書籍紹介'
            },
            {
                'name': 'ブックレビュー',
                'description': '読了した本の詳細レビュー、感想、要約'
            }
        ]
        
        created_categories = []
        
        for cat_info in recommended_categories:
            cat_id = self.add_category(cat_info['name'], cat_info['description'])
            if cat_id:
                created_categories.append({
                    'id': cat_id,
                    'name': cat_info['name'],
                    'description': cat_info['description']
                })
        
        print(f"\n✅ {len(created_categories)}個のカテゴリを作成しました")
        return created_categories
    
    def update_homepage_categories(self, page_id=2821):
        """トップページのカテゴリ表示を更新"""
        print(f"🔄 トップページ(ID: {page_id})のカテゴリ表示を更新...")
        
        # 最新のカテゴリ情報でコンテンツを再生成
        updated_content = f"""
<!-- wp:group {{"align":"full","style":{{"spacing":{{"padding":{{"top":"60px","bottom":"60px"}}}}}},"backgroundColor":"white","className":"hero-section"}} -->
<div class="wp-block-group alignfull hero-section has-white-background-color has-background" style="padding-top:60px;padding-bottom:60px">
    <!-- wp:container -->
    <div class="wp-block-container">
        <!-- wp:columns {{"align":"wide"}} -->
        <div class="wp-block-columns alignwide">
            <!-- wp:column {{"width":"60%"}} -->
            <div class="wp-block-column" style="flex-basis:60%">
                <!-- wp:heading {{"level":1,"style":{{"typography":{{"fontSize":"3.5rem","lineHeight":"1.2"}},"color":{{"text":"#2c3e50"}}}} -->
                <h1 class="wp-block-heading" style="color:#2c3e50;font-size:3.5rem;line-height:1.2">READ<br>LEARN<br><span style="color:#e74c3c">GROW</span></h1>
                <!-- /wp:heading -->
                
                <!-- wp:paragraph {{"style":{{"typography":{{"fontSize":"1.2rem"}},"color":{{"text":"#34495e"}}}} -->
                <p style="color:#34495e;font-size:1.2rem">1年後の自分を楽にするブログ</p>
                <!-- /wp:paragraph -->
                
                <!-- wp:paragraph {{"style":{{"color":{{"text":"#7f8c8d"}}}} -->
                <p style="color:#7f8c8d">Audible・読書・学習で、あなたの成長をサポートします。</p>
                <!-- /wp:paragraph -->
            </div>
            <!-- /wp:column -->
            
            <!-- wp:column {{"width":"40%"}} -->
            <div class="wp-block-column" style="flex-basis:40%">
                <!-- wp:image {{"align":"center","style":{{"border":{{"radius":"20px"}}}} -->
                <figure class="wp-block-image aligncenter" style="border-radius:20px">
                    <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjZjBmOGZmIi8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTIwIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iNDAiIGZpbGw9IiMzNDk4ZGIiIHRleHQtYW5jaG9yPSJtaWRkbGUiPvCfp6E8L3RleHQ+Cjx0ZXh0IHg9IjE1MCIgeT0iMTgwIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMjQiIGZpbGw9IiM0MjczNWUiIHRleHQtYW5jaG9yPSJtaWRkbGUiPk1hZmZpbjwvdGV4dD4KPHRleHQgeD0iMTUwIiB5PSIyMTAiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIyNCIgZmlsbD0iIzQyNzM1ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+QmxvZzwvdGV4dD4KPC9zdmc+" alt="マフィンブログ"/>
                </figure>
                <!-- /wp:image -->
            </div>
            <!-- /wp:column -->
        </div>
        <!-- /wp:columns -->
    </div>
    <!-- /wp:container -->
</div>
<!-- /wp:group -->

<!-- wp:group {{"align":"full","style":{{"spacing":{{"padding":{{"top":"80px","bottom":"80px"}}}}}},"className":"audible-section"}} -->
<div class="wp-block-group alignfull audible-section" style="padding-top:80px;padding-bottom:80px">
    <!-- wp:container -->
    <div class="wp-block-container">
        <!-- wp:heading {{"textAlign":"center","level":2,"style":{{"typography":{{"fontSize":"2.5rem"}},"color":{{"text":"#2c3e50"}}}} -->
        <h2 class="wp-block-heading has-text-align-center" style="color:#2c3e50;font-size:2.5rem">🎧 Audible活用術</h2>
        <!-- /wp:heading -->
        
        <!-- wp:swell-blocks/post-list {{"postType":"post","postsToShow":6,"layout":"card","imageSize":"medium","categoryFilter":["Audible活用術"],"showDate":true,"showCategory":true}} /-->
        
        <!-- wp:buttons {{"layout":{{"type":"flex","justifyContent":"center"}}}} -->
        <div class="wp-block-buttons">
            <!-- wp:button {{"backgroundColor":"orange","textColor":"white","style":{{"border":{{"radius":"50px"}}}} -->
            <div class="wp-block-button">
                <a class="wp-block-button__link has-white-color has-orange-background-color has-text-color has-background wp-element-button" style="border-radius:50px" href="https://www.audible.co.jp/" target="_blank" rel="noopener">🎧 Audible 30日間無料体験</a>
            </div>
            <!-- /wp:button -->
        </div>
        <!-- /wp:buttons -->
    </div>
    <!-- /wp:container -->
</div>
<!-- /wp:group -->

<!-- wp:group {{"align":"full","style":{{"spacing":{{"padding":{{"top":"80px","bottom":"80px"}}}}}},"backgroundColor":"light-gray","className":"reading-section"}} -->
<div class="wp-block-group alignfull reading-section has-light-gray-background-color has-background" style="padding-top:80px;padding-bottom:80px">
    <!-- wp:container -->
    <div class="wp-block-container">
        <!-- wp:heading {{"textAlign":"center","level":2,"style":{{"typography":{{"fontSize":"2.5rem"}},"color":{{"text":"#2c3e50"}}}} -->
        <h2 class="wp-block-heading has-text-align-center" style="color:#2c3e50;font-size:2.5rem">📚 読書術・学習法</h2>
        <!-- /wp:heading -->
        
        <!-- wp:swell-blocks/post-list {{"postType":"post","postsToShow":6,"layout":"card","imageSize":"medium","categoryFilter":["読書術・速読","学習・自己啓発"],"showDate":true,"showCategory":true}} /-->
        
        <!-- wp:buttons {{"layout":{{"type":"flex","justifyContent":"center"}}}} -->
        <div class="wp-block-buttons">
            <!-- wp:button {{"backgroundColor":"blue","textColor":"white","style":{{"border":{{"radius":"50px"}}}} -->
            <div class="wp-block-button">
                <a class="wp-block-button__link has-white-color has-blue-background-color has-text-color has-background wp-element-button" style="border-radius:50px" href="/category/読書術・速読/">📖 読書術をもっと見る</a>
            </div>
            <!-- /wp:button -->
        </div>
        <!-- /wp:buttons -->
    </div>
    <!-- /wp:container -->
</div>
<!-- /wp:group -->

<!-- wp:group {{"align":"full","style":{{"spacing":{{"padding":{{"top":"80px","bottom":"80px"}}}}}},"className":"latest-posts-section"}} -->
<div class="wp-block-group alignfull latest-posts-section" style="padding-top:80px;padding-bottom:80px">
    <!-- wp:container -->
    <div class="wp-block-container">
        <!-- wp:heading {{"textAlign":"center","level":2,"style":{{"typography":{{"fontSize":"2.5rem"}},"color":{{"text":"#2c3e50"}}}} -->
        <h2 class="wp-block-heading has-text-align-center" style="color:#2c3e50;font-size:2.5rem">🕒 最新記事</h2>
        <!-- /wp:heading -->
        
        <!-- wp:swell-blocks/post-list {{"postType":"post","postsToShow":9,"layout":"card","imageSize":"medium","showDate":true,"showCategory":true}} /-->
    </div>
    <!-- /wp:container -->
</div>
<!-- /wp:group -->
"""
        
        try:
            update_data = {'content': updated_content}
            response = requests.post(f"{self.wp.api_url}/pages/{page_id}", 
                                   headers=self.wp.headers, 
                                   json=update_data)
            
            if response.status_code == 200:
                print("✅ トップページ更新完了!")
                return True
            else:
                print(f"❌ 更新失敗: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ エラー: {e}")
            return False

def main():
    """メイン実行"""
    cm = CategoryManager()
    
    print("📂 カテゴリ管理システム")
    print("=" * 40)
    
    # 現在のカテゴリ表示
    cm.list_categories()
    
    print(f"\n🚀 おすすめカテゴリを追加しますか？")
    print(f"追加されるカテゴリ:")
    print(f"- Audible活用術")
    print(f"- 読書術・速読") 
    print(f"- 学習・自己啓発")
    print(f"- 時間管理術")
    print(f"- Kindle・電子書籍")
    print(f"- おすすめ本")
    print(f"- ブックレビュー")

if __name__ == "__main__":
    main()