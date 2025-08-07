# Unlimi Channel風 LP制作 詳細設計書

## 📋 プロジェクト概要
- **目的**: WordPress LP機能を使用したUnlimi Channel風トップページ制作
- **対象サイト**: https://muffin-blog.com
- **参考サイト**: https://unlimichannel.com/
- **制作方針**: HTML/CSS完全制御 → WordPressのHTMLブロックに貼り付け

---

## 🎨 デザインシステム仕様

### カラーパレット
```css
:root {
  /* メインカラー */
  --color-primary: #FF6B35;        /* オレンジ（CTA、アクセント） */
  --color-secondary: #F7931E;      /* サブオレンジ（ホバー） */
  
  /* ニュートラルカラー */
  --color-text-dark: #333333;      /* メインテキスト */
  --color-text-medium: #666666;    /* サブテキスト */
  --color-text-light: #999999;     /* キャプション */
  
  /* 背景色 */
  --color-bg-white: #FFFFFF;       /* セクション背景 */
  --color-bg-light: #F8F9FA;       /* 交互背景 */
  --color-bg-neutral: #F5F5F5;     /* カード背景 */
  
  /* ボーダー・影 */
  --color-border: #E5E5E5;
  --shadow-light: 0 2px 10px rgba(0,0,0,0.08);
  --shadow-medium: 0 4px 20px rgba(0,0,0,0.12);
  --shadow-hover: 0 8px 30px rgba(0,0,0,0.15);
}
```

### タイポグラフィ
```css
:root {
  /* フォントファミリー */
  --font-main: 'Noto Sans JP', '游ゴシック Medium', '游ゴシック', sans-serif;
  --font-en: 'Inter', 'Helvetica Neue', sans-serif;
  
  /* フォントサイズ（clamp使用でレスポンシブ） */
  --font-hero: clamp(2.5rem, 5vw, 4rem);      /* ヒーロータイトル */
  --font-xl: clamp(2rem, 4vw, 2.5rem);        /* セクションタイトル */
  --font-lg: clamp(1.25rem, 2.5vw, 1.5rem);   /* カードタイトル */
  --font-base: clamp(1rem, 2vw, 1.125rem);    /* 本文 */
  --font-sm: clamp(0.875rem, 1.5vw, 1rem);    /* キャプション */
  
  /* 行間 */
  --line-height-tight: 1.2;
  --line-height-base: 1.6;
  --line-height-loose: 1.8;
  
  /* フォントウェイト */
  --font-light: 300;
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}
```

### スペーシングシステム
```css
:root {
  /* 基本スペース */
  --space-xs: 0.5rem;    /* 8px */
  --space-sm: 1rem;      /* 16px */
  --space-md: 1.5rem;    /* 24px */
  --space-lg: 2rem;      /* 32px */
  --space-xl: 3rem;      /* 48px */
  --space-2xl: 4rem;     /* 64px */
  --space-3xl: 6rem;     /* 96px */
  
  /* セクション間余白 */
  --section-padding-mobile: clamp(3rem, 8vw, 5rem);
  --section-padding-desktop: clamp(5rem, 10vw, 8rem);
  
  /* コンテナ */
  --container-max: 1200px;
  --container-padding: clamp(1rem, 4vw, 2rem);
}
```

---

## 📐 レイアウト構造仕様

### セクション構成（7セクション）

#### 1. ファーストビュー
```
[Hero Section]
├── Background: グラデーション（白→薄いオレンジ）
├── Container (max-width: 1200px)
│   ├── Title: "READ LEARN SUCCEED"
│   ├── Subtitle: "読書をもっと身近に。1年後の自分を楽にするブログ"
│   └── CTA Button: "おすすめ本を今すぐ見る"
└── Padding: 80px 0 (mobile: 60px 0)
```

#### 2. グローバルメニュー（スティッキー）
```
[Navigation]
├── Position: sticky (top: 0)
├── Background: rgba(255,255,255,0.95)
├── Items: Audible | 読書術 | 学習法 | プロフィール
└── Height: 60px
```

#### 3. カテゴリバナー
```
[Category Section]
├── Grid: 2x2 (mobile: 1x4)
├── Card Design:
│   ├── Icon: 3rem emoji
│   ├── Title: 1.3rem bold
│   ├── Description: 0.95rem
│   └── Hover: translateY(-5px) + shadow
└── Gap: 30px (mobile: 20px)
```

#### 4. 新着記事一覧
```
[Latest Posts]
├── Grid: 3x2 (tablet: 2x3, mobile: 1x6)
├── Card Elements:
│   ├── Image: 16:9 ratio, 200px height
│   ├── Category Badge: pill shape
│   ├── Title: 2行まで表示
│   └── Date: 小さめテキスト
└── Auto Query: WordPress latest 6 posts
```

#### 5. プロフィール
```
[Profile Section]
├── Layout: 左画像 + 右テキスト (mobile: 縦並び)
├── Image: 150px circle, border
├── Content:
│   ├── Name: 1.8rem bold
│   ├── Bio: 1.1rem, line-height 1.8
│   └── SNS Links: アイコン付き
└── Background: 白
```

#### 6. 人気記事ランキング
```
[Popular Posts]
├── Layout: 3カラム (mobile: 1カラム)
├── Ranking: 数字バッジ付き
└── Manual Content: 固定3記事
```

#### 7. フッターCTA
```
[Footer CTA]
├── Background: --color-primary
├── Color: white text
├── CTA: Audible無料体験
└── Padding: 60px 0
```

---

## 📱 レスポンシブ設計

### ブレイクポイント
```css
/* Mobile First */
@media (min-width: 640px)  { /* sm */ }
@media (min-width: 768px)  { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
```

### グリッドシステム
```css
.grid-responsive {
  display: grid;
  gap: var(--space-lg);
  
  /* Mobile: 1 column */
  grid-template-columns: 1fr;
  
  /* Tablet: 2 columns */
  @media (min-width: 768px) {
    grid-template-columns: repeat(2, 1fr);
  }
  
  /* Desktop: 3 columns */
  @media (min-width: 1024px) {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

---

## 🎯 WordPress連携仕様

### 動的コンテンツ部分
```php
<!-- 新着記事取得用PHPコード -->
<?php
$latest_posts = new WP_Query([
    'posts_per_page' => 6,
    'post_status' => 'publish'
]);
?>

<!-- 人気記事（手動設定 or プラグイン連携） -->
<?php
$popular_posts = get_posts([
    'numberposts' => 3,
    'meta_key' => 'post_views_count',
    'orderby' => 'meta_value_num',
    'order' => 'DESC'
]);
?>
```

### LP機能設定
- post_type: 'lp'
- ヘッダー・フッター非表示
- 全幅レイアウト

---

## 🚀 実装フェーズ

### Phase 1: HTML骨組み作成
- セマンティックHTML構造
- 基本CSS（レイアウトのみ）
- WordPress初回テスト

### Phase 2: デザイン詳細実装
- Unlimi Channel風ビジュアル再現
- アニメーション・インタラクション
- 完全レスポンシブ対応

### Phase 3: WordPress統合・最適化
- 動的コンテンツ統合
- パフォーマンス最適化
- 最終調整・完成

---

## 📊 成功指標
- [ ] Unlimi Channelと90%以上の視覚的類似度
- [ ] 全デバイスでの完璧な表示
- [ ] WordPress管理画面での編集可能性
- [ ] ページ読み込み速度3秒以内
- [ ] ユーザビリティの高さ