# 付録B: WordPress連携仕様

**対応プログラム機能**: WordPress API関連全機能  
**API仕様**: WordPress REST API v2  
**最終更新**: 2025年08月14日

---

## 🔌 API接続設定

### 基本設定
```yaml
site_url: "https://muffin-blog.com"
api_base: "https://muffin-blog.com/wp-json/wp/v2"
username: "muffin1203"
password: "TMLy Z4Wi RhPu oVLm 0lcO gZdi"  # API用アプリケーションパスワード
```

### 認証ヘッダー
```python
credentials = f"{username}:{password}"
auth_header = base64.b64encode(credentials.encode()).decode()

headers = {
    'Authorization': f'Basic {auth_header}',
    'Content-Type': 'application/json'
}
```

### 接続テスト実装
```python
def test_wordpress_connection() -> bool:
    """WordPress API接続テスト"""
    try:
        response = requests.get(
            f"{api_url}/users/me", 
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ 接続成功: {user_data.get('name')} として認証")
            return True
        else:
            print(f"❌ 接続失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 接続エラー: {e}")
        return False
```

---

## 📝 記事投稿API仕様

### 投稿データ構造
```json
{
    "title": "記事タイトル",
    "content": "記事内容（HTMLまたはMarkdown）",
    "categories": [カテゴリID],
    "tags": [タグID配列],
    "status": "draft|publish|pending",
    "meta": {
        "description": "メタディスクリプション",
        "keywords": "SEOキーワード"
    },
    "slug": "url-slug",
    "excerpt": "記事抜粋"
}
```

### 投稿API実装
```python
def create_wordpress_post(title: str, content: str, 
                         category: str = "Audible",
                         tags: List[str] = None,
                         meta_description: str = "",
                         status: str = "draft") -> Optional[Dict]:
    
    # カテゴリとタグのIDを取得
    category_id = find_or_create_category(category)
    tag_ids = find_or_create_tags(tags or [])
    
    # 投稿データ作成
    post_data = {
        'title': title,
        'content': content,
        'categories': [category_id],
        'tags': tag_ids,
        'status': status,
        'meta': {'description': meta_description}
    }
    
    try:
        response = requests.post(
            f"{api_url}/posts",
            headers=headers, 
            json=post_data
        )
        
        if response.status_code == 201:
            post_info = response.json()
            return post_info
        else:
            print(f"❌ 投稿失敗: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 投稿エラー: {e}")
        return None
```

---

## 🏷️ カテゴリ・タグ管理

### カテゴリ管理API
```python
def get_categories() -> List[Dict]:
    """カテゴリ一覧取得"""
    try:
        response = requests.get(
            f"{api_url}/categories",
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"カテゴリ取得エラー: {e}")
        return []

def find_or_create_category(category_name: str) -> int:
    """カテゴリ検索・作成"""
    categories = get_categories()
    
    # 既存カテゴリを検索（大文字小文字無視）
    for cat in categories:
        if cat['name'].lower() == category_name.lower():
            return cat['id']
    
    # 新規カテゴリ作成
    data = {'name': category_name}
    try:
        response = requests.post(
            f"{api_url}/categories",
            headers=headers, 
            json=data
        )
        if response.status_code == 201:
            new_category = response.json()
            print(f"✅ 新規カテゴリ作成: {category_name}")
            return new_category['id']
        else:
            return 1  # デフォルトカテゴリ（未分類）
    except Exception as e:
        print(f"カテゴリ作成エラー: {e}")
        return 1
```

### タグ管理API
```python
def find_or_create_tags(tag_names: List[str]) -> List[int]:
    """タグ検索・作成"""
    try:
        response = requests.get(
            f"{api_url}/tags",
            headers=headers
        )
        existing_tags = response.json() if response.status_code == 200 else []
    except:
        existing_tags = []
    
    tag_ids = []
    for tag_name in tag_names:
        # 既存タグを検索
        found = False
        for tag in existing_tags:
            if tag['name'].lower() == tag_name.lower():
                tag_ids.append(tag['id'])
                found = True
                break
        
        # 新規タグ作成
        if not found:
            data = {'name': tag_name}
            try:
                response = requests.post(
                    f"{api_url}/tags",
                    headers=headers,
                    json=data
                )
                if response.status_code == 201:
                    new_tag = response.json()
                    tag_ids.append(new_tag['id'])
                    print(f"✅ 新規タグ作成: {tag_name}")
            except Exception as e:
                print(f"タグ作成エラー: {e}")
    
    return tag_ids
```

---

## 💾 バックアップ・削除機能

### 記事バックアップ実装
```python
def backup_post(post_id: int) -> Optional[str]:
    """記事バックアップ"""
    try:
        response = requests.get(
            f"{api_url}/posts/{post_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            post_data = response.json()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"記事{post_id}_backup_{timestamp}.json"
            backup_path = backup_dir / backup_filename
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(post_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 記事{post_id}バックアップ完了: {backup_filename}")
            return str(backup_path)
        else:
            print(f"❌ 記事{post_id}バックアップ失敗: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ バックアップエラー: {e}")
        return None
```

