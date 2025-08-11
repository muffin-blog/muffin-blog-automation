/**
 * ポートフォリオサイト用自動画像取得・管理システム
 * 記事情報からUnsplash画像を自動取得・ダウンロード・管理
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const crypto = require('crypto');

class PortfolioImageManager {
    constructor() {
        // Unsplash API設定（環境変数から読み込み）
        this.unsplashAccessKey = process.env.UNSPLASH_ACCESS_KEY || 'YOUR_ACCESS_KEY_HERE';
        this.unsplashApiUrl = 'https://api.unsplash.com';
        
        // ディレクトリ設定
        this.imageDir = path.join(__dirname, 'public/assets/images/blog-thumbnails');
        this.articlesJsonPath = path.join(__dirname, 'public/content/articles/articles.json');
        
        // 画像設定
        this.imageSize = { width: 400, height: 250 };
        this.imageQuality = 80;
        
        this.ensureImageDirectory();
    }

    /**
     * 画像管理ディレクトリの存在確認・作成
     */
    ensureImageDirectory() {
        if (!fs.existsSync(this.imageDir)) {
            fs.mkdirSync(this.imageDir, { recursive: true });
            console.log(`📁 画像管理ディレクトリ作成: ${this.imageDir}`);
        }
    }

    /**
     * 記事からキーワードを抽出
     * @param {Object} article - 記事オブジェクト
     * @returns {Array} キーワード配列
     */
    extractKeywords(article) {
        const keywords = [];
        
        // タグからキーワード抽出
        if (article.tags && article.tags.length > 0) {
            keywords.push(...article.tags);
        }
        
        // タイトルからキーワード抽出（日本語対応）
        const titleKeywords = article.title
            .replace(/[！？。、]/g, ' ')
            .split(/[\\s\\u3000]+/)
            .filter(word => word.length > 1)
            .slice(0, 3); // 最初の3単語
        
        keywords.push(...titleKeywords);
        
        // 英語キーワードマッピング（検索精度向上）
        const keywordMapping = {
            'Audible': 'audiobook',
            '読書': 'book',
            '学習': 'study',
            '時間管理': 'time management',
            '睡眠': 'sleep',
            'ブログ': 'blog',
            '投資': 'investment',
            '健康': 'health'
        };
        
        keywords.forEach(keyword => {
            if (keywordMapping[keyword]) {
                keywords.push(keywordMapping[keyword]);
            }
        });
        
        return [...new Set(keywords)]; // 重複除去
    }

    /**
     * Unsplash APIで画像を検索
     * @param {Array} keywords - 検索キーワード
     * @returns {Promise<Object>} 画像情報
     */
    async searchUnsplashImage(keywords) {
        const query = keywords.slice(0, 3).join(' '); // 最初の3つのキーワード
        const apiUrl = `${this.unsplashApiUrl}/search/photos?query=${encodeURIComponent(query)}&per_page=5&orientation=landscape`;
        
        return new Promise((resolve, reject) => {
            const options = {
                headers: {
                    'Authorization': `Client-ID ${this.unsplashAccessKey}`,
                    'Accept-Version': 'v1'
                }
            };

            https.get(apiUrl, options, (res) => {
                let data = '';
                res.on('data', (chunk) => data += chunk);
                res.on('end', () => {
                    try {
                        const response = JSON.parse(data);
                        if (response.results && response.results.length > 0) {
                            // 最適な画像を選択（いいね数重視）
                            const bestImage = response.results.sort((a, b) => b.likes - a.likes)[0];
                            resolve(bestImage);
                        } else {
                            reject(new Error('No images found'));
                        }
                    } catch (error) {
                        reject(error);
                    }
                });
            }).on('error', reject);
        });
    }

    /**
     * 画像をダウンロード
     * @param {string} imageUrl - 画像URL
     * @param {string} fileName - 保存ファイル名
     * @returns {Promise<string>} ローカル画像パス
     */
    async downloadImage(imageUrl, fileName) {
        const filePath = path.join(this.imageDir, fileName);
        
        return new Promise((resolve, reject) => {
            const file = fs.createWriteStream(filePath);
            
            https.get(imageUrl, (response) => {
                response.pipe(file);
                
                file.on('finish', () => {
                    file.close();
                    console.log(`✅ 画像ダウンロード完了: ${fileName}`);
                    resolve(filePath);
                });
                
                file.on('error', (error) => {
                    fs.unlink(filePath, () => {}); // 失敗時はファイル削除
                    reject(error);
                });
            }).on('error', reject);
        });
    }

    /**
     * 記事用の画像ファイル名生成
     * @param {Object} article - 記事オブジェクト
     * @returns {string} ファイル名
     */
    generateImageFileName(article) {
        const hash = crypto.createHash('md5').update(article.url).digest('hex').substring(0, 8);
        const date = article.date.replace(/-/g, '');
        return `${date}_${hash}.jpg`;
    }

    /**
     * 記事に自動で画像を設定
     * @param {Object} article - 記事オブジェクト
     * @returns {Promise<string>} 画像パス
     */
    async processArticleImage(article) {
        try {
            // 既に画像が設定されている場合はスキップ
            if (article.thumbnail && article.thumbnail !== null) {
                console.log(`⏭️ 画像設定済み: ${article.title}`);
                return article.thumbnail;
            }

            console.log(`🔍 画像検索開始: ${article.title}`);
            
            // キーワード抽出
            const keywords = this.extractKeywords(article);
            console.log(`🏷️ キーワード: ${keywords.join(', ')}`);
            
            // Unsplash画像検索
            const imageInfo = await this.searchUnsplashImage(keywords);
            
            // 最適化された画像URLを生成
            const optimizedUrl = `${imageInfo.urls.regular}?w=${this.imageSize.width}&h=${this.imageSize.height}&fit=crop&crop=smart&auto=format&q=${this.imageQuality}`;
            
            // ファイル名生成
            const fileName = this.generateImageFileName(article);
            
            // 画像ダウンロード
            await this.downloadImage(optimizedUrl, fileName);
            
            // 相対パス生成
            const relativePath = `/assets/images/blog-thumbnails/${fileName}`;
            
            console.log(`✅ 画像設定完了: ${article.title} → ${relativePath}`);
            return relativePath;
            
        } catch (error) {
            console.error(`❌ 画像取得エラー (${article.title}): ${error.message}`);
            // エラー時はデフォルト画像を使用
            return '/assets/images/default-blog-thumbnail.jpg';
        }
    }

    /**
     * articles.jsonを読み込み
     * @returns {Object} 記事データ
     */
    loadArticlesData() {
        try {
            const data = fs.readFileSync(this.articlesJsonPath, 'utf8');
            return JSON.parse(data);
        } catch (error) {
            console.error('❌ articles.json読み込みエラー:', error);
            return null;
        }
    }

    /**
     * articles.jsonを保存
     * @param {Object} articlesData - 記事データ
     */
    saveArticlesData(articlesData) {
        try {
            fs.writeFileSync(this.articlesJsonPath, JSON.stringify(articlesData, null, 2), 'utf8');
            console.log('✅ articles.json保存完了');
        } catch (error) {
            console.error('❌ articles.json保存エラー:', error);
        }
    }

    /**
     * 全記事の画像を一括処理
     * @returns {Promise<void>}
     */
    async processAllArticles() {
        console.log('🚀 全記事画像処理開始');
        
        const articlesData = this.loadArticlesData();
        if (!articlesData) return;
        
        let processedCount = 0;
        let skipCount = 0;
        
        // SEO記事処理
        if (articlesData.seoArticles) {
            for (const article of articlesData.seoArticles) {
                if (!article.thumbnail || article.thumbnail === null) {
                    article.thumbnail = await this.processArticleImage(article);
                    processedCount++;
                } else {
                    skipCount++;
                }
            }
        }
        
        // ブログ記事処理
        if (articlesData.blogArticles) {
            for (const article of articlesData.blogArticles) {
                if (!article.thumbnail || article.thumbnail === null) {
                    article.thumbnail = await this.processArticleImage(article);
                    processedCount++;
                } else {
                    skipCount++;
                }
            }
        }
        
        // 保存
        this.saveArticlesData(articlesData);
        
        console.log('🎉 全記事画像処理完了');
        console.log(`📊 処理済み: ${processedCount}件, スキップ: ${skipCount}件`);
    }

    /**
     * 特定記事の画像を処理
     * @param {string} articleUrl - 記事URL
     * @returns {Promise<string>} 画像パス
     */
    async processSpecificArticle(articleUrl) {
        const articlesData = this.loadArticlesData();
        if (!articlesData) return null;
        
        // 記事を検索
        let targetArticle = null;
        let articleType = null;
        
        if (articlesData.seoArticles) {
            targetArticle = articlesData.seoArticles.find(article => article.url === articleUrl);
            if (targetArticle) articleType = 'seoArticles';
        }
        
        if (!targetArticle && articlesData.blogArticles) {
            targetArticle = articlesData.blogArticles.find(article => article.url === articleUrl);
            if (targetArticle) articleType = 'blogArticles';
        }
        
        if (!targetArticle) {
            console.error('❌ 指定された記事が見つかりません:', articleUrl);
            return null;
        }
        
        // 画像処理
        const imagePath = await this.processArticleImage(targetArticle);
        targetArticle.thumbnail = imagePath;
        
        // 保存
        this.saveArticlesData(articlesData);
        
        return imagePath;
    }

    /**
     * 画像管理状況の確認
     * @returns {Object} 画像管理統計
     */
    getImageStats() {
        const articlesData = this.loadArticlesData();
        if (!articlesData) return null;
        
        let total = 0;
        let withImages = 0;
        let withLocalImages = 0;
        let withNullImages = 0;
        
        const processArticles = (articles) => {
            articles.forEach(article => {
                total++;
                if (article.thumbnail) {
                    withImages++;
                    if (article.thumbnail.startsWith('/assets/images/blog-thumbnails/')) {
                        withLocalImages++;
                    }
                } else {
                    withNullImages++;
                }
            });
        };
        
        if (articlesData.seoArticles) processArticles(articlesData.seoArticles);
        if (articlesData.blogArticles) processArticles(articlesData.blogArticles);
        
        return {
            total,
            withImages,
            withLocalImages,
            withNullImages,
            withExternalImages: withImages - withLocalImages
        };
    }
}

// CLI実行対応
if (require.main === module) {
    const manager = new PortfolioImageManager();
    
    const command = process.argv[2];
    
    switch (command) {
        case 'process-all':
            manager.processAllArticles();
            break;
        case 'process-article':
            const url = process.argv[3];
            if (!url) {
                console.error('❌ 記事URLを指定してください');
                process.exit(1);
            }
            manager.processSpecificArticle(url);
            break;
        case 'stats':
            const stats = manager.getImageStats();
            console.log('📊 画像管理統計:');
            console.log(`   総記事数: ${stats.total}`);
            console.log(`   画像設定済み: ${stats.withImages}`);
            console.log(`   ローカル画像: ${stats.withLocalImages}`);
            console.log(`   外部画像: ${stats.withExternalImages}`);
            console.log(`   画像未設定: ${stats.withNullImages}`);
            break;
        default:
            console.log('使用方法:');
            console.log('  node portfolio_image_manager.js process-all    # 全記事処理');
            console.log('  node portfolio_image_manager.js process-article [URL] # 特定記事処理');
            console.log('  node portfolio_image_manager.js stats         # 統計情報表示');
    }
}

module.exports = PortfolioImageManager;