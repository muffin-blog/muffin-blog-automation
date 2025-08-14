# A_API設定・環境変数

**対応プログラム機能**: WordPress API連携・認証管理  
**最終更新**: 2025年08月14日

---

## 🔐 WordPress API設定

### 基本API設定
```yaml
wordpress_api_config:
  site_url: "https://muffin-blog.com"
  username: "muffin1203"
  application_password: "TMLy Z4Wi RhPu oVLm 0lcO gZdi"
  api_version: "wp/v2"
  timeout: 30
  retry_attempts: 3
```

### API認証方式
```python
# Basic認証（推奨）
import base64
import requests

def create_auth_header(username: str, password: str) -> str:
    """Basic認証ヘッダー作成"""
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded_credentials}"

# 使用例
auth_header = create_auth_header("muffin1203", "TMLy Z4Wi RhPu oVLm 0lcO gZdi")
headers = {
    "Authorization": auth_header,
    "Content-Type": "application/json"
}
```

### API接続テスト
```python
def test_wordpress_api_connection(self) -> Dict[str, Any]:
    """WordPress API接続テスト"""
    
    test_result = {
        "connection_status": "failed",
        "response_time": 0,
        "api_version": None,
        "user_info": None,
        "error_message": None
    }
    
    try:
        start_time = time.time()
        
        # 基本情報取得テスト
        response = requests.get(
            f"{self.wordpress_site_url}/wp-json/wp/v2/users/me",
            headers=self._get_auth_headers(),
            timeout=30
        )
        
        test_result["response_time"] = time.time() - start_time
        
        if response.status_code == 200:
            test_result["connection_status"] = "success"
            user_data = response.json()
            test_result["user_info"] = {
                "id": user_data.get("id"),
                "name": user_data.get("name"),
                "roles": user_data.get("roles", [])
            }
        else:
            test_result["error_message"] = f"HTTP {response.status_code}: {response.text}"
            
    except requests.exceptions.RequestException as e:
        test_result["error_message"] = f"接続エラー: {str(e)}"
    
    return test_result
```

---

## 🌍 環境変数設定

### 必須環境変数
```bash
# WordPress API設定
export WORDPRESS_SITE_URL="https://muffin-blog.com"
export WORDPRESS_USERNAME="muffin1203" 
export WORDPRESS_PASSWORD="TMLy Z4Wi RhPu oVLm 0lcO gZdi"

# システム設定
export BACKUP_RETENTION_DAYS=30
export CLEANUP_RETENTION_DAYS=7
export LOG_LEVEL="INFO"
export MAX_RETRY_ATTEMPTS=3

# ファイルパス設定
export BLOG_AUTOMATION_PATH="/Users/satoumasamitsu/Desktop/osigoto/ブログ自動化"
export INTEGRATION_SYSTEM_PATH="/Users/satoumasamitsu/Desktop/osigoto/統合管理システム"
export TEMPLATE_PATH="/Users/satoumasamitsu/Desktop/osigoto/ブログ自動化"
export OUTPUT_PATH="/Users/satoumasamitsu/Desktop/osigoto/ブログ自動化/WordPress投稿下書き"
```

### 環境変数読み込み実装
```python
import os
from typing import Optional

class EnvironmentConfig:
    """環境変数管理クラス"""
    
    def __init__(self):
        self.wordpress_site_url = self._get_env_var("WORDPRESS_SITE_URL", "https://muffin-blog.com")
        self.wordpress_username = self._get_env_var("WORDPRESS_USERNAME", "muffin1203")
        self.wordpress_password = self._get_env_var("WORDPRESS_PASSWORD")
        self.backup_retention_days = int(self._get_env_var("BACKUP_RETENTION_DAYS", "30"))
        self.cleanup_retention_days = int(self._get_env_var("CLEANUP_RETENTION_DAYS", "7"))
        self.log_level = self._get_env_var("LOG_LEVEL", "INFO")
        self.max_retry_attempts = int(self._get_env_var("MAX_RETRY_ATTEMPTS", "3"))
        
        # パス設定
        self.blog_automation_path = self._get_env_var("BLOG_AUTOMATION_PATH")
        self.integration_system_path = self._get_env_var("INTEGRATION_SYSTEM_PATH")
        self.template_path = self._get_env_var("TEMPLATE_PATH")
        self.output_path = self._get_env_var("OUTPUT_PATH")
    
    def _get_env_var(self, var_name: str, default: Optional[str] = None) -> str:
        """環境変数取得（必須チェック付き）"""
        value = os.getenv(var_name, default)
        if value is None and default is None:
            raise ValueError(f"必須環境変数が設定されていません: {var_name}")
        return value
    
    def validate_config(self) -> Dict[str, Any]:
        """設定値検証"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # WordPress設定検証
        if not self.wordpress_password:
            validation_result["valid"] = False
            validation_result["errors"].append("WORDPRESS_PASSWORD が設定されていません")
        
        # パス存在確認
        paths_to_check = [
            ("BLOG_AUTOMATION_PATH", self.blog_automation_path),
            ("INTEGRATION_SYSTEM_PATH", self.integration_system_path),
            ("TEMPLATE_PATH", self.template_path)
        ]
        
        for path_name, path_value in paths_to_check:
            if path_value and not os.path.exists(path_value):
                validation_result["warnings"].append(f"{path_name} のパスが存在しません: {path_value}")
        
        return validation_result
```

