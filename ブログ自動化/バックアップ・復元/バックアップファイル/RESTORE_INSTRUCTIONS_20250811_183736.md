# 復元手順

## 元に戻すコマンド:
1. 独立リポジトリ復元: 
   cd /Users/satoumasamitsu/Desktop/osigoto/muffin-portfolio-backup-20250811_183253
   gh repo create muffin-blog/muffin-portfolio --public --source .
   git push origin main

2. Vercel本番環境復元:
   vercel projects rm muffin-portfolio-public --yes
   # その後、vercel.com で muffin-blog/muffin-portfolio を再接続

## バックアップ日時: #午後
## 元のVercel設定: muffin-blog/muffin-portfolio リポジトリ接続

