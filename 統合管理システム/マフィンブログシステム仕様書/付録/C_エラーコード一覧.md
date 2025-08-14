# C_エラーコード一覧

**対応プログラム機能**: 全システムエラーハンドリング・デバッグ支援  
**最終更新**: 2025年08月14日

---

## 🚨 システムエラーコード体系

### エラーコード分類
```yaml
error_classification:
  E001-E099: "WordPress API関連エラー"
  E100-E199: "ファイル・テンプレート関連エラー" 
  E200-E299: "記事作成・品質チェック関連エラー"
  E300-E399: "同期・バックアップ関連エラー"
  E400-E499: "設定・環境変数関連エラー"
  E500-E599: "システム内部エラー"
  E600-E699: "ネットワーク・接続関連エラー"
  E700-E799: "セキュリティ関連エラー"
  E800-E899: "パフォーマンス・リソース関連エラー"
  E900-E999: "その他・未分類エラー"
```

---

## 🔗 WordPress API関連エラー（E001-E099）

### E001: WordPress API接続失敗
```yaml
error_code: "E001"
description: "WordPress REST API への接続に失敗"
severity: "CRITICAL"
causes:
  - "認証情報の誤り"
  - "ネットワーク接続問題"
  - "サーバー側の問題"
  - "URL設定の誤り"
solutions:
  - "認証情報（ユーザー名・パスワード）の確認"
  - "WordPress サイトURLの確認"
  - "ネットワーク接続の確認"
  - "WordPress サーバーの稼働状況確認"
example_log: |
  [ERROR E001] WordPress API接続失敗: 401 Unauthorized
  URL: https://muffin-blog.com/wp-json/wp/v2/posts
  Response: {"code":"rest_forbidden","message":"Sorry, you are not allowed to do that."}
```

### E002: WordPress投稿作成失敗
```yaml
error_code: "E002"
description: "WordPress への記事投稿に失敗"
severity: "HIGH"
causes:
  - "投稿権限不足"
  - "投稿データの形式エラー"
  - "必須フィールドの不足"
  - "サーバー容量不足"
solutions:
  - "ユーザー権限の確認・調整"
  - "投稿データ形式の確認"
  - "必須フィールド（title, content）の確認"
  - "サーバー容量の確認"
example_log: |
  [ERROR E002] WordPress投稿作成失敗: 400 Bad Request
  Post Data: {"title": "", "content": "記事内容"}
  Error: タイトルが空です
```

### E003: カテゴリ・タグ作成失敗
```yaml
error_code: "E003"
description: "WordPress カテゴリまたはタグの作成に失敗"
severity: "MEDIUM"
causes:
  - "重複する名前のカテゴリ・タグ"
  - "権限不足"
  - "文字数制限超過"
solutions:
  - "既存カテゴリ・タグとの重複確認"
  - "管理者権限の確認"
  - "カテゴリ・タグ名の文字数確認"
example_log: |
  [ERROR E003] カテゴリ作成失敗: "Audible" は既に存在します
  Suggested Action: 既存カテゴリID 15 を使用してください
```

### E004: WordPress記事バックアップ失敗
```yaml
error_code: "E004"
description: "WordPress 記事のバックアップ取得に失敗"
severity: "MEDIUM"
causes:
  - "記事IDの不正"
  - "アクセス権限不足"
  - "記事が削除済み"
solutions:
  - "記事IDの確認"
  - "記事の存在確認"
  - "アクセス権限の確認"
example_log: |
  [ERROR E004] 記事バックアップ失敗: Post ID 999 が見つかりません
  Action: 記事一覧から正しいIDを確認してください
```

---

## 📁 ファイル・テンプレート関連エラー（E100-E199）

### E101: テンプレートファイル読み込み失敗
```yaml
error_code: "E101"
description: "記事テンプレートファイルの読み込みに失敗"
severity: "CRITICAL"
causes:
  - "ファイルパスの誤り"
  - "ファイルが存在しない"
  - "ファイル権限の問題"
  - "ファイルが破損している"
solutions:
  - "ファイルパスの確認"
  - "ファイルの存在確認"
  - "ファイル権限の確認（読み取り権限）"
  - "ファイル内容の確認・修復"
example_log: |
  [ERROR E101] サービス紹介型テンプレート読み込み失敗
  Path: /Users/satoumasamitsu/Desktop/osigoto/ブログ自動化/サービス紹介型記事_構成テンプレート.md
  Error: [Errno 2] No such file or directory
```

