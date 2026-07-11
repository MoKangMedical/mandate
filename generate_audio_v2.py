#!/usr/bin/env python3
"""
Mandate Audio Generation v3.0 — Full-Course Narration
======================================================
Layer 1: Full course text cleaned for speech (NOT summary)
Layer 2: edge-tts zh-CN-YunyangNeural (rate -5%, natural pitch)
Layer 3: ffmpeg loudnorm (I=-16:TP=-1.5:LRA=9, 24000Hz, mono, 48kbps)
Layer 4: Quality audit

Usage: python3 generate_audio_v2.py [--force] [--courses 7,8,9]
"""
import json, os, re, shlex, shutil, subprocess, sys, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request

# ── Configuration ──────────────────────────────────────────────
AUDIO_DIR = "audio"
VOICE = "zh-CN-YunyangNeural"   # Professional male news voice
RATE = "-5%"                    # v3.0: slightly faster, more natural
PITCH = "+0Hz"                   # v3.0: natural pitch, no artificial change
BITRATE = "48k"
MAX_WORKERS = 3
# v3.0: Full text limits (much larger for full-course reading)
SCRIPT_MIN_CHARS = 200
SCRIPT_MAX_CHARS = 8000  # Full course text can be long

# ── DeepSeek API ───────────────────────────────────────────────
def _load_api_key():
    """Load DeepSeek API key from env or Hermes config."""
    if os.getenv("DEEPSEEK_API_KEY"):
        return os.getenv("DEEPSEEK_API_KEY", "").strip()

    config_path = os.path.expanduser("~/.hermes/config.yaml")
    if not os.path.exists(config_path):
        return ""

    try:
        import yaml  # type: ignore
    except Exception:
        yaml = None

    if yaml is not None:
        try:
            data = yaml.safe_load(Path(config_path).read_text()) or {}
            providers = data.get("providers", {})
            deepseek = providers.get("deepseek", {})
            if isinstance(deepseek, dict):
                if deepseek.get("api_key"):
                    return str(deepseek["api_key"]).strip()
                models = deepseek.get("models", {})
                if isinstance(models, dict):
                    for model_cfg in models.values():
                        if isinstance(model_cfg, dict) and model_cfg.get("api_key"):
                            return str(model_cfg["api_key"]).strip()
            model_cfg = data.get("model", {})
            if isinstance(model_cfg, dict) and model_cfg.get("provider") == "deepseek" and model_cfg.get("api_key"):
                return str(model_cfg["api_key"]).strip()
        except Exception:
            pass

    text = Path(config_path).read_text(errors="ignore")
    block = re.search(r'(?ms)^\\s*deepseek:\\s*\\n(?P<body>(?:^\\s{4}.*\\n?)*)', text)
    if block:
        key_match = re.search(r'(?m)^\\s{4}api_key:\\s*(.+?)\\s*$', block.group("body"))
        if key_match:
            return key_match.group(1).strip().strip("'\"")
    return ""

DEEPSEEK_KEY = _load_api_key()
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"


# ═══════════════════════════════════════════════════════════════
# Layer 1: Full Course Text → Spoken Script (v3.0)
# ═══════════════════════════════════════════════════════════════
def generate_spoken_script(title: str, content: str, course_id: int) -> str:
    """v3.0: Convert full course content to spoken narration script.
    Instead of summarizing into 150 chars, we take the FULL course text,
    clean it for speech, and return the complete narration script.
    """
    text = _clean_course_text(content)
    if not text.strip():
        return f"这一讲我们来看{title}。课程内容暂时无法加载，请稍后再试。"

    # Split into natural spoken segments (sentences/phrases)
    sentences = [s.strip() for s in re.split(r'[。！？；\n]+', text) if s.strip()]
    
    if len(sentences) < 2:
        return text[:SCRIPT_MAX_CHARS]
    
    # Build natural spoken script with pauses
    script_parts = []
    # Opening: course title as intro
    script_parts.append(f"帝王学课程。{title}。")
    
    for s in sentences:
        clean = s.strip('，、：； ""''「」()[]')
        if not clean and s:
            continue  # skip empty after cleaning punctuation
        if clean and len(clean) >= 2:
            script_parts.append(clean)
    
    full_script = "。".join(script_parts)
    
    # Enforce max length
    if len(full_script) > SCRIPT_MAX_CHARS:
        full_script = full_script[:SCRIPT_MAX_CHARS]
        # Try to end at a natural break
        last_period = full_script.rfind("。")
        if last_period > SCRIPT_MAX_CHARS * 0.7:
            full_script = full_script[:last_period+1]
    
    if len(full_script) < SCRIPT_MIN_CHARS:
        # Fallback: use cleaned text directly
        full_script = text[:SCRIPT_MAX_CHARS]
    
    return full_script


