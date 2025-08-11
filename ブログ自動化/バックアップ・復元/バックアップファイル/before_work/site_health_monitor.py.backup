"""
WordPress サイトヘルス監視システム
エラー検知、リンク切れチェック、パフォーマンス監視
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wordpress_api import WordPressBlogAutomator
import requests
import re
from urllib.parse import urljoin, urlparse
from datetime import datetime
import time

class WordPressSiteHealthMonitor:
    """WordPress サイトの総合ヘルス監視システム"""
    
    def __init__(self):
        self.wp = WordPressBlogAutomator(
            site_url="https://muffin-blog.com",
            username="muffin1203", 
            password="TMLy Z4Wi RhPu oVLm 0lcO gZdi"
        )
        self.site_url = "https://muffin-blog.com"
        self.errors = []
        self.warnings = []
        
    def comprehensive_health_check(self):
        """包括的なサイトヘルスチェック"""
        
        print("🏥 WordPress サイトヘルス総合診断開始")
        print("=" * 60)
        print(f"対象サイト: {self.site_url}")
        print(f"診断開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 1. WordPress API接続チェック
        self._check_wordpress_api()
        
        # 2. 全記事のリンクチェック
        self._check_all_post_links()
        
        # 3. サイト全体のエラーチェック
        self._check_site_errors()
        
        # 4. パフォーマンスチェック
        self._check_site_performance()
        
        # 5. SEO健全性チェック
        self._check_seo_health()
        
        # 結果レポート
        self._generate_health_report()
        
    def _check_wordpress_api(self):
        """WordPress API接続状態確認"""
        
        print("🔌 WordPress API接続チェック")
        print("-" * 40)
        
        if self.wp.test_connection():
            print("✅ WordPress API接続正常")
        else:
            self.errors.append("WordPress API接続失敗")
            print("❌ WordPress API接続エラー")
            
        # API応答時間チェック
        start_time = time.time()
        try:
            response = requests.get(f"{self.wp.api_url}/posts?per_page=1", 
                                  headers=self.wp.headers, 
                                  timeout=10)
            response_time = time.time() - start_time
            
            if response_time < 2.0:
                print(f"✅ API応答時間: {response_time:.2f}秒（良好）")
            elif response_time < 5.0:
                print(f"⚠️ API応答時間: {response_time:.2f}秒（やや遅い）")
                self.warnings.append(f"API応答時間が遅い: {response_time:.2f}秒")
            else:
                print(f"❌ API応答時間: {response_time:.2f}秒（遅すぎ）")
                self.errors.append(f"API応答時間が遅い: {response_time:.2f}秒")
                
        except Exception as e:
            self.errors.append(f"API応答時間測定エラー: {e}")
            print(f"❌ API応答時間測定失敗: {e}")
            
        print()
        
    def _check_all_post_links(self):
        """全記事のリンク切れチェック"""
        
        print("🔗 全記事リンクチェック")
        print("-" * 40)
        
        try:
            # 全記事取得
            response = requests.get(f"{self.wp.api_url}/posts?per_page=100", 
                                  headers=self.wp.headers)
            
            if response.status_code != 200:
                self.errors.append("記事一覧取得失敗")
                return
                
            posts = response.json()
            print(f"チェック対象記事数: {len(posts)}件")
            
            total_links = 0
            broken_links = 0
            
            for post in posts:
                post_id = post['id']
                title = post['title']['rendered'][:30]
                content = post['content']['rendered']
                
                print(f"\n📝 記事ID {post_id}: {title}...")
                
                # リンク抽出
                links = re.findall(r'href=["\']([^"\']+)["\']', content)
                external_links = [link for link in links if link.startswith('http') 
                                and 'muffin-blog.com' not in link]
                
                print(f"   外部リンク数: {len(external_links)}個")
                
                # 各リンクをチェック
                post_broken = 0
                for link in external_links:
                    total_links += 1
                    if self._check_single_link(link):
                        print(f"   ✅ {link[:50]}...")
                    else:
                        print(f"   ❌ {link[:50]}...")
                        broken_links += 1
                        post_broken += 1
                        self.errors.append(f"記事ID {post_id}: リンク切れ {link}")
                
                if post_broken == 0:
                    print(f"   ✅ この記事のリンクは全て正常")
                else:
                    print(f"   ⚠️ この記事で{post_broken}件のリンク切れ")
            
            print(f"\n📊 リンクチェック結果:")
            print(f"   総リンク数: {total_links}件")
            print(f"   正常リンク: {total_links - broken_links}件")
            print(f"   リンク切れ: {broken_links}件")
            
            if broken_links == 0:
                print("✅ 全てのリンクが正常です")
            else:
                print(f"⚠️ {broken_links}件のリンク切れを発見")
                
        except Exception as e:
            self.errors.append(f"リンクチェックエラー: {e}")
            print(f"❌ リンクチェック失敗: {e}")
            
        print()
        
    def _check_single_link(self, url):
        """個別リンクの状態確認"""
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            return response.status_code < 400
        except:
            # HEADが失敗した場合はGETを試行
            try:
                response = requests.get(url, timeout=10, allow_redirects=True)
                return response.status_code < 400
            except:
                return False
    
    def _check_site_errors(self):
        """サイト全体のエラーチェック"""
        
        print("🚨 サイトエラーチェック")
        print("-" * 40)
        
        # メインページチェック
        self._check_page_errors(self.site_url, "トップページ")
        
        # 主要ページチェック
        important_pages = [
            f"{self.site_url}/category/audible/",
            f"{self.site_url}/sitemap.xml",
            f"{self.site_url}/robots.txt"
        ]
        
        for url in important_pages:
            page_name = url.split('/')[-1] or url.split('/')[-2]
            self._check_page_errors(url, page_name)
            
        print()
        
    def _check_page_errors(self, url, page_name):
        """個別ページのエラーチェック"""
        try:
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                print(f"✅ {page_name}: 正常 (200)")
                
                # 基本的なHTMLエラーチェック
                content = response.text
                if "Fatal error" in content:
                    self.errors.append(f"{page_name}: Fatal error検出")
                    print(f"   ❌ Fatal error検出")
                elif "Warning:" in content:
                    self.warnings.append(f"{page_name}: PHP Warning検出")
                    print(f"   ⚠️ PHP Warning検出")
                elif "Notice:" in content:
                    self.warnings.append(f"{page_name}: PHP Notice検出")
                    print(f"   ⚠️ PHP Notice検出")
                    
            elif response.status_code == 404:
                self.errors.append(f"{page_name}: ページが見つかりません (404)")
                print(f"❌ {page_name}: ページが見つかりません (404)")
                
            elif response.status_code >= 500:
                self.errors.append(f"{page_name}: サーバーエラー ({response.status_code})")
                print(f"❌ {page_name}: サーバーエラー ({response.status_code})")
                
            else:
                self.warnings.append(f"{page_name}: 異常なステータス ({response.status_code})")
                print(f"⚠️ {page_name}: 異常なステータス ({response.status_code})")
                
        except requests.RequestException as e:
            self.errors.append(f"{page_name}: 接続エラー ({e})")
            print(f"❌ {page_name}: 接続エラー ({e})")
            
    def _check_site_performance(self):
        """サイトパフォーマンスチェック"""
        
        print("⚡ パフォーマンスチェック")
        print("-" * 40)
        
        # ページ読み込み速度
        start_time = time.time()
        try:
            response = requests.get(self.site_url, timeout=30)
            load_time = time.time() - start_time
            
            if load_time < 2.0:
                print(f"✅ ページ読み込み速度: {load_time:.2f}秒（高速）")
            elif load_time < 4.0:
                print(f"⚠️ ページ読み込み速度: {load_time:.2f}秒（普通）")
                self.warnings.append(f"ページ読み込みがやや遅い: {load_time:.2f}秒")
            else:
                print(f"❌ ページ読み込み速度: {load_time:.2f}秒（遅い）")
                self.errors.append(f"ページ読み込みが遅い: {load_time:.2f}秒")
                
            # レスポンスサイズ
            content_length = len(response.content)
            if content_length < 500000:  # 500KB未満
                print(f"✅ ページサイズ: {content_length/1024:.1f}KB（適切）")
            elif content_length < 1000000:  # 1MB未満
                print(f"⚠️ ページサイズ: {content_length/1024:.1f}KB（やや大きい）")
                self.warnings.append(f"ページサイズが大きい: {content_length/1024:.1f}KB")
            else:
                print(f"❌ ページサイズ: {content_length/1024:.1f}KB（大きすぎ）")
                self.errors.append(f"ページサイズが大きすぎ: {content_length/1024:.1f}KB")
                
        except Exception as e:
            self.errors.append(f"パフォーマンステストエラー: {e}")
            print(f"❌ パフォーマンステスト失敗: {e}")
            
        print()
        
    def _check_seo_health(self):
        """SEO健全性チェック"""
        
        print("🎯 SEO健全性チェック")
        print("-" * 40)
        
        try:
            response = requests.get(self.site_url)
            content = response.text
            
            # 基本的なSEO要素チェック
            if "<title>" in content:
                title_match = re.search(r'<title>(.*?)</title>', content)
                if title_match:
                    title = title_match.group(1)
                    if len(title) < 60:
                        print(f"✅ タイトルタグ: {len(title)}文字（適切）")
                    else:
                        print(f"⚠️ タイトルタグ: {len(title)}文字（長すぎ）")
                        self.warnings.append("タイトルタグが長すぎます")
                else:
                    print("❌ タイトルタグが空です")
                    self.errors.append("タイトルタグが空")
            else:
                print("❌ タイトルタグがありません")
                self.errors.append("タイトルタグなし")
                
            # メタディスクリプション
            if 'name="description"' in content:
                print("✅ メタディスクリプション: 設定済み")
            else:
                print("⚠️ メタディスクリプション: 未設定")
                self.warnings.append("メタディスクリプション未設定")
                
            # robots.txt
            robots_response = requests.get(f"{self.site_url}/robots.txt")
            if robots_response.status_code == 200:
                print("✅ robots.txt: 存在")
            else:
                print("⚠️ robots.txt: 存在しない")
                self.warnings.append("robots.txt未設置")
                
            # XMLサイトマップ
            sitemap_response = requests.get(f"{self.site_url}/sitemap.xml")
            if sitemap_response.status_code == 200:
                print("✅ XMLサイトマップ: 存在")
            else:
                print("⚠️ XMLサイトマップ: 存在しない")
                self.warnings.append("XMLサイトマップ未設置")
                
        except Exception as e:
            self.errors.append(f"SEOチェックエラー: {e}")
            print(f"❌ SEOチェック失敗: {e}")
            
        print()
        
    def _generate_health_report(self):
        """ヘルスレポート生成"""
        
        print("📋 サイトヘルス診断レポート")
        print("=" * 60)
        
        # 総合評価
        if len(self.errors) == 0:
            if len(self.warnings) == 0:
                print("🎉 サイト状態: 優秀（エラー・警告なし）")
                health_score = "A+"
            elif len(self.warnings) <= 3:
                print("✅ サイト状態: 良好（警告あり）")
                health_score = "A"
            else:
                print("⚠️ サイト状態: 注意（多数の警告）")
                health_score = "B"
        elif len(self.errors) <= 2:
            print("⚠️ サイト状態: 改善が必要")
            health_score = "C"
        else:
            print("❌ サイト状態: 深刻な問題あり")
            health_score = "D"
            
        print(f"総合評価: {health_score}")
        print()
        
        # エラー詳細
        if self.errors:
            print("🚨 要修正エラー:")
            for i, error in enumerate(self.errors, 1):
                print(f"   {i}. {error}")
            print()
            
        # 警告詳細
        if self.warnings:
            print("⚠️ 改善推奨項目:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning}")
            print()
            
        print(f"診断完了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # レポートファイル保存
        self._save_report_file(health_score)
        
    def _save_report_file(self, health_score):
        """レポートをファイルに保存"""
        
        report_content = f"""# サイトヘルス診断レポート

