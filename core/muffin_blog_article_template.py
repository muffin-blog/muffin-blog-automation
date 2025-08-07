"""
マフィンブログ記事作成テンプレートシステム
完成記事のフォーマットに基づいて新しい記事を生成するシステム
"""

import os
import re
from datetime import datetime

class MuffinBlogArticleTemplate:
    """マフィンブログのフォーマットに準拠した記事作成テンプレート"""
    
    def __init__(self):
        self.template_path = "/Users/satoumasamitsu/osigoto/ブログ自動化/マフィンブログ完成記事/audiobook_jp単品購入ガイド_完成版.md"
        self.output_dir = "/Users/satoumasamitsu/osigoto/ブログ自動化/マフィンブログ完成記事"
        
        # マフィンブログの文章スタイル特徴
        self.style_guidelines = {
            "tone": "自然で親しみやすい関西弁のマフィンさんとの対話形式",
            "structure": "H2見出しごとに明確な答えを提示",
            "sentence_style": "簡潔で読みやすい、AI的表現を避ける",
            "dialogue_format": "「」を使った会話で親近感を演出",
            "evidence_based": "正確な情報に基づいた内容",
            "seo_optimized": "読者の検索意図に応える構成"
        }
    
    def load_template_structure(self):
        """テンプレート記事の構造を読み込み"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # 記事構造を解析
            structure = self.analyze_article_structure(template_content)
            return structure
            
        except FileNotFoundError:
            print(f"テンプレートファイルが見つかりません: {self.template_path}")
            return None
    
    def analyze_article_structure(self, content):
        """記事の構造を解析してテンプレート化"""
        structure = {
            "title_pattern": r"^# (.+)",
            "h2_sections": [],
            "dialogue_examples": [],
            "list_formats": [],
            "conclusion_format": ""
        }
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            # H1タイトル
            if line.startswith('# '):
                structure["title"] = line[2:].strip()
            
            # H2見出し
            elif line.startswith('## '):
                current_section = {
                    "heading": line[3:].strip(),
                    "content": [],
                    "has_dialogue": False,
                    "has_lists": False
                }
                structure["h2_sections"].append(current_section)
            
            # 対話の検出
            elif '「' in line and '」' in line:
                structure["dialogue_examples"].append(line.strip())
                if current_section:
                    current_section["has_dialogue"] = True
            
            # リスト形式の検出
            elif line.startswith('- ') or line.startswith('1. ') or line.startswith('**'):
                structure["list_formats"].append(line.strip())
                if current_section:
                    current_section["has_lists"] = True
            
            # セクション内容の追加
            elif current_section and line.strip():
                current_section["content"].append(line)
        
        return structure
    
    def create_article_template(self, topic, target_keywords, content_outline):
        """新しい記事のテンプレートを作成"""
        structure = self.load_template_structure()
        if not structure:
            return None
        
        # 新しい記事の基本構造を作成
        article_template = self.generate_article_structure(
            topic, target_keywords, content_outline, structure
        )
        
        return article_template
    
    def generate_article_structure(self, topic, keywords, outline, template_structure):
        """マフィンブログフォーマットに基づく記事構造生成"""
        
        # タイトル生成（テンプレートのパターンを参考）
        title = f"{topic}完全ガイド！2025年8月最新情報と賢い選び方"
        
        # 記事冒頭の対話
        opening_dialogue = f'''「マフィンさん、{topic}について教えてください！」

「ええ質問やな！{topic}について詳しく解説するで。知っとかなあかんポイントがようけあるからな」

「ありがとうございます！よろしくお願いします」

「任せとき！分かりやすう説明したるから安心してや」

---'''
        
        # この記事で分かることセクション
        article_benefits = f'''**この記事で分かること**
- {keywords[0]}の基本知識と選び方
- {keywords[1]}の活用方法と注意点
- {keywords[2]}の比較とおすすめ
- 失敗しない選択方法と具体的手順
- よくある疑問への回答'''
        
        # 結論部分
        conclusion = f'''{topic}を選ぶなら、正確な情報に基づいて判断することが重要です。

この記事で解説したポイントを参考に、あなたに最適な選択をしてください。'''
        
        # 完整的な記事テンプレート
        full_template = f'''# {title}

{opening_dialogue}

{article_benefits}

{conclusion}

{self.generate_main_sections(outline, template_structure)}

{self.generate_faq_section(topic)}

{self.generate_conclusion_section(topic)}
'''
        
        return full_template
    
    def generate_main_sections(self, outline, template_structure):
        """メインセクションの生成"""
        sections = []
        
        for i, section_topic in enumerate(outline, 1):
            # H2見出し
            section_title = f"## {section_topic}"
            
            # マフィンさんとの対話を挿入
            dialogue = f'''「マフィンさん、{section_topic}について詳しく教えてください」

「{section_topic}はな、重要なポイントがいくつかあるねん。順番に説明するで」'''
            
            # セクション内容のプレースホルダー
            content_placeholder = f'''
{section_topic}のポイント：

**重要な要素**
- ポイント1：具体的な内容
- ポイント2：実用的な情報
- ポイント3：注意すべき事項

**具体例**
実際の例を使って分かりやすく説明します。

{dialogue}
'''
            
            sections.append(f"{section_title}\n\n{content_placeholder}")
        
        return "\n\n".join(sections)
    
    def generate_faq_section(self, topic):
        """Q&Aセクションの生成"""
        return f'''## よくある質問：{topic}の疑問を解決

### Q1. 基本的な疑問について
回答内容をここに記載します。読者の実際の疑問に答える形で、分かりやすく説明します。

「マフィンさんからのアドバイス」

### Q2. 選び方について  
具体的な選択基準や判断方法を説明します。

「マフィンさんからのアドバイス」

### Q3. 注意点について
気をつけるべきポイントや失敗しない方法を解説します。

「マフィンさんからのアドバイス」

### Q4. おすすめの方法は？
最も効果的で実用的な方法を推奨します。

「マフィンさんからのアドバイス」'''
    
    def generate_conclusion_section(self, topic):
        """まとめセクションの生成"""
        return f'''## まとめ：{topic}で成功するためのポイント

{topic}について重要なポイントをお伝えしました。正確な情報に基づいて、あなたに最適な選択をしてください。

**成功のための4つのポイント**
1. **基本を理解する**：まずは基礎知識をしっかり把握
2. **比較検討する**：複数の選択肢を客観的に比較  
3. **実際に試す**：可能な場合は体験や試用を活用
4. **継続的に見直す**：定期的に最適性を確認

初心者の方は、まず基本的な部分から始めて、徐々に詳しい内容に進んでいくことをおすすめします。

「マフィンさん、ありがとうございました！とても分かりやすかったです」

「どういたしまして！分からんことがあったらまた聞いてや。成功を祈っとるで」'''
    
    def generate_filename(self, main_keyword, sub_keyword="", date=None):
        """マフィンブログ命名規則に基づくファイル名生成"""
        if date is None:
            date = datetime.now().strftime("%Y%m%d")
        
        # サブキーワードがある場合は追加
        if sub_keyword:
            filename = f"{main_keyword}_{sub_keyword}_{date}_完成版.md"
        else:
            filename = f"{main_keyword}_{date}_完成版.md"
        
        return filename
    
    def add_meta_info(self, article_content, main_keyword, sub_keywords, target_audience, purpose, reference_article=""):
        """記事冒頭にメタ情報を追加"""
        current_date = datetime.now().strftime("%Y年%m月%d日")
        
        meta_info = f'''<!--
記事メタ情報:
- メインキーワード: {main_keyword}
- サブキーワード: {", ".join(sub_keywords) if isinstance(sub_keywords, list) else sub_keywords}
- 作成日: {current_date}
- 対象読者: {target_audience}
- 記事の目的: {purpose}
- 参考とした完成記事: {reference_article}
-->

{article_content}'''
        
        return meta_info
    
    def save_new_article(self, article_content, main_keyword, sub_keyword="", meta_info=None):
        """新しい記事をマフィンブログ完成記事フォルダに保存（命名規則準拠）"""
        
        # ファイル名生成
        filename = self.generate_filename(main_keyword, sub_keyword)
        filepath = os.path.join(self.output_dir, filename)
        
        # メタ情報を追加
        if meta_info:
            final_content = self.add_meta_info(
                article_content,
                meta_info.get("main_keyword", main_keyword),
                meta_info.get("sub_keywords", sub_keyword),
                meta_info.get("target_audience", ""),
                meta_info.get("purpose", ""),
                meta_info.get("reference_article", "")
            )
        else:
            final_content = article_content
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            print(f"✅ 新しい記事が保存されました: {filename}")
            print(f"📁 保存場所: {filepath}")
            print(f"📋 ファイル名は命名規則に準拠: [メインキーワード]_[サブキーワード]_YYYYMMDD_完成版.md")
            return filepath
            
        except Exception as e:
            print(f"❌ 記事の保存に失敗しました: {e}")
            return None
    
    def get_style_guidelines(self):
        """マフィンブログのスタイルガイドラインを取得"""
        return f"""
