// ===== シンプル版 JavaScript - 確実に動作させる =====

console.log('🚀 JavaScript読み込み開始');

// ===== データ =====
const seoArticles = [
    {
        "title": "夏の睡眠適温は26°C！朝までぐっすり眠れる快眠テクニック",
        "url": "https://minerva-sleep.jp/blogs/worries/20250829",
        "description": "夏の夜、暑さで寝苦しくて夜中に何度も目が覚めてしまう方向けの快眠テクニック。",
        "date": "2025-07-31",
        "tags": ["睡眠", "快眠", "エアコン", "夏"],
        "client": "Minerva Sleep",
        "thumbnail": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=300&h=200&fit=crop&auto=format"
    },
    {
        "title": "朝までぐっすり！失敗しない枕の選び方完全ガイド【首・肩こり解消】",
        "url": "https://minerva-sleep.jp/blogs/pillow/20250729",
        "description": "睡眠の専門家として、あなたの睡眠の悩みを解決し、朝までぐっすり眠れる理想の枕を見つけるための選び方を詳しく解説。",
        "date": "2025-07-29",
        "tags": ["睡眠・健康", "睡眠", "こり", "寝具"],
        "client": "Minerva Sleep",
        "thumbnail": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=300&h=200&fit=crop&auto=format"
    }
];

const blogArticles = [
    {
        "title": "Audible二刀流読書で集中力・読解力向上！効果と始め方",
        "url": "https://muffin-blog.com/audible-concentration-reading-improvement/",
        "description": "Audible二刀流読書で集中力・読解力が科学的に向上！音声と文字を同時活用する効果的な読書法の実践方法とコツを詳しく解説。",
        "date": "2025-08-16",
        "tags": ["ブログ", "オーディオブック", "オーディブル", "読書効果", "集中力向上"],
        "client": "Muffin Blog",
        "thumbnail": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&h=200&fit=crop&auto=format"
    },
    {
        "title": "【オーディオブック】単品購入ならaudiobook.jpがお得？比較とセールまとめ",
        "url": "https://muffin-blog.com/audiobook-jp-tanpin-guide/",
        "description": "audiobook.jp単品購入が最安値！2025年8月開催中の50%OFFセール情報とAudibleとの価格比較。",
        "date": "2025-08-11",
        "tags": ["ブログ", "オーディオブック", "放題", "セール"],
        "client": "Muffin Blog",
        "thumbnail": "./assets/images/default-blog-thumbnail.jpg"
    },
    {
        "title": "本が読めない悩み解決！Audibleで始める聴く読書の魅力とは",
        "url": "https://muffin-blog.com/audible-reading-dislike-solution/",
        "description": "本が読めない、続かない悩みを解決！Audible（オーディブル）なら耳で聞く読書で挫折知らず。",
        "date": "2025-08-10",
        "tags": ["ブログ", "読書苦手", "オーディオブック", "オーディブル"],
        "client": "Muffin Blog",
        "thumbnail": "./assets/images/default-blog-thumbnail.jpg"
    }
];

const profileData = {
    "name": "マフィン",
    "title": "AI×SEO Writer",
    "subtitle": "Content Creator",
    "bio": "読者一人ひとりの未来を豊かにする、価値あるコンテンツ作りを追求しています。適応障害をきっかけに副業から始めたライティングを本格展開。現在はAIツールを駆使した効率的な記事制作で、クライアントの成果向上と読者の課題解決を両立。執筆からディレクションまで、幅広くサポートいたします。",
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
    ]
};

// ===== 初期化 =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOMContentLoaded発火');
    
    try {
        hideLoading();
        renderProfile();
        renderServices();
        renderSeoArticles();
        renderBlogArticles();
        renderFAQ();
        renderContact();
        console.log('✅ 全ての描画完了');
    } catch (error) {
        console.error('❌ エラー:', error);
    }
});

// ===== 描画関数 =====
function hideLoading() {
    const loadings = document.querySelectorAll('.loading');
    loadings.forEach(loading => loading.remove());
}

function renderProfile() {
    const nameElement = document.querySelector('.profile-text h3');
    const bioElement = document.querySelector('.profile-text p');
    
    if (nameElement) nameElement.textContent = profileData.name;
    if (bioElement) bioElement.textContent = profileData.bio;
    
    console.log('✅ プロフィール描画完了');
}

function renderServices() {
    const container = document.getElementById('services-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    profileData.services.forEach((service, index) => {
        const serviceCard = document.createElement('div');
        serviceCard.className = 'service-card';
        serviceCard.innerHTML = `
            <div class="service-icon">${service.icon}</div>
            <h3>${service.title}</h3>
            <p>${service.description}</p>
        `;
        container.appendChild(serviceCard);
    });
    
    console.log('✅ サービス描画完了');
}

