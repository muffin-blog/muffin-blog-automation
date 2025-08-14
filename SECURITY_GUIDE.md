# セキュリティガイド

## 📋 機密情報管理方法

### 1. 環境変数ファイル
**場所**: `/Users/satoumasamitsu/Desktop/osigoto/.env`

機密情報は全て`.env`ファイルで管理し、コードでは環境変数を参照する。

```python
import os
from dotenv import load_dotenv

load_dotenv()

# WordPressAPI使用例
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')
CONTACT_EMAIL = os.getenv('CONTACT_EMAIL')
CANVA_ACCESS_TOKEN = os.getenv('CANVA_ACCESS_TOKEN')
```

### 2. Git管理から除外
`.gitignore`で以下を除外済み：
- `.env`（機密情報）
- `*.log`（ログファイル）
- `**/*_token.txt`（トークンファイル）

### 3. 現在の機密情報一覧

#### WordPress API
- **ユーザー名**: `muffin1203`
- **パスワード**: `TMLy Z4Wi RhPu oVLm 0lcO gZdi`
- **サイトURL**: `https://muffin-blog.com`

#### メール
- **連絡先**: `0527muffin1203@gmail.com`

#### Canva API
- **アクセストークン**: [長期JWT - 2025年8月期限]

### 4. セキュリティ対策済み項目
- ✅ `.env`ファイルでの一元管理
- ✅ `.gitignore`での除外設定
- ✅ 機密情報ファイルの削除完了
- ✅ ソースコードでの環境変数参照

### 5. 今後の注意事項
- **新しい機密情報は必ず`.env`ファイルに追加**
- **コードには直接書き込まない**
- **環境変数で参照する**
- **定期的にトークンの有効期限を確認**

## 🚨 緊急時の対応
1. WordPressパスワード変更：管理画面→ユーザー→アプリケーションパスワード
2. Canvaトークン再発行：Canva開発者ページで新規発行
3. `.env`ファイルの更新

---
**最終更新**: 2025年8月14日  
**セキュリティレベル**: 強化済み