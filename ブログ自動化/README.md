# 🤖 ブログ自動化プロジェクト

WordPressブログの記事生成・画像作成・投稿を自動化するPythonシステム

## 📁 プロジェクト構造

```
ブログ自動化/
├── 📄 README.md                    - このファイル
├── 🔧 core/                        - コアシステム
│   ├── wordpress_api.py             - WordPress API連携基盤
│   ├── blog_article_generator.py    - 記事生成システム
│   ├── complete_blog_automation.py  - メイン自動化機能
│   └── category_manager.py          - カテゴリ管理機能
├── 🖼️ image_generation/             - 画像生成システム
│   ├── canva_image_generator.py     - Canva API連携
│   ├── unsplash_image_generator.py  - Unsplash API連携
│   └── canva_working_token.txt      - Canva認証トークン
├── ⚙️ scripts/                     - ユーティリティスクリプト
│   ├── get_blog_categories.py       - ブログカテゴリ取得
│   ├── publish_draft.py             - 下書き記事公開
│   └── fix_test_post_status.py      - テスト投稿修正
└── 📋 docs/                        - ドキュメント
    ├── setup_guide.md               - セットアップガイド
    ├── unlimi_design_spec.md        - デザイン仕様書（参考）
    ├── Claude主導ブログ自動化企画書.md - プロジェクト企画書
    ├── ファイル整理計画.md            - ファイル整理記録
    └── 整理完了報告.md              - 整理完了報告
```

## 🚀 クイックスタート

### 1. セットアップ
```bash
# 依存関係のインストール
pip install requests openai

# 設定ファイルの準備
cp docs/setup_guide.md ./
```

### 2. 基本的な使用方法

**記事生成 + 投稿:**
```python
from core.complete_blog_automation import BlogAutomator

automator = BlogAutomator()
automator.create_and_publish_article("Audibleのおすすめ使い方")
```

**画像生成:**
```python
from image_generation.canva_image_generator import CanvaImageGenerator

generator = CanvaImageGenerator()
image_url = generator.create_blog_image("読書術", "効率的な読書方法")
```

**カテゴリ管理:**
```python
from scripts.get_blog_categories import get_blog_categories

categories = get_blog_categories()
print(categories)
```

## 📖 詳細ドキュメント

- **[セットアップガイド](docs/setup_guide.md)** - 初期設定方法
- **[プロジェクト企画書](docs/Claude主導ブログ自動化企画書.md)** - プロジェクトの背景と目的
- **[デザイン仕様書](docs/unlimi_design_spec.md)** - UI/UXデザインの参考資料

## ⚡ 主要機能

### 🔧 コアシステム
- **WordPress API連携** - 記事投稿・カテゴリ管理・メディアアップロード
- **AI記事生成** - OpenAI GPTを使った高品質記事作成
- **自動化ワークフロー** - 記事生成→画像作成→投稿の全自動実行

### 🖼️ 画像生成
- **Canva API** - プロ品質のブログアイキャッチ画像生成
- **Unsplash API** - 高品質ストック画像の自動取得・加工

### ⚙️ ユーティリティ
- **カテゴリ分析** - ブログの既存カテゴリ構造分析
- **下書き管理** - 下書き記事の一括公開機能
- **投稿修正** - テスト投稿の状態修正機能

## 🔒 セキュリティ

- **認証情報の保護** - `.gitignore`で認証トークンを除外
- **API制限対応** - レート制限を考慮した安全な API呼び出し
- **エラーハンドリング** - 堅牢なエラー処理とログ出力

## 🤝 貢献

このプロジェクトへの貢献を歓迎します：

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 📞 サポート

質問や問題がある場合は、GitHub Issuesを使用してください。

---

**🤖 Generated with Claude Code**