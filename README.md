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

### 1. 파이썬 환경 구축 (터미널)
```bash
# 레포지토리 클론
git clone https://github.com/airaum/geek-collector.git
cd geek-collector

# 필수 라이브러리 설치
pip install requests beautifulsoup4
```

### 2. 옵시디언 설정
- **Dataview** 플러그인 설치 및 활성화
- **Shell Commands** 플러그인 설치 (대시보드 사용 시)

---

## 🌌 Antigravity & Claude Code 통합 설치 (추천)

이 도구를 **Antigravity** 또는 **Claude Code**에서 즉시 사용하려면 아래 단계를 따르세요.

### 1단계: 스킬 등록
사용자 PC의 `.antigravity/skills/geek-collector/` 폴더를 만들고, 아래 내용을 `SKILL.md`로 저장하세요.

```markdown
# 📰 긱뉴스 수집 스킬 (Geek-Collector)

## 워크플로우
1. 사용자가 "긱뉴스 수집해줘"라고 하면 `scripts/collector.py`를 실행합니다.
2. 실행 시 `--date` 인자를 사용하여 특정 날짜를 지정할 수 있습니다.
3. 수집 완료 후 생성된 옵시디언 노트를 확인하라고 안내합니다.

## 실행 명령어
python C:\경로\to\scripts\collector.py --date {{date}}
```

### 2단계: 자동 실행 설정 (mcp_config.json)
클로드가 이 스크립트를 도구로 인식하게 하려면 `mcp_config.json`에 추가하세요. (Python 경로와 스크립트 경로를 본인 환경에 맞게 수정)

```json
{
  "mcpServers": {
    "geek-collector": {
      "command": "python",
      "args": ["C:\\절대경로\\scripts\\collector.py"]
    }
  }
}
```

---

## 🚀 사용 방법

### 1. 클로드에게 명령하기
> "오늘자 긱뉴스 수집해서 내 옵시디언에 정리해줘."

### 2. 옵시디언 대시보드 사용
`obsidian-template/수집기.md`를 볼트에 복사한 후, 파일 내의 Python 및 스크립트 경로를 수정하여 버튼으로 사용하세요.

---

## 📜 라이선스
MIT License
