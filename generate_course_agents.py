#!/usr/bin/env python3
"""
Mandate 三 Agent 课程内容生产流水线 v1.0
========================================
Agent 1 (内容产生) → Agent 2 (质量控制) → Agent 3 (前后呼应检查) → 输出

用法:
  python3 generate_course_agents.py --course 7    # 重新生成第7课
  python3 generate_course_agents.py --batch 7,8,9  # 批量生成
  python3 generate_course_agents.py --all           # 全部94门（慎用）
  python3 generate_course_agents.py --openings-only # 只改开头不重写全文
"""
import json, os, re, sys, time, urllib.request
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────
MODEL = "deepseek-chat"
API_URL = "https://api.deepseek.com/v1/chat/completions"
COURSES_FILE = "js/courses-data.js"
AUDIO_DIR = "audio"
MAX_RETRIES = 2

def load_api_key():
    """Load DeepSeek API key from env or Hermes config."""
    key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if key:
        return key
    config_path = os.path.expanduser("~/.hermes/config.yaml")
    if not os.path.exists(config_path):
        return ""
    try:
        import yaml
        data = yaml.safe_load(Path(config_path).read_text()) or {}
        providers = data.get("providers", {})
        deepseek = providers.get("deepseek", {})
        if isinstance(deepseek, dict) and deepseek.get("api_key"):
            return str(deepseek["api_key"]).strip()
        for models in [deepseek.get("models", {})]:
            if isinstance(models, dict):
                for cfg in models.values():
                    if isinstance(cfg, dict) and cfg.get("api_key"):
                        return str(cfg["api_key"]).strip()
    except Exception:
        pass
    return ""

API_KEY = load_api_key()

