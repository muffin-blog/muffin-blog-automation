// ===== DOM要素の取得 =====
const elements = {
    profileName: document.querySelector('.profile-text h3'),
    profileBio: document.querySelector('.profile-text p'),
    profileImg: document.getElementById('profile-img'),
    socialLinksContainer: document.createElement('div'),
    servicesContainer: document.getElementById('services-container'),
    seoArticlesContainer: document.querySelector('.seo-articles-container'),
    blogArticlesContainer: document.querySelector('.blog-articles-container'),
    faqContainer: document.querySelector('.faq-container'),
    contactContainer: document.querySelector('.contact-container'),
    header: document.querySelector('header')
};

// ===== データ格納用変数 =====
let profileData = null;
let seoArticles = null;
let blogArticles = null;
let allTags = new Set();

// ===== セキュリティ変数 =====
let honeypotTriggered = false;
let lastSubmissionTime = 0;
const MIN_FORM_TIME = 3000; // 最低3秒はフォーム表示が必要
let formDisplayTime = Date.now();

// ===== 初期化 =====
document.addEventListener('DOMContentLoaded', function() {
    initializeWebsite();
    addScrollEffects();
    addSmoothScrolling();
});

// ===== メイン初期化関数 =====
async function initializeWebsite() {
    try {
        showLoading();
        
        // 記事データをJSONから読み込み
        await loadArticlesData();
        
        // JSONデータを直接使用（ローカルファイルアクセス問題を回避）
        profileData = {
            "name": "マフィン",
            "title": "AI×SEO Writer",
            "subtitle": "Content Creator",
            "bio": "読者一人ひとりの未来を豊かにする、価値あるコンテンツ作りを追求しています。適応障害をきっかけに副業から始めたライティングを本格展開。現在はAIツールを駆使した効率的な記事制作で、クライアントの成果向上と読者の課題解決を両立。執筆からディレクションまで、幅広くサポートいたします。",
            "achievements": [
                {
                    "number": "100+",
                    "label": "執筆記事数",
                    "description": "様々なジャンルで高品質な記事を執筆"
                },
                {
                    "number": "50+",  
                    "label": "満足クライアント",
                    "description": "継続的な関係を築く信頼のパートナー"
                },
                {
                    "number": "3年+",
                    "label": "業界経験", 
                    "description": "SEO・コンテンツマーケティング分野"
                }
            ],
            "services": [
                {
                    "title": "SEO記事執筆",
                    "description": "検索エンジンに最適化された高品質な記事を作成",
                    "icon": "🎯"
                },
                {
                    "title": "AIツール活用", 
                    "description": "最新のAIツールを駆使した効率的なコンテンツ制作",
                    "icon": "🤖"
                },
                {
                    "title": "ブログ運営支援",
                    "description": "継続的なブログ運営とコンテンツ戦略の提案", 
                    "icon": "📈"
                },
                {
                    "title": "ディレクション",
                    "description": "コンテンツ制作チームの統括と品質管理",
                    "icon": "💡"
                }
            ],
            "socialLinks": [
                {
                    "platform": "X",
                    "url": "https://twitter.com/niconico2020_",
                    "icon": "𝕏"
                },
                {
                    "platform": "WordPress",
                    "url": "https://muffin-blog.com/",
                    "icon": "💻"
                },
                {
                    "platform": "Note",
                    "url": "https://note.com/muffin_writer",
                    "icon": "📝"
                },
                {
                    "platform": "Instagram", 
                    "url": "https://instagram.com/muffin_writer",
                    "icon": "📷"
                }
            ],
            "skills": [
                {
                    "name": "SEOライティング",
                    "level": 95,
                    "category": "ライティング"
                },
                {
                    "name": "AIツール活用",
                    "level": 90,
                    "category": "テクノロジー"
                },
                {
                    "name": "ブログ制作",
                    "level": 85,
                    "category": "Webサイト"
                },
                {
                    "name": "コンテンツマーケティング",
                    "level": 88,
                    "category": "マーケティング"
                },
                {
                    "name": "Webサイト分析",
                    "level": 82,
                    "category": "アナリティクス"
                },
                {
                    "name": "WordPress",
                    "level": 80,
                    "category": "CMS"
                }
            ]
        };

        // SEO記事（外部サイト向け執筆）とブログ記事（自分のブログ）に分類
        let seoArticlesRaw = [
            {
                "title": "UQモバイルは海外でも使える！利用方法や料金について徹底解説",
                "url": "https://my-best.com/articles/550",
                "description": "モバイル・通信サービス記事",
                "metaDescription": "UQモバイルを海外で使う方法を詳しく解説。国際ローミング料金、設定方法、注意点まで格安SIMユーザー必見の完全ガイドです。",
                "date": "2024-07-15",
                "tags": ["UQモバイル", "海外利用", "国際ローミング", "格安SIM", "通信"],
                "client": "my-best.com",
                "thumbnail": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=300&h=200&fit=crop&auto=format"
            },
            {
                "title": "夏の睡眠適温は26°C！朝までぐっすり眠れる快眠テクニック",
                "url": "https://minerva-sleep.jp/blogs/worries/20250829",
                "description": "夏の快適な睡眠環境を作るための実践的なアドバイス。室温26-27℃、湿度50-60%の重要性とエアコンの効果的な使用方法を解説",
                "metaDescription": "夏の夜も快適に眠るための室温・湿度管理法を専門家が解説。エアコン設定のコツや寝具選びまで、暑い夜の睡眠改善テクニックをご紹介。",
                "date": "2025-07-31",
                "tags": ["夏", "睡眠", "快眠", "エアコン", "室温", "健康"],
                "client": "Minerva Sleep",
                "thumbnail": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=300&h=200&fit=crop&auto=format"
            },
            {
                "title": "朝までぐっすり！失敗しない枕の選び方完全ガイド【首・肩こり解消】",
                "url": "https://minerva-sleep.jp/blogs/pillow/20250729",
                "description": "首・肩こり解消のための枕選びの完全ガイド。高さ・サイズ・素材・形状・硬さの5つのポイントを詳しく解説",
                "metaDescription": "首・肩こりに悩む方必見！枕の正しい選び方を5つのポイントで解説。高さ調整のコツから素材別の特徴まで、快眠のための完全ガイド。",
                "date": "2025-07-29",
                "tags": ["枕", "睡眠", "首こり", "肩こり", "寝具", "健康"],
                "client": "Minerva Sleep",
                "thumbnail": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=300&h=200&fit=crop&auto=format"
            },
            {
                "title": "失敗しないマットレスの選び方｜体型・悩み別に解説",
                "url": "https://minerva-sleep.jp/blogs/mattress/20250726",
                "description": "Minerva Sleepコラム記事",
                "metaDescription": "あなたの体型と睡眠の悩みに最適なマットレスの選び方を専門家が解説。硬さ・素材・サイズの選択基準から、腰痛・肩こり対策まで詳しくご紹介。",
                "date": "2025-07-26",
                "tags": ["マットレス", "睡眠", "健康", "寝具", "体型別"],
                "client": "Minerva Sleep",
                "thumbnail": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=300&h=200&fit=crop&auto=format"
            },
            {
                "title": "ダイエット中の停滞期を抜ける前兆サインと早く終わらせる7つのコツ",
                "url": "https://baumclinic.jp/column/stagnationperiod-getout/",
                "description": "ダイエット・美容コラム記事",
                "metaDescription": "ダイエット停滞期の前兆サインを見逃さず、効果的に抜け出す7つの方法を医師が解説。体重が減らない理由と対策で理想の体型を目指しましょう。",
                "date": "2024-07-01",
                "tags": ["ダイエット", "停滞期", "健康", "美容", "体重管理"],
                "client": "バウムクリニック",
                "thumbnail": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=300&h=200&fit=crop&auto=format"
            },
            {
                "title": "正しい食事制限で健康的なダイエット！リバウンドを防ぐ食事法",
                "url": "https://baumclinic.jp/column/diet-dietaryrestrictions/",
                "description": "ダイエット・美容コラム記事",
                "metaDescription": "リバウンドしない健康的なダイエットのための正しい食事制限方法を管理栄養士が解説。極端な食事制限を禁物にし、継続可能な食事法で理想の体型へ。",
                "date": "2024-06-15",
                "tags": ["ダイエット", "食事制限", "健康", "美容", "リバウンド防止", "栄養"],
                "client": "バウムクリニック",
                "thumbnail": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=300&h=200&fit=crop&auto=format"
            },
            {
                "title": "ちょっと食べただけですぐ太るあなたに役立つ７つの理由と４つの対策",
                "url": "https://baumclinic.jp/column/gain-weight-quickly/",
                "description": "ダイエット・美容コラム記事",
                "metaDescription": "少し食べただけですぐ体重が増えてしまう原因7つと対策方法を医師が詳しく解説。代謝改善から食事のタイミングまで、太りやすい体質改善の秘訣。",
                "date": "2024-06-02",
                "tags": ["ダイエット", "体重管理", "健康", "美容", "代謝", "食事"],
                "client": "バウムクリニック",
                "thumbnail": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=200&fit=crop&auto=format"
            },
            {
                "title": "空腹のピークを過ぎると食欲がおさまるメカニズムと体への７つの影響",
                "url": "https://baumclinic.jp/column/hunger-toopeak/",
                "description": "ダイエット・美容コラム記事",
                "metaDescription": "空腹のピークを過ぎると食欲がおさまるメカニズムと、体に与える7つの影響を医学的観点から解説。空腹時の正しい対処法と健康への影響を理解しましょう。",
                "date": "2024-05-20",
                "tags": ["ダイエット", "空腹", "食欲", "健康"],
                "client": "バウムクリニック",
                "thumbnail": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=300&h=200&fit=crop&auto=format"
            }
        ];

        // 記事データがJSONから読み込み済みの場合のみレンダリング
        renderProfile();
        renderServices();
        renderSeoArticles();
        if (blogArticles && blogArticles.length > 0) {
            renderBlogArticles();
        } else {
            console.error('blogArticlesが読み込まれていません');
            // フォールバック処理
            setTimeout(() => {
                if (blogArticles && blogArticles.length > 0) {
                    renderBlogArticles();
                }
            }, 1000);
        }
        renderFAQ();
        renderContact();
        hideLoading();
        
        console.log('✅ ポートフォリオサイトの初期化完了');
    } catch (error) {
        console.error('初期化エラー:', error);
        showError('データの読み込みに失敗しました');
    }
}

