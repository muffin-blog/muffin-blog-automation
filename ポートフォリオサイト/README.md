# マフィン - AI × SEOライター | ポートフォリオサイト

スタイリッシュでモダンなポートフォリオサイトです。JSONデータを活用した動的コンテンツ表示機能を搭載しています。

## 🚀 特徴

- **レスポンシブデザイン**: モバイル・タブレット・デスクトップに完全対応
- **動的コンテンツ**: JSONファイルからプロフィールと記事情報を自動読み込み
- **フィルタリング機能**: タグベースの記事フィルタリング
- **モダンUI**: グラデーション、アニメーション、ホバーエフェクト
- **アクセシビリティ対応**: ARIA属性とセマンティックHTML
- **SEO最適化**: メタタグ、構造化データ、Open Graph対応

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
├── CLAUDE.md                  # Claude Code メモリーファイル
├── MAINTENANCE.md             # メンテナンス手順
├── package.json               # プロジェクト設定
├── vercel.json               # Vercel設定
└── README.md
```

## 🛠️ 使用方法

### 基本的な使用

1. ブラウザで `index.html` を開いてサイトを表示
2. すべてのコンテンツは自動的にJSONファイルから読み込まれます

### プロフィール情報の更新

`public/content/profile.json` を編集してプロフィール情報を更新：

```json
{
  "name": "あなたの名前",
  "title": "あなたの職業",
  "bio": "自己紹介文...",
  "profileImage": "assets/images/profile/profile.jpg",
  "socialLinks": [
    {
      "platform": "X",
      "url": "https://twitter.com/your-handle"
    }
  ],
  "skills": ["スキル1", "スキル2", "スキル3"]
}
```

### 記事の追加・更新

`public/content/articles/articles.json` の `articles` 配列に新しい記事を追加：

```json
{
  "articles": [
    {
      "title": "記事タイトル",
      "url": "https://example.com/article",
      "description": "記事の簡単な説明",
      "date": "2025-01-01",
      "tags": ["タグ1", "タグ2", "タグ3"]
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

- **HTML5**: セマンティックマークアップ
- **CSS3**: フレックスボックス、グリッド、カスタムプロパティ
- **ES6+ JavaScript**: Fetch API、Promise、モジュラー設計
- **レスポンシブ**: モバイルファースト設計
- **アニメーション**: CSS Transitions & Keyframes

## 📱 対応ブラウザ

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## 🚀 デプロイ

このサイトは静的ファイルなので、以下のサービスで簡単にデプロイできます：

- GitHub Pages
- Netlify
- Vercel
- Firebase Hosting

## 🤝 メンテナンス

### 記事の追加時の手順

1. `public/content/articles/articles.json` に記事情報を追加
2. ブラウザでサイトをリロードして表示確認
3. 新しいタグが追加された場合、フィルターボタンが自動生成されます

### 定期的なメンテナンス

- 記事のリンク切れチェック
- プロフィール情報の更新
- 新しい記事の追加

---

🎯 **サイトの目的**: プロフェッショナルなポートフォリオとして、スキル・経験・実績を効果的に紹介

📧 **お問い合わせ**: プロフィールページのSNSリンクからご連絡ください
# Updated #午後