# ── Helpers ─────────────────────────────────────────────────────
def call_deepseek(system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: int = 4000) -> str:
    """Call DeepSeek API with system + user prompt."""
    req = urllib.request.Request(
        API_URL,
        data=json.dumps({
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
    )
    resp = urllib.request.urlopen(req, timeout=120)
    data = json.loads(resp.read())
    return data["choices"][0]["message"]["content"].strip()


def load_course(course_id: int) -> dict | None:
    """Load a single course from courses-data.js."""
    with open(COURSES_FILE) as f:
        content = f.read()
    # Find the course block
    pattern = re.compile(
        r'{\s*id:\s*' + str(course_id) + r',\s*title:\s*\'([^\']+)\'\s*,\s*'
        r'desc:\s*\'([^\']+)\'\s*,\s*'
        r'tags:\s*(.+?)\s*,\s*'
        r'content:\s*`([\s\S]*?)`\s*,\s*'
        r'quiz:\s*(\[[\s\S]*?\])\s*\}',
        re.DOTALL
    )
    m = pattern.search(content)
    if not m:
        return None
    return {
        "id": course_id,
        "title": m.group(1),
        "desc": m.group(2),
        "tags_raw": m.group(3),
        "content": m.group(4),
        "quiz_raw": m.group(5),
    }


def load_all_courses() -> list[dict]:
    """Load all courses with basic info for cross-reference."""
    with open(COURSES_FILE) as f:
        content = f.read()
    pattern = re.compile(
        r'{\s*id:\s*(\d+),\s*title:\s*\'([^\']+)\'\s*,\s*'
        r'desc:\s*\'([^\']+)\'',
        re.DOTALL
    )
    return [
        {"id": int(m.group(1)), "title": m.group(2), "desc": m.group(3)}
        for m in pattern.finditer(content)
    ]


def count_chinese(text: str) -> int:
    return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', text))


# ═══════════════════════════════════════════════════════════════
# AGENT 1: 内容产生
# ═══════════════════════════════════════════════════════════════
AGENT1_SYSTEM = """你是帝王学课程内容创作专家。你的任务是为「帝王学分析师」平台撰写深度课程内容。

写作要求：
1. **开头必须独特**：用一句名言、一个著名历史场景、或一段震撼的史书记载来破题。绝不千篇一律。
   例如：「王侯将相，宁有种乎！」——陈胜在大泽乡喊出的这句话，揭开了中国历史上第一次大规模农民起义的序幕。
   或用：「朕为始皇帝。后世以计数，二世三世至于万世，传之无穷。」——秦始皇的这句豪言，既是自信也是诅咒。

2. **内容深度**：3000-5000中文字，分3-5个小节，每节有明确的主题
3. **可读性**：像老师在讲课，不是维基百科。有故事、有细节、有洞察
4. **结构**：使用 ## 标题和 ### 小节，适当使用 blockquote（> ）引用原文
5. **结尾**：留一个引人深思的问题或洞察
6. **格式**：纯 Markdown，不使用任何代码块标记
7. **口语化**：用自然的讲述语气，避免学术论文腔调

输出格式：
第一行：OPENING_QUOTE: 名言/场景原文
第二行开始：Markdown 格式的课程正文"""


def agent1_generate(course_id: int, title: str, desc: str, existing_content: str = "") -> str:
    """Agent 1: Generate course content with unique opening."""
    context = f"已有内容（如为空则全新创作）：\n{existing_content[:500] if existing_content else '（全新创作）'}"

    user_prompt = f"""请为以下课程撰写完整内容：

课程编号：#{course_id}
课程标题：{title}
课程描述：{desc}

{context}

请严格按照格式要求输出：第一行为 OPENING_QUOTE，然后是一个空行，然后是完整的 Markdown 课程正文（3000-5000中文字）。
注意：开头必须独特，用名言或著名历史场景破题！"""

    return call_deepseek(AGENT1_SYSTEM, user_prompt, temperature=0.8, max_tokens=6000)


# ═══════════════════════════════════════════════════════════════
# AGENT 2: 质量控制
# ═══════════════════════════════════════════════════════════════
AGENT2_SYSTEM = """你是帝王学课程质量控制专家。你需要严格审查课程内容的质量。

检查维度（每项 1-5 分）：
1. **开头吸引力**：第一段是否用名言/名场面破题？是否有冲击力？
2. **历史准确性**：史实是否准确？年代、人名、事件是否正确？
3. **结构清晰度**：小节划分是否合理？逻辑是否连贯？
4. **可读性**：语言是否口语化、有故事感？是否存在 AI 腔？
5. **深度与洞察**：是否有独到分析？是否超越常识？
6. **字数达标**：中文字数是否在 3000-5000 范围？

输出格式：
```
评分：开头X/5 准确X/5 结构X/5 可读X/5 深度X/5 字数X/5
总分：X/30
通过：是/否（总分≥24为通过）

问题清单：
- 具体问题1
- 具体问题2

修改建议：
- 建议1
- 建议2

总结：一句话评价
```"""


def agent2_review(content: str, course_id: int, title: str) -> dict:
    """Agent 2: Quality review. Returns dict with scores, pass/fail, issues."""
    cn_count = count_chinese(content)
    user_prompt = f"""请审查以下课程内容：

课程编号：#{course_id}
课程标题：{title}
中文字数：{cn_count}

课程内容：
{content[:8000]}"""

    result = call_deepseek(AGENT2_SYSTEM, user_prompt, temperature=0.3, max_tokens=1500)

    # Parse scores
    scores = {}
    score_match = re.search(r'开头(\d+)/5.*?准确(\d+)/5.*?结构(\d+)/5.*?可读(\d+)/5.*?深度(\d+)/5.*?字数(\d+)/5', result)
    if score_match:
        scores = {
            "opening": int(score_match.group(1)),
            "accuracy": int(score_match.group(2)),
            "structure": int(score_match.group(3)),
            "readability": int(score_match.group(4)),
            "depth": int(score_match.group(5)),
            "length": int(score_match.group(6)),
        }

    total_match = re.search(r'总分：(\d+)/30', result)
    total = int(total_match.group(1)) if total_match else sum(scores.values()) if scores else 0

    passed = "通过：是" in result or total >= 24

    return {
        "scores": scores,
        "total": total,
        "passed": passed,
        "feedback": result,
        "char_count": cn_count,
    }


# ═══════════════════════════════════════════════════════════════
# AGENT 3: 前后呼应检查
# ═══════════════════════════════════════════════════════════════
AGENT3_SYSTEM = """你是帝王学课程体系一致性检查专家。你需要检查新课程与已有课程之间是否存在矛盾、重复或断裂。

检查维度：
1. **史实矛盾**：新课程中的史实是否与已有课程冲突？
2. **内容重复**：是否有大段内容与已有课程高度重叠？
3. **叙事断裂**：课程间的衔接是否自然？前后是否呼应？
4. **引用一致**：同一人物、事件在不同课程中的描述是否一致？
5. **体系完整**：新课程是否填补了知识空白？还是与已有课程重叠？

输出格式：
```
一致性评分：X/25（每项5分）
通过：是/否

矛盾/重复项：
- 具体问题（指明与哪个课程、什么内容冲突）

呼应建议：
- 如果需要建立跨课程关联，在此建议
```"""


def agent3_check(new_content: str, course_id: int, title: str, all_courses: list[dict]) -> dict:
    """Agent 3: Consistency check against all existing courses."""
    # Build context from nearby courses (previous/following IDs)
    nearby = [c for c in all_courses if abs(c["id"] - course_id) <= 5 and c["id"] != course_id]
    context_str = "附近课程：\n" + "\n".join(
        f"#{c['id']}: {c['title']} — {c['desc']}" for c in nearby
    ) if nearby else "（暂无附近课程）"

    # Also include courses that might share emperors/eras
    all_summary = "\n全部课程列表：\n" + "\n".join(
        f"#{c['id']}: {c['title']}" for c in all_courses if c["id"] != course_id
    )

    user_prompt = f"""请检查以下新课程与已有课程体系的一致性：

新课程编号：#{course_id}
新课程标题：{title}

{context_str}

{all_summary}

新课程内容（前2000字）：
{new_content[:2000]}

请输出一致性检查报告。"""

    result = call_deepseek(AGENT3_SYSTEM, user_prompt, temperature=0.3, max_tokens=1500)

    score_match = re.search(r'一致性评分：(\d+)/25', result)
    score = int(score_match.group(1)) if score_match else 0
    passed = "通过：是" in result or score >= 18

    return {
        "score": score,
        "passed": passed,
        "feedback": result,
    }


# ═══════════════════════════════════════════════════════════════
# OPENING-ONLY MODE: 只改写开头
# ═══════════════════════════════════════════════════════════════
OPENING_SYSTEM = """你是课程开头改写专家。你的唯一任务：为课程写一个独特的、有冲击力的开头段落。

要求：
1. 用一句名言、一个著名历史场景、或一段震撼的史书记载破题
2. 100-200字，自然的口语化讲述
3. 与课程主题紧密相关
4. 绝不千篇一律
5. 像老师在课堂上讲一个引人入胜的故事开头

输出：只输出开头段落，不要任何标记。"""


def agent_opening_only(course_id: int, title: str, desc: str, existing_content: str) -> str:
    """Generate only a new opening paragraph for an existing course."""
    # Get current opening (first 200 chars after stripping markdown headers)
    clean = re.sub(r'^#+\s*.*?\n', '', existing_content, count=1)
    current_opening = clean[:200].strip()

    user_prompt = f"""课程编号：#{course_id}
课程标题：{title}
课程描述：{desc}
当前开头：{current_opening}

请为这门课写一个新的开头段落（100-200字），用名言或名场面破题。直接输出，不要任何额外说明。"""

    return call_deepseek(OPENING_SYSTEM, user_prompt, temperature=0.9, max_tokens=500)


# ═══════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ═══════════════════════════════════════════════════════════════
def pipeline_generate(course_id: int, openings_only: bool = False):
    """Run the full 3-agent pipeline for one course."""
    print(f"\n{'='*60}")
    print(f"Pipeline — 课程 #{course_id}")
    print(f"{'='*60}")

    # Load existing course
    existing = load_course(course_id)
    if not existing:
        print(f"✗ 课程 #{course_id} 不存在")
        return None

    title = existing["title"]
    desc = existing["desc"]
    old_content = existing["content"]

    if openings_only:
        # ═══ Opening-only mode ═══
        print(f"\n🎤 改写开头: {title}")
        new_opening = agent_opening_only(course_id, title, desc, old_content)
        return {"opening": new_opening, "mode": "opening_only"}

    # ═══ Full pipeline ═══
    for attempt in range(MAX_RETRIES + 1):
        print(f"\n{'─'*40}")
        print(f"🔄 尝试 {attempt + 1}/{MAX_RETRIES + 1}")

        # Agent 1: Generate
        print("📝 Agent 1 (内容产生) 工作中...")
        raw = agent1_generate(course_id, title, desc, old_content if attempt == 0 else "")

        # Parse opening quote and body
        lines = raw.split("\n")
        opening_quote = ""
        body_start = 0
        for i, line in enumerate(lines):
            if line.startswith("OPENING_QUOTE:"):
                opening_quote = line.replace("OPENING_QUOTE:", "").strip()
                body_start = i + 1
                break
        body = "\n".join(lines[body_start:]).strip()
        cn_count = count_chinese(body)

        print(f"  生成: {cn_count} 中文字, 开头: {opening_quote[:50]}...")

        # Agent 2: Review
        print("🔍 Agent 2 (质量控制) 审查中...")
        review = agent2_review(body, course_id, title)
        print(f"  评分: {review['total']}/30 {'✅ 通过' if review['passed'] else '❌ 不通过'}")

        # Agent 3: Consistency
        print("🔗 Agent 3 (前后呼应) 检查中...")
        all_courses = load_all_courses()
        consistency = agent3_check(body, course_id, title, all_courses)
        print(f"  一致性: {consistency['score']}/25 {'✅ 通过' if consistency['passed'] else '❌ 问题'}")

        if review["passed"] and consistency["passed"]:
            print(f"\n✅ 课程 #{course_id} 通过审核！")
            return {
                "opening": opening_quote,
                "body": body,
                "review": review,
                "consistency": consistency,
                "attempts": attempt + 1,
                "mode": "full",
            }
        else:
            print(f"  ⚠ 未通过，准备重试...")
            if not review["passed"]:
                print(f"    质控问题：\n{review['feedback'][:300]}")
            if not consistency["passed"]:
                print(f"    一致性问题：\n{consistency['feedback'][:300]}")

    print(f"\n❌ 课程 #{course_id} 在 {MAX_RETRIES + 1} 次尝试后仍未通过")
    return None


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Mandate 三 Agent 课程生产流水线")
    parser.add_argument("--course", type=int, help="单门课程编号")
    parser.add_argument("--batch", type=str, help="批量课程，逗号分隔，如 7,8,9")
    parser.add_argument("--all", action="store_true", help="处理全部94门课程")
    parser.add_argument("--openings-only", action="store_true", help="只改写开头，不重写全文")
    parser.add_argument("--preview", action="store_true", help="预览模式，不实际写入文件")
    args = parser.parse_args()

    if not API_KEY:
        print("❌ 未找到 DeepSeek API Key")
        print("请设置 DEEPSEEK_API_KEY 环境变量或在 ~/.hermes/config.yaml 中配置")
        sys.exit(1)

    course_ids = []
    if args.course:
        course_ids = [args.course]
    elif args.batch:
        course_ids = [int(x.strip()) for x in args.batch.split(",")]
    elif args.all:
        course_ids = list(range(7, 101))  # Courses 7-100

    if not course_ids:
        print("请指定 --course, --batch, 或 --all")
        sys.exit(1)

    results = {}
    for cid in course_ids:
        try:
            result = pipeline_generate(cid, openings_only=args.openings_only)
            if result:
                results[cid] = result
                if not args.preview:
                    if result.get("mode") == "full":
                        write_course_content(cid, result)
                    elif result.get("mode") == "opening_only":
                        write_course_opening(cid, result["opening"])
        except Exception as e:
            print(f"✗ 课程 #{cid} 错误: {e}")

    print(f"\n{'='*60}")
    print(f"流水线完成: {len(results)}/{len(course_ids)} 门课程成功")
    if not args.preview:
        print(f"  已写入 courses-data.js")


def write_course_content(course_id: int, result: dict):
    """Write full course content back to courses-data.js."""
    with open(COURSES_FILE) as f:
        content = f.read()
    
    opening = result["opening"]
    body = result["body"]
    full_content = f"## 开场\\n\\n{opening}\\n\\n{body}" if opening else body
    
    # Escape for JS template literal
    escaped = full_content.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    
    # Find the course block and replace content
    pattern = re.compile(
        r'(id:\s*' + str(course_id) + r',\s*title:\s*\'[^\']+\'\s*,\s*'
        r'desc:\s*\'[^\']+\'\s*,\s*'
        r'tags:\s*.+?\s*,\s*'
        r'content:\s*)`[\s\S]*?`(\s*,\s*quiz:)',
        re.DOTALL
    )
    
    new_content = content
    m = pattern.search(content)
    if m:
        new_content = pattern.sub(rf'\1`{escaped}`\2', content)
    else:
        # Fallback: simpler pattern
        start_marker = f"id: {course_id},"
        pos = content.find(start_marker)
        if pos >= 0:
            content_start = content.find("content: `", pos)
            content_end = content.find("`,\n", content_start + 12)
            if content_end < 0:
                content_end = content.find("`,\\", content_start + 12)
            if content_start >= 0 and content_end >= 0:
                new_content = content[:content_start+11] + escaped + content[content_end:]
    
    with open(COURSES_FILE, "w") as f:
        f.write(new_content)
    
    cn = count_chinese(full_content)
    print(f"  💾 #{course_id}: {cn} 中文字已写入")


def write_course_opening(course_id: int, new_opening: str):
    """Replace only the first paragraph (after title) with new opening."""
    with open(COURSES_FILE) as f:
        content = f.read()
    
    # Find the course block
    start_marker = f"id: {course_id},"
    pos = content.find(start_marker)
    if pos < 0:
        print(f"  ✗ 未找到课程 #{course_id}")
        return
    
    # Find content start
    content_start = content.find("## ", pos)
    if content_start < 0:
        content_start = content.find("# ", pos)
    if content_start < 0:
        print(f"  ✗ 未找到课程 #{course_id} 的正文")
        return
    
    # Find first paragraph after headers
    first_header_end = content.find("\\n", content_start)
    if first_header_end < 0:
        first_header_end = content_start + 50
    
    # Find end of first paragraph
    first_para_end = content.find("\\n\\n", first_header_end)
    if first_para_end < 0:
        first_para_end = content.find("\\n## ", first_header_end)
    if first_para_end < 0:
        first_para_end = first_header_end + 200
    
    # Replace: keep headers, replace first paragraph
    escape_opening = new_opening.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    new_content = content[:first_header_end+1] + escape_opening + content[first_para_end:]
    
    with open(COURSES_FILE, "w") as f:
        f.write(new_content)
    
    print(f"  💾 #{course_id}: 开头已替换")