// ===== データ読み込み関数 =====
async function loadProfileData() {
    try {
        const response = await fetch('./content/profile.json');
        if (!response.ok) throw new Error('プロフィールデータの読み込みに失敗');
        profileData = await response.json();
    } catch (error) {
        console.error('プロフィールデータエラー:', error);
        throw error;
    }
}

async function loadArticlesData() {
    try {
        console.log('🚀 記事データ読み込み開始');
        let response;
        
        // 複数のパスを試行
        const paths = ['/content/articles/articles.json', './content/articles/articles.json', 'content/articles/articles.json'];
        
        for (const path of paths) {
            try {
                console.log(`📡 試行中: ${path}`);
                response = await fetch(path);
                if (response.ok) {
                    console.log(`✅ 成功: ${path} (${response.status})`);
                    break;
                }
            } catch (e) {
                console.log(`❌ 失敗: ${path} - ${e.message}`);
                continue;
            }
        }
        
        if (!response || !response.ok) {
            throw new Error('全てのパスで記事データ読み込みに失敗');
        }
        
        const data = await response.json();
        console.log('📄 JSON読み込み完了:', data);
        
        // 新しいデータ構造に対応
        seoArticles = data.seoArticles || [];
        blogArticles = data.blogArticles || [];
        console.log('📝 記事データ設定:', {
            seoArticles: seoArticles.length,
            blogArticles: blogArticles.length,
            firstBlogArticle: blogArticles[0]?.title
        });
        
        // 後方互換性のため
        featuredArticles = data.featured || [];
        articlesData = [...seoArticles, ...blogArticles].sort((a, b) => new Date(b.date) - new Date(a.date));
        
        // 全記事からタグを収集
        [...seoArticles, ...blogArticles].forEach(article => {
            if (article.tags) {
                article.tags.forEach(tag => allTags.add(tag));
            }
        });
        
        console.log('✅ 記事データ読み込み成功:', {
            seoArticles: seoArticles.length,
            blogArticles: blogArticles.length,
            totalTags: allTags.size
        });
    } catch (error) {
        console.error('❌ 記事データエラー:', error);
        throw error;
    }
}


