"""
Claude主導のブログ記事自動生成システム
既存記事のスタイルを分析し、一貫性のある記事を自動作成
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import os

class BlogStyleAnalyzer:
    """既存ブログ記事のスタイル分析クラス"""
    
    def __init__(self, portfolio_articles_path: str):
        """
        初期化
        
        Args:
            portfolio_articles_path: ポートフォリオサイトのarticles.jsonのパス
        """
        self.articles_path = portfolio_articles_path
        self.blog_articles = []
        self.style_patterns = {}
        
        self._load_articles()
        self._analyze_style_patterns()
    
    def _load_articles(self):
        """ポートフォリオサイトから既存ブログ記事を読み込み"""
        try:
            with open(self.articles_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.blog_articles = data.get('blogArticles', [])
            print(f"✅ {len(self.blog_articles)}件のブログ記事を読み込みました")
        except Exception as e:
            print(f"❌ 記事読み込みエラー: {e}")
            self.blog_articles = []
    
    def _analyze_style_patterns(self):
        """既存記事のスタイルパターンを分析"""
        if not self.blog_articles:
            return
        
        # タイトルパターン分析
        title_patterns = []
        tag_patterns = []
        description_patterns = []
        
        for article in self.blog_articles:
            title = article.get('title', '')
            tags = article.get('tags', [])
            description = article.get('description', '')
            
            title_patterns.append(title)
            tag_patterns.extend(tags)
            description_patterns.append(description)
        
        self.style_patterns = {
            'title_style': self._analyze_title_style(title_patterns),
            'common_tags': self._get_common_tags(tag_patterns),
            'description_style': self._analyze_description_style(description_patterns),
            'content_themes': self._extract_content_themes()
        }
        
        print("✅ スタイルパターン分析完了")
    
    def _analyze_title_style(self, titles: List[str]) -> Dict:
        """タイトルのスタイルパターンを分析"""
        patterns = {
            'average_length': sum(len(title) for title in titles) / len(titles) if titles else 0,
            'common_formats': [],
            'exclamation_usage': sum(1 for title in titles if '！' in title) / len(titles) if titles else 0,
            'question_usage': sum(1 for title in titles if '？' in title) / len(titles) if titles else 0,
            'number_usage': sum(1 for title in titles if any(char.isdigit() for char in title)) / len(titles) if titles else 0
        }
        
        # よくある形式を抽出
        format_patterns = [
            r'.*で.*する.*',  # 「Audibleで学習する方法」
            r'.*の.*方.*',    # 「退会の仕方」
            r'.*ガイド.*',    # 「完全ガイド」
            r'.*！.*',        # 感嘆符パターン
        ]
        
        for pattern in format_patterns:
            matches = sum(1 for title in titles if re.search(pattern, title))
            if matches > 0:
                patterns['common_formats'].append({
                    'pattern': pattern,
                    'frequency': matches / len(titles)
                })
        
        return patterns
    
    def _get_common_tags(self, all_tags: List[str]) -> List[str]:
        """よく使われるタグを抽出"""
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # 頻度順にソート
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        return [tag for tag, count in sorted_tags[:10]]  # 上位10個
    
    def _analyze_description_style(self, descriptions: List[str]) -> Dict:
        """説明文のスタイルパターンを分析"""
        if not descriptions:
            return {}
        
        return {
            'average_length': sum(len(desc) for desc in descriptions) / len(descriptions),
            'common_endings': self._extract_common_endings(descriptions),
            'keyword_patterns': self._extract_description_keywords(descriptions)
        }
    
    def _extract_common_endings(self, descriptions: List[str]) -> List[str]:
        """説明文の共通する語尾を抽出"""
        endings = []
        for desc in descriptions:
            if desc:
                # 最後の文を取得
                sentences = desc.split('。')
                if sentences:
                    last_sentence = sentences[-1].strip()
                    if last_sentence:
                        endings.append(last_sentence)
        
        # 共通パターンを簡単に抽出
        common_endings = []
        for ending in set(endings):
            if endings.count(ending) > 1:
                common_endings.append(ending)
        
        return common_endings[:5]  # 上位5個
    
    def _extract_description_keywords(self, descriptions: List[str]) -> List[str]:
        """説明文によく使われるキーワードを抽出"""
        all_words = []
        for desc in descriptions:
            # 簡単な単語分割（実際はより高度な形態素解析が望ましい）
            words = re.findall(r'[ァ-ヴー]+|[あ-ん]+|[一-龯]+', desc)
            all_words.extend(words)
        
        # 頻度カウント
        word_counts = {}
        for word in all_words:
            if len(word) >= 2:  # 2文字以上
                word_counts[word] = word_counts.get(word, 0) + 1
        
        # 頻度順にソート
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:20]]  # 上位20個
    
    def _extract_content_themes(self) -> Dict:
        """記事のコンテンツテーマを分析"""
        themes = {
            'audible': 0,
            'learning': 0,
            'money': 0,
            'productivity': 0,
            'habit': 0
        }
        
        for article in self.blog_articles:
            title = article.get('title', '').lower()
            tags = [tag.lower() for tag in article.get('tags', [])]
            description = article.get('description', '').lower()
            
            all_text = f"{title} {' '.join(tags)} {description}"
            
            # テーマキーワードでカウント
            if any(keyword in all_text for keyword in ['audible', 'オーディブル', 'オーディオブック']):
                themes['audible'] += 1
            if any(keyword in all_text for keyword in ['学習', '勉強', '学び', 'learning']):
                themes['learning'] += 1
            if any(keyword in all_text for keyword in ['お金', '投資', '節約', 'money']):
                themes['money'] += 1
            if any(keyword in all_text for keyword in ['効率', '生産性', 'productivity']):
                themes['productivity'] += 1
            if any(keyword in all_text for keyword in ['習慣', 'habit', '継続']):
                themes['habit'] += 1
        
        return themes
    
    def get_style_summary(self) -> Dict:
        """スタイル分析の結果を返す"""
        return self.style_patterns

class BlogArticleGenerator:
    """Claude主導のブログ記事自動生成クラス"""
    
    def __init__(self, style_analyzer: BlogStyleAnalyzer):
        """
        初期化
        
        Args:
            style_analyzer: スタイル分析済みのBlogStyleAnalyzer
        """
        self.analyzer = style_analyzer
        self.style_patterns = style_analyzer.get_style_summary()
    
    def generate_title(self, theme: str, keywords: List[str]) -> str:
        """
        テーマとキーワードに基づいてタイトルを生成
        
        Args:
            theme: 記事のテーマ（例：audible, learning, money）
            keywords: 関連キーワードのリスト
        
        Returns:
            生成されたタイトル
        """
        # 既存タイトルのスタイルを参考に生成
        title_style = self.style_patterns.get('title_style', {})
        
        # テーマ別のタイトル形式
        theme_formats = {
            'audible': [
                "Audibleで{keyword}！{benefit}な{method}",
                "{keyword}学習にAudibleが最適な理由と効果的な使い方",
                "忙しい人のためのAudible活用術：{keyword}で人生を変える方法"
            ],
            'learning': [
                "効率的な{keyword}学習法！{benefit}を実現する{method}",
                "{keyword}の勉強を継続させる{method}のコツ",
                "忙しい社会人が{keyword}をマスターする実践的方法"
            ],
            'money': [
                "{keyword}で資産形成！初心者でもできる{method}",
                "お金の勉強を始めるなら{keyword}から！{benefit}な方法",
                "{keyword}投資の基本：リスクを抑えて賢く増やす方法"
            ],
            'productivity': [
                "{keyword}で生産性アップ！{benefit}な{method}",
                "効率化ツール{keyword}の使い方完全ガイド",
                "{keyword}を使って仕事の効率を劇的に改善する方法"
            ],
            'habit': [
                "{keyword}習慣で人生が変わる！{benefit}な{method}",
                "続けられる{keyword}の始め方：{benefit}を実現するコツ",
                "{keyword}を習慣化する{method}の実践法"
            ]
        }
        
        formats = theme_formats.get(theme, theme_formats['learning'])
        
        # キーワードから適切なものを選択
        main_keyword = keywords[0] if keywords else theme
        
        # プレースホルダーを実際の値で置換
        title_template = formats[0]  # 最初の形式を使用
        
        title = title_template.format(
            keyword=main_keyword,
            benefit="効果的",
            method="方法"
        )
        
        return title
    
    def generate_meta_description(self, title: str, theme: str) -> str:
        """
        タイトルとテーマに基づいてメタディスクリプションを生成
        
        Args:
            title: 記事タイトル
            theme: 記事テーマ
        
        Returns:
            メタディスクリプション
        """
        desc_style = self.style_patterns.get('description_style', {})
        target_length = int(desc_style.get('average_length', 120))
        
        # テーマ別の説明文テンプレート
        theme_descriptions = {
            'audible': "Audibleを活用した効率的な学習方法について詳しく解説。忙しい社会人でも続けられる実践的なアドバイスを提供します。",
            'learning': "効果的な学習法と継続のコツを詳しく解説。忙しい日常でも実践できる具体的な方法を紹介します。",
            'money': "お金の勉強と資産形成について初心者にもわかりやすく解説。実践的な投資方法とリスク管理のポイントを紹介します。",
            'productivity': "生産性向上のための具体的な方法とツール活用法を解説。仕事の効率化に役立つ実践的なアドバイスを提供します。",
            'habit': "良い習慣の作り方と継続のコツを詳しく解説。日常生活に取り入れやすい実践的な方法を紹介します。"
        }
        
        base_description = theme_descriptions.get(theme, theme_descriptions['learning'])
        
        # 目標文字数に調整
        if len(base_description) > target_length:
            base_description = base_description[:target_length-3] + "..."
        
        return base_description
    
    def select_tags(self, theme: str, keywords: List[str]) -> List[str]:
        """
        テーマとキーワードに基づいてタグを選択
        
        Args:
            theme: 記事テーマ
            keywords: 関連キーワード
        
        Returns:
            選択されたタグのリスト
        """
        common_tags = self.style_patterns.get('common_tags', [])
        
        # テーマ別の基本タグ
        theme_tags = {
            'audible': ["Audible", "オーディオブック", "学習法"],
            'learning': ["学習法", "自己啓発", "スキルアップ"],
            'money': ["投資", "お金", "資産形成"],
            'productivity': ["生産性", "効率化", "ツール"],
            'habit': ["習慣化", "継続", "ライフスタイル"]
        }
        
        # 基本タグを取得
        selected_tags = theme_tags.get(theme, ["学習法", "自己啓発"])
        
        # キーワードから追加
        for keyword in keywords[:2]:  # 最大2個まで
            if keyword not in selected_tags:
                selected_tags.append(keyword)
        
        # 既存の人気タグから関連するものを追加
        for tag in common_tags[:3]:  # 上位3個を確認
            if any(keyword in tag.lower() for keyword in [theme] + keywords):
                if tag not in selected_tags:
                    selected_tags.append(tag)
        
        return selected_tags[:5]  # 最大5個まで
    
    def select_category(self, theme: str) -> str:
        """
        テーマに基づいてカテゴリを選択
        
        Args:
            theme: 記事テーマ
        
        Returns:
            カテゴリ名
        """
        theme_categories = {
            'audible': "Audible活用",
            'learning': "学習・自己啓発",
            'money': "お金・投資",
            'productivity': "生産性向上",
            'habit': "習慣・ライフスタイル"
        }
        
        return theme_categories.get(theme, "学習・自己啓発")
    
    def generate_article_content(self, 
                                title: str, 
                                theme: str, 
                                keywords: List[str],
                                word_count: int = 2000) -> str:
        """
        記事本文を生成
        
        Args:
            title: 記事タイトル
            theme: 記事テーマ
            keywords: 関連キーワード
            word_count: 目標文字数
        
        Returns:
            HTML形式の記事本文
        """
        # 既存記事のスタイルを参考に構成を決定
        content_structure = self._get_content_structure(theme)
        
        # セクション別に内容を生成
        content_sections = []
        
        # 導入部
        intro = self._generate_introduction(title, theme, keywords)
        content_sections.append(intro)
        
        # メインセクション
        for section in content_structure['main_sections']:
            section_content = self._generate_section_content(section, theme, keywords)
            content_sections.append(section_content)
        
        # まとめ
        conclusion = self._generate_conclusion(title, theme, keywords)
        content_sections.append(conclusion)
        
        # HTMLとして結合
        full_content = '\n\n'.join(content_sections)
        
        return full_content
    
    def _get_content_structure(self, theme: str) -> Dict:
        """テーマに基づいて記事構成を決定"""
        structures = {
            'audible': {
                'main_sections': [
                    {'title': 'Audibleとは？基本的な使い方', 'type': 'explanation'},
                    {'title': '効果的な学習方法', 'type': 'howto'},
                    {'title': 'おすすめ書籍・ジャンル', 'type': 'recommendation'},
                    {'title': '継続のコツ', 'type': 'tips'}
                ]
            },
            'learning': {
                'main_sections': [
                    {'title': '効率的な学習の基本原則', 'type': 'principle'},
                    {'title': '具体的な学習方法', 'type': 'howto'},
                    {'title': '学習を継続させるコツ', 'type': 'tips'},
                    {'title': '成果を最大化する工夫', 'type': 'optimization'}
                ]
            },
            'money': {
                'main_sections': [
                    {'title': '基本的な考え方', 'type': 'principle'},
                    {'title': '具体的な実践方法', 'type': 'howto'},
                    {'title': 'リスク管理のポイント', 'type': 'caution'},
                    {'title': '長期的な戦略', 'type': 'strategy'}
                ]
            }
        }
        
        return structures.get(theme, structures['learning'])
    
    def _generate_introduction(self, title: str, theme: str, keywords: List[str]) -> str:
        """導入部を生成"""
        intro_templates = {
            'audible': f"""
            <p>「忙しくて読書の時間が取れない」「通勤時間を有効活用したい」そんな悩みを持つ方におすすめなのがAudibleです。</p>
            <p>この記事では、{', '.join(keywords[:2])}に関する効果的なAudible活用法を詳しく解説します。忙しい日常の中でも継続できる学習方法をお伝えしますので、ぜひ参考にしてください。</p>
            """,
            'learning': f"""
            <p>効率的な学習方法を身につけることは、現代社会において非常に重要なスキルです。特に{', '.join(keywords[:2])}の分野では、正しい学習アプローチが成果に大きく影響します。</p>
            <p>この記事では、科学的根拠に基づいた学習法と、実際に効果を実感できる実践的なテクニックを紹介します。</p>
            """
        }
        
        return intro_templates.get(theme, intro_templates['learning'])
    
    def _generate_section_content(self, section: Dict, theme: str, keywords: List[str]) -> str:
        """各セクションの内容を生成"""
        title = section['title']
        content_type = section['type']
        
        # セクションタイトル
        html_content = f"<h2>{title}</h2>\n"
        
        # 内容タイプに応じて本文生成
        if content_type == 'howto':
            html_content += self._generate_howto_content(keywords)
        elif content_type == 'tips':
            html_content += self._generate_tips_content(keywords)
        elif content_type == 'explanation':
            html_content += self._generate_explanation_content(keywords)
        else:
            html_content += self._generate_general_content(title, keywords)
        
        return html_content
    
    def _generate_howto_content(self, keywords: List[str]) -> str:
        """ハウツー系の内容を生成"""
        return f"""
        <p>効果的な方法を実践するためには、以下のステップを順番に行うことが重要です。</p>
        <h3>ステップ1: 基本的な準備</h3>
        <p>{keywords[0] if keywords else '対象分野'}について学習する前に、まず基本的な準備を整えましょう。適切な環境作りが成功への第一歩です。</p>
        
        <h3>ステップ2: 実践的なアプローチ</h3>
        <p>理論だけでなく、実際に手を動かして学ぶことが大切です。以下のような方法を試してみてください：</p>
        <ul>
            <li>毎日少しずつでも継続する</li>
            <li>記録をつけて進捗を可視化する</li>
            <li>定期的に振り返りを行う</li>
        </ul>
        
        <h3>ステップ3: 応用と発展</h3>
        <p>基本ができるようになったら、より高度な技術や応用的な内容にチャレンジしていきましょう。</p>
        """
    
    def _generate_tips_content(self, keywords: List[str]) -> str:
        """コツ・ヒント系の内容を生成"""
        return f"""
        <p>継続的に成果を出すためには、いくつかの重要なポイントがあります。</p>
        
        <h3>継続のための工夫</h3>
        <p>習慣化を成功させるには、以下のような工夫が効果的です：</p>
        <ul>
            <li><strong>小さく始める</strong>：最初は無理のない範囲で始めましょう</li>
            <li><strong>環境を整える</strong>：継続しやすい環境を作ることが大切です</li>
            <li><strong>記録をつける</strong>：進捗が見えると motivationが維持できます</li>
        </ul>
        
        <h3>モチベーション維持の秘訣</h3>
        <p>長期的に続けるためには、モチベーションの管理が重要です。目標を明確にし、小さな成功を積み重ねることで、継続への意欲を保つことができます。</p>
        """
    
    def _generate_explanation_content(self, keywords: List[str]) -> str:
        """説明系の内容を生成"""
        return f"""
        <p>まず基本的な概念について理解を深めていきましょう。</p>
        
        <h3>基本的な仕組み</h3>
        <p>{keywords[0] if keywords else 'この分野'}の基本的な仕組みを理解することで、より効果的に活用することができます。重要なのは、表面的な知識だけでなく、根本的な原理を理解することです。</p>
        
        <h3>メリットと注意点</h3>
        <p>適切に活用すれば多くのメリットを得ることができますが、同時に注意すべき点もあります：</p>
        <ul>
            <li><strong>メリット</strong>：効率的な学習が可能になる</li>
            <li><strong>注意点</strong>：継続的な取り組みが必要</li>
        </ul>
        """
    
    def _generate_general_content(self, title: str, keywords: List[str]) -> str:
        """一般的な内容を生成"""
        return f"""
        <p>{title}について詳しく解説していきます。</p>
        <p>この分野では、{', '.join(keywords[:2]) if keywords else '基本的な原則'}を理解することが重要です。実践的なアプローチを通じて、効果的な結果を得ることができます。</p>
        <p>具体的な方法や事例を通じて、実際にどのように活用すれば良いかを説明します。</p>
        """
    
    def _generate_conclusion(self, title: str, theme: str, keywords: List[str]) -> str:
        """まとめ部分を生成"""
        return f"""
        <h2>まとめ</h2>
        <p>この記事では、{title}について詳しく解説しました。</p>
        <p>重要なポイントをまとめると以下の通りです：</p>
        <ul>
            <li>基本的な理解が成功の鍵</li>
            <li>継続的な実践が大切</li>
            <li>自分に合った方法を見つけることが重要</li>
        </ul>
        <p>今回紹介した方法を参考に、ぜひ実践してみてください。継続することで、必ず成果を実感できるはずです。</p>
        """
    
    def create_complete_article(self, 
                               theme: str, 
                               keywords: List[str],
                               custom_title: str = "") -> Dict:
        """
        完全な記事データを作成
        
        Args:
            theme: 記事テーマ
            keywords: 関連キーワード
            custom_title: カスタムタイトル（指定した場合）
        
        Returns:
            記事データの辞書
        """
        # タイトル生成
        title = custom_title if custom_title else self.generate_title(theme, keywords)
        
        # メタ情報生成
        meta_description = self.generate_meta_description(title, theme)
        tags = self.select_tags(theme, keywords)
        category = self.select_category(theme)
        
        # 記事本文生成
        content = self.generate_article_content(title, theme, keywords)
        
        # 内部リンク戦略
        internal_links = self._generate_internal_links(theme, keywords)
        
        return {
            'title': title,
            'content': content,
            'meta_description': meta_description,
            'category': category,
            'tags': tags,
            'theme': theme,
            'keywords': keywords,
            'internal_links': internal_links,
            'created_at': datetime.now().isoformat()
        }
    
    def _generate_internal_links(self, theme: str, keywords: List[str]) -> List[Dict]:
        """内部リンクの提案を生成"""
        # 既存記事から関連性の高いものを抽出
        related_articles = []
        
        for article in self.analyzer.blog_articles:
            article_tags = [tag.lower() for tag in article.get('tags', [])]
            article_title = article.get('title', '').lower()
            
            # テーマやキーワードとの関連性をチェック
            relevance_score = 0
            
            if theme.lower() in article_title:
                relevance_score += 3
            
            for keyword in keywords:
                if keyword.lower() in article_title:
                    relevance_score += 2
                if keyword.lower() in ' '.join(article_tags):
                    relevance_score += 1
            
            if relevance_score > 0:
                related_articles.append({
                    'title': article.get('title'),
                    'url': article.get('url'),
                    'relevance': relevance_score,
                    'suggested_anchor': keyword if keywords else theme
                })
        
        # 関連性の高い順にソート
        related_articles.sort(key=lambda x: x['relevance'], reverse=True)
        
        return related_articles[:3]  # 上位3件

# 使用例
if __name__ == "__main__":
    # ポートフォリオサイトのarticles.jsonのパス
    articles_path = "/Users/satoumasamitsu/osigoto/ポートフォリオサイト/public/content/articles/articles.json"
    
    # スタイル分析
    style_analyzer = BlogStyleAnalyzer(articles_path)
    print("スタイル分析結果:")
    print(json.dumps(style_analyzer.get_style_summary(), ensure_ascii=False, indent=2))
    
    # 記事生成器の初期化
    article_generator = BlogArticleGenerator(style_analyzer)
    
    # テスト記事作成
    test_article = article_generator.create_complete_article(
        theme="audible",
        keywords=["読書術", "効率化", "時間活用"]
    )
    
    print("\n生成された記事データ:")
    print(f"タイトル: {test_article['title']}")
    print(f"カテゴリ: {test_article['category']}")
    print(f"タグ: {', '.join(test_article['tags'])}")
    print(f"メタディスクリプション: {test_article['meta_description']}")
    print("\n記事本文（最初の500文字）:")
    print(test_article['content'][:500] + "...")