## 基本情報
- サイトURL: {self.site_url}
- 診断日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 総合評価: {health_score}

## エラー ({len(self.errors)}件)
"""
        
        for i, error in enumerate(self.errors, 1):
            report_content += f"{i}. {error}\n"
            
        report_content += f"\n## 警告 ({len(self.warnings)}件)\n"
        
        for i, warning in enumerate(self.warnings, 1):
            report_content += f"{i}. {warning}\n"
            
        report_content += "\n## 推奨対応\n"
        if self.errors:
            report_content += "1. エラー項目を優先的に修正してください\n"
        if self.warnings:
            report_content += "2. 警告項目も時間のあるときに改善してください\n"
        if not self.errors and not self.warnings:
            report_content += "現在問題は検出されていません。定期的な監視を継続してください。\n"
            
        # ファイル保存
        report_filename = f"site_health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path = os.path.join(os.path.dirname(__file__), "..", "reports", report_filename)
        
        # reportsディレクトリ作成
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        print(f"📄 詳細レポート保存: {report_path}")

def continuous_monitoring():
    """継続的監視モード"""
    
    print("🔄 継続的サイト監視モード開始")
    print("Ctrl+Cで停止")
    print()
    
    monitor = WordPressSiteHealthMonitor()
    
    try:
        while True:
            monitor.comprehensive_health_check()
            print("\n⏰ 次回チェックまで30分待機...")
            time.sleep(1800)  # 30分待機
            
    except KeyboardInterrupt:
        print("\n🛑 監視を停止しました")

if __name__ == "__main__":
    print("🏥 WordPress サイトヘルス監視システム")
    print("=" * 60)
    print("即座にヘルスチェックを実行します...")
    print()
    
    monitor = WordPressSiteHealthMonitor()
    monitor.comprehensive_health_check()