function renderSeoArticles() {
    const container = document.querySelector('.seo-articles-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    seoArticles.slice(0, 3).forEach(article => {
        const card = createArticleCard(article);
        container.appendChild(card);
    });
    
    console.log('✅ SEO記事描画完了');
}

function renderBlogArticles() {
    const container = document.querySelector('.blog-articles-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    blogArticles.slice(0, 3).forEach(article => {
        const card = createArticleCard(article);
        container.appendChild(card);
    });
    
    console.log('✅ ブログ記事描画完了');
}

function createArticleCard(article) {
    const card = document.createElement('article');
    card.className = 'article-card';
    
    const formattedDate = new Date(article.date).toLocaleDateString('ja-JP');
    
    card.innerHTML = `
        <div class="article-thumbnail">
            <img src="${article.thumbnail}" alt="${article.title}" loading="lazy">
        </div>
        <div class="article-content">
            <h3>${article.title}</h3>
            <div class="article-meta">
                <span class="article-date">${formattedDate}</span>
            </div>
            <p class="article-description">${article.description}</p>
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

function renderFAQ() {
    const container = document.querySelector('.faq-container');
    if (!container) return;
    
    const faqData = [
        {
            question: "記事執筆の料金はどのくらいですか？",
            answer: "【初回お試し価格】初めてのお客様には文字単価1円でお受けいたします！通常価格はSEO記事3〜5円、専門性の高い記事5〜8円程度です。"
        },
        {
            question: "納期はどのくらいですか？",
            answer: "通常、3000〜5000文字の記事で1週間程度いただいております。お急ぎの場合はご相談ください。"
        },
        {
            question: "どのような分野の記事が得意ですか？",
            answer: "テクノロジー、マーケティング、ビジネス、健康・美容、金融など幅広い分野に対応しています。AIツールを活用した効率的な調査により、専門分野以外でも質の高い記事を執筆できます。"
        }
    ];
    
    container.innerHTML = '';
    
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
        container.appendChild(faqItem);
    });
    
    console.log('✅ FAQ描画完了');
}

function renderContact() {
    const container = document.querySelector('.contact-container');
    if (!container) return;
    
    container.innerHTML = `
        <div class="contact-intro">
            <p>お仕事のご依頼・お見積もりについては下記フォームよりお気軽にお問い合わせください。</p>
            <p>フォームが送信できない場合は直接メール（<a href="mailto:0527muffin1203@gmail.com">0527muffin1203@gmail.com</a>）でご連絡ください。</p>
        </div>
        
        <form class="contact-form" onsubmit="handleContactForm(event)">
            <div class="form-group">
                <label class="form-label" for="name">お名前 *</label>
                <input type="text" id="name" name="name" class="form-input" required>
            </div>
            
            <div class="form-group">
                <label class="form-label" for="email">メールアドレス *</label>
                <input type="email" id="email" name="email" class="form-input" required>
            </div>
            
            <div class="form-group">
                <label class="form-label" for="message">案件詳細 *</label>
                <textarea id="message" name="message" class="form-textarea" required placeholder="・記事のテーマや内容&#10;・想定文字数&#10;・ターゲット読者&#10;・その他ご要望など詳しくお聞かせください"></textarea>
            </div>
            
            <button type="submit" class="form-submit">送信する</button>
        </form>
    `;
    
    console.log('✅ コンタクト描画完了');
}

// ===== FAQ機能 =====
function toggleFAQ(index) {
    const answer = document.getElementById(`faq-answer-${index}`);
    const toggle = answer.previousElementSibling.querySelector('.faq-toggle');
    
    if (answer.classList.contains('active')) {
        answer.classList.remove('active');
        toggle.textContent = '+';
    } else {
        // 他のFAQを閉じる
        document.querySelectorAll('.faq-answer.active').forEach(openAnswer => {
            openAnswer.classList.remove('active');
            openAnswer.previousElementSibling.querySelector('.faq-toggle').textContent = '+';
        });
        
        answer.classList.add('active');
        toggle.textContent = '×';
    }
}

// ===== コンタクトフォーム =====
function handleContactForm(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const name = formData.get('name');
    const email = formData.get('email');
    const message = formData.get('message');
    
    if (!name || !email || !message) {
        alert('必須項目をすべて入力してください。');
        return;
    }
    
    const subject = `【ポートフォリオサイト】お問い合わせ - ${name}様`;
    const emailBody = `【お名前】${name}\n【メールアドレス】${email}\n\n【案件詳細】\n${message}`;
    
    const mailtoLink = `mailto:0527muffin1203@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(emailBody)}`;
    window.location.href = mailtoLink;
    
    event.target.reset();
    alert('メールクライアントが開きます。送信をお願いいたします。');
}

console.log('✅ JavaScript読み込み完了');