### E102: ファイル保存失敗
```yaml
error_code: "E102"
description: "記事ファイルの保存に失敗"
severity: "HIGH"
causes:
  - "ディスク容量不足"
  - "書き込み権限なし"
  - "ファイルパスの誤り"
  - "ファイルがロックされている"
solutions:
  - "ディスク容量の確認・解放"
  - "ディレクトリの書き込み権限確認"
  - "保存先パスの確認"
  - "ファイルロック状態の確認"
example_log: |
  [ERROR E102] ファイル保存失敗
  Path: /Users/satoumasamitsu/Desktop/osigoto/ブログ自動化/WordPress投稿下書き/article_20250814.md
  Error: [Errno 28] No space left on device
```

### E103: ファイル削除失敗
```yaml
error_code: "E103"
description: "不要ファイルの削除に失敗"
severity: "LOW"
causes:
  - "ファイルが使用中"
  - "削除権限なし"
  - "ファイルが既に削除済み"
solutions:
  - "ファイル使用状況の確認"
  - "削除権限の確認"
  - "ファイル存在確認"
example_log: |
  [ERROR E103] ファイル削除失敗
  Path: /Users/satoumasamitsu/Desktop/osigoto/ブログ自動化/temp_file.md
  Error: ファイルが他のプロセスで使用中です
```

---

## 📝 記事作成・品質チェック関連エラー（E200-E299）

### E201: 品質チェック不合格
```yaml
error_code: "E201"
description: "記事の品質チェックで不合格判定"
severity: "MEDIUM"
causes:
  - "文字数不足（2,000文字未満）"
  - "FAQ数不足（5個未満）"
  - "禁止表現の使用"
  - "必須セクションの不足"
solutions:
  - "文字数の増加（2,000文字以上）"
  - "FAQ の追加（最低5個）"
  - "禁止表現の削除・修正"
  - "必須セクションの追加"
example_log: |
  [ERROR E201] 品質チェック不合格: スコア 65/100
  Issues:
  - 文字数不足: 1,800文字 (最低2,000文字)
  - FAQ不足: 3個 (最低5個)
  - 禁止表現: "めっちゃ有名"
```

### E202: キーワード不足
```yaml
error_code: "E202"
description: "記事内のキーワード密度が不足"
severity: "MEDIUM"
causes:
  - "メインキーワードの出現頻度不足"
  - "関連キーワードの不足"
  - "キーワードの不自然な使用"
solutions:
  - "メインキーワードの自然な追加"
  - "関連キーワードの挿入"
  - "キーワード配置の見直し"
example_log: |
  [ERROR E202] キーワード密度不足
  Main Keyword: "Audible" - 出現回数: 3回 (推奨: 8-12回)
  Related Keywords: 不足しています
```

### E203: 記事構成の不備
```yaml
error_code: "E203"
description: "記事の構成に問題がある"
severity: "MEDIUM"
causes:
  - "「この記事で分かること」セクション不足"
  - "「まとめ」セクション不足"
  - "見出し階層の不正"
  - "FAQ セクション不足"
solutions:
  - "必須セクションの追加"
  - "見出し階層の修正（H2→H3→H4）"
  - "FAQ セクションの作成"
example_log: |
  [ERROR E203] 記事構成の不備
  Missing Sections:
  - "この記事で分かること" セクション
  - "FAQ" セクション
  Heading Issues: H2の後にH4が直接続いています
```

---

## 🔄 同期・バックアップ関連エラー（E300-E399）

### E301: 統合管理システム同期失敗
```yaml
error_code: "E301"
description: "統合管理システムとの同期処理に失敗"
severity: "HIGH"
causes:
  - "同期先ディレクトリのアクセス権限不足"
  - "ネットワークドライブの接続問題"
  - "ファイルロック状態"
  - "ディスク容量不足"
solutions:
  - "ディレクトリ権限の確認・修正"
  - "ネットワーク接続の確認"
  - "ファイルロック解除"
  - "ディスク容量の確保"
example_log: |
  [ERROR E301] 統合管理システム同期失敗
  Target: /Users/satoumasamitsu/Desktop/osigoto/統合管理システム/
  Error: Permission denied: 書き込み権限がありません
```