### 保護記事チェック付き削除
```python
# 保護記事ID（削除禁止）
PROTECTED_POST_IDS = [2732, 2677, 2625, 2535, 2210, 649, 2809, 2775]

def delete_post(post_id: int, force: bool = False) -> bool:
    """記事削除（保護記事チェック付き）"""
    if post_id in PROTECTED_POST_IDS:
        print(f"❌ 記事ID {post_id} は保護対象のため削除できません")
        return False
    
    # 削除前にバックアップ作成
    backup_path = backup_post(post_id)
    if not backup_path:
        print(f"⚠️ 記事{post_id}のバックアップ失敗、削除を中止")
        return False
    
    try:
        params = {'force': 'true'} if force else {}
        response = requests.delete(
            f"{api_url}/posts/{post_id}",
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            print(f"✅ 記事{post_id}削除完了（バックアップ済み）")
            return True
        else:
            print(f"❌ 記事{post_id}削除失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 削除エラー: {e}")
        return False
```

---

## 🔍 SEO最適化設定

### メタディスクリプション設定
```python
def set_meta_description(post_id: int, description: str):
    """メタディスクリプション設定"""
    meta_data = {
        'meta': {
            'description': description[:160]  # 160文字制限
        }
    }
    
    try:
        response = requests.post(
            f"{api_url}/posts/{post_id}",
            headers=headers,
            json=meta_data
        )
        return response.status_code == 200
    except Exception as e:
        print(f"メタディスクリプション設定エラー: {e}")
        return False
```

### スラッグ（URL）設定
```python
def generate_seo_slug(title: str, main_keyword: str) -> str:
    """SEO最適化スラッグ生成"""
    keyword_translation = {
        "読書苦手": "reading-dislike",
        "Audible": "audible",
        "オーディブル": "audible",
        "聴く読書": "listening-reading",
        "オーディオブック": "audiobook",
    }
    
    main_key_eng = keyword_translation.get(main_keyword, "guide")
    
    if "解決" in title:
        return f"{main_key_eng}-solution"
    elif "方法" in title or "始め方" in title:
        return f"{main_key_eng}-guide"
    elif "比較" in title:
        return f"{main_key_eng}-comparison"
    else:
        return f"{main_key_eng}-complete-guide"
```

---

## ⚠️ エラーハンドリング

### HTTPステータスコード対応
```python
def handle_api_response(response: requests.Response) -> Dict:
    """API レスポンス処理"""
    status_handlers = {
        200: lambda r: {"success": True, "data": r.json()},
        201: lambda r: {"success": True, "data": r.json()},
        400: lambda r: {"success": False, "error": "不正なリクエスト"},
        401: lambda r: {"success": False, "error": "認証失敗"},
        403: lambda r: {"success": False, "error": "アクセス権限なし"},
        404: lambda r: {"success": False, "error": "リソースが見つかりません"},
        500: lambda r: {"success": False, "error": "サーバーエラー"},
    }
    
    handler = status_handlers.get(
        response.status_code,
        lambda r: {"success": False, "error": f"不明なエラー: {r.status_code}"}
    )
    
    return handler(response)
```

### 接続エラー処理
```python
def safe_api_request(method: str, url: str, **kwargs) -> Dict:
    """安全なAPI リクエスト実行"""
    try:
        response = requests.request(method, url, timeout=10, **kwargs)
        return handle_api_response(response)
    except requests.exceptions.Timeout:
        return {"success": False, "error": "タイムアウト"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "接続エラー"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"リクエストエラー: {e}"}
```

---

## 🧪 テスト・デバッグ

### API接続テスト手順
```bash
# 1. 接続テスト
curl -H "Authorization: Basic [BASE64_CREDENTIALS]" \
     https://muffin-blog.com/wp-json/wp/v2/users/me

# 2. カテゴリ取得テスト
curl -H "Authorization: Basic [BASE64_CREDENTIALS]" \
     https://muffin-blog.com/wp-json/wp/v2/categories

# 3. 投稿テスト（下書き）
curl -X POST \
     -H "Authorization: Basic [BASE64_CREDENTIALS]" \
     -H "Content-Type: application/json" \
     -d '{"title":"テスト投稿","content":"テスト内容","status":"draft"}' \
     https://muffin-blog.com/wp-json/wp/v2/posts
```

### ログ出力設定
```python
import logging

# API通信ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_api_request(method: str, url: str, response: requests.Response):
    """API リクエストログ出力"""
    logger.info(f"{method} {url} -> {response.status_code}")
    if response.status_code >= 400:
        logger.error(f"Error response: {response.text}")
```

---

## 📊 使用制限・制約事項

### WordPressの制限
- **投稿サイズ**: 最大64MB
- **API レート制限**: なし（自サイトのため）
- **同時接続**: 推奨10接続まで

### 推奨実装
- **タイムアウト**: 10秒
- **リトライ**: 3回まで
- **バックアップ**: 削除前必須

---

**プログラム参照**: `マフィンブログ統合システム.py:336-500行目`  
**関連仕様書**: [付録/A_API設定・環境変数.md](./A_API設定・環境変数.md), [付録/C_エラーコード一覧.md](./C_エラーコード一覧.md)