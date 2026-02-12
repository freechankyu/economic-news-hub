## 📦 GitHub 푸시 가이드

### 준비 단계

1. **GitHub 계정 준비**
   - GitHub.com에 로그인
   - 계정이 없다면 https://github.com/join 에서 가입

2. **Git 설치 확인**
   ```bash
   git --version
   ```
   - 없다면 https://git-scm.com/download/win 에서 설치

### 1단계: GitHub 저장소 생성

1. GitHub.com 접속 → 우측 상단 `+` 버튼 클릭
2. `New repository` 선택
3. 설정:
   - Repository name: `economic-news-hub`
   - Public 선택 (중요!)
   - **"Add README file" 체크하지 마세요** (이미 있음)
4. `Create repository` 클릭
5. 저장소 URL 복사 (예: `https://github.com/사용자명/economic-news-hub.git`)

### 2단계: 로컬에서 Git 초기화 및 푸시

PowerShell 또는 CMD에서 아래 명령어 실행:

```powershell
# 프로젝트 폴더로 이동
cd "d:\구글 안티그래비티\economic-news-hub"

# Git 초기화
git init

# 모든 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit: Economic News Hub MVP"

# 기본 브랜치 이름 설정
git branch -M main

# GitHub 저장소 연결 (URL은 본인 것으로 변경!)
git remote add origin https://github.com/사용자명/economic-news-hub.git

# 푸시!
git push -u origin main
```

### 3단계: GitHub Pages 활성화

1. GitHub 저장소 페이지로 이동
2. `Settings` 탭 클릭
3. 왼쪽 메뉴에서 `Pages` 클릭
4. Source 설정:
   - `Deploy from a branch` 선택
   - Branch: `main` 선택
   - 폴더: `/public` 선택 (또는 `/` 루트)
5. `Save` 클릭
6. 몇 분 후 `https://사용자명.github.io/economic-news-hub/` 접속!

### 4단계: GitHub Actions 확인

1. 저장소에서 `Actions` 탭 클릭
2. `Collect Economic News` 워크플로우 확인
3. 처음에는 실패할 수 있음 (data가 없어서)
4. `Run workflow` 클릭 → `Run workflow` 버튼으로 수동 실행
5. 성공하면 `data/` 폴더에 JSON 파일 생성됨

### ⚠️ 문제 해결

**1. Git 인증 오류**
```
Username for 'https://github.com': [GitHub 사용자명]
Password for 'https://...': [Personal Access Token]
```
- 비밀번호 대신 Personal Access Token 사용
- https://github.com/settings/tokens 에서 생성
- Note: `경제뉴스허브`, Expiration: `90 days`, Scope: `repo` 체크

**2. "data/" 폴더가 비어있음**
- 정상입니다! GitHub Actions가 처음 실행되면 채워집니다
- 또는 로컬에서 `python scripts/collect.py` 실행 후 푸시

**3. GitHub Pages가 안 보임**
- 몇 분 기다려주세요 (최대 10분)
- `public/index.html`이 있는지 확인
- Settings → Pages에서 URL 확인

### ✅ 완료 체크리스트

- [ ] GitHub 저장소 생성
- [ ] 로컬 → GitHub 푸시 완료
- [ ] GitHub Pages 활성화
- [ ] Actions 워크플로우 정상 작동
- [ ] 웹사이트 접속 확인

---

**다음 단계**: 첫 데이터 수집을 위해 `Actions` 탭에서 워크플로우를 수동 실행하세요!