// ===== プロフィール表示関数 =====
function renderProfile() {
    if (!profileData) return;
    
    // 名前とタイトルの更新
    if (elements.profileName) {
        elements.profileName.textContent = profileData.name;
    }
    
    // タイトルとサブタイトルの追加
    const profileTitle = document.createElement('div');
    profileTitle.className = 'profile-title';
    profileTitle.textContent = profileData.title;
    elements.profileName.parentNode.insertBefore(profileTitle, elements.profileName.nextSibling);
    
    if (profileData.subtitle) {
        const profileSubtitle = document.createElement('div');
        profileSubtitle.className = 'profile-subtitle';
        profileSubtitle.textContent = profileData.subtitle;
        profileTitle.parentNode.insertBefore(profileSubtitle, profileTitle.nextSibling);
    }
    
    // 自己紹介の更新
    if (elements.profileBio) {
        elements.profileBio.textContent = profileData.bio;
    }
    
    // プロフィール画像の更新
    if (elements.profileImg && profileData.profileImage) {
        elements.profileImg.src = profileData.profileImage;
        elements.profileImg.alt = `${profileData.name}のプロフィール画像`;
    }
    
    // SNSリンクの追加
    renderSocialLinks();
}

// ===== SNSリンク表示函数 =====
function renderSocialLinks() {
    if (!profileData.socialLinks) return;
    
    elements.socialLinksContainer.className = 'social-links';
    
    profileData.socialLinks.forEach(link => {
        const socialLink = document.createElement('a');
        socialLink.href = link.url;
        socialLink.target = '_blank';
        socialLink.rel = 'noopener noreferrer';
        socialLink.className = 'social-link';
        socialLink.innerHTML = `
            <span>${link.icon || '🔗'}</span>
            ${link.platform}
        `;
        
        elements.socialLinksContainer.appendChild(socialLink);
    });
    
    elements.profileBio.parentNode.appendChild(elements.socialLinksContainer);
}


