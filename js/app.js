// 전역 상태
let allItems = [];
let filteredItems = [];
let currentCategory = '전체';
let displayCount = 20;

// 카테고리 색상 매핑
const categoryColors = {
    '거시경제': 'bg-blue-100 text-blue-800',
    '금리': 'bg-red-100 text-red-800',
    '환율': 'bg-green-100 text-green-800',
    '주식': 'bg-purple-100 text-purple-800',
    '원자재': 'bg-yellow-100 text-yellow-800',
    '부동산': 'bg-orange-100 text-orange-800',
    '암호화폐': 'bg-indigo-100 text-indigo-800',
    '정책': 'bg-pink-100 text-pink-800',
    '무역': 'bg-teal-100 text-teal-800',
    '기타': 'bg-gray-100 text-gray-800'
};

// 초기 로드
document.addEventListener('DOMContentLoaded', () => {
    loadData();
});

// 데이터 로드
async function loadData() {
    try {
        const response = await fetch('data/feed-latest.json');
        const data = await response.json();

        allItems = data.items || [];

        // 업데이트 시간 표시
        const updateTime = new Date(data.generated_at);
        document.getElementById('lastUpdate').textContent =
            `마지막 업데이트: ${formatTime(updateTime)}`;

        // 통계 업데이트
        updateStats();

        // 카테고리 탭 생성
        createCategoryTabs();

        // 기본 필터 적용
        filterCategory('전체');

    } catch (error) {
        console.error('데이터 로드 실패:', error);
        document.getElementById('newsList').innerHTML = `
            <div class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
                <p class="text-red-600 font-semibold">데이터를 불러오는데 실패했습니다.</p>
                <p class="text-red-500 text-sm mt-2">잠시 후 다시 시도해주세요.</p>
            </div>
        `;
    }
}

// 통계 업데이트
function updateStats() {
    document.getElementById('totalCount').textContent = allItems.length;

    // 최근 6시간
    const sixHoursAgo = new Date(Date.now() - 6 * 60 * 60 * 1000);
    const recentItems = allItems.filter(item => {
        const pubTime = new Date(item.published_at);
        return pubTime > sixHoursAgo;
    });
    document.getElementById('recentCount').textContent = recentItems.length;

    // 트렌딩
    const trending = allItems.filter(item => item.is_trending);
    document.getElementById('trendingCount').textContent = trending.length;
}

// 카테고리 탭 생성
function createCategoryTabs() {
    const categories = ['전체', ...new Set(allItems.map(item => item.category))];
    const tabsContainer = document.getElementById('categoryTabs');

    // 전체 탭은 이미 있으므로 나머지만 추가
    categories.slice(1).forEach(cat => {
        const button = document.createElement('button');
        button.onclick = () => filterCategory(cat);
        button.className = 'category-badge px-4 py-2 rounded-full bg-gray-200 text-gray-700 font-medium whitespace-nowrap hover:bg-gray-300';
        button.textContent = cat;
        tabsContainer.appendChild(button);
    });
}

// 카테고리 필터링
function filterCategory(category) {
    currentCategory = category;
    displayCount = 20;

    // 탭 활성화 상태 변경
    const tabs = document.querySelectorAll('.category-badge');
    tabs.forEach(tab => {
        if (tab.textContent === category) {
            tab.className = 'category-badge px-4 py-2 rounded-full bg-blue-500 text-white font-medium whitespace-nowrap';
        } else {
            tab.className = 'category-badge px-4 py-2 rounded-full bg-gray-200 text-gray-700 font-medium whitespace-nowrap hover:bg-gray-300';
        }
    });

    // 필터링
    if (category === '전체') {
        filteredItems = allItems;
    } else {
        filteredItems = allItems.filter(item => item.category === category);
    }

    renderNews();
}

// 뉴스 렌더링
function renderNews() {
    const container = document.getElementById('newsList');
    const itemsToShow = filteredItems.slice(0, displayCount);

    if (itemsToShow.length === 0) {
        container.innerHTML = `
            <div class="bg-gray-50 border border-gray-200 rounded-xl p-8 text-center">
                <p class="text-gray-600">해당 카테고리의 뉴스가 없습니다.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = itemsToShow.map(item => createNewsCard(item)).join('');

    // 더 보기 버튼 표시/숨김
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (filteredItems.length > displayCount) {
        loadMoreBtn.classList.remove('hidden');
    } else {
        loadMoreBtn.classList.add('hidden');
    }
}

// 뉴스 카드 생성
function createNewsCard(item) {
    const colorClass = categoryColors[item.category] || categoryColors['기타'];
    const publishedTime = formatTimeAgo(new Date(item.published_at));
    const trendingBadge = item.is_trending ?
        '<span class="inline-block px-2 py-1 bg-red-500 text-white text-xs rounded-full">🔥 트렌딩</span>' : '';

    return `
        <article class="news-card bg-white rounded-xl shadow-md p-6">
            <div class="flex justify-between items-start mb-3">
                <div class="flex gap-2 flex-wrap">
                    <span class="px-3 py-1 rounded-full text-sm font-medium ${colorClass}">
                        ${item.category}
                    </span>
                    ${trendingBadge}
                </div>
                <span class="text-sm text-gray-500">${publishedTime}</span>
            </div>
            
            <h2 class="text-xl font-bold text-gray-800 mb-2 hover:text-blue-600 cursor-pointer">
                ${item.title}
            </h2>
            
            <p class="text-gray-600 text-sm mb-4 line-clamp-2">
                ${item.summary.auto || item.summary.source}
            </p>
            
            <div class="flex justify-between items-center">
                <div class="flex items-center gap-2 text-sm text-gray-500">
                    <span class="font-medium">${item.source.name}</span>
                    <span>•</span>
                    <span>${item.country}</span>
                </div>
                
                <a href="${item.url}" target="_blank" rel="noopener noreferrer" 
                   class="inline-flex items-center gap-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition font-medium">
                    원문 보기
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                    </svg>
                </a>
            </div>
            
            ${item.tags.length > 0 ? `
                <div class="mt-4 pt-4 border-t border-gray-100 flex gap-2 flex-wrap">
                    ${item.tags.map(tag => `
                        <span class="text-xs px-2 py-1 bg-gray-100 text-gray-600 rounded">#${tag}</span>
                    `).join('')}
                </div>
            ` : ''}
        </article>
    `;
}

// 더 보기
function loadMore() {
    displayCount += 20;
    renderNews();
}

// 시간 포맷팅
function formatTime(date) {
    return date.toLocaleString('ko-KR', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// 상대 시간 포맷팅
function formatTimeAgo(date) {
    const now = new Date();
    const diff = Math.floor((now - date) / 1000); // 초 단위

    if (diff < 60) return '방금 전';
    if (diff < 3600) return `${Math.floor(diff / 60)}분 전`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}시간 전`;
    if (diff < 604800) return `${Math.floor(diff / 86400)}일 전`;

    return formatTime(date);
}