### E302: バックアップ作成失敗
```yaml
error_code: "E302"
description: "自動バックアップの作成に失敗"
severity: "HIGH"
causes:
  - "バックアップ先の容量不足"
  - "ソースファイルの読み込み失敗"
  - "圧縮処理の失敗"
solutions:
  - "バックアップ先の容量確認"
  - "ソースファイルの存在・権限確認"
  - "圧縮ライブラリの確認"
example_log: |
  [ERROR E302] バックアップ作成失敗
  Source: マフィンブログ統合システム.py
  Destination: /backup/20250814_backup.zip
  Error: ディスク容量不足
```

### E303: 日報生成失敗
```yaml
error_code: "E303"
description: "自動日報の生成に失敗"
severity: "MEDIUM"
causes:
  - "実行ログの不足"
  - "テンプレート読み込み失敗"
  - "データ集計エラー"
solutions:
  - "ログファイルの確認"
  - "日報テンプレートの確認"
  - "データ形式の確認"
example_log: |
  [ERROR E303] 日報生成失敗
  Date: 2025-08-14
  Error: 実行データが不足しています（記事作成: 0件）
```

---

## ⚙️ 設定・環境変数関連エラー（E400-E499）

### E401: 必須環境変数未設定
```yaml
error_code: "E401"
description: "必須の環境変数が設定されていない"
severity: "CRITICAL"
causes:
  - "環境変数の設定忘れ"
  - "環境変数名の誤り"
  - "システム再起動による環境変数消失"
solutions:
  - "環境変数の設定確認"
  - "設定ファイルの作成"
  - "システム環境変数の永続化"
example_log: |
  [ERROR E401] 必須環境変数未設定
  Missing Variables:
  - WORDPRESS_PASSWORD
  - WORDPRESS_SITE_URL
  Action: export WORDPRESS_PASSWORD="your_password" を実行してください
```

### E402: 設定値の形式エラー
```yaml
error_code: "E402"
description: "設定値の形式が不正"
severity: "HIGH"
causes:
  - "数値項目に文字列設定"
  - "URL形式の不正"
  - "パス形式の不正"
solutions:
  - "設定値の形式確認"
  - "デフォルト値の適用"
  - "設定ファイルの修正"
example_log: |
  [ERROR E402] 設定値形式エラー
  Variable: BACKUP_RETENTION_DAYS
  Value: "thirty" (期待値: 数値)
  Fixed: デフォルト値 30 を適用しました
```

### E403: ファイルパス設定エラー
```yaml
error_code: "E403"
description: "ファイル・ディレクトリパスの設定に問題"
severity: "HIGH"
causes:
  - "存在しないパスの指定"
  - "相対パスの使用"
  - "権限のないディレクトリ指定"
solutions:
  - "パスの存在確認"
  - "絶対パスでの指定"
  - "ディレクトリ権限の確認"
example_log: |
  [ERROR E403] ファイルパス設定エラー
  Path: TEMPLATE_PATH="/nonexistent/path"
  Error: 指定されたパスが存在しません
  Suggestion: 正しいパスを設定してください
```

---

## 🚨 システム内部エラー（E500-E599）

### E501: メモリ不足
```yaml
error_code: "E501"
description: "システムメモリが不足"
severity: "CRITICAL"
causes:
  - "大容量ファイルの処理"
  - "メモリリークの発生"
  - "並列処理の過多"
solutions:
  - "処理データサイズの削減"
  - "メモリ使用量の最適化"
  - "並列処理数の制限"
example_log: |
  [ERROR E501] メモリ不足
  Available: 256MB, Required: 512MB
  Process: 大容量記事の品質チェック処理
  Suggestion: チャンク処理または並列数削減を検討
```

