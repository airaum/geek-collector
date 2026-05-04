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

---

## 🔧 설치 및 환경 설정

### 1. 레포 클론 및 라이브러리 설치

```bash
git clone https://github.com/airaum/geek-collector.git
cd geek-collector
pip install requests beautifulsoup4
```

### 2. 옵시디언 설정
- **Dataview** 플러그인 설치 및 활성화
- **Shell Commands** 플러그인 설치 (대시보드 사용 시)

---

## 🤖 Claude Code 통합 사용법

Claude Code에서 이 도구를 말로 실행하려면 아래 단계를 따르세요.

### 1단계: 스킬 파일 등록

프로젝트 폴더의 `.claude/skills/` 폴더를 만들고, 아래 내용을 `geek-collector.md`로 저장하세요.

```markdown
# 긱뉴스 수집 스킬 (Geek-Collector)

## 워크플로우
1. 사용자가 "긱뉴스 수집해줘"라고 하면 `scripts/collector.py`를 실행합니다.
2. 실행 시 `--date` 인자로 특정 날짜를 지정할 수 있습니다.
3. 수집 완료 후 생성된 옵시디언 노트 경로를 안내합니다.

## 실행 명령어
python scripts/collector.py --date {{date}}
```

### 2단계: Claude Code settings.json에 등록

`~/.claude/settings.json`의 `mcpServers` 항목에 추가하세요.  
`절대경로` 부분을 실제 경로로 바꿔주세요.

```json
"geek-collector": {
  "command": "python",
  "args": ["C:\\Users\\사용자명\\geek-collector\\scripts\\collector.py"]
}
```

> **경로 확인 방법**: 터미널에서 `cd geek-collector && pwd` 실행 후 나오는 경로를 사용하세요.

---

## 🚀 사용 방법

### Claude Code에서 명령하기

```text
오늘자 긱뉴스 수집해서 내 옵시디언에 정리해줘.
```

### 옵시디언 대시보드 사용

`obsidian-template/수집기.md`를 볼트에 복사한 후, 파일 내의 스크립트 경로를 본인 환경에 맞게 수정하여 버튼으로 사용하세요.

---

## 📜 라이선스

MIT License
