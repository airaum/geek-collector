import sys
import io
import os
import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# ── 설정 (본인 환경에 맞게 수정) ──────────────────────
VAULT_DIR = r"d:\내프로젝트폴더\geek"  # ← 본인 옵시디언 볼트 경로로 변경
MAX_ITEMS = 20
MIN_CONTENT_LEN = 80
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

AI_BLOCK = [
    "chatgpt", "gpt", "llm", "claude", "gemini", "openai", "anthropic",
    "인공지능", "딥러닝", "머신러닝", "언어모델", "생성형", "에이전트",
    "neural network", "diffusion", "midjourney", "huggingface", "deepseek",
    "copilot", "mistral", "ollama", "stable diffusion", "sora", "dall-e",
    "agentic", "swe-agent", "코딩 도구", "llama", "코드 생성", "ai 모델",
    "ai 시장", "ai 에이전트", "ai 코딩", "버티컬 ai", "foundation model"
]

def is_ai(text: str) -> bool:
    t = text.lower()
    return any(kw in t for kw in AI_BLOCK)

def clean_filename(text: str) -> str:
    text = re.sub(r'[\\/*?:"<>|\n\r\t]', " ", text)
    return text.strip()[:60]

# ── 1. 긱뉴스 목록 수집 (포인트+댓글순 정렬) ──────────
def fetch_topic_list() -> list:
    r = requests.get("https://news.hada.io", headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    topics = []
    seen_ids = set()
    all_links = soup.find_all("a", href=True)

    vote_points = {}
    for a in all_links:
        href = a.get("href", "")
        if href.startswith("javascript:vote("):
            tid = href.split("(")[1].split(",")[0].strip()
            parent_text = a.parent.get_text(" ") if a.parent else ""
            nums = re.findall(r'\b(\d+)\b', parent_text)
            vote_points[tid] = int(nums[0]) if nums else 0

    comment_counts = {}
    for a in all_links:
        href = a.get("href", "")
        if "go=comments" in href:
            tid = href.split("id=")[1].split("&")[0]
            txt = a.text.strip()
            nums = re.findall(r'\d+', txt)
            comment_counts[tid] = int(nums[0]) if nums else 0

    i = 0
    while i < len(all_links):
        href = all_links[i].get("href", "")
        text = all_links[i].text.strip()

        if href.startswith("http") and text and len(text) > 5:
            orig_url   = href
            orig_title = text
            topic_id   = None
            topic_url  = None

            if i + 1 < len(all_links):
                next_href = all_links[i + 1].get("href", "")
                if next_href.startswith("topic?id="):
                    topic_id  = next_href.split("=")[1].split("&")[0]
                    topic_url = "https://news.hada.io/" + next_href

            if topic_id and topic_id not in seen_ids:
                if not is_ai(orig_title):
                    pts      = vote_points.get(topic_id, 0)
                    comments = comment_counts.get(topic_id, 0)
                    topics.append({
                        "id":        topic_id,
                        "title":     orig_title,
                        "orig_url":  orig_url,
                        "topic_url": topic_url,
                        "points":    pts,
                        "comments":  comments,
                        "score":     pts + (comments * 2),
                    })
                    seen_ids.add(topic_id)
        i += 1

    topics.sort(key=lambda x: x["score"], reverse=True)
    return topics

# ── 2. 토픽 페이지에서 한국어 내용 추출 ─────────────
def fetch_topic_content(topic_url: str) -> dict:
    try:
        r = requests.get(topic_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        sentences = []
        for tag in soup.find_all(["p", "li"]):
            text = tag.text.strip()
            if (20 < len(text) < 400
                    and re.search(r"[\uAC00-\uD7A3]", text)
                    and "답변달기" not in text
                    and "긱뉴스" not in text
                    and "로그인" not in text
                    and "숨기기" not in text):
                sentences.append(text)

        unique = []
        for s in sentences:
            if not any(s in u or u in s for u in unique):
                unique.append(s)

        summary = "\n\n".join(unique[:8])

        tags = []
        for a in soup.find_all("a", href=True):
            if "/tag/" in a["href"] or "tag=" in a["href"]:
                t = a.text.strip()
                if t:
                    tags.append(t.replace(" ", "-"))

        return {"summary": summary, "tags": tags}

    except Exception as e:
        return {"summary": "", "tags": []}

# ── 3. 노트 저장 (프론트매터 + 위키링크) ──────────────
def save_notes(topics: list, folder_name: str, full_date: str):
    folder = os.path.join(VAULT_DIR, folder_name)
    os.makedirs(folder, exist_ok=True)

    saved_items = []

    for item in topics:
        if len(saved_items) >= MAX_ITEMS:
            break

        print(f"[{len(saved_items)+1:02d}] {item['title'][:50]}")
        detail = fetch_topic_content(item["topic_url"])
        time.sleep(0.5)

        if len(detail["summary"]) < MIN_CONTENT_LEN:
            print(f"      ↳ 내용 부족 → 건너뜀")
            continue

        num      = f"{len(saved_items)+1:02d}"
        fm_tags  = ["geek", folder_name] + detail["tags"][:3]
        pts      = item.get("points", 0)
        comments = item.get("comments", 0)

        frontmatter = f"""---
title: "{item['title'].replace('"', "'")}"
date: {full_date}
tags:
{chr(10).join(f'  - {t}' for t in fm_tags)}
source: "{item['orig_url']}"
geek: "{item['topic_url']}"
points: {pts}
comments: {comments}
---"""

        content = f"""{frontmatter}

# {item['title']}

↩ [[index|← {folder_name} 목록]]

- 원문: {item['orig_url']}
- 긱뉴스: {item['topic_url']}
- 태그: {" ".join(f"#{t}" for t in fm_tags)}
- 추천: {pts}점  |  댓글: {comments}개

---

## 📌 내용

{detail['summary']}
"""

        filepath = os.path.join(folder, f"{num}.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        saved_items.append({"num": num, "title": item["title"]})

    index_links = "\n".join(
        f"- [[{it['num']}|{it['num']}. {it['title']}]]"
        for it in saved_items
    )

    index_content = f"""---
title: "{folder_name} 긱뉴스"
date: {full_date}
tags:
  - geek
  - index
  - {folder_name}
---

# 📅 {folder_name} 긱뉴스

> 수집일: {full_date} | 총 {len(saved_items)}개

---

## 목록

{index_links}
"""

    index_path = os.path.join(folder, "index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)

    print(f"\n✅ 완료: {folder}")
    print(f"   노트 {len(saved_items)}개 + index.md 생성")

# ── 실행 ──────────────────────────────────────────
def main():
    if len(sys.argv) > 1:
        try:
            dt = datetime.strptime(sys.argv[1], "%Y-%m-%d")
        except ValueError:
            dt = datetime.now()
    else:
        dt = datetime.now()

    folder_name = dt.strftime("%y-%m-%d")
    full_date   = dt.strftime("%Y-%m-%d")

    print(f"긱뉴스 수집 시작 → {folder_name}")
    topics = fetch_topic_list()
    print(f"AI 제외 후 {len(topics)}개 항목\n")
    save_notes(topics, folder_name, full_date)

if __name__ == "__main__":
    main()
