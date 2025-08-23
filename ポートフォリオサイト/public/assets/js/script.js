console.log('🚀 JavaScript読み込み開始');
console.log('🔍 デバッグ: スクリプト実行中');

// ===== データ管理 =====
let seoArticles = [];
let blogArticles = [];
let profileData = {};
let faqData = [];

async function loadAllData() {
    try {
        console.log('🔄 データ読み込み開始...');
        
        // 記事データ読み込み
        console.log('📚 articles.json読み込み中...');
        const articlesResponse = await fetch('./content/articles/articles.json');
        if (!articlesResponse.ok) {
            throw new Error(`Articles HTTP error! status: ${articlesResponse.status}`);
        }
        const articlesData = await articlesResponse.json();
        seoArticles = articlesData.seoArticles || [];
        blogArticles = articlesData.blogArticles || [];
        console.log('✅ 記事データ取得:', seoArticles.length, 'SEO,', blogArticles.length, 'Blog');
        
        // プロフィールデータ読み込み
        console.log('👤 profile.json読み込み中...');
        const profileResponse = await fetch('./content/profile.json');
        if (!profileResponse.ok) {
            throw new Error(`Profile HTTP error! status: ${profileResponse.status}`);
        }
        profileData = await profileResponse.json();
        console.log('✅ プロフィールデータ取得:', profileData.name);
        
        console.log('✅ 全データ読み込み完了:', {
            seoArticles: seoArticles.length,
            blogArticles: blogArticles.length,
            profile: profileData.name
        });
        
        return true;
    } catch (error) {
        console.error('❌ データ読み込みエラー:', error);
        return false;
    }
}

// profileDataは上でletで宣言済み、JSONから読み込む

// ===== 初期化 =====
document.addEventListener('DOMContentLoaded', async function() {
    console.log('🚀 DOMContentLoaded発火');
    
    try {
        console.log('📡 全データ読み込み開始');
        const dataLoaded = await loadAllData();
        console.log('📊 データ読み込み結果:', dataLoaded);
        
        if (!dataLoaded) {
            console.warn('⚠️ 記事データ読み込み失敗、空配列で継続');
        }
        
        console.log('🎨 描画処理開始');
        hideLoading();
        renderProfile();
        renderServices();
        renderSkills();
        renderSeoArticles();
        renderBlogArticles();
        renderTestimonials();
        renderFAQ();
        renderContact();
        console.log('✅ 全ての描画完了');
    } catch (error) {
        console.error('❌ エラー:', error);
        hideLoading(); // エラー時でもローディング表示を消す
    }
});

// ===== 描画関数 =====
function hideLoading() {
    const loadings = document.querySelectorAll('.loading');
    loadings.forEach(loading => loading.remove());
}

function renderProfile() {
    const profileText = document.querySelector('.profile-text');
    if (!profileText) return;
    
    // プロフィール基本情報
    profileText.innerHTML = `
        <h3>${profileData.name || 'マフィン'}</h3>
        <div class="profile-title">${profileData.title || 'AI × SEOライター'}</div>
        <p>${profileData.bio || ''}</p>
        <div class="profile-stats">
            ${profileData.achievements ? profileData.achievements.map(achievement => `
                <div class="stat-item">
                    <div class="stat-number">${achievement.number}</div>
                    <div class="stat-label">${achievement.label}</div>
                </div>
            `).join('') : ''}
        </div>
        <div class="social-links">
            ${profileData.socialLinks ? profileData.socialLinks.map(link => `
                <a href="${link.url}" target="_blank" rel="noopener noreferrer" class="social-link" aria-label="${link.platform}">
                    <span style="color: ${link.color}">${link.icon}</span>
                </a>
            `).join('') : ''}
        </div>
    `;
    
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
    
    // 初期表示数
    let displayCount = 3;
    let isExpanded = false;
    
    function showArticles() {
        container.innerHTML = '';
        seoArticles.slice(0, displayCount).forEach(article => {
            const card = createArticleCard(article);
            container.appendChild(card);
        });
        
        // MOREボタン表示（記事が3件より多い場合のみ）
        if (seoArticles.length > 3) {
            const moreButton = document.createElement('button');
            moreButton.className = 'more-button';
            
            if (isExpanded) {
                moreButton.textContent = 'CLOSE';
                moreButton.onclick = () => {
                    displayCount = 3;
                    isExpanded = false;
                    showArticles();
                };
            } else {
                moreButton.textContent = 'MORE';
                moreButton.onclick = () => {
                    displayCount = seoArticles.length;
                    isExpanded = true;
                    showArticles();
                };
            }
            
            container.appendChild(moreButton);
        }
    }
    
    showArticles();
    console.log('✅ SEO記事描画完了');
}