### 環境変数の安全な管理
```python
class SecureEnvironmentManager:
    """セキュアな環境変数管理"""
    
    @staticmethod
    def mask_sensitive_value(value: str, mask_length: int = 4) -> str:
        """機密情報のマスク処理"""
        if len(value) <= mask_length * 2:
            return "*" * len(value)
        
        start = value[:mask_length]
        end = value[-mask_length:]
        middle = "*" * (len(value) - mask_length * 2)
        return f"{start}{middle}{end}"
    
    @staticmethod
    def log_environment_status() -> None:
        """環境変数の状態をログ出力（機密情報マスク）"""
        env_status = {
            "WORDPRESS_SITE_URL": os.getenv("WORDPRESS_SITE_URL", "未設定"),
            "WORDPRESS_USERNAME": os.getenv("WORDPRESS_USERNAME", "未設定"),
            "WORDPRESS_PASSWORD": SecureEnvironmentManager.mask_sensitive_value(
                os.getenv("WORDPRESS_PASSWORD", "未設定")
            ) if os.getenv("WORDPRESS_PASSWORD") else "未設定",
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
            "BACKUP_RETENTION_DAYS": os.getenv("BACKUP_RETENTION_DAYS", "30")
        }
        
        print("=== 環境変数設定状況 ===")
        for key, value in env_status.items():
            print(f"{key}: {value}")
```

---

## 🔗 WordPress API エンドポイント

### 主要エンドポイント一覧
```yaml
wordpress_endpoints:
  # 投稿管理
  posts:
    list: "GET /wp-json/wp/v2/posts"
    create: "POST /wp-json/wp/v2/posts"
    read: "GET /wp-json/wp/v2/posts/{id}"
    update: "PUT /wp-json/wp/v2/posts/{id}"
    delete: "DELETE /wp-json/wp/v2/posts/{id}"
  
  # カテゴリ管理
  categories:
    list: "GET /wp-json/wp/v2/categories"
    create: "POST /wp-json/wp/v2/categories"
    read: "GET /wp-json/wp/v2/categories/{id}"
    update: "PUT /wp-json/wp/v2/categories/{id}"
    delete: "DELETE /wp-json/wp/v2/categories/{id}"
  
  # タグ管理
  tags:
    list: "GET /wp-json/wp/v2/tags"
    create: "POST /wp-json/wp/v2/tags"
    read: "GET /wp-json/wp/v2/tags/{id}"
    update: "PUT /wp-json/wp/v2/tags/{id}"
    delete: "DELETE /wp-json/wp/v2/tags/{id}"
  
  # ユーザー管理
  users:
    me: "GET /wp-json/wp/v2/users/me"
    list: "GET /wp-json/wp/v2/users"
    read: "GET /wp-json/wp/v2/users/{id}"
```

### API呼び出し実装例
```python
class WordPressAPIClient:
    """WordPress API クライアント"""
    
    def __init__(self, site_url: str, username: str, password: str):
        self.site_url = site_url.rstrip('/')
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.headers.update(self._get_auth_headers())
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """認証ヘッダー取得"""
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }
    
    def create_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """記事作成"""
        endpoint = f"{self.site_url}/wp-json/wp/v2/posts"
        
        response = self.session.post(endpoint, json=post_data, timeout=30)
        
        if response.status_code == 201:
            return {
                "success": True,
                "post_id": response.json()["id"],
                "post_url": response.json()["link"]
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}"
            }
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """カテゴリ一覧取得"""
        endpoint = f"{self.site_url}/wp-json/wp/v2/categories"
        
        response = self.session.get(endpoint, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"カテゴリ取得失敗: HTTP {response.status_code}")
    
    def create_category(self, name: str, description: str = "") -> Dict[str, Any]:
        """カテゴリ作成"""
        endpoint = f"{self.site_url}/wp-json/wp/v2/categories"
        
        category_data = {
            "name": name,
            "description": description
        }
        
        response = self.session.post(endpoint, json=category_data, timeout=30)
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"カテゴリ作成失敗: HTTP {response.status_code}")
```

