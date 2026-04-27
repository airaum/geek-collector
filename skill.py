"""
GeekNews Collector — Antigravity Skill

사용 예시:
  "오늘 긱뉴스 수집해줘"
  "2026-04-20 날짜로 긱뉴스 수집해줘"
"""

import subprocess
import sys
import os
from datetime import datetime

# ── 설정 (본인 환경에 맞게 수정) ──────────────────────
PYTHON_PATH = r"d:\내프로젝트폴더\venv\Scripts\python.exe"   # ← 수정
SCRIPT_PATH = r"d:\내프로젝트폴더\geek\scripts\collector.py" # ← 수정

def run(date: str = None) -> str:
    """
    긱뉴스를 수집하여 옵시디언 볼트에 저장합니다.

    Args:
        date: 저장 날짜 (YYYY-MM-DD 형식, 미입력시 오늘 날짜)

    Returns:
        수집 결과 메시지
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return f"❌ 날짜 형식 오류: {date} (올바른 형식: YYYY-MM-DD)"

    if not os.path.exists(PYTHON_PATH):
        return f"❌ Python 경로를 찾을 수 없음: {PYTHON_PATH}\nskill.py 상단의 PYTHON_PATH를 수정하세요."

    if not os.path.exists(SCRIPT_PATH):
        return f"❌ 스크립트를 찾을 수 없음: {SCRIPT_PATH}\nskill.py 상단의 SCRIPT_PATH를 수정하세요."

    try:
        result = subprocess.run(
            [PYTHON_PATH, SCRIPT_PATH, date],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=120
        )

        if result.returncode == 0:
            output = result.stdout.strip()
            return f"✅ 긱뉴스 수집 완료 ({date})\n\n{output}"
        else:
            return f"❌ 수집 실패\n\n{result.stderr.strip()}"

    except subprocess.TimeoutExpired:
        return "❌ 시간 초과 (120초) — 네트워크 상태를 확인하세요."
    except Exception as e:
        return f"❌ 실행 오류: {e}"


if __name__ == "__main__":
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    print(run(date_arg))
