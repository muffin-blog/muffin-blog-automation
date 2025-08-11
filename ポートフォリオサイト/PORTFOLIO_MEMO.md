# Claude Code メモリーファイル

## プロジェクト概要
- **プロジェクト名:** マフィン - AI×SEOライター ポートフォリオサイト
- **メインURL:** https://muffin-portfolio-public.vercel.app
- **作成日:** 2025年7月31日
- **技術スタック:** HTML, CSS, JavaScript, Vercel

## ファイル構成
```
portfolio/
├── assets/
│   ├── css/style.css           # メインスタイルシート
│   ├── js/script.js           # メインJavaScript
│   └── images/profile/profile.jpg
├── content/
│   ├── articles/articles.json  # 記事データ（SEO記事・ブログ記事）
│   └── profile.json           # プロフィールデータ
├── index.html                 # メインHTML
├── package.json              # プロジェクト設定
├── vercel.json              # Vercel設定
├── MAINTENANCE.md           # メンテナンスガイド
└── CLAUDE.md               # このファイル
```

## 重要な設定・特徴
1. **ミニマルデザイン:** https://doisena.jp/ を参考にしたクリーンなデザイン
2. **記事分類:** SEO記事（クライアント向け）とブログ記事（個人）を分離表示
3. **レスポンシブ:** モバイル完全対応
4. **セキュリティ:** コンタクトフォームにスパム対策実装
5. **SEO最適化:** メタタグ、構造化データ完備

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

## メンテナンス対応
ユーザーが新記事を追加する際は：
1. **サイトへの反映:**
   - `content/articles/articles.json` を更新
   - 適切な配列（seoArticles or blogArticles）に追加
   - git commit & vercel deploy
   - URL動作確認

2. **既存記事ファイルの編集:**
   - ユーザーが指定した既存の記事ファイルの中身を編集
   - 新しい記事の情報や内容を既存ファイルに追加・更新
   - 記事ファイルも同時にgit commit

## 過去の主要変更
- パスワード保護解除でパブリックアクセス実現
- publicフォルダ削除でプロジェクト整理
- モバイル最適化（iOS zoom防止、タッチ対応）
- セキュリティ機能追加（ハニーポット、レート制限）

## 連絡先設定
メールアドレス: 0527muffin1203@gmail.com