---

## 📝 投稿データ形式

### 記事投稿データ構造
```python
post_data_structure = {
    "title": "記事タイトル",
    "content": "記事本文（HTML形式）",
    "status": "draft",  # draft, publish, private
    "categories": [1, 2, 3],  # カテゴリID配列
    "tags": [4, 5, 6],  # タグID配列
    "meta": {
        "description": "メタディスクリプション",
        "keywords": "キーワード1,キーワード2"
    },
    "excerpt": "記事抜粋",
    "featured_media": 0,  # アイキャッチ画像ID
    "comment_status": "open",  # open, closed
    "ping_status": "open",  # open, closed
    "format": "standard",  # standard, aside, chat, gallery, link, image, quote, status, video, audio
    "sticky": False,  # 固定投稿
    "author": 1,  # 著者ID
    "date": "2025-08-14T10:00:00",  # 投稿日時（ISO 8601形式）
    "slug": "article-slug"  # URL スラッグ
}
```

### メタデータ設定
```python
def create_post_metadata(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
    """投稿メタデータ作成"""
    
    # SEO メタデータ
    meta_description = article_data.get("meta_description", "")
    if not meta_description and "content" in article_data:
        # 自動でメタディスクリプション生成
        content_text = self._strip_html_tags(article_data["content"])
        meta_description = content_text[:150] + "..." if len(content_text) > 150 else content_text
    
    # 構造化データ
    structured_data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article_data.get("title", ""),
        "description": meta_description,
        "author": {
            "@type": "Person",
            "name": "マフィン"
        },
        "publisher": {
            "@type": "Organization",
            "name": "マフィンブログ",
            "url": "https://muffin-blog.com"
        }
    }
    
    return {
        "description": meta_description,
        "structured_data": json.dumps(structured_data),
        "reading_time": self._calculate_reading_time(article_data.get("content", "")),
        "word_count": self._count_words(article_data.get("content", ""))
    }
```

---

## 🔄 API レート制限・エラーハンドリング

### レート制限対応
```python
import time
from functools import wraps

def rate_limited(max_calls_per_minute: int = 60):
    """API レート制限デコレータ"""
    def decorator(func):
        last_called = [0.0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = 60.0 / max_calls_per_minute - elapsed
            
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        
        return wrapper
    return decorator

class WordPressAPIClientWithRateLimit(WordPressAPIClient):
    """レート制限対応 WordPress API クライアント"""
    
    @rate_limited(max_calls_per_minute=30)
    def create_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """レート制限付き記事作成"""
        return super().create_post(post_data)
    
    @rate_limited(max_calls_per_minute=60)
    def get_categories(self) -> List[Dict[str, Any]]:
        """レート制限付きカテゴリ取得"""
        return super().get_categories()
```

### エラーハンドリング
```python
class WordPressAPIError(Exception):
    """WordPress API エラー"""
    pass

class WordPressAPIRetryableError(WordPressAPIError):
    """再試行可能な WordPress API エラー"""
    pass

def handle_api_errors(func):
    """API エラーハンドリングデコレータ"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        max_retries = 3
        retry_delay = 1.0
        
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            
            except requests.exceptions.ConnectionError as e:
                if attempt < max_retries - 1:
                    print(f"接続エラー（再試行 {attempt + 1}/{max_retries}）: {e}")
                    time.sleep(retry_delay * (2 ** attempt))
                    continue
                raise WordPressAPIRetryableError(f"接続エラー: {e}")
            
            except requests.exceptions.Timeout as e:
                if attempt < max_retries - 1:
                    print(f"タイムアウト（再試行 {attempt + 1}/{max_retries}）: {e}")
                    time.sleep(retry_delay * (2 ** attempt))
                    continue
                raise WordPressAPIRetryableError(f"タイムアウト: {e}")
            
            except requests.exceptions.HTTPError as e:
                if e.response.status_code in [500, 502, 503, 504] and attempt < max_retries - 1:
                    print(f"サーバーエラー（再試行 {attempt + 1}/{max_retries}）: {e}")
                    time.sleep(retry_delay * (2 ** attempt))
                    continue
                raise WordPressAPIError(f"HTTP エラー: {e}")
        
        return None
    
    return wrapper
```

---

## 🔧 API 設定のトラブルシューティング