// ===== サービス表示関数 =====
function renderServices() {
    if (!profileData?.services) return;
    
    elements.servicesContainer.innerHTML = '';
    
    profileData.services.forEach((service, index) => {
        const serviceCard = document.createElement('div');
        serviceCard.className = 'service-card';
        serviceCard.style.animationDelay = `${index * 0.15}s`;
        
        serviceCard.innerHTML = `
            <div class="service-icon">${service.icon}</div>
            <h3>${service.title}</h3>
            <p>${service.description}</p>
        `;
        
        elements.servicesContainer.appendChild(serviceCard);
    });
}

// ===== SEO記事表示関数 =====
function renderSeoArticles() {
    if (!seoArticles?.length) return;
    
    elements.seoArticlesContainer.innerHTML = '';
    
    // 初期表示は3記事のみ
    const initialArticles = seoArticles.slice(0, 3);
    const remainingArticles = seoArticles.slice(3);
    
    initialArticles.forEach((article, index) => {
        const articleCard = createSeoArticleCard(article, index);
        elements.seoArticlesContainer.appendChild(articleCard);
    });
    
    // 残りの記事がある場合はMoreボタンを追加
    if (remainingArticles.length > 0) {
        const moreButton = createMoreButton('seo', remainingArticles);
        elements.seoArticlesContainer.appendChild(moreButton);
    }
}

// ===== ブログ記事表示関数 =====
function renderBlogArticles() {
    console.log('🎨 renderBlogArticles開始', {
        blogArticles: blogArticles?.length || 0,
        container: elements.blogArticlesContainer
    });
    
    if (!blogArticles?.length) {
        console.warn('⚠️ blogArticlesが空または未定義');
        return;
    }
    
    elements.blogArticlesContainer.innerHTML = '';
    
    // 初期表示は3記事のみ
    const initialArticles = blogArticles.slice(0, 3);
    const remainingArticles = blogArticles.slice(3);
    
    initialArticles.forEach((article, index) => {
        const articleCard = createBlogArticleCard(article, index);
        elements.blogArticlesContainer.appendChild(articleCard);
    });
    
    // 残りの記事がある場合はMoreボタンを追加
    if (remainingArticles.length > 0) {
        const moreButton = createMoreButton('blog', remainingArticles);
        elements.blogArticlesContainer.appendChild(moreButton);
    }
}

// ===== SEO記事カード作成関数 =====
function createSeoArticleCard(article, index) {
    const card = document.createElement('article');
    card.className = 'article-card';
    card.style.animationDelay = `${index * 0.1}s`;
    
    const formattedDate = formatDate(article.date);
    
    card.innerHTML = `
        <div class="article-thumbnail">
            <img src="${article.thumbnail || './assets/images/default-blog-thumbnail.jpg'}" alt="${article.title}" loading="lazy">
        </div>
        <div class="article-content">
            <h3>${article.title}</h3>
            <div class="article-meta">
                <span class="article-date">${formattedDate}</span>
            </div>
            ${article.metaDescription ? `<p class="article-meta-description">${article.metaDescription}</p>` : `<p>${article.description}</p>`}
            <div class="article-tags">
                ${article.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
            </div>
            <a href="${article.url}" target="_blank" rel="noopener noreferrer" class="read-more">
                記事を読む
            </a>
        </div>
    `;
    
    return card;
}

// ===== ブログ記事カード作成関数 =====
function createBlogArticleCard(article, index) {
    const card = document.createElement('article');
    card.className = 'article-card';
    card.style.animationDelay = `${index * 0.1}s`;
    
    const formattedDate = formatDate(article.date);
    
    card.innerHTML = `
        <div class="article-thumbnail">
            <img src="${article.thumbnail || './assets/images/default-blog-thumbnail.jpg'}" alt="${article.title}" loading="lazy">
        </div>
        <div class="article-content">
            <h3>${article.title}</h3>
            <div class="article-meta">
                <span class="article-date">${formattedDate}</span>
            </div>
            ${article.metaDescription ? `<p class="article-meta-description">${article.metaDescription}</p>` : `<p>${article.description}</p>`}
            <div class="article-tags">
                ${article.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
            </div>
            <a href="${article.url}" target="_blank" rel="noopener noreferrer" class="read-more">
                記事を読む
            </a>
        </div>
    `;
    
    return card;
}

