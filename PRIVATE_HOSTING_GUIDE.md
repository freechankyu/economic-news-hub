# 🔒 비공개 호스팅 가이드 (GitHub Pages 대체)

## 1. GitHub 저장소 비공개(Private) 전환

먼저 소스 코드를 다른 사람이 볼 수 없게 만듭니다.

1. GitHub 저장소 **Settings** 탭 클릭
2. 왼쪽 사이드바 맨 아래 **Danger Zone**으로 이동
3. **Change repository visibility** 클릭
4. **Change visibility** 버튼 클릭
5. **Make private** 선택
6. 저장소 이름 입력 후 승인

> **주의**: Private으로 바꾸면 기존 GitHub Pages(https://....github.io)는 **작동이 중단됩니다**.

## 2. 무료 호스팅 서비스 선택 (Private 지원)

GitHub Pages는 Private 저장소에서 유료(Pro)지만, 아래 서비스들은 **Private 저장소도 무료**로 호스팅해줍니다.

### 추천 1: Cloudflare Pages (강력 추천)
- **장점**: 전 세계 가장 빠른 속도, 완전 무료, 설정 매우 간편
- **단점**: 회원가입 필요

### 추천 2: Vercel (가장 대중적)
- **장점**: UI가 예쁘고 설정이 직관적
- **단점**: 무료 사용량 제한이 있지만 이 프로젝트엔 충분

---

## 3. Cloudflare Pages로 배포하기 (5분 컷)

1. [Cloudflare 대시보드](https://dash.cloudflare.com/) 로그인 (가입 필요)
2. 왼쪽 메뉴 **Workers & Pages** 클릭
3. **Create application** → **Pages** 탭 → **Connect to Git** 클릭
4. **GitHub** 연결하고 `economic-news-hub` 저장소 선택
   - (Private 저장소도 보입니다!)
5. **Begin setup** 클릭
6. **Build settings** 설정:
   - **Framework preset**: `None` (기본값 유지)
   - **Build command**: (비워두기)
   - **Build output directory**: `public` **(중요! 반드시 입력)**
7. **Save and Deploy** 클릭

끝! 이제 `https://economic-news-hub-xxxxx.pages.dev` 같은 주소로 서비스가 실행됩니다.

---

## 4. Vercel로 배포하기 (대안)

1. [Vercel.com](https://vercel.com) 접속 및 GitHub로 로그인
2. **Add New...** → **Project** 클릭
3. GitHub의 `economic-news-hub` 저장소 옆 **Import** 클릭
4. **Build and Output Settings** 펼치기
   - **Output Directory**: `public` 입력 (Override 체크)
5. **Deploy** 클릭

---

## 5. 자동 업데이트 확인

호스팅을 바꿔도 **데이터 수집은 GitHub Actions**가 담당합니다.

1. GitHub Actions가 매시간 데이터를 수집해서 커밋
2. Cloudflare/Vercel이 **새 커밋을 감지하고 자동으로 재배포**
3. 사이트 자동 최신화 완료!

> **팁**: Private 저장소에서도 GitHub Actions는 월 2,000분 무료입니다. (이 프로젝트는 하루 5분도 안 써서 충분합니다)