### E502: プロセス実行失敗
```yaml
error_code: "E502"
description: "子プロセスの実行に失敗"
severity: "HIGH"
causes:
  - "実行ファイルの不存在"
  - "権限不足"
  - "依存ライブラリの不足"
solutions:
  - "実行ファイルの確認"
  - "実行権限の付与"
  - "必要ライブラリのインストール"
example_log: |
  [ERROR E502] プロセス実行失敗
  Command: python3 /path/to/script.py
  Error: command not found: python3
  Solution: Python3のインストールまたはパス設定が必要
```

### E503: タイムアウト
```yaml
error_code: "E503"
description: "処理がタイムアウト"
severity: "MEDIUM"
causes:
  - "API応答の遅延"
  - "大容量データの処理"
  - "ネットワーク不安定"
solutions:
  - "タイムアウト時間の延長"
  - "処理の分割"
  - "ネットワーク状況の確認"
example_log: |
  [ERROR E503] 処理タイムアウト
  Operation: WordPress API 記事投稿
  Timeout: 30秒
  Suggestion: タイムアウト値を60秒に延長することを推奨
```

---

## 🌐 ネットワーク・接続関連エラー（E600-E699）

### E601: ネットワーク接続失敗
```yaml
error_code: "E601"
description: "外部サービスへの接続に失敗"
severity: "HIGH"
causes:
  - "インターネット接続の問題"
  - "DNS解決の失敗"
  - "ファイアウォールによる制限"
  - "プロキシ設定の問題"
solutions:
  - "インターネット接続の確認"
  - "DNS設定の確認"
  - "ファイアウォール設定の確認"
  - "プロキシ設定の確認"
example_log: |
  [ERROR E601] ネットワーク接続失敗
  Target: https://muffin-blog.com
  Error: Name or service not known
  DNS Check: nslookup muffin-blog.com を実行してください
```

### E602: SSL証明書エラー
```yaml
error_code: "E602"
description: "SSL証明書の検証に失敗"
severity: "MEDIUM"
causes:
  - "証明書の期限切れ"
  - "自己署名証明書"
  - "証明書チェーンの問題"
solutions:
  - "証明書の更新"
  - "SSL検証の一時無効化"
  - "証明書チェーンの確認"
example_log: |
  [ERROR E602] SSL証明書エラー
  Site: https://muffin-blog.com
  Error: certificate verify failed: certificate has expired
  Temporary Fix: SSL検証を無効化して接続テスト
```

---

## 🔐 セキュリティ関連エラー（E700-E799）

### E701: 認証失敗
```yaml
error_code: "E701"
description: "認証処理に失敗"
severity: "CRITICAL"
causes:
  - "認証情報の誤り"
  - "認証トークンの期限切れ"
  - "アカウントロック"
solutions:
  - "認証情報の再確認"
  - "トークンの再取得"
  - "アカウント状態の確認"
example_log: |
  [ERROR E701] 認証失敗
  User: muffin1203
  Error: Invalid username or password
  Action: パスワードを再確認してください
```

### E702: 権限不足
```yaml
error_code: "E702"
description: "必要な権限が不足"
severity: "HIGH"
causes:
  - "ユーザー権限の不足"
  - "ファイル権限の不足"
  - "API権限の制限"
solutions:
  - "ユーザー権限の追加"
  - "ファイル権限の変更"
  - "API権限の確認・調整"
example_log: |
  [ERROR E702] 権限不足
  Operation: WordPress記事投稿
  Required Role: editor以上
  Current Role: subscriber
  Solution: ユーザーロールをeditorに変更してください
```

---

## 📊 パフォーマンス・リソース関連エラー（E800-E899）

### E801: 処理速度低下
```yaml
error_code: "E801"
description: "処理速度が著しく低下"
severity: "MEDIUM"
causes:
  - "システムリソース不足"
  - "大容量データの処理"
  - "非効率なアルゴリズム"
solutions:
  - "リソース使用量の最適化"
  - "処理の並列化"
  - "アルゴリズムの改善"
example_log: |
  [WARNING E801] 処理速度低下検出
  Operation: 記事品質チェック
  Time: 45秒 (通常: 5秒)
  CPU: 98% Memory: 85%
  Recommendation: 処理の分割を推奨
```