// ===== Moreボタン作成関数 =====
function createMoreButton(type, remainingArticles) {
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'more-button-container';
    buttonContainer.style.cssText = `
        grid-column: 1 / -1;
        text-align: center;
        margin-top: var(--spacing-lg);
    `;
    
    const moreButton = document.createElement('button');
    moreButton.className = 'more-button';
    moreButton.textContent = `More (${remainingArticles.length})`;
    moreButton.style.cssText = `
        background: var(--primary-color);
        color: var(--bg-primary);
        border: none;
        padding: 12px 24px;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    `;
    
    moreButton.addEventListener('mouseover', () => {
        moreButton.style.background = 'var(--secondary-color)';
        moreButton.style.transform = 'translateY(-2px)';
        moreButton.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.2)';
    });
    
    moreButton.addEventListener('mouseout', () => {
        moreButton.style.background = 'var(--primary-color)';
        moreButton.style.transform = 'translateY(0)';
        moreButton.style.boxShadow = 'none';
    });
    
    moreButton.addEventListener('click', () => {
        expandArticles(type, remainingArticles, buttonContainer);
    });
    
    buttonContainer.appendChild(moreButton);
    return buttonContainer;
}

// ===== 記事展開関数 =====
function expandArticles(type, remainingArticles, buttonContainer) {
    const container = type === 'seo' ? elements.seoArticlesContainer : elements.blogArticlesContainer;
    const createCard = type === 'seo' ? createSeoArticleCard : createBlogArticleCard;
    
    // Moreボタンを削除
    buttonContainer.remove();
    
    // 残りの記事を追加（IDを設定して後で削除できるようにする）
    const expandedArticles = [];
    remainingArticles.forEach((article, index) => {
        const articleCard = createCard(article, index + 3); // インデックスを調整
        articleCard.classList.add('expanded-article'); // 展開された記事にクラスを追加
        container.appendChild(articleCard);
        expandedArticles.push(articleCard);
    });
    
    // Lessボタンを追加
    const lessButton = createLessButton(type, remainingArticles, expandedArticles);
    container.appendChild(lessButton);
}

// ===== Lessボタン作成関数 =====
function createLessButton(type, remainingArticles, expandedArticles) {
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'less-button-container';
    buttonContainer.style.cssText = `
        grid-column: 1 / -1;
        text-align: center;
        margin-top: var(--spacing-lg);
    `;
    
    const lessButton = document.createElement('button');
    lessButton.className = 'less-button';
    lessButton.textContent = 'Less';
    lessButton.style.cssText = `
        background: var(--secondary-color);
        color: var(--bg-primary);
        border: none;
        padding: 12px 24px;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    `;
    
    lessButton.addEventListener('mouseover', () => {
        lessButton.style.background = 'var(--text-light)';
        lessButton.style.transform = 'translateY(-2px)';
        lessButton.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.2)';
    });
    
    lessButton.addEventListener('mouseout', () => {
        lessButton.style.background = 'var(--secondary-color)';
        lessButton.style.transform = 'translateY(0)';
        lessButton.style.boxShadow = 'none';
    });
    
    lessButton.addEventListener('click', () => {
        collapseArticles(type, remainingArticles, expandedArticles, buttonContainer);
    });
    
    buttonContainer.appendChild(lessButton);
    return buttonContainer;
}

// ===== 記事折りたたみ関数 =====
function collapseArticles(type, remainingArticles, expandedArticles, lessButtonContainer) {
    const container = type === 'seo' ? elements.seoArticlesContainer : elements.blogArticlesContainer;
    
    // 展開された記事を削除
    expandedArticles.forEach(article => {
        article.remove();
    });
    
    // Lessボタンを削除
    lessButtonContainer.remove();
    
    // Moreボタンを再追加
    const moreButton = createMoreButton(type, remainingArticles);
    container.appendChild(moreButton);
}

