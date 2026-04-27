# 📡 geek-collector

> 긱뉴스(GeekNews) 자동 수집기  
> 옵시디언 버튼 클릭 한 번 → AI 관련 글 제외 → 추천+댓글 높은 순으로 최대 20개 저장

---

## ✨ 특징

- **무료** — 외부 API, 유료 서비스 일절 없음
- **AI 뉴스 자동 제외** — GPT, LLM, 에이전트 등 30개 키워드 필터
- **추천+댓글순 정렬** — 반응 좋은 글부터 저장
- **한국어 요약** — 긱뉴스가 이미 번역한 내용 그대로 저장
- **노트 연결** — index.md ↔ 각 노트 양방향 위키링크, 그래프 뷰 연결
- **날짜 선택** — 원하는 날짜 폴더에 저장 가능

---

## 📁 파일 구조

```
geek-collector/
├── README.md
├── skill.py                        ← Antigravity Skill
├── scripts/
│   └── collector.py                ← 수집 스크립트
└── obsidian-template/
    ├── 수집기.md                   ← 버튼 대시보드 (복사해서 사용)
    └── .obsidian/
        └── community-plugins.json
```

---

## 🔧 설치 방법

### 1. 필수 조건

- Python 3.8 이상
- pip 패키지 설치

```bash
pip install requests beautifulsoup4
```

### 2. 옵시디언 플러그인 설치

옵시디언 → 설정 → 커뮤니티 플러그인 → 다음 2개 설치 및 활성화

| 플러그인 | 필수 설정 |
|---------|----------|
| **Dataview** | JavaScript queries 활성화 |
| **Shell Commands** | 설치만 하면 됨 |

### 3. 스크립트 경로 설정

`scripts/collector.py` 상단의 `VAULT_DIR` 경로를 본인 옵시디언 볼트 경로로 수정

```python
# 예시
VAULT_DIR = r"C:\Users\홍길동\Documents\geek"
```

### 4. 대시보드 노트 설정

`obsidian-template/수집기.md` 를 볼트에 복사 후  
파일 안의 Python 경로 2줄을 본인 환경에 맞게 수정

```javascript
const python = "C:\\Users\\홍길동\\AppData\\Local\\Programs\\Python\\python.exe";
const script = "C:\\Users\\홍길동\\Documents\\geek\\scripts\\collector.py";
```

---

## 🚀 사용 방법

1. 옵시디언에서 `수집기.md` 열기
2. 날짜 선택 (기본값: 오늘)
3. **▶ 수집 시작** 버튼 클릭
4. 30~60초 후 `YY-MM-DD/` 폴더 자동 생성

### 저장 구조

```
geek/
└── 26-04-27/
    ├── index.md      ← 전체 목록 + 위키링크
    ├── 01.md
    ├── 02.md
    └── ...
```

### 노트 형식

```markdown
---
title: "제목"
date: 2026-04-27
tags:
  - geek
  - 26-04-27
source: "https://원문링크"
points: 42
comments: 7
---

# 제목

↩ [[index|← 26-04-27 목록]]

- 원문: https://...
- 긱뉴스: https://news.hada.io/topic?id=...
- 태그: #geek #26-04-27
- 추천: 42점  |  댓글: 7개

---

## 📌 내용

한국어 요약 내용...
```

---

## ⚡ Antigravity Skill 사용법

`skill.py` 를 Antigravity에 등록하면 AI 어시스턴트에게 수집을 명령할 수 있습니다.

```
"오늘 긱뉴스 수집해줘"
"2026-04-20 날짜로 긱뉴스 수집해줘"
```

---

## ⚠️ 참고사항

- 긱뉴스 메인 페이지 기준으로 수집 (약 20~25개 중 AI 제외 후 저장)
- AI 관련 글이 많은 날은 저장 수가 줄어들 수 있음 (정상)
- 내용이 80자 미만인 글은 자동 제외

---

## 📜 라이선스

MIT License