### 設定確認チェックリスト
```yaml
configuration_checklist:
  basic_settings:
    - "WordPress サイト URL が正確か"
    - "ユーザー名が正確か"
    - "アプリケーションパスワードが有効か"
    - "HTTPS 接続が可能か"
  
  permissions:
    - "ユーザーに投稿権限があるか"
    - "REST API が有効になっているか"
    - "プラグインによる制限がないか"
    - "テーマによる制限がないか"
  
  network:
    - "ファイアウォールによる制限がないか"
    - "DNS 解決が正常か"
    - "SSL 証明書が有効か"
    - "プロキシ設定が正しいか"
```

### よくあるエラーと解決方法
```yaml
common_errors:
  "401 Unauthorized":
    causes:
      - "認証情報の誤り"
      - "アプリケーションパスワードの期限切れ"
      - "ユーザーアカウントの無効化"
    solutions:
      - "認証情報の再確認"
      - "新しいアプリケーションパスワードの生成"
      - "ユーザーアカウントの確認"
  
  "403 Forbidden":
    causes:
      - "権限不足"
      - "IP アドレス制限"
      - "セキュリティプラグインによる制限"
    solutions:
      - "ユーザー権限の確認・追加"
      - "IP ホワイトリストへの追加"
      - "セキュリティプラグイン設定の調整"
  
  "404 Not Found":
    causes:
      - "URL の誤り"
      - "REST API の無効化"
      - "パーマリンク設定の問題"
    solutions:
      - "URL の再確認"
      - "REST API の有効化"
      - "パーマリンク設定の更新"
  
  "500 Internal Server Error":
    causes:
      - "サーバー側の問題"
      - "プラグインの競合"
      - "メモリ不足"
    solutions:
      - "サーバーログの確認"
      - "プラグインの一時無効化"
      - "メモリ制限の増加"
```

### 診断スクリプト
```python
def diagnose_api_configuration(self) -> Dict[str, Any]:
    """API 設定診断スクリプト"""
    
    diagnosis_result = {
        "overall_status": "unknown",
        "checks": {},
        "recommendations": []
    }
    
    # 基本接続テスト
    try:
        response = requests.get(f"{self.wordpress_site_url}/wp-json/", timeout=10)
        diagnosis_result["checks"]["basic_connection"] = {
            "status": "success" if response.status_code == 200 else "failed",
            "response_code": response.status_code
        }
    except Exception as e:
        diagnosis_result["checks"]["basic_connection"] = {
            "status": "failed",
            "error": str(e)
        }
    
    # 認証テスト
    try:
        response = requests.get(
            f"{self.wordpress_site_url}/wp-json/wp/v2/users/me",
            headers=self._get_auth_headers(),
            timeout=10
        )
        diagnosis_result["checks"]["authentication"] = {
            "status": "success" if response.status_code == 200 else "failed",
            "response_code": response.status_code
        }
    except Exception as e:
        diagnosis_result["checks"]["authentication"] = {
            "status": "failed",
            "error": str(e)
        }
    
    # 投稿権限テスト
    try:
        test_post_data = {
            "title": "API テスト投稿",
            "content": "テスト内容",
            "status": "draft"
        }
        response = requests.post(
            f"{self.wordpress_site_url}/wp-json/wp/v2/posts",
            headers=self._get_auth_headers(),
            json=test_post_data,
            timeout=10
        )
        diagnosis_result["checks"]["post_permission"] = {
            "status": "success" if response.status_code == 201 else "failed",
            "response_code": response.status_code
        }
        
        # テスト投稿を削除
        if response.status_code == 201:
            post_id = response.json()["id"]
            requests.delete(
                f"{self.wordpress_site_url}/wp-json/wp/v2/posts/{post_id}",
                headers=self._get_auth_headers(),
                timeout=10
            )
    
    except Exception as e:
        diagnosis_result["checks"]["post_permission"] = {
            "status": "failed",
            "error": str(e)
        }
    
    # 総合判定
    failed_checks = [k for k, v in diagnosis_result["checks"].items() if v["status"] == "failed"]
    if not failed_checks:
        diagnosis_result["overall_status"] = "healthy"
    elif len(failed_checks) == len(diagnosis_result["checks"]):
        diagnosis_result["overall_status"] = "critical"
    else:
        diagnosis_result["overall_status"] = "warning"
    
    # 推奨事項生成
    if failed_checks:
        diagnosis_result["recommendations"] = [
            f"失敗したチェック: {', '.join(failed_checks)}",
            "認証情報の確認を行ってください",
            "WordPress 管理画面でREST API設定を確認してください"
        ]
    
    return diagnosis_result
```

---

**プログラム参照**: `マフィンブログ統合システム.py:100-300行目（WordPress API実装部分）`  
**関連仕様書**: [B_WordPress連携仕様.md](./B_WordPress連携仕様.md), [C_エラーコード一覧.md](./C_エラーコード一覧.md)