// ===== FAQ表示関数 =====
function renderFAQ() {
    const faqData = [
        {
            question: "記事執筆の料金はどのくらいですか？",
            answer: "【初回お試し価格】初めてのお客様には文字単価1円でお受けいたします！通常価格はSEO記事3〜5円、専門性の高い記事5〜8円程度です。まずはお気軽にお試しください。"
        },
        {
            question: "納期はどのくらいですか？",
            answer: "通常、3000〜5000文字の記事で1週間程度いただいております。お急ぎの場合はご相談ください。品質を保つため、無理な短納期はお受けできない場合があります。"
        },
        {
            question: "どのような分野の記事が得意ですか？",
            answer: "テクノロジー、マーケティング、ビジネス、健康・美容、金融など幅広い分野に対応しています。AIツールを活用した効率的な調査により、専門分野以外でも質の高い記事を執筆できます。"
        },
        {
            question: "修正対応はしていただけますか？",
            answer: "はい、初回納品後の軽微な修正は無料で対応いたします。大幅な内容変更や追加執筆が必要な場合は、別途ご相談させていただきます。"
        },
        {
            question: "SEO対策はどの程度まで対応できますか？",
            answer: "キーワード選定、タイトル・見出し最適化、内部リンク設計、メタディスクリプション作成など、基本的なSEO対策は全て対応可能です。より高度な技術的SEOについてもご相談ください。"
        },
        {
            question: "初回お試し価格について詳しく教えてください",
            answer: "新規のお客様限定で、最初の1記事を文字単価1円（通常3〜5円）でご提供いたします。文字数は2000〜5000文字程度、SEO対策も通常通り実施いたします。品質にご満足いただけましたら、継続してお仕事をお受けできれば幸いです。"
        }
    ];

    elements.faqContainer.innerHTML = '';
    
    faqData.forEach((faq, index) => {
        const faqItem = document.createElement('div');
        faqItem.className = 'faq-item';
        faqItem.innerHTML = `
            <div class="faq-question" onclick="toggleFAQ(${index})">
                <span>${faq.question}</span>
                <span class="faq-toggle">+</span>
            </div>
            <div class="faq-answer" id="faq-answer-${index}">
                ${faq.answer}
            </div>
        `;
        elements.faqContainer.appendChild(faqItem);
    });
}

// ===== FAQ開閉機能 =====
function toggleFAQ(index) {
    const answer = document.getElementById(`faq-answer-${index}`);
    const toggle = answer.previousElementSibling.querySelector('.faq-toggle');
    
    if (answer.classList.contains('active')) {
        answer.classList.remove('active');
        toggle.classList.remove('active');
        toggle.textContent = '+';
    } else {
        // 他のFAQを閉じる
        document.querySelectorAll('.faq-answer.active').forEach(openAnswer => {
            openAnswer.classList.remove('active');
            openAnswer.previousElementSibling.querySelector('.faq-toggle').classList.remove('active');
            openAnswer.previousElementSibling.querySelector('.faq-toggle').textContent = '+';
        });
        
        // 選択されたFAQを開く
        answer.classList.add('active');
        toggle.classList.add('active');
        toggle.textContent = '×';
    }
}

// ===== コンタクト表示関数 =====
function renderContact() {
    // フォーム表示時間をリセット
    formDisplayTime = Date.now();
    
    elements.contactContainer.innerHTML = `
        <div class="contact-intro">
            <p>お仕事のご依頼・お見積もりについては下記フォームよりお気軽にお問い合わせください。</p>
            <p>フォームが送信できない場合は直接メール（<a href="mailto:0527muffin1203@gmail.com">0527muffin1203@gmail.com</a>）でご連絡ください。</p>
        </div>
        
        <form class="contact-form" onsubmit="handleContactForm(event)">
            <!-- ハニーポット（スパム対策） -->
            <input type="text" id="website" name="website" style="display: none !important;" tabindex="-1" autocomplete="off">
            
            <div class="form-group">
                <label class="form-label" for="contact-type">お問い合わせ種別 *</label>
                <select id="contact-type" name="contactType" class="form-select" required>
                    <option value="">選択してください</option>
                    <option value="estimate">お見積もり</option>
                    <option value="consultation">ご相談</option>
                    <option value="other">その他</option>
                </select>
            </div>
            
            <div class="form-group">
                <label class="form-label" for="name">お名前 *</label>
                <input type="text" id="name" name="name" class="form-input" required>
            </div>
            
            <div class="form-group">
                <label class="form-label" for="company">会社名・屋号</label>
                <input type="text" id="company" name="company" class="form-input">
            </div>
            
            <div class="form-group">
                <label class="form-label" for="email">メールアドレス *</label>
                <input type="email" id="email" name="email" class="form-input" required>
            </div>
            
            <div class="form-group">
                <label class="form-label" for="phone">電話番号</label>
                <input type="tel" id="phone" name="phone" class="form-input">
            </div>
            
            <div class="form-group">
                <label class="form-label" for="budget">ご予算</label>
                <select id="budget" name="budget" class="form-select">
                    <option value="">選択してください</option>
                    <option value="~10000">〜1万円</option>
                    <option value="10000-30000">1万〜3万円</option>
                    <option value="30000-50000">3万〜5万円</option>
                    <option value="50000-100000">5万〜10万円</option>
                    <option value="100000~">10万円以上</option>
                    <option value="undecided">未定</option>
                </select>
            </div>
            
            <div class="form-group">
                <label class="form-label" for="timeline">希望納期</label>
                <select id="timeline" name="timeline" class="form-select">
                    <option value="">選択してください</option>
                    <option value="urgent">至急（数日以内）</option>
                    <option value="normal">通常（1週間程度）</option>
                    <option value="flexible">相談して決める</option>
                </select>
            </div>
            
            <div class="form-group">
                <label class="form-label" for="usage">記事の用途</label>
                <select id="usage" name="usage" class="form-select">
                    <option value="">選択してください</option>
                    <option value="website">自社サイト・ブログ</option>
                    <option value="media">メディア・プラットフォーム</option>
                    <option value="sns">SNS投稿</option>
                    <option value="other">その他</option>
                </select>
            </div>
            
            <div class="form-group">
                <label class="form-label" for="files">参考資料（任意）</label>
                <input type="file" id="files" name="files" class="form-file" multiple accept=".pdf,.doc,.docx,.txt,.jpg,.png">
                <small class="form-note">PDF, Word, テキスト, 画像ファイル対応（最大5MB）</small>
            </div>
            
            <div class="form-group">
                <label class="form-label" for="message">案件詳細 *</label>
                <textarea id="message" name="message" class="form-textarea" required placeholder="・記事のテーマや内容&#10;・想定文字数&#10;・ターゲット読者&#10;・参考サイトやキーワード&#10;・その他ご要望など詳しくお聞かせください"></textarea>
            </div>
            
            <div class="form-group form-checkbox">
                <label class="checkbox-label">
                    <input type="checkbox" id="privacy" name="privacy" required>
                    <span class="checkmark"></span>
                    <a href="#" class="privacy-link">プライバシーポリシー</a>に同意する *
                </label>
            </div>
            
            <button type="submit" class="form-submit">送信する</button>
        </form>
    `;
}