### E802: ディスク容量不足
```yaml
error_code: "E802"
description: "ディスク容量が不足"
severity: "HIGH"
causes:
  - "ログファイルの蓄積"
  - "バックアップファイルの蓄積"
  - "一時ファイルの残留"
solutions:
  - "不要ファイルの削除"
  - "ログローテーションの設定"
  - "古いバックアップの削除"
example_log: |
  [ERROR E802] ディスク容量不足
  Available: 1.2GB / Total: 50GB
  Usage: 97.6%
  Suggestion: 古いログファイル・バックアップの削除を推奨
```

---

## 🔧 デバッグ・診断支援

### エラー診断スクリプト
```python
def diagnose_error(error_code: str) -> Dict[str, Any]:
    """エラーコードに基づく診断実行"""
    
    error_info = ERROR_CODE_REGISTRY.get(error_code, {})
    
    diagnosis = {
        "error_code": error_code,
        "description": error_info.get("description", "不明なエラー"),
        "severity": error_info.get("severity", "UNKNOWN"),
        "automated_checks": [],
        "suggested_actions": error_info.get("solutions", []),
        "related_logs": []
    }
    
    # 自動診断チェック実行
    if error_code.startswith("E0"):  # WordPress API関連
        diagnosis["automated_checks"].extend(
            _check_wordpress_connectivity()
        )
    elif error_code.startswith("E1"):  # ファイル関連
        diagnosis["automated_checks"].extend(
            _check_file_permissions()
        )
    elif error_code.startswith("E4"):  # 環境変数関連
        diagnosis["automated_checks"].extend(
            _check_environment_variables()
        )
    
    return diagnosis

def _check_wordpress_connectivity() -> List[Dict[str, Any]]:
    """WordPress接続診断"""
    checks = []
    
    # 基本接続チェック
    try:
        response = requests.get("https://muffin-blog.com/wp-json/", timeout=10)
        checks.append({
            "check": "WordPress REST API 基本接続",
            "status": "OK" if response.status_code == 200 else "FAILED",
            "details": f"HTTP {response.status_code}"
        })
    except Exception as e:
        checks.append({
            "check": "WordPress REST API 基本接続",
            "status": "FAILED",
            "details": str(e)
        })
    
    return checks
```

### ログ分析機能
```python
def analyze_error_patterns(log_file_path: str) -> Dict[str, Any]:
    """エラーパターン分析"""
    
    analysis = {
        "total_errors": 0,
        "error_frequency": {},
        "time_patterns": {},
        "severity_distribution": {},
        "trends": []
    }
    
    with open(log_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if "ERROR" in line:
                analysis["total_errors"] += 1
                
                # エラーコード抽出
                error_code = extract_error_code(line)
                if error_code:
                    analysis["error_frequency"][error_code] = \
                        analysis["error_frequency"].get(error_code, 0) + 1
                
                # 時間パターン分析
                timestamp = extract_timestamp(line)
                if timestamp:
                    hour = timestamp.hour
                    analysis["time_patterns"][hour] = \
                        analysis["time_patterns"].get(hour, 0) + 1
    
    return analysis
```

---

## 📋 エラー対応チェックリスト

### 緊急時対応手順
```yaml
critical_error_response:
  immediate_actions:
    - "システム停止の判断"
    - "データ損失の確認"
    - "バックアップからの復旧準備"
    - "影響範囲の特定"
  
  investigation_steps:
    - "エラーログの詳細確認"
    - "システム環境の確認"
    - "最近の変更内容の確認"
    - "外部依存サービスの確認"
  
  recovery_actions:
    - "バックアップからの復旧"
    - "設定の修正・復元"
    - "システムの段階的再起動"
    - "動作確認テスト"
```

### 予防的メンテナンス
```yaml
preventive_maintenance:
  daily:
    - "エラーログの確認"
    - "ディスク容量の確認"
    - "メモリ使用量の確認"
  
  weekly:
    - "エラー傾向の分析"
    - "パフォーマンス指標の確認"
    - "設定ファイルのバックアップ"
  
  monthly:
    - "システム全体の動作確認"
    - "依存ライブラリの更新確認"
    - "セキュリティ設定の見直し"
```

---

**プログラム参照**: `マフィンブログ統合システム.py` 全体（エラーハンドリング実装）  
**関連仕様書**: [05_実行・運用ガイド.md](../05_実行・運用ガイド.md), [A_API設定・環境変数.md](./A_API設定・環境変数.md)