def _clean_course_text(text: str) -> str:
    """Strip markdown/noise while keeping readable Chinese prose."""
    text = text.replace("\\n", "\n")
    text = re.sub(r'[#>*`_|\-]', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'[「」"()]', '', text)
    text = re.sub(r'\n{2,}', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()


def build_fallback_script(title: str, text: str) -> str:
    """Deterministic fallback that still sounds like a spoken course intro."""
    cleaned = _clean_course_text(text)
    sentences = [s.strip() for s in re.split(r'[。！？；\n]+', cleaned) if s.strip()]
    intro = f"这一讲我们来看{title}。"
    bridge = "你会看到，这门课真正要讲的，不只是故事本身，更是背后的权力逻辑、制度选择和历史后果。"
    closing = "听完以后，你会更容易理解这段历史为什么会走到那一步。"
    booster = "重点不是记住细节，而是看清关键人物如何在局势、资源和人心之间做选择。"

    summary_parts = []
    reserved = len(intro) + len(bridge) + len(closing)
    body_budget = max(0, SCRIPT_MAX_CHARS - reserved)
    body_length = 0
    for sentence in sentences:
        sentence = re.sub(r'\s+', '', sentence).strip("，、；： ")
        if not sentence:
            continue
        add_len = len(sentence) + (1 if summary_parts else 0)
        if body_length + add_len > body_budget:
            break
        summary_parts.append(sentence)
        body_length += add_len
        if body_length >= min(260, body_budget):
            break

    summary = "，".join(summary_parts)
    script = intro + bridge
    if summary:
        script += summary
        if not script.endswith(("。", "！", "？")):
            script += "。"

    if len(script) + len(closing) < SCRIPT_MIN_CHARS and len(script) + len(booster) + len(closing) <= SCRIPT_MAX_CHARS:
        script += booster

    script += closing
    return script[:SCRIPT_MAX_CHARS]


# ═══════════════════════════════════════════════════════════════
# Layer 2: edge-tts Neural TTS
# ═══════════════════════════════════════════════════════════════
def synthesize_audio(script: str, outpath: str, course_id: int) -> bool:
    """Synthesize speech with edge-tts zh-CN-YunyangNeural."""
    tmpfile = f"/tmp/mandate_v2_{course_id}.txt"
    with open(tmpfile, "w") as f:
        f.write(script)

    # shell=True required for --rate=-8% (subprocess list mode fails with %)
    cmd = (
        f"edge-tts -v {shlex.quote(VOICE)} "
        f"--rate={RATE} --pitch={PITCH} "
        f"-f {shlex.quote(tmpfile)} "
        f"--write-media {shlex.quote(outpath)}"
    )
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=120
        )
        os.remove(tmpfile)
        return os.path.exists(outpath) and os.path.getsize(outpath) > 1000
    except Exception as e:
        print(f"  ✗ TTS error #{course_id}: {e}", file=sys.stderr)
        if os.path.exists(tmpfile):
            os.remove(tmpfile)
        return False


# ═══════════════════════════════════════════════════════════════
# Layer 3: ffmpeg Loudnorm + Format Standardization
# ═══════════════════════════════════════════════════════════════
def normalize_audio(raw_path: str, final_path: str, course_id: int) -> bool:
    """Apply loudnorm & reformat to 24000Hz mono 48kbps."""
    cmd = [
        "ffmpeg", "-y", "-i", raw_path,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=9",
        "-ar", "24000", "-ac", "1", "-b:a", BITRATE,
        final_path,
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=True)
        if os.path.exists(raw_path):
            os.remove(raw_path)
        return os.path.exists(final_path) and os.path.getsize(final_path) > 1000
    except subprocess.CalledProcessError:
        # Fallback: simple volume normalization
        cmd2 = [
            "ffmpeg", "-y", "-i", raw_path,
            "-af", "volume=1.2",
            "-ar", "24000", "-ac", "1", "-b:a", BITRATE,
            final_path,
        ]
        try:
            subprocess.run(cmd2, capture_output=True, text=True, timeout=60)
            if os.path.exists(raw_path):
                os.remove(raw_path)
            return os.path.exists(final_path) and os.path.getsize(final_path) > 1000
        except Exception as e:
            print(f"  ✗ ffmpeg error #{course_id}: {e}", file=sys.stderr)
            return False