// ===== セキュリティチェック関数 =====
function checkHoneypot() {
    const honeypot = document.getElementById('website');
    if (honeypot && honeypot.value !== '') {
        honeypotTriggered = true;
        return false;
    }
    return true;
}

function checkRateLimit() {
    const now = Date.now();
    if (now - lastSubmissionTime < 60000) { // 1分以内の連続送信を防ぐ
        return false;
    }
    return true;
}

function checkFormTime() {
    const now = Date.now();
    return (now - formDisplayTime) >= MIN_FORM_TIME;
}

// ===== コンタクトフォーム送信処理 =====
function handleContactForm(event) {
    event.preventDefault();
    
    // セキュリティチェック
    if (!checkHoneypot()) {
        console.log('スパム検出: ハニーポット');
        return;
    }
    
    if (!checkRateLimit()) {
        alert('送信間隔が短すぎます。1分以上お待ちください。');
        return;
    }
    
    if (!checkFormTime()) {
        alert('入力時間が短すぎます。もう一度お試しください。');
        return;
    }
    
    const formData = new FormData(event.target);
    const contactType = formData.get('contactType');
    const name = formData.get('name');
    const company = formData.get('company');
    const email = formData.get('email');
    const phone = formData.get('phone');
    const budget = formData.get('budget');
    const timeline = formData.get('timeline');
    const usage = formData.get('usage');
    const message = formData.get('message');
    
    // 必須項目の検証
    if (!name || !email || !contactType || !message) {
        alert('必須項目をすべて入力してください。');
        return;
    }
    
    // メール形式の簡単な検証
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert('正しいメールアドレスを入力してください。');
        return;
    }
    
    // メール本文を構築
    let emailBody = `【お問い合わせ種別】${contactType}\n\n`;
    emailBody += `【お名前】${name}\n`;
    if (company) emailBody += `【会社名・屋号】${company}\n`;
    emailBody += `【メールアドレス】${email}\n`;
    if (phone) emailBody += `【電話番号】${phone}\n`;
    if (budget) emailBody += `【ご予算】${budget}\n`;
    if (timeline) emailBody += `【希望納期】${timeline}\n`;
    if (usage) emailBody += `【記事の用途】${usage}\n`;
    emailBody += `\n【案件詳細】\n${message}`;
    
    const subject = `【ポートフォリオサイト】${contactType} - ${name}様`;
    
    // 送信時間を記録
    lastSubmissionTime = Date.now();
    
    // メール送信処理
    const mailtoLink = `mailto:0527muffin1203@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(emailBody)}`;
    window.location.href = mailtoLink;
    
    // フォームリセット
    event.target.reset();
    alert('メールクライアントが開きます。送信をお願いいたします。');
}

