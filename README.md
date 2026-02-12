# 📊 Economic News Hub

신뢰할 수 있는 경제 정보를 한눈에 - 저작권 친화적 뉴스 큐레이션 서비스

## ✨ 특징

- 🔒 **저작권 안전**: 원문 저장 없이 메타데이터와 링크만 제공
- 🆓 **완전 무료**: GitHub Pages + Actions로 운영 비용 0원
- 🤖 **자동 수집**: 매시간 자동으로 최신 정보 업데이트
- 📱 **반응형 디자인**: 모바일/태블릿/데스크톱 모두 지원
- 🎯 **신뢰할 수 있는 소스**: 공공기관과 중앙은행 공식 RSS만 사용

## 🚀 빠른 시작

### 1. 저장소 클론

```bash
git clone https://github.com/사용자명/economic-news-hub.git
cd economic-news-hub
```

### 2. Python 의존성 설치

```bash
pip install -r scripts/requirements.txt
```

### 3. 수동 테스트

```bash
python scripts/collect.py
```

### 4. GitHub Pages 배포

1. GitHub 저장소 Settings → Pages
2. Source: `Deploy from a branch`
3. Branch: `main` → 폴더: `/public`
4. Save

### 5. 자동 수집 활성화

GitHub Actions는 자동으로 활성화됩니다. (`.github/workflows/collect-news.yml`)

## 📁 프로젝트 구조

```
economic-news-hub/
├─ .github/workflows/
│  └─ collect-news.yml       # 매시간 자동 수집
├─ scripts/
│  ├─ collect.py             # 메인 수집 스크립트
│  ├─ requirements.txt       # Python 의존성
│  └─ config/
│     ├─ sources.json        # 수집 소스 리스트
│     └─ categories.json     # 카테고리 정의
├─ data/
│  ├─ feed-latest.json       # 최근 48시간 데이터
│  ├─ trending.json          # 트렌딩 데이터
│  └─ archive/               # 시간별 아카이브
├─ public/
│  ├─ index.html             # 메인 페이지
│  └─ js/app.js              # 프론트엔드 로직
└─ README.md
```

## 🔧 설정

### 소스 추가

`scripts/config/sources.json`에 새 소스를 추가하세요:

```json
{
  "id": "unique-id",
  "name": "소스 이름",
  "rss_url": "https://example.com/rss",
  "category": "카테고리",
  "country": "KR",
  "copyright_status": "public",
  "status": "active"
}
```

**중요**: 새 소스 추가 전 반드시 확인하세요:
- ✅ RSS 공식 제공 여부
- ✅ robots.txt 허용 확인
- ✅ 이용약관에서 크롤링 금지 여부

### 카테고리 수정

`scripts/config/categories.json`에서 카테고리와 키워드를 수정할 수 있습니다.

## 📊 데이터 정책

### 저장하는 것
- URL, 제목, 발행일, 출처 정보
- RSS 제공 요약 (100자 이내)
- 자체 생성 요약 (50자 이내)
- 카테고리, 태그, 메타데이터

### 저장하지 않는 것
- ❌ 기사 본문 전체
- ❌ 이미지, 동영상
- ❌ 원문을 대체할 수준의 긴 요약

## 🎨 커스터마이징

### 디자인 변경

`public/index.html`과 Tailwind CSS 클래스를 수정하세요.

### 수집 주기 변경

`.github/workflows/collect-news.yml`의 cron 표현식 수정:

```yaml
schedule:
  - cron: '0 */2 * * *'  # 2시간마다
```

## 📝 라이선스 & 저작권

본 프로젝트는 뉴스 콘텐츠를 재배포하지 않으며, 공식 RSS 피드의 메타데이터와 원문 링크만 제공합니다.

- 모든 뉴스 저작권은 원 출처에 있습니다
- 본 서비스는 링크 기반 큐레이션 도구입니다
- 저작권 관련 문의나 삭제 요청은 Issues를 통해 제출해주세요

## 🤝 기여

버그 리포트, 기능 제안, Pull Request 환영합니다!

## 📞 문의

- GitHub Issues: 버그 리포트 및 기능 제안
- Email: [이메일 주소]

---

**면책 조항**: 본 서비스는 정보 제공 목적으로만 사용되며, 투자 결정의 근거로 사용되어서는 안 됩니다.
