# マフィン - AI × SEOライター | ポートフォリオサイト

Phase4統合自動化システムと連携した、スタイリッシュでモダンなポートフォリオサイトです。統合管理システムからの自動更新機能を搭載しています。

## 🚀 特徴

- **完全自動化対応**: 統合管理システムからの自動記事更新・画像取得
- **Phase4品質管理**: 101点満点品質システムによる自動品質保証
- **レスポンシブデザイン**: モバイル・タブレット・デスクトップに完全対応
- **動的コンテンツ**: JSONファイルからプロフィールと記事情報を自動読み込み
- **自動画像管理**: Unsplash APIによる記事アイキャッチ画像の自動取得・最適化
- **フィルタリング機能**: タグベースの記事フィルタリング
- **モダンUI**: グラデーション、アニメーション、ホバーエフェクト
- **アクセシビリティ対応**: ARIA属性とセマンティックHTML
- **SEO最適化**: メタタグ、構造化データ、Open Graph対応
- **統合リポジトリ管理**: muffin-blog-automation リポジトリとの完全統合

## 📁 ファイル構造

```
portfolio/
├── public/                    # Vercelデプロイ用メインディレクトリ
│   ├── assets/
│   │   ├── css/
│   │   │   └── style.css      # メインスタイルシート
│   │   ├── images/
│   │   │   └── profile/
│   │   │       └── profile.jpg # プロフィール画像
│   │   └── js/
│   │       └── script.js      # メイン機能スクリプト
│   ├── content/
│   │   ├── profile.json       # プロフィール情報
│   │   └── articles/
│   │       └── articles.json  # 記事情報
│   └── index.html             # メインHTMLファイル
├── PORTFOLIO_MEMO.md          # Claude Code メモリーファイル
├── MAINTENANCE.md             # メンテナンス手順（統合自動化システム対応）
├── portfolio_image_manager.js # 画像自動管理システム（Unsplash API連携）
├── package.json               # プロジェクト設定
├── vercel.json               # Vercel設定（統合リポジトリ対応）
└── README.md
```

## 🛠️ 使用方法

### **統合自動化システムによる自動更新（推奨）**

**新記事追加時の完全自動化フロー**:
1. **WordPress記事完成** → URL確定
2. **完全自動化ワークフローシステム起動** (URL検出で自動実行)
3. **記事情報自動抽出** → articles.json自動更新
4. **画像自動取得・最適化** → Unsplash API経由で自動配置
5. **Git自動コミット・プッシュ** → Vercel自動デプロイ

```python
# システムによる自動実行（ユーザー操作不要）
from 完全自動化ワークフローシステム import CompleteAutomationWorkflowSystem
system = CompleteAutomationWorkflowSystem()
system.execute_complete_automation(wordpress_url)
```

### **手動更新方法（バックアップ手順）**

#### プロフィール情報の更新

`public/content/profile.json` を編集してプロフィール情報を更新：

```json
{
  "name": "マフィン",
  "title": "AI × SEOライター", 
  "bio": "適応障害をきっかけに副業から始めたライティングを本格的に展開...",
  "achievements": [
    {"number": "100+", "label": "執筆記事数"},
    {"number": "50+", "label": "満足クライアント"}
  ]
}
```

#### 記事の手動追加・更新

`public/content/articles/articles.json` の適切な配列に新しい記事を追加：

```json
{
  "seoArticles": [/* クライアント向けSEO記事 */],
  "blogArticles": [
    {
      "title": "記事タイトル",
      "url": "https://muffin-blog.com/article-slug/",
      "description": "120-160文字の最適化されたメタディスクリプション",
      "date": "2025-08-11",
      "tags": ["メインキーワード", "サブキーワード1", "サブキーワード2"],
      "client": "Muffin Blog",
      "thumbnail": "/assets/images/blog-thumbnails/article-slug.jpg"
    }
  ]
}
```

### プロフィール画像の更新

1. 新しい画像を `public/assets/images/profile/` フォルダに配置
2. `public/content/profile.json` の `profileImage` パスを更新

## 🎨 カスタマイズ

### カラーテーマの変更

`public/assets/css/style.css` の `:root` セクションでカラー変数を編集：

```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #f093fb;
    /* その他の色設定... */
}
```

### レイアウトの調整

CSSファイル内の各セクション（プロフィール、記事カードなど）のスタイルを編集して、レイアウトをカスタマイズできます。

## 🔧 技術仕様

### **フロントエンド**
- **HTML5**: セマンティックマークアップ
- **CSS3**: フレックスボックス、グリッド、カスタムプロパティ
- **ES6+ JavaScript**: Fetch API、Promise、モジュラー設計
- **レスポンシブ**: モバイルファースト設計
- **アニメーション**: CSS Transitions & Keyframes

### **統合自動化システム連携**
- **Python統合システム**: Phase4品質管理システムとの連携
- **完全自動化ワークフロー**: URL検出→記事更新→Git操作→デプロイの完全自動化
- **画像管理API**: Unsplash API + portfolio_image_manager.js
- **品質保証**: 101点満点品質検証システムとの統合
- **Git自動化**: 自動コミット・プッシュ・Vercelデプロイ連携

## 📱 対応ブラウザ

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## 🚀 デプロイ

### **現在のデプロイ環境**
- **メインデプロイ**: Vercel (https://muffin-portfolio-public.vercel.app)
- **リポジトリ**: muffin-blog-automation（統合管理）
- **自動デプロイ**: Git push時に自動更新

### **統合システムによる自動デプロイフロー**
1. **WordPress記事完成** → 完全自動化ワークフローシステム起動
2. **記事情報・画像自動更新** → articles.json自動編集
3. **Git自動操作** → add, commit, push自動実行
4. **Vercel自動デプロイ** → サイト即座更新

## 🤝 メンテナンス

### **統合自動化システム対応（推奨）**

**記事追加の完全自動化**:
- WordPress記事URL確定時に自動検出・実行
- 記事情報抽出・画像取得・Git操作まで完全自動
- ユーザー操作：WordPress記事URLの確定のみ

### **手動メンテナンス（バックアップ手順）**

#### 記事の手動追加時の手順
1. `public/content/articles/articles.json` に記事情報を追加
2. 画像が必要な場合は `portfolio_image_manager.js` を実行
3. Git操作: add → commit → push
4. Vercel自動デプロイの確認

#### 定期的なメンテナンス
- **自動**: 記事追加・画像管理・デプロイ（統合システム対応）
- **手動**: プロフィール情報の定期更新
- **監視**: 統合システム品質ログの確認

---

🎯 **サイトの目的**: プロフェッショナルなポートフォリオとして、スキル・経験・実績を効果的に紹介

📧 **お問い合わせ**: プロフィールページのSNSリンクからご連絡ください
# Updated #午後