マフィンブログ記事作成ガイドライン：

🎯 **基本方針**
- 読者に寄り添う自然な文章
- AI的表現を避け、人間らしい語りかけ
- 正確な情報に基づいた信頼できる内容
- SEOを意識しつつ読者ファーストの構成

📝 **文章スタイル**
- 簡潔で分かりやすい表現
- 断定的すぎる表現を避ける
- 具体例や実体験を含める
- 読者の疑問を先回りして解答

💬 **対話形式**
- マフィンさん（関西弁の親しみやすいキャラクター）
- 学習者との自然な会話
- 「」を使った読みやすい対話表現

📊 **構成要素**
- 明確なH2見出し（それ単体で答えが分かる）
- 箇条書きや表での視覚的整理
- Q&Aセクションで読者の疑問解決
- 実用的な手順やステップの提示

🔍 **SEO対策**
- タイトルに年月とキーワードを含む
- 見出しに検索意図を反映
- 内部リンクの自然な配置
- メタディスクリプションを意識した導入文
        """

# 使用例
if __name__ == "__main__":
    template_system = MuffinBlogArticleTemplate()
    
    # サンプル記事作成（正しい命名規則のデモ）
    main_keyword = "Audible"
    sub_keyword = "おすすめ作品"
    keywords = ["Audible", "おすすめ", "2025年"]
    outline = [
        "Audibleおすすめ作品ランキング",
        "ジャンル別人気作品紹介", 
        "初心者向け選び方ガイド",
        "お得な利用方法"
    ]
    
    # 新記事テンプレート生成
    new_article = template_system.create_article_template("Audibleおすすめ作品", keywords, outline)
    
    if new_article:
        # メタ情報設定
        meta_info = {
            "main_keyword": main_keyword,
            "sub_keywords": ["おすすめ作品", "2025年", "ランキング"],
            "target_audience": "Audible初心者〜中級者、作品選びに迷う利用者",
            "purpose": "Audibleで聴くべきおすすめ作品を厳選紹介し、効果的な選び方を提供",
            "reference_article": "audiobook_jp単品購入_20250806_完成版.md"
        }
        
        # 記事を保存（命名規則準拠）
        saved_path = template_system.save_new_article(
            new_article, 
            main_keyword, 
            sub_keyword, 
            meta_info
        )
        
        if saved_path:
            print(f"\n📖 スタイルガイドライン:")
            print(template_system.get_style_guidelines())
            print(f"\n🔥 重要: 今後すべての記事はこの命名規則で保存してください！")
            print(f"命名例: {template_system.generate_filename('新キーワード', 'サブキーワード')}")