# ═══════════════════════════════════════════════════════════════
# Layer 4: Quality Audit
# ═══════════════════════════════════════════════════════════════
def audit_audio(filepath: str) -> dict:
    """Audit a single audio file. Returns dict with grade and issues."""
    result = {"file": os.path.basename(filepath), "grade": "A", "issues": []}

    if not os.path.exists(filepath):
        return {**result, "grade": "F", "issues": ["missing"]}

    size = os.path.getsize(filepath)
    if size < 1000:
        result["issues"].append(f"too small: {size}B")
        result["grade"] = "F"
        return result

    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", filepath,
    ]
    try:
        probe = json.loads(subprocess.check_output(cmd, text=True, timeout=10))
    except Exception as e:
        result["issues"].append(f"ffprobe failed: {e}")
        result["grade"] = "C"
        return result

    fmt = probe.get("format", {})
    duration = float(fmt.get("duration", 0))
    streams = probe.get("streams", [])
    audio = next((s for s in streams if s.get("codec_type") == "audio"), {})

    # Duration check (25-90s for spoken scripts)
    if duration < 20:
        result["issues"].append(f"too short: {duration:.1f}s")
        if result["grade"] == "A": result["grade"] = "B"
    elif duration > 120:
        result["issues"].append(f"too long: {duration:.1f}s")
        if result["grade"] == "A": result["grade"] = "B"

    # Sample rate
    sr = int(audio.get("sample_rate", 0))
    if sr != 24000:
        result["issues"].append(f"sample rate: {sr}Hz (expected 24000)")
        result["grade"] = "C"

    # Channels
    ch = int(audio.get("channels", 0))
    if ch != 1:
        result["issues"].append(f"channels: {ch} (expected 1)")
        if result["grade"] == "A": result["grade"] = "B"

    # Bitrate
    br = int(fmt.get("bit_rate", 0)) // 1000
    if br < 40 or br > 72:
        result["issues"].append(f"bitrate: {br}kbps (expected 48-64)")
        if result["grade"] == "A": result["grade"] = "B"

    result["specs"] = {
        "duration": f"{duration:.1f}s",
        "sample_rate": f"{sr}Hz",
        "channels": "mono" if ch == 1 else str(ch),
        "bitrate": f"{br}kbps",
        "size_kb": size // 1024,
    }
    return result


# ═══════════════════════════════════════════════════════════════
# Course Extraction
# ═══════════════════════════════════════════════════════════════
def extract_courses(filepath: str) -> list:
    """Extract (id, title, content) from a JS/HTML file containing course objects."""
    with open(filepath, "r") as f:
        raw = f.read()

    courses = []
    content_markers = list(re.finditer(r'content\s*:\s*`', raw))
    for marker in content_markers:
        start = marker.end()
        close = raw.find('`,', start)
        if close < 0:
            close = raw.find('`\n', start)
        if close < 0:
            continue
        content_raw = raw[start:close]
        content = content_raw.replace('\\n', '\n')

        # Find course id and title from the segment before this content
        before = raw[:marker.start()]
        id_matches = list(re.finditer(r'id\s*:\s*(\d+)', before))
        id_match = id_matches[-1] if id_matches else None
        title_matches = list(re.finditer(r"title\s*:\s*'([^']+)'", before))
        title_match = title_matches[-1] if title_matches else None
        if not title_match:
            title_matches = list(re.finditer(r'title\s*:\s*"([^"]+)"', before))
            title_match = title_matches[-1] if title_matches else None

        if id_match:
            cid = int(id_match.group(1))
            title = title_match.group(1) if title_match else f"课程{cid}"
            courses.append((cid, title, content))

    return courses


def extract_all_courses() -> list:
    """Extract inline overview courses and extended course data."""
    courses = []
    if os.path.exists("courses.html"):
        courses.extend(c for c in extract_courses("courses.html") if c[0] <= 6)
    courses.extend(extract_courses("js/courses-data.js"))
    seen = set()
    unique = []
    for cid, title, content in sorted(courses, key=lambda item: item[0]):
        if cid in seen:
            continue
        seen.add(cid)
        unique.append((cid, title, content))
    return unique


