"""
完全自動ブログ投稿システム
記事生成 → 画像作成 → WordPress投稿
"""

from blog_article_generator import BlogStyleAnalyzer, BlogArticleGenerator
from canva_image_generator import SimpleImageGenerator
from wordpress_api import WordPressBlogAutomator
import os

def complete_blog_automation(theme: str, keywords: list, title: str = ""):
    """
    完全自動ブログ投稿
    
    Args:
        theme: 記事テーマ（audible, learning, money, etc.）
        keywords: 関連キーワードのリスト
        title: カスタムタイトル（オプション）
    
    Returns:
        投稿結果の辞書
    """
    print("🚀 Claude完全自動ブログシステム開始")
    
    # 1. 記事スタイル分析・生成
    print("📝 ステップ1: 記事生成...")
    articles_path = "/Users/satoumasamitsu/osigoto/ポートフォリオサイト/public/content/articles/articles.json"
    
    try:
        style_analyzer = BlogStyleAnalyzer(articles_path)
        article_generator = BlogArticleGenerator(style_analyzer)
        
        article_data = article_generator.create_complete_article(
            theme=theme,
            keywords=keywords,
            custom_title=title
        )
        
        print(f"✅ 記事生成完了: {article_data['title']}")
        
    except Exception as e:
        print(f"❌ 記事生成エラー: {e}")
        return None
    
    # 2. アイキャッチ画像生成
    print("🎨 ステップ2: 画像生成...")
    try:
        image_generator = SimpleImageGenerator()
        image_path = image_generator.create_simple_image(
            title=article_data['title'],
            theme=theme
        )
        print(f"✅ 画像生成完了: {image_path}")
        
    except Exception as e:
        print(f"❌ 画像生成エラー: {e}")
        image_path = None
    
    # 3. WordPress投稿
    print("📤 ステップ3: WordPress投稿...")
    try:
        # WordPress設定
        SITE_URL = "https://muffin-blog.com"
        USERNAME = "muffin1203"
        PASSWORD = "TMLy Z4Wi RhPu oVLm 0lcO gZdi"
        
        blog_automator = WordPressBlogAutomator(SITE_URL, USERNAME, PASSWORD)
        
        # 投稿データ準備
        post_result = blog_automator.create_post(
            title=article_data['title'],
            content=article_data['content'],
            category=article_data['category'],
            tags=article_data['tags'],
            meta_description=article_data['meta_description'],
            featured_image_path=image_path,
            status="draft"  # 下書きとして保存
        )
        
        if post_result:
            print(f"✅ WordPress投稿完了!")
            print(f"   記事ID: {post_result['id']}")
            print(f"   URL: {post_result['link']}")
            
            return {
                "success": True,
                "article": article_data,
                "image_path": image_path,
                "wordpress_post": post_result
            }
        else:
            print("❌ WordPress投稿失敗")
            return None
            
    except Exception as e:
        print(f"❌ WordPress投稿エラー: {e}")
        return None

if __name__ == "__main__":
    # テスト実行
    print("=" * 50)
    print("Claude完全自動ブログシステム デモ")
    print("=" * 50)
    
    result = complete_blog_automation(
        theme="audible",
        keywords=["効率的学習", "時間活用", "読書術"],
        title="Audibleで時間を有効活用！忙しい人のための効率的読書術"
    )
    
    if result:
        print("\n🎉 全システム動作成功！")
        print(f"📝 記事: {result['article']['title']}")
        print(f"🎨 画像: {result['image_path']}")
        print(f"📤 投稿: {result['wordpress_post']['link']}")
    else:
        print("\n❌ システムエラーが発生しました")