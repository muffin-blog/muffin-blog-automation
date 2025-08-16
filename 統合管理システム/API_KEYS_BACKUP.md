# 🔑 APIキー バックアップ記録

**作成日**: 2025年8月16日  
**最終更新**: 2025年8月16日

## 🚨 重要事項
- **このファイルはGitにコミットしません**
- **APIキーは絶対に外部に漏洩させません**
- **紛失時はこのファイルから復元します**

## 📋 登録済みAPIキー一覧

### Unsplash API
- **サービス名**: Unsplash Developer API
- **アプリケーション名**: Muffin Portfolio Image Manager
- **Access Key**: `q0wEe7cmJ1Hp-eUBo3SSbvFBDY4PyTUWuIqLR1v1co8`
- **用途**: ポートフォリオサイト用画像自動取得
- **制限**: 50リクエスト/時間（無料プラン）
- **設定場所**: `/Users/satoumasamitsu/Desktop/osigoto/.env`
- **設定済み**: ✅ 2025-08-16

### WordPress API
- **サイトURL**: https://muffin-blog.com
- **ユーザー名**: muffin1203
- **アプリケーションパスワード**: `TMLy Z4Wi RhPu oVLm 0lcO gZdi`
- **用途**: 記事自動投稿・管理
- **設定済み**: ✅

### Canva API
- **Access Token**: `eyJraWQiOiIyMzY4ZjRhYi00N2ZiLTQwN2MtYjM5Ni00NzgxODcwMjZkN2UiLCJhbGciOiJSUzI1NiJ9.eyJqdGkiOiJSVE9La1hTNDZIcUZCcXA3d2cxNThRIiwiY2xpZW50X2lkIjoiT0MtQVpodXJjWS03N0NQIiwiYXVkIjoiaHR0cHM6Ly93d3cuY2FudmEuY29tIiwiaWF0IjoxNzU0MjcwOTUwLCJuYmYiOjE3NTQyNzA5NTAsImV4cCI6MTc1NDI4NTM1MCwic3ViIjoib1VYSHRtZy1iR1lLRWl4Q1FtZEtQWSIsImJyYW5kIjoib0JYSHRfZzFHblZLX2d2eS1FYzQ2MCIsIm9yZ2FuaXphdGlvbiI6bnVsbCwic2NvcGVzIjpbImRlc2lnbjpjb250ZW50OnJlYWQiLCJkZXNpZ246Y29udGVudDp3cml0ZSIsImFzc2V0OnJlYWQiLCJhc3NldDp3cml0ZSJdLCJidW5kbGVzIjpbIlBST1MiXSwiY29kZV9pZCI6IjNEckR5ZGRsa1YxZVFmOXRoSWotWWciLCJhY3RfYXMiOiJ1IiwiYWN4IjoiUGNlcVVmNlBldFBsbEJzbTJFMDlDcnc1ci1CX3AwRDZFcmUybk9tbGEwMmk1bDltSTJnZV96S042clZYMkNfalh0SGl5bnBSa2EtNzBGTktjM3hNWElUT0ZFVSJ9.dLPma8XxqZNGZxd-rb0NFPGZHudDvv2yjTT0r1wkxApR2VaNvBeqNeI4FwuFIEvhhLOHge7EM3mmobn6dRbHddhP4K3PdRvFn__r-YuTSEyK9Kgaspl2oOT6tysHtsfWGEvpiAkDdYMix_Ghyfi5lwaHMj9W8NzvlAxSNeeNcc2bgKEAJk8BNBYJPbHXLEas57gyX5jBoUfDyt2lXLyPO2E4XU3SXq1uLaL8g-IdycSZ5TasuSOxrzWlqjBpIrVejVQcZWn-WWB1YbNVt9dyI33xLFM0t9dC8KVcyVzY9V1wNFF-laWMhCSirHJQmjQNFzLafi9mNzvB9C0ct-FkvQ`
- **用途**: 画像生成システム（現在廃止中）
- **設定済み**: ✅

## 🔄 復元手順

### .envファイル紛失時の復元方法
1. `/Users/satoumasamitsu/Desktop/osigoto/.env` ファイルを作成
2. 以下の内容をコピー貼り付け：

```env
# WordPress API設定
WORDPRESS_SITE_URL=https://muffin-blog.com
WORDPRESS_USERNAME=muffin1203
WORDPRESS_PASSWORD=TMLy Z4Wi RhPu oVLm 0lcO gZdi

# メール設定  
CONTACT_EMAIL=0527muffin1203@gmail.com

# Unsplash API設定
UNSPLASH_ACCESS_KEY=q0wEe7cmJ1Hp-eUBo3SSbvFBDY4PyTUWuIqLR1v1co8

# Canva API設定
CANVA_ACCESS_TOKEN=eyJraWQiOiIyMzY4ZjRhYi00N2ZiLTQwN2MtYjM5Ni00NzgxODcwMjZkN2UiLCJhbGciOiJSUzI1NiJ9.eyJqdGkiOiJSVE9La1hTNDZIcUZCcXA3d2cxNThRIiwiY2xpZW50X2lkIjoiT0MtQVpodXJjWS03N0NQIiwiYXVkIjoiaHR0cHM6Ly93d3cuY2FudmEuY29tIiwiaWF0IjoxNzU0MjcwOTUwLCJuYmYiOjE3NTQyNzA5NTAsImV4cCI6MTc1NDI4NTM1MCwic3ViIjoib1VYSHRtZy1iR1lLRWl4Q1FtZEtQWSIsImJyYW5kIjoib0JYSHRfZzFHblZLX2d2eS1FYzQ2MCIsIm9yZ2FuaXphdGlvbiI6bnVsbCwic2NvcGVzIjpbImRlc2lnbjpjb250ZW50OnJlYWQiLCJkZXNpZ246Y29udGVudDp3cml0ZSIsImFzc2V0OnJlYWQiLCJhc3NldDp3cml0ZSJdLCJidW5kbGVzIjpbIlBST1MiXSwiY29kZV9pZCI6IjNEckR5ZGRsa1YxZVFmOXRoSWotWWciLCJhY3RfYXMiOiJ1IiwiYWN4IjoiUGNlcVVmNlBldFBsbEJzbTJFMDlDcnc1ci1CX3AwRDZFcmUybk9tbGEwMmk1bDltSTJnZV96S042clZYMkNmalh0SGl5bnBSa2EtNzBGTktjM3hNWElUT0ZFVSJ9.dLPma8XxqZNGZxd-rb0NFPGZHudDvv2yjTT0r1wkxApR2VaNvBeqNeI4FwuFIEvhhLOHge7EM3mmobn6dRbHddhP4K3PdRvFn__r-YuTSEyK9Kgaspl2oOT6tysHtsfWGEvpiAkDdYMix_Ghyfi5lwaHMj9W8NzvlAxSNeeNcc2bgKEAJk8BNBYJPbHXLEas57gyX5jBoUfDyt2lXLyPO2E4XU3SXq1uLaL8g-IdycSZ5TasuSOxrzWlqjBpIrVejVQcZWn-WWB1YbNVt9dyI33xLFM0t9dC8KVcyVzY9V1wNFF-laWMhCSirHJQmjQNFzLafi9mNzvB9C0ct-FkvQ
```

## 🛡️ セキュリティ対策
- ✅ .envファイルは.gitignoreで除外済み
- ✅ このバックアップファイルもGitにコミットしない
- ✅ APIキーは必要最小限の権限のみ
- ✅ 定期的な有効性確認実施

## 📝 更新履歴
- 2025-08-16: Unsplash APIキー追加・動作確認完了
- 既存: WordPress API、Canva API設定済み