# ポートフォリオサイト メンテナンスガイド（Phase4統合システム対応版）

## 現在の運用情報

**メインURL:** https://muffin-portfolio-public.vercel.app
**初期構築日:** 2025年7月31日
**Phase4統合完了日:** 2025年8月11日  
**管理者:** マフィン  
**管理システム:** Phase4統合自動化システム
**リポジトリ:** muffin-blog-automation（統合管理）

## 記事追加・更新の手順

### **🚀 完全自動化手順（推奨・メイン手順）**

**WordPress記事完成時の完全自動化フロー:**

1. **WordPress記事完成・URL確定**
2. **完全自動化ワークフローシステム自動起動**
   - URL自動検出・記事情報抽出
   - SEO最適化メタディスクリプション自動生成
   - タグ・カテゴリ自動最適化
3. **ポートフォリオ自動更新**
   - `public/content/articles/articles.json` 自動更新
   - 適切な配列（seoArticles/blogArticles）に自動追加
4. **画像自動管理**
   - Unsplash API経由で記事画像自動取得・最適化
   - `/public/assets/images/blog-thumbnails/` 自動格納
5. **Git自動操作・デプロイ**
   - `git add .` → `git commit` → `git push` 自動実行
   - Vercel自動デプロイ → サイト即座更新
6. **品質保証**
   - Phase4品質管理システムによる101点満点品質検証

**ユーザー操作:** WordPress記事URLの確定のみ（その他完全自動）

---

### **🛠️ 手動更新手順（バックアップ・緊急時用）**

#### 1. SEO記事を手動追加する場合
`public/content/articles/articles.json` の `seoArticles` 配列に手動追加：

```json
{
    "title": "記事タイトル（28-32文字最適化）",
    "url": "https://記事のURL",
    "description": "120-160文字の最適化されたメタディスクリプション",
    "date": "2025-MM-DD",
    "tags": ["メインキーワード", "サブキーワード1", "サブキーワード2"],
    "client": "クライアント名",
    "thumbnail": "/assets/images/blog-thumbnails/article-slug.jpg"
}
```

#### 2. ブログ記事を手動追加する場合
`public/content/articles/articles.json` の `blogArticles` 配列に手動追加：

```json
{
    "title": "記事タイトル（28-32文字最適化）",
    "url": "https://muffin-blog.com/article-slug/", 
    "description": "120-160文字の最適化されたメタディスクリプション",
    "date": "2025-MM-DD",
    "tags": ["メインキーワード", "サブキーワード1", "サブキーワード2"],
    "client": "Muffin Blog",
    "thumbnail": "/assets/images/blog-thumbnails/article-slug.jpg"
}
```

#### 3. プロフィール情報を手動更新する場合
`public/content/profile.json` を編集

#### 4. 画像管理（手動の場合）
```bash
node portfolio_image_manager.js process-article [記事URL]
```

#### 5. 手動デプロイ手順
```bash
git add .
git commit -m "🎉 新記事追加: [記事タイトル] - Phase4統合システム対応"
git push origin master
# Vercel自動デプロイ実行（Git push時）
```

## 定期メンテナンス項目（Phase4統合システム対応）

### **自動化済み項目（システムで自動実行）**
- ✅ **新しい記事の追加:** 完全自動化済み
- ✅ **画像管理:** Unsplash API自動取得システム
- ✅ **Git操作・デプロイ:** 完全自動化済み
- ✅ **品質管理:** Phase4品質システムで自動監視

### **月次手動チェック**
- [ ] プロフィール情報の手動更新（実績数値・スキル・サービス内容）
- [ ] リンク切れチェック（自動化対象外のリンク）
- [ ] 統合システム品質ログの確認
- [ ] Vercelデプロイ状況の確認

### **四半期チェック**
- [ ] デザインの改善
- [ ] 新機能の追加検討
- [ ] 統合システムのアップデート確認
- [ ] パフォーマンスの最適化

## 連絡事項（Phase4統合システム対応）

### **完全自動化対応（推奨）**
**WordPress記事完成時:**
- WordPress記事URLの確定のみでOK
- システムが自動で記事情報抽出・ポートフォリオ更新・デプロイを実行

### **手動対応が必要な場合**
1. **プロフィール更新:**
   - 実績数値の更新
   - 新しいスキル・サービスの追加
   - 連絡先情報の変更

2. **システム障害時の緊急対応:**
   - 手動でarticles.jsonを編集
   - portfolio_image_manager.js の手動実行
   - 手動Git操作

3. **カスタム要件:**
   - 特殊なデザイン変更
   - 新機能の追加

## システム統合情報
- **統合管理システム:** `/Users/satoumasamitsu/Desktop/osigoto/統合管理システム/`
- **完全自動化システム:** `完全自動化ワークフローシステム.py`
- **品質管理システム:** `継続的品質管理統合システム.py`
- **画像管理システム:** `portfolio_image_manager.js`

## バックアップ（統合システム対応）
**自動バックアップ対象:**
- 統合システムが自動でバックアップ作成
- タイムスタンプ付きバックアップファイル管理

**重要ファイル:**
- `public/content/articles/articles.json` （自動更新対象）
- `public/content/profile.json`（手動更新対象）
- `public/assets/css/style.css`
- `public/assets/js/script.js`（絶対パス対応済み）
- `portfolio_image_manager.js`（画像自動管理システム）