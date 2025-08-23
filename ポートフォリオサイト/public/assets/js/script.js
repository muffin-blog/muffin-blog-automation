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
        renderSeoArticles();
        renderBlogArticles();
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
    
    // シンプルなプロフィール
    profileText.innerHTML = `
        <h3>${profileData.name || 'マフィン'}</h3>
        <div class="profile-title">${profileData.title || 'AI × SEOライター'}</div>
        <p>${profileData.bio || ''}</p>
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


function renderSeoArticles() {
    const container = document.querySelector('.seo-articles-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    // 横スクロール用に全記事表示
    seoArticles.forEach(article => {
        const card = createArticleCard(article);
        container.appendChild(card);
    });
    
    // 横スクロールボタン初期化
    initializeScrollButtons('seo-scroll');
    
    console.log('✅ SEO記事描画完了');
}

function renderBlogArticles() {
    const container = document.querySelector('.blog-articles-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    // 横スクロール用に全記事表示
    blogArticles.forEach(article => {
        const card = createArticleCard(article);
        container.appendChild(card);
    });
    
    // 横スクロールボタン初期化
    initializeScrollButtons('blog-scroll');
    
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
    const faqData = profileData.faq || {};
    const categories = Object.keys(faqData);
    
    container.innerHTML = `
        <div class="faq-categories">
            <h3 class="faq-category-title">ライティングについて</h3>
            <ul class="faq-category-menu">
                ${categories.map(category => `
                    <li><a href="#${category}" onclick="switchFAQCategory('${category}')">${category}</a></li>
                `).join('')}
            </ul>
        </div>
        <div class="faq-questions">
            ${categories.map(category => `
                <div class="faq-category-section" id="category-${category}" style="display: ${category === categories[0] ? 'block' : 'none'};">
                    <h3 class="faq-section-title">${category}</h3>
                    <div class="faq-items">
                        ${faqData[category].map((faq, index) => `
                            <div class="faq-item">
                                <div class="faq-question" onclick="toggleFAQ('${category}-${index}')">
                                    <span class="faq-question-text">${faq.question}</span>
                                    <span class="faq-toggle">+</span>
                                </div>
                                <div class="faq-answer" id="faq-answer-${category}-${index}">
                                    <p>${faq.answer}</p>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `).join('')}
        </div>
    `;
    
    console.log('✅ FAQ描画完了');
}

// カテゴリ切り替え関数
function switchFAQCategory(targetCategory) {
    // 全てのカテゴリセクションを非表示
    document.querySelectorAll('.faq-category-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // 選択されたカテゴリのセクションを表示
    const targetSection = document.getElementById(`category-${targetCategory}`);
    if (targetSection) {
        targetSection.style.display = 'block';
    }
    
    // メニューのアクティブ状態更新
    document.querySelectorAll('.faq-category-menu a').forEach(link => {
        link.classList.remove('active');
    });
    event.target.classList.add('active');
}



function renderContact() {
    const container = document.querySelector('.contact-container');
    if (!container) return;
    
    const contactInfo = profileData.contact || {};
    const email = contactInfo.email || '0527muffin1203@gmail.com';
    const message = contactInfo.message || 'お仕事のご依頼・お見積もりについては下記フォームよりお気軽にお問い合わせください。';
    
    container.innerHTML = `
        <div class="contact-progress">
            <div class="progress-step active">
                <div class="step-number">入力</div>
            </div>
            <div class="progress-line"></div>
            <div class="progress-step">
                <div class="step-number">確認</div>
            </div>
            <div class="progress-line"></div>
            <div class="progress-step">
                <div class="step-number">完了</div>
            </div>
        </div>
        
        <div class="contact-form-wrapper">
            <h3 class="contact-form-title">お問い合わせフォーム</h3>
            <p class="contact-form-subtitle">* は必須項目です。</p>
            
            <form class="contact-form" onsubmit="handleContactForm(event)">
                <div class="form-group">
                    <label class="form-label" for="inquiry-type">お問い合わせ項目 *</label>
                    <div class="radio-group">
                        <label class="radio-option">
                            <input type="radio" name="inquiry-type" value="consultation" checked>
                            <span class="radio-custom"></span>
                            ご相談・お見積り依頼
                        </label>
                        <label class="radio-option">
                            <input type="radio" name="inquiry-type" value="other">
                            <span class="radio-custom"></span>
                            その他
                        </label>
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label" for="name">お名前 *</label>
                        <input type="text" id="name" name="name" class="form-input" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="company">会社名 *</label>
                        <input type="text" id="company" name="company" class="form-input" required>
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label" for="email">メールアドレス *</label>
                        <input type="email" id="email" name="email" class="form-input" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="phone">電話番号 *</label>
                        <input type="tel" id="phone" name="phone" class="form-input" required>
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label" for="budget">ご予算</label>
                        <select id="budget" name="budget" class="form-select">
                            <option value="">選択してください</option>
                            <option value="under-50k">5万円未満</option>
                            <option value="50k-100k">5万円〜10万円</option>
                            <option value="100k-300k">10万円〜30万円</option>
                            <option value="300k-500k">30万円〜50万円</option>
                            <option value="over-500k">50万円以上</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="timeline">ご希望の納期</label>
                        <select id="timeline" name="timeline" class="form-select">
                            <option value="">選択してください</option>
                            <option value="urgent">1週間以内</option>
                            <option value="normal">2週間以内</option>
                            <option value="flexible">1ヶ月以内</option>
                            <option value="negotiable">要相談</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="file-upload">ファイルアップロード</label>
                    <div class="file-upload-area">
                        <input type="file" id="file-upload" name="files" multiple accept=".zip,.jpg,.jpeg,.gif,.png,.pdf,.ppt,.doc,.docx" class="file-input">
                        <div class="file-upload-content">
                            <span class="file-upload-text">ファイルを選択する</span>
                            <span class="file-upload-button">アップロードする</span>
                        </div>
                    </div>
                    <p class="file-upload-note">* デザインラフなど共有したいイメージがありましたらアップロードください（5MBまで）<br>対応ファイル形式：zip, jpg, jpeg, gif, png, pdf, ppt, doc, docx</p>
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="message">ご相談・ご依頼内容 *</label>
                    <textarea id="message" name="message" class="form-textarea" required placeholder="お仕事の概要&#10;・ご使用媒体&#10;・イラストボリューム（点数など）&#10;・ご希望タッチ（ご相談しながら進めていくことも可能です。）&#10;・詳細スケジュール"></textarea>
                </div>
                
                <div class="form-group">
                    <label class="checkbox-option">
                        <input type="checkbox" name="privacy-agreement" required>
                        <span class="checkbox-custom"></span>
                        <a href="#" class="privacy-link">プライバシーポリシー</a>に同意します
                    </label>
                </div>
                
                <button type="submit" class="form-submit">
                    送信する
                    <span class="submit-arrow">→</span>
                </button>
            </form>
        </div>
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
    
    // 必須項目チェック
    const name = formData.get('name');
    const email = formData.get('email');
    const company = formData.get('company');
    const phone = formData.get('phone');
    const message = formData.get('message');
    const privacyAgreement = formData.get('privacy-agreement');
    
    if (!name || !email || !company || !phone || !message || !privacyAgreement) {
        alert('必須項目をすべて入力し、プライバシーポリシーに同意してください。');
        return;
    }
    
    // メール内容作成
    const inquiryType = formData.get('inquiry-type');
    const budget = formData.get('budget');
    const timeline = formData.get('timeline');
    
    const subject = `【ポートフォリオサイト】${inquiryType === 'consultation' ? 'ご相談・お見積り' : 'お問い合わせ'} - ${name}様`;
    
    const emailBody = `
【お問い合わせ項目】${inquiryType === 'consultation' ? 'ご相談・お見積り依頼' : 'その他'}

【お名前】${name}
【会社名】${company}
【メールアドレス】${email}
【電話番号】${phone}
【ご予算】${budget || '未選択'}
【ご希望納期】${timeline || '未選択'}

【ご相談・ご依頼内容】
${message}

---
このメールはポートフォリオサイトのお問い合わせフォームから送信されました。
    `.trim();
    
    const mailtoLink = `mailto:0527muffin1203@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(emailBody)}`;
    window.location.href = mailtoLink;
    
    event.target.reset();
    alert('メールクライアントが開きます。送信ボタンを押してお送りください。');
}

// 横スクロールボタン初期化
function initializeScrollButtons(scrollId) {
    const scrollContainer = document.getElementById(scrollId);
    if (!scrollContainer) return;
    
    const scrollBtns = scrollContainer.parentElement.querySelectorAll('.scroll-btn');
    const leftBtn = scrollContainer.parentElement.querySelector('.scroll-btn-left');
    const rightBtn = scrollContainer.parentElement.querySelector('.scroll-btn-right');
    
    if (!leftBtn || !rightBtn) return;
    
    leftBtn.onclick = () => {
        scrollContainer.scrollBy({
            left: -400,
            behavior: 'smooth'
        });
    };
    
    rightBtn.onclick = () => {
        scrollContainer.scrollBy({
            left: 400,
            behavior: 'smooth'
        });
    };
    
    // ボタン表示/非表示の判定
    function updateButtonVisibility() {
        const { scrollLeft, scrollWidth, clientWidth } = scrollContainer;
        leftBtn.style.opacity = scrollLeft > 0 ? '1' : '0.5';
        rightBtn.style.opacity = scrollLeft < scrollWidth - clientWidth - 10 ? '1' : '0.5';
    }
    
    scrollContainer.addEventListener('scroll', updateButtonVisibility);
    setTimeout(updateButtonVisibility, 100);
}

console.log('✅ JavaScript読み込み完了');