# ═══════════════════════════════════════════════════════════════
# Full Pipeline (per course)
# ═══════════════════════════════════════════════════════════════
def process_course(course_id: int, title: str, content: str, outdir: str, force: bool) -> tuple:
    """Run the full 4-layer pipeline for one course."""
    final_path = os.path.join(outdir, f"lesson{course_id}.mp3")

    # Check if already exists and passes audit
    if not force and os.path.exists(final_path) and os.path.getsize(final_path) > 1000:
        audit = audit_audio(final_path)
        if audit["grade"] == "A":
            return course_id, final_path, "skipped (A-grade)", audit["specs"]["duration"]

    # Layer 1: DeepSeek spoken script
    print(f"  [{course_id}] L1: Generating spoken script...", flush=True)
    script = generate_spoken_script(title, content, course_id)
    print(f"  [{course_id}] L1: Script {len(script)} chars", flush=True)

    # Layer 2: edge-tts synthesis
    raw_path = os.path.join(outdir, f"lesson{course_id}_raw.mp3")
    print(f"  [{course_id}] L2: TTS synthesis...", flush=True)
    if not synthesize_audio(script, raw_path, course_id):
        return course_id, final_path, "FAILED (TTS)", "0s"

    # Layer 3: ffmpeg loudnorm
    print(f"  [{course_id}] L3: ffmpeg normalize...", flush=True)
    if not normalize_audio(raw_path, final_path, course_id):
        # If normalize fails but raw exists, keep raw as fallback
        if os.path.exists(raw_path):
            shutil.move(raw_path, final_path)
            print(f"  [{course_id}] L3: Normalize failed, kept raw", flush=True)

    # Layer 4: Quality audit
    audit = audit_audio(final_path)
    grade = audit["grade"]
    duration = audit.get("specs", {}).get("duration", "?")
    status = f"{grade}-grade" if grade != "F" else "FAILED (audit)"
    return course_id, final_path, status, duration


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Mandate Audio v2.0.0")
    parser.add_argument("--force", action="store_true", help="Regenerate even if A-grade exists")
    parser.add_argument("--courses", type=str, help="Comma-separated course IDs (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="Extract courses without generating")
    args = parser.parse_args()

    os.makedirs(AUDIO_DIR, exist_ok=True)

    # Extract courses
    courses = extract_all_courses()
    print(f"Extracted {len(courses)} courses")

    if args.courses:
        target_ids = {int(x) for x in args.courses.split(",")}
        courses = [(cid, t, c) for cid, t, c in courses if cid in target_ids]
        print(f"Filtered to {len(courses)} courses: {sorted(target_ids)}")

    if args.dry_run:
        for cid, title, content in courses:
            cn = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', content))
            print(f"  #{cid}: {title} ({cn} cn chars)")
        return

    print(f"Voice: {VOICE} | Rate: {RATE} | Pitch: {PITCH}")
    print(f"Loudnorm: I=-16:TP=-1.5:LRA=9 | {24000}Hz mono {BITRATE}")
    print(f"Workers: {MAX_WORKERS} | Force: {args.force}")
    print(f"{'─'*60}")

    start_time = time.time()
    completed = {"A": 0, "B": 0, "C": 0, "skipped": 0, "failed": 0}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(process_course, cid, title, content, AUDIO_DIR, args.force): cid
            for cid, title, content in courses
        }
        for future in as_completed(futures):
            cid = futures[future]
            try:
                cid_result, path, status, duration = future.result()
                status_lower = status.lower()
                if "skipped" in status_lower:
                    completed["skipped"] += 1
                elif "a-grade" in status_lower:
                    completed["A"] += 1
                elif "b-grade" in status_lower:
                    completed["B"] += 1
                elif "c-grade" in status_lower:
                    completed["C"] += 1
                else:
                    completed["failed"] += 1
                done = sum(completed.values())
                print(f"  #{cid:3d} {status:20s} {duration:>6s}  [{done}/{len(courses)}]", flush=True)
            except Exception as e:
                completed["failed"] += 1
                print(f"  #{cid:3d} CRASH: {e}", flush=True)

    elapsed = time.time() - start_time
    print(f"\n{'═'*60}")
    print(f"Done in {elapsed:.0f}s")
    print(f"   A-grade: {completed['A']} | B-grade: {completed['B']} | C-grade: {completed['C']}")
    print(f"   Skipped: {completed['skipped']} | Failed: {completed['failed']}")

    # Full audit at end if any files were generated
    if completed["A"] + completed["B"] + completed["C"] > 0:
        print(f"\nRunning full audit...")
        time.sleep(1)
        audit_results = {}
        for cid, title, _ in courses:
            fp = os.path.join(AUDIO_DIR, f"lesson{cid}.mp3")
            audit_results[cid] = audit_audio(fp)

        grades = {"A": 0, "B": 0, "C": 0, "F": 0}
        issues = []
        for cid, r in sorted(audit_results.items()):
            grades[r["grade"]] += 1
            if r["grade"] != "A":
                issues.append((cid, r["grade"], r["issues"]))

        print(f"   Final: A={grades['A']} B={grades['B']} C={grades['C']} F={grades['F']}")
        if issues:
            print(f"   Issues ({len(issues)}):")
            for cid, grade, iss in issues:
                print(f"     #{cid} [{grade}]: {', '.join(iss)}")


if __name__ == "__main__":
    main()