function renderBlogArticles() {
    const container = document.querySelector('.blog-articles-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    // 初期表示数
    let displayCount = 3;
    let isExpanded = false;
    
    function showArticles() {
        container.innerHTML = '';
        blogArticles.slice(0, displayCount).forEach(article => {
            const card = createArticleCard(article);
            container.appendChild(card);
        });
        
        // MOREボタン表示（記事が3件より多い場合のみ）
        if (blogArticles.length > 3) {
            const moreButton = document.createElement('button');
            moreButton.className = 'more-button';
            
            if (isExpanded) {
                moreButton.textContent = 'CLOSE';
                moreButton.onclick = () => {
                    displayCount = 3;
                    isExpanded = false;
                    showArticles();
                    // CLOSEボタン押下時にセクションの上部にスクロール
                    document.getElementById('blog-articles').scrollIntoView({ behavior: 'smooth' });
                };
            } else {
                moreButton.textContent = 'MORE';
                moreButton.onclick = () => {
                    displayCount = blogArticles.length;
                    isExpanded = true;
                    showArticles();
                };
            }
            
            container.appendChild(moreButton);
        }
    }
    
    showArticles();
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
                ${(article.tags && Array.isArray(article.tags)) ? article.tags.map(tag => `<span class="tag">${tag}</span>`).join('') : ''}
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
    
    // profileData.faqからデータを取得
    const faqData = profileData.faq || [];
    
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

function renderSkills() {
    const profileContainer = document.querySelector('.profile-container');
    if (!profileContainer || !profileData.skills) return;
    
    // スキルセクションを追加
    const skillsSection = document.createElement('div');
    skillsSection.className = 'skills-section';
    skillsSection.innerHTML = `
        <h3 class="skills-title">SKILLS</h3>
        <div class="skills-grid">
            ${profileData.skills.map(skill => `
                <div class="skill-item">
                    <div class="skill-header">
                        <span class="skill-name">${skill.name}</span>
                        <span class="skill-level">${skill.level}%</span>
                    </div>
                    <div class="skill-bar">
                        <div class="skill-progress" style="width: ${skill.level}%"></div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
    
    profileContainer.appendChild(skillsSection);
    console.log('✅ スキル描画完了');
}

function renderTestimonials() {
    const blogSection = document.getElementById('blog-articles');
    if (!blogSection || !profileData.testimonials) return;
    
    // お客様の声セクションを作成
    const testimonialsSection = document.createElement('section');
    testimonialsSection.id = 'testimonials';
    testimonialsSection.innerHTML = `
        <h2>TESTIMONIALS</h2>
        <p style="text-align: center; color: var(--secondary-color); margin-bottom: var(--spacing-xl); font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Client Reviews & Feedback</p>
        <div class="testimonials-container">
            ${profileData.testimonials.map(testimonial => `
                <div class="testimonial-card">
                    <div class="testimonial-content">
                        <p class="testimonial-text">"${testimonial.text}"</p>
                        <div class="testimonial-author">
                            <strong>${testimonial.author}</strong>
                            <span>${testimonial.company}</span>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
    
    // blog-articlesセクションの後に挿入
    blogSection.parentNode.insertBefore(testimonialsSection, blogSection.nextSibling);
    console.log('✅ お客様の声描画完了');
}

function renderContact() {
    const container = document.querySelector('.contact-container');
    if (!container) return;
    
    const contactInfo = profileData.contact || {};
    const email = contactInfo.email || '0527muffin1203@gmail.com';
    const message = contactInfo.message || 'お仕事のご依頼・お見積もりについては下記フォームよりお気軽にお問い合わせください。';
    
    container.innerHTML = `
        <div class="contact-intro">
            <p>${message}</p>
            <p>フォームが送信できない場合は直接メール（<a href="mailto:${email}">${email}</a>）でご連絡ください。</p>
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