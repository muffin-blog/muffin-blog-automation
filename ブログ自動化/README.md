# 🤖 ブログ自動化プロジェクト（Phase4統合版）

WordPress記事の完全自動化システム - URL検出からポートフォリオ反映まで全自動 + 101点満点品質保証

## 📁 プロジェクト構造（Phase4統合版）

```
ブログ自動化/
├── 📄 README.md                    - このファイル
├── 🔧 システム実行ファイル/
│   └── コア/                        - Phase4統合システム
│       ├── 継続的品質管理統合システム.py - 101点満点品質保証
│       ├── 投稿前確認システム.py      - SEO検証システム
│       ├── システム監視・品質管理.py   - リアルタイム監視
│       ├── 完全自動化ワークフローシステム.py - URL検出自動実行
│       ├── WordPress連携API.py       - WordPress API連携
│       └── マフィンブログワークフローシステム.py
├── 📁 システム監視データ/           - 品質・エラー・パフォーマンスログ
├── 📁 WordPress投稿下書き/        - 記事下書き・記事データ保存
├── 📁 NotebookLM資料/            - 記事作成用資料
├── 📁 バックアップ・復元/         - システムバックアップ
│   └── 廃止システム/                - 画像生成システム（廃止済み）
└── 📄 絶対的見本テンプレート.md    - 記事品質基準
```

## 🚀 クイックスタート

### 1. セットアップ
```bash
# 依存関係のインストール
pip install requests openai

# 設定ファイルの準備
cp docs/setup_guide.md ./
```

### 2. 基本的な使用方法（Phase4統合版）

**完全自動化ワークフロー:**
```python
from システム実行ファイル.コア.完全自動化ワークフローシステム import CompleteAutomationWorkflowSystem

system = CompleteAutomationWorkflowSystem()
# WordPress URLを検出して自動実行
result = system.execute_complete_automation("https://muffin-blog.com/article-url/")
```

**101点満点品質保証:**
```python
from システム実行ファイル.コア.継続的品質管理統合システム import 継続的品質管理統合システム
from システム実行ファイル.コア.投稿前確認システム import 投稿前確認システム

# 品質チェック実行
quality_system = 継続的品質管理統合システム()
validator = 投稿前確認システム()
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