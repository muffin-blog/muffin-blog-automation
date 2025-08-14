# Claude Code メモリーファイル（Phase4統合システム対応版）

## プロジェクト概要
- **プロジェクト名:** マフィン - AI×SEOライター ポートフォリオサイト
- **メインURL:** https://muffin-portfolio-public.vercel.app
- **作成日:** 2025年7月31日
- **統合完了日:** 2025年8月11日
- **技術スタック:** HTML, CSS, JavaScript, Vercel + Phase4統合自動化システム
- **管理方式:** 統合リポジトリ管理（muffin-blog-automation）

## ファイル構成（統合システム対応版）
```
ポートフォリオサイト/（統合リポジトリ内）
├── public/                    # Vercel デプロイ対象
│   ├── assets/
│   │   ├── css/style.css           # メインスタイルシート
│   │   ├── js/script.js           # メインJavaScript（絶対パス対応）
│   │   └── images/
│   │       ├── blog-thumbnails/    # 自動生成画像格納
│   │       └── profile/profile.jpg
│   ├── content/
│   │   ├── articles/articles.json  # 記事データ（自動更新対応）
│   │   └── profile.json           # プロフィールデータ
│   └── index.html                 # メインHTML
├── portfolio_image_manager.js     # 画像自動管理システム
├── package.json                  # プロジェクト設定
├── vercel.json                  # Vercel設定（統合対応）
├── MAINTENANCE.md              # メンテナンスガイド（自動化対応）
├── PORTFOLIO_MEMO.md          # このファイル
└── README.md                  # 統合システム対応説明書
```

## 重要な設定・特徴（Phase4統合システム対応）
1. **完全自動化対応:** WordPress記事URL → ポートフォリオ自動更新の完全自動化
2. **Phase4品質管理:** 101点満点品質システムとの統合連携
3. **自動画像管理:** Unsplash API + portfolio_image_manager.js による画像自動取得・最適化
4. **統合リポジトリ管理:** muffin-blog-automation での一元管理
5. **ミニマルデザイン:** https://doisena.jp/ を参考にしたクリーンなデザイン
6. **記事分類:** SEO記事（クライアント向け）とブログ記事（個人）を分離表示
7. **レスポンシブ:** モバイル完全対応
8. **セキュリティ:** コンタクトフォームにスパム対策実装
9. **SEO最適化:** メタタグ、構造化データ完備
10. **Git自動化:** 記事追加時の自動コミット・プッシュ・デプロイ

## データ構造
### articles.json
- `seoArticles`: クライアント向けSEO記事（client フィールド含む）
- `blogArticles`: 個人ブログ記事

### プロフィール情報
- 初回料金: 1円/文字
- 通常料金: SEO記事 3-5円、専門記事 5-8円
- 納期: 1週間標準

## デプロイ設定
- **Vercel プロジェクト:** muffin-blogs-projects/muffin-portfolio-public
- **認証:** Vercel Authentication = Disabled（パブリックアクセス）
- **自動デプロイ:** Git push時に自動更新

## メンテナンス対応（Phase4統合システム対応）

### **自動メンテナンス（推奨・主要手順）**
**WordPress記事完成時の完全自動化フロー:**
1. **URL検出:** 完全自動化ワークフローシステムがWordPress URLを検出
2. **記事情報自動抽出:** タイトル・メタディスクリプション・タグを自動抽出・最適化
3. **articles.json自動更新:** 適切な配列（seoArticles/blogArticles）に自動追加
4. **画像自動取得:** Unsplash API経由で記事アイキャッチ画像を自動取得・最適化
5. **Git自動操作:** add → commit → push自動実行
6. **Vercel自動デプロイ:** サイト即座更新
7. **品質保証:** Phase4品質管理システムによる101点満点品質検証

### **手動メンテナンス（バックアップ手順）**
緊急時やシステム障害時の手動対応：
1. **サイトへの手動反映:**
   - `public/content/articles/articles.json` を手動更新
   - 適切な配列（seoArticles or blogArticles）に手動追加
   - 画像が必要な場合は `portfolio_image_manager.js` 実行
   - git commit & push → vercel自動deploy
   - URL動作確認

2. **既存記事ファイルの編集:**
   - 既存の記事ファイルの中身を編集（統合管理システムからの指示に従い）
   - 新しい記事の情報や内容を既存ファイルに追加・更新
   - 記事ファイルも同時にgit commit

## 過去の主要変更
### **Phase4統合システム対応（2025-08-11）**
- **統合リポジトリ管理:** 独立リポジトリから統合リポジトリ（muffin-blog-automation）への移行完了
- **完全自動化ワークフロー:** WordPress記事URL検出から記事更新・Git操作・デプロイまでの完全自動化実装
- **画像自動管理システム:** Unsplash API + portfolio_image_manager.js による自動画像取得・最適化システム構築
- **Phase4品質管理統合:** 101点満点品質システムとの連携実装
- **JavaScript絶対パス対応:** script.js のfetchパスを相対パスから絶対パスに変更（統合環境対応）

### **初期構築（2025-07-31）**
- パスワード保護解除でパブリックアクセス実現
- publicフォルダ削除でプロジェクト整理
- モバイル最適化（iOS zoom防止、タッチ対応）
- セキュリティ機能追加（ハニーポット、レート制限）

## 連絡先設定
メールアドレス: ${CONTACT_EMAIL} # .envファイルから取得

## システム連携情報
- **統合管理システム:** `/Users/satoumasamitsu/Desktop/osigoto/統合管理システム/`
- **完全自動化システム:** `/Users/satoumasamitsu/Desktop/osigoto/ブログ自動化/システム実行ファイル/コア/完全自動化ワークフローシステム.py`
- **品質管理システム:** `/Users/satoumasamitsu/Desktop/osigoto/ブログ自動化/システム実行ファイル/コア/継続的品質管理統合システム.py`