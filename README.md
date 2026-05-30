# test
# change
# gh push test

## 브랜치 전략

### 브랜치 구조

```
master   ← 프로덕션 릴리즈 (안정 버전)
develop  ← 기능 통합 (다음 릴리즈 준비)
feature/ ← 개별 기능 개발
```

### 워크플로

1. `develop`에서 `feature/기능명` 분기
2. 기능 개발 후 `feature/*` → `develop` PR 생성
3. 리뷰 승인 후 merge
4. 릴리즈 시 `develop` → `master` PR 생성 후 merge

### 브랜치 생성

```bash
# feature 브랜치 생성
git checkout develop
git checkout -b feature/기능명
git push origin feature/기능명
```

### PR & Merge

```bash
# feature → develop PR 생성
gh pr create --base develop --head feature/기능명

# develop → master 릴리즈 PR 생성
gh pr create --base master --head develop --title "release: ..."
```

### 브랜치 보호 규칙

| 브랜치 | 직접 push | PR 필수 | 승인 |
|--------|-----------|---------|------|
| `master` | 차단 | ✅ | 1명 (팀) / 0명 (솔로) |
| `develop` | 차단 | ✅ | 1명 (팀) / 0명 (솔로) |
| `feature/*` | 허용 | - | - |