// パーティクルエフェクトは削除（シンプルなデザインのため）

// ===== ユーティリティ関数 =====
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ja-JP', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function showLoading() {
    // SEO記事とブログ記事の両方にローディング表示
    if (elements.seoArticlesContainer) {
        elements.seoArticlesContainer.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>SEO記事を読み込み中...</p>
            </div>
        `;
    }
    if (elements.blogArticlesContainer) {
        elements.blogArticlesContainer.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>ブログ記事を読み込み中...</p>
            </div>
        `;
    }
}

function hideLoading() {
    const loading = document.querySelector('.loading');
    if (loading) {
        loading.remove();
    }
}

function showError(message) {
    const errorHtml = `
        <div style="text-align: center; color: var(--secondary-color); grid-column: 1 / -1; padding: 4rem;">
            <h3 style="color: var(--secondary-color); margin-bottom: 1rem;">エラーが発生しました</h3>
            <p>${message}</p>
            <button onclick="location.reload()" style="
                margin-top: 2rem; 
                padding: 1rem 2rem; 
                background: var(--gradient-primary); 
                color: var(--bg-primary);
                border: none;
                border-radius: var(--border-radius);
                cursor: pointer;
                font-weight: 600;
            ">再読み込み</button>
        </div>
    `;
    
    if (elements.seoArticlesContainer) {
        elements.seoArticlesContainer.innerHTML = errorHtml;
    }
    if (elements.blogArticlesContainer) {
        elements.blogArticlesContainer.innerHTML = errorHtml;
    }
}

// ===== スクロール効果 =====
function addScrollEffects() {
    let ticking = false;
    
    function updateHeader() {
        const scrolled = window.scrollY > 20;
        elements.header.classList.toggle('scrolled', scrolled);
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            ticking = true;
            requestAnimationFrame(updateHeader);
        }
    }
    
    window.addEventListener('scroll', requestTick);
    
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                
                // スキルバーのアニメーション
                const skillBars = entry.target.querySelectorAll('.skill-progress');
                skillBars.forEach(bar => {
                    bar.style.animation = 'skillLoad 2s ease-out forwards';
                });
                
                // カウントアップアニメーション
                const statNumbers = entry.target.querySelectorAll('.stat-number');
                statNumbers.forEach(number => {
                    animateCounter(number);
                });
            }
        });
    }, observerOptions);
    
    // セクションの監視を開始
    setTimeout(() => {
        document.querySelectorAll('section, .stats, .skill-item, .service-card').forEach(element => {
            observer.observe(element);
        });
    }, 100);
}

// ===== カウンターアニメーション =====
function animateCounter(element) {
    const target = element.textContent;
    const number = parseInt(target.replace(/[^\d]/g, ''));
    
    if (isNaN(number)) return;
    
    let current = 0;
    const increment = number / 60; // 60フレームで完了
    const suffix = target.replace(/[\d]/g, '');
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= number) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current) + suffix;
        }
    }, 16);
}

// ===== スムーズスクロール =====
function addSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                const headerHeight = elements.header.offsetHeight;
                const targetPosition = target.offsetTop - headerHeight - 30;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// マウス追従エフェクトは削除（シンプルなデザインのため）

// ===== キーボードショートカット =====
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
            case '1':
                e.preventDefault();
                document.querySelector('#profile').scrollIntoView({ behavior: 'smooth' });
                break;
            case '2':
                e.preventDefault();
                document.querySelector('#seo-articles').scrollIntoView({ behavior: 'smooth' });
                break;
            case '3':
                e.preventDefault();
                document.querySelector('#blog-articles').scrollIntoView({ behavior: 'smooth' });
                break;
            case '4':
                e.preventDefault();
                document.querySelector('#faq').scrollIntoView({ behavior: 'smooth' });
                break;
            case '5':
                e.preventDefault();
                document.querySelector('#contact').scrollIntoView({ behavior: 'smooth' });
                break;
        }
    }
});

// ===== パフォーマンス最適化 =====
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ===== エラーハンドリング =====
window.addEventListener('error', function(event) {
    console.error('🚨 JavaScript エラー:', event.error);
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('🚨 Promise エラー:', event.reason);
    event.preventDefault();
});

// ===== 開発用デバッグ関数 =====
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    window.portfolioDebug = {
        profileData: () => profileData,
        seoArticles: () => seoArticles,
        blogArticles: () => blogArticles,
        allTags: () => Array.from(allTags),
        reloadData: initializeWebsite,
        version: '3.0 - SEO & Blog Separated Edition'
    };
    
    console.log('✨ Portfolio Debug Mode Activated');
    console.log('Use window.portfolioDebug to access debug functions');
}