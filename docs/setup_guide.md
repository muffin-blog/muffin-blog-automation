# ブログ分析API設定ガイド

## 確認済み情報
- **サイトURL**: https://muffin-blog.com/
- **GA4トラッキングID**: G-PK3K7M7N5B
- **Search Console**: 登録済み・正常動作中

## 次の設定手順

### 1. Google Cloud Console設定

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. プロジェクトを作成または選択
3. 以下のAPIを有効化：
   - Google Analytics Data API
   - Google Search Console API

### 2. サービスアカウント作成

1. 「IAMと管理」→「サービスアカウント」
2. 「サービスアカウントを作成」をクリック
3. 名前: `blog-analytics-service`
4. 「キーを作成」→「JSON」を選択
5. ダウンロードしたJSONファイルを以下の名前で保存：
   - GA4用: `ga4_credentials.json`
   - Search Console用: `search_console_credentials.json`

### 3. 権限設定

#### Google Analytics 4
1. [Google Analytics](https://analytics.google.com/) にアクセス
2. 管理 → アカウントアクセス管理
3. サービスアカウントメールアドレスを追加
4. 権限: 「閲覧者」

#### Google Search Console
1. [Search Console](https://search.google.com/search-console/) にアクセス
2. プロパティ設定 → ユーザーと権限
3. サービスアカウントメールアドレスを追加
4. 権限: 「制限付き」または「フル」

### 4. ファイル設定

`blog_analytics_dashboard.py` の以下の行を更新：

```python
ga4_property_id = "449565416"  # G-PK3K7M7N5B の数値部分
```

### 5. 必要なライブラリインストール

```bash
pip install google-analytics-data google-api-python-client google-auth
```

### 6. 実行テスト

```bash
python3 blog_analytics_dashboard.py
```

## 予想される分析結果

Search Consoleの画面から推測される現在の状況：
- 月間クリック数: 約98回
- インデックス済みページ: 10ページ
- 最適化が必要なページ: 27ページ

APIを設定すると、これらのデータをより詳細に分析できます。