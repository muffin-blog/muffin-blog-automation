"""
SEO統一のためのWordPress抜粋削除
SEO SIMPLE PACKでの一元管理を可能にする
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests

def clear_excerpts_for_seo_unification():
    """WordPress抜粋を削除してSEO SIMPLE PACKでの一元管理を可能にする"""
    
    wp = WordPressBlogAutomator()  # 環境変数から自動読み込み
    
    print("🧹 WordPress抜粋削除 - SEO SIMPLE PACK統一準備")
    print("=" * 60)
    
    # 抜粋を設定したメタディスクリプションを保存（手動設定用）
    meta_descriptions = {
        "Audibleでお金の勉強！これから貯金・節約・投資を学びたい人におすすめの書籍6選": 
        "Audibleでお金の知識を身につけよう！貯蓄・節約・投資が学べるおすすめ書籍6選を厳選紹介。お金の勉強を楽しく続ける方法も解説。",
        
        "Audibleの休会制度を完全ガイド！メリットや注意点、退会との違いを丁寧に解説": 
        "Audibleの休会制度を完全ガイド！メリット・デメリット、退会との違い、手続き方法まで分かりやすく解説します。",
        
        "安心してAudibleを始めるために事前にチェック！退会・解約方法を徹底解説": 
        "Audibleを活用した効率的な学習方法を詳しく解説。忙しい日常でも読書時間を確保し、知識を身につける具体的なノウハウを紹介します。",
        
        "世界一分かりやすいAudible（オーディブル）の始め方！アプリの使い方を完全ガイド": 
        "Audibleの始め方を初心者向けに完全解説！アプリの使い方から料金プラン、おすすめ機能まで、世界一分かりやすくガイドします。",
        
        "「耳活で人生は変わる！」1年後の自分が楽になるたった一つの習慣": 
        "Audibleで人生が変わる！効率的な学習方法と時間活用術を紹介。通勤時間を自己投資の時間に変える具体的な方法を解説します。"
    }
    
    try:
        # Audible関連記事を取得
        response = requests.get(f"{wp.api_url}/posts?search=Audible&per_page=100", 
                               headers=wp.headers)
        
        if response.status_code == 200:
            posts = response.json()
            
            print(f"📄 {len(posts)}件のAudible関連記事を処理中...")
            print("\n🎯 WordPress抜粋削除とSEO SIMPLE PACK設定用データ出力:")
            print("=" * 70)
            
            success_count = 0
            
            for post in posts:
                post_id = post['id']
                title = post['title']['rendered']
                current_excerpt = post['excerpt']['rendered']
                
                # HTMLタグを除去してテキストのみ抽出
                import re
                clean_excerpt = re.sub(r'<[^>]+>', '', current_excerpt).strip()
                
                print(f"\\n📖 記事ID {post_id}: {title}")
                
                if clean_excerpt and len(clean_excerpt) > 10:
                    print(f"🔄 抜粋削除前: {clean_excerpt}")
                    
                    # SEO SIMPLE PACK用のメタディスクリプション（コピー用）
                    recommended_meta = meta_descriptions.get(title, clean_excerpt)
                    print(f"📋 SEO SIMPLE PACK設定推奨値:")
                    print(f"   {recommended_meta}")
                    
                    # WordPress抜粋を空にする
                    update_data = {
                        'excerpt': ''
                    }
                    
                    # 記事を更新
                    response = requests.post(f"{wp.api_url}/posts/{post_id}", 
                                           headers=wp.headers, 
                                           json=update_data)
                    
                    if response.status_code == 200:
                        print("✅ WordPress抜粋削除完了")
                        success_count += 1
                    else:
                        print(f"❌ 削除失敗: {response.status_code}")
                        print(response.text)
                else:
                    print("⏭️  抜粋が空または短いためスキップ")
            
            print(f"\\n🎯 処理完了: {success_count}件の記事から抜粋を削除しました")
            
            # 手動設定用の説明書出力
            print("\\n" + "="*70)
            print("📝 **次の手順**: WordPress管理画面での手動設定")
            print("="*70)
            print("1. WordPress管理画面 → 投稿 → 投稿一覧")
            print("2. 各記事を編集")
            print("3. 下部のSEO SIMPLE PACKセクションで「メタディスクリプション」に上記の推奨値をコピー&ペースト")
            print("4. 更新ボタンをクリック")
            print("\\n✨ これで一元管理が完成します！")
            
        else:
            print(f"❌ 記事取得失敗: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ エラー: {e}")

def verify_excerpt_removal():
    """抜粋削除結果を確認"""
    
    wp = WordPressBlogAutomator()  # 環境変数から自動読み込み
    
    print("\\n🔍 抜粋削除結果の確認")
    print("=" * 40)
    
    try:
        response = requests.get(f"{wp.api_url}/posts?search=Audible&per_page=10", 
                               headers=wp.headers)
        
        if response.status_code == 200:
            posts = response.json()
            
            for post in posts:
                title = post['title']['rendered']
                excerpt = post['excerpt']['rendered'].strip()
                
                status = "✅ 削除済み" if not excerpt else f"⚠️  残存: {excerpt[:30]}..."
                print(f"📖 {title}")
                print(f"   抜粋状態: {status}")
                
        else:
            print(f"❌ 確認失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    print("🚀 SEO統一化ツール - 第1段階")
    print("WordPress抜粋削除 → SEO SIMPLE PACK統一準備")
    print("=" * 70)
    
    # Step 1: 抜粋削除実行
    clear_excerpts_for_seo_unification()
    
    # Step 2: 削除結果確認
    verify_excerpt_removal()
    
    print("\\n✅ 第1段階完了！")
    print("次はWordPress管理画面でSEO SIMPLE PACKに手動設定してください。")