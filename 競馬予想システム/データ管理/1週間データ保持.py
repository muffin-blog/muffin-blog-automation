"""
1週間データ保持システム
直近7日間のデータのみを保持し、古いデータを自動削除
"""

import os
import json
from datetime import datetime, timedelta
import glob

class WeeklyDataManager:
    """1週間データローテーション管理システム"""
    
    def __init__(self, data_directory=None):
        # データディレクトリ設定
        self.data_dir = data_directory if data_directory else os.path.dirname(os.path.abspath(__file__))
        
        # 管理対象ファイルパターン
        self.file_patterns = {
            'prediction_files': '予想データ_*.json',
            'race_files': 'レースデータ_*.json',
            'weather_files': '天気データ_*.json',
            'verification_files': '検証結果_*.json',
            'learning_files': '学習レポート_*.json',
            'note_articles': 'note記事_*.md',
            'twitter_posts': 'X投稿文_*.json'
        }
        
        # 保持期間（日）
        self.retention_days = 7
        
        # ログファイル
        self.log_file = os.path.join(self.data_dir, "データ管理ログ.json")
    
    def clean_old_files(self):
        """古いファイルを削除"""
        
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        deleted_files = []
        protected_files = []
        
        print(f"🧹 {self.retention_days}日より古いファイルを削除中...")
        print(f"基準日時: {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        for file_type, pattern in self.file_patterns.items():
            file_path = os.path.join(self.data_dir, pattern)
            matching_files = glob.glob(file_path)
            
            for file_path in matching_files:
                try:
                    # ファイルの日付を抽出
                    file_date = self._extract_date_from_filename(file_path)
                    
                    if file_date and file_date < cutoff_date.date():
                        # ファイル削除実行
                        if self._is_safe_to_delete(file_path):
                            os.remove(file_path)
                            deleted_files.append({
                                'file_path': file_path,
                                'file_date': file_date.isoformat(),
                                'file_type': file_type,
                                'deleted_at': datetime.now().isoformat()
                            })
                            print(f"🗑️ 削除: {os.path.basename(file_path)}")
                        else:
                            protected_files.append(file_path)
                            print(f"🔒 保護: {os.path.basename(file_path)}")
                    
                except Exception as e:
                    print(f"⚠️ ファイル処理エラー {file_path}: {e}")
        
        # 削除結果をログに記録
        deletion_log = {
            'deletion_date': datetime.now().isoformat(),
            'cutoff_date': cutoff_date.isoformat(),
            'deleted_files': deleted_files,
            'protected_files': protected_files,
            'total_deleted': len(deleted_files)
        }
        
        self._save_deletion_log(deletion_log)
        
        print(f"✅ クリーンアップ完了: {len(deleted_files)}ファイル削除")
        return deletion_log
    
    def _extract_date_from_filename(self, file_path):
        """ファイル名から日付を抽出"""
        
        filename = os.path.basename(file_path)
        
        # YYYYMMDD形式の日付パターンを検索
        import re
        date_pattern = r'(\d{8})'
        match = re.search(date_pattern, filename)
        
        if match:
            date_str = match.group(1)
            try:
                return datetime.strptime(date_str, '%Y%m%d').date()
            except ValueError:
                return None
        
        # ファイルの更新日時をフォールバックとして使用
        try:
            file_mtime = os.path.getmtime(file_path)
            return datetime.fromtimestamp(file_mtime).date()
        except:
            return None
    
    def _is_safe_to_delete(self, file_path):
        """ファイル削除の安全性チェック"""
        
        filename = os.path.basename(file_path)
        
        # 削除禁止ファイルパターン
        protected_patterns = [
            'システム',
            'config',
            'setting',
            'template',
            '設定',
            'ログ'
        ]
        
        for pattern in protected_patterns:
            if pattern in filename.lower():
                return False
        
        # ファイルサイズチェック（空ファイルは削除OK）
        try:
            file_size = os.path.getsize(file_path)
            return file_size >= 0  # 常にTrue（サイズ制限なし）
        except:
            return False
    
    def get_current_data_status(self):
        """現在のデータ状況を取得"""
        
        status = {
            'scan_date': datetime.now().isoformat(),
            'data_directory': self.data_dir,
            'retention_days': self.retention_days,
            'file_counts': {},
            'oldest_file': None,
            'newest_file': None,
            'total_files': 0,
            'total_size': 0
        }
        
        all_files = []
        
        # 各ファイルタイプをスキャン
        for file_type, pattern in self.file_patterns.items():
            file_path = os.path.join(self.data_dir, pattern)
            matching_files = glob.glob(file_path)
            
            file_info = []
            total_size = 0
            
            for file_path in matching_files:
                try:
                    file_stat = os.stat(file_path)
                    file_date = self._extract_date_from_filename(file_path)
                    
                    file_details = {
                        'path': file_path,
                        'name': os.path.basename(file_path),
                        'size': file_stat.st_size,
                        'modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                        'extracted_date': file_date.isoformat() if file_date else None
                    }
                    
                    file_info.append(file_details)
                    total_size += file_stat.st_size
                    all_files.append(file_details)
                    
                except Exception as e:
                    print(f"⚠️ ファイル情報取得エラー {file_path}: {e}")
            
            status['file_counts'][file_type] = {
                'count': len(file_info),
                'total_size': total_size,
                'files': file_info
            }
        
        # 全体統計
        if all_files:
            status['total_files'] = len(all_files)
            status['total_size'] = sum(f['size'] for f in all_files)
            
            # 最古・最新ファイル
            sorted_files = sorted(all_files, key=lambda x: x['modified'])
            status['oldest_file'] = sorted_files[0]['name']
            status['newest_file'] = sorted_files[-1]['name']
        
        return status
    
    def _save_deletion_log(self, deletion_log):
        """削除ログを保存"""
        
        try:
            # 既存ログを読み込み
            logs = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            
            # 新しいログを追加
            logs.append(deletion_log)
            
            # 古いログも7日で削除（ログのログ）
            cutoff = datetime.now() - timedelta(days=self.retention_days)
            logs = [log for log in logs 
                   if datetime.fromisoformat(log['deletion_date']) > cutoff]
            
            # ログ保存
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
            
        except Exception as e:
            print(f"⚠️ ログ保存エラー: {e}")
    
    def schedule_daily_cleanup(self):
        """毎日のクリーンアップをスケジューリング"""
        
        print("📅 毎日のデータクリーンアップを実行...")
        
        # 現在のデータ状況確認
        before_status = self.get_current_data_status()
        print(f"クリーンアップ前: {before_status['total_files']}ファイル")
        
        # ファイル削除実行
        deletion_result = self.clean_old_files()
        
        # クリーンアップ後の状況確認
        after_status = self.get_current_data_status()
        print(f"クリーンアップ後: {after_status['total_files']}ファイル")
        
        # サマリーレポート作成
        summary = {
            'cleanup_date': datetime.now().isoformat(),
            'before_count': before_status['total_files'],
            'after_count': after_status['total_files'],
            'deleted_count': deletion_result['total_deleted'],
            'space_freed': before_status['total_size'] - after_status['total_size']
        }
        
        print(f"📊 削除ファイル数: {summary['deleted_count']}")
        print(f"💾 解放容量: {summary['space_freed']:,} bytes")
        
        return summary
    
    def manual_file_removal(self, file_pattern):
        """手動ファイル削除（特定パターン）"""
        
        print(f"🎯 手動削除モード: {file_pattern}")
        
        file_path = os.path.join(self.data_dir, file_pattern)
        matching_files = glob.glob(file_path)
        
        if not matching_files:
            print("該当ファイルなし")
            return []
        
        deleted_files = []
        
        for file_path in matching_files:
            try:
                filename = os.path.basename(file_path)
                
                # 確認プロンプト（実際の運用では削除）
                print(f"削除対象: {filename}")
                
                if self._is_safe_to_delete(file_path):
                    os.remove(file_path)
                    deleted_files.append(filename)
                    print(f"✅ 削除完了: {filename}")
                else:
                    print(f"🔒 削除保護: {filename}")
                    
            except Exception as e:
                print(f"❌ 削除エラー {filename}: {e}")
        
        print(f"手動削除完了: {len(deleted_files)}ファイル")
        return deleted_files
    
    def get_file_age_distribution(self):
        """ファイル年齢分布取得"""
        
        distribution = {
            '0-1日': 0,
            '1-3日': 0,
            '3-7日': 0,
            '7日以上': 0
        }
        
        now = datetime.now()
        
        for file_type, pattern in self.file_patterns.items():
            file_path = os.path.join(self.data_dir, pattern)
            matching_files = glob.glob(file_path)
            
            for file_path in matching_files:
                try:
                    file_date = self._extract_date_from_filename(file_path)
                    if file_date:
                        age = (now.date() - file_date).days
                        
                        if age <= 1:
                            distribution['0-1日'] += 1
                        elif age <= 3:
                            distribution['1-3日'] += 1
                        elif age <= 7:
                            distribution['3-7日'] += 1
                        else:
                            distribution['7日以上'] += 1
                
                except Exception as e:
                    continue
        
        return distribution

# テスト実行用
if __name__ == "__main__":
    print("🗂️ データ管理システムテスト開始...")
    
    # テスト用データディレクトリ
    test_dir = os.path.dirname(os.path.abspath(__file__))
    manager = WeeklyDataManager(test_dir)
    
    # 現在のデータ状況
    print("\n📊 現在のデータ状況:")
    status = manager.get_current_data_status()
    print(f"総ファイル数: {status['total_files']}")
    print(f"総サイズ: {status['total_size']:,} bytes")
    
    # ファイル年齢分布
    print("\n📅 ファイル年齢分布:")
    distribution = manager.get_file_age_distribution()
    for age_range, count in distribution.items():
        print(f"- {age_range}: {count}ファイル")
    
    # クリーンアップ実行（テストモード）
    print("\n🧹 クリーンアップテスト:")
    # cleanup_result = manager.schedule_daily_cleanup()
    print("（実際の削除は実行されません）")
    
    print("\n✅ データ管理システムテスト完了")