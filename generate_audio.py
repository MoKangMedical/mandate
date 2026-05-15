#!/usr/bin/env python3
"""Generate MP3 audio for all Mandate courses using Edge TTS warm male voice."""
import re, os, sys, subprocess, shlex
from concurrent.futures import ThreadPoolExecutor, as_completed

AUDIO_DIR = "audio"
VOICE = "zh-CN-YunjianNeural"
RATE = "-8%"
MAX_WORKERS = 3

def extract_courses(filepath):
    with open(filepath, 'r') as f:
        raw = f.read()
    segs = raw.split('content: `')[1:]
    courses = []
    for i, seg in enumerate(segs):
        cid = i + 7
        close = seg.find('`,')
        if close < 0: close = seg.find('`')
        if close < 0: continue
        content_raw = seg[:close]
        content = content_raw.replace('\\n', '\n')
        courses.append((cid, content))
    return courses

def clean_for_speech(text):
    text = re.sub(r'[#>*`_|\-]', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'[「」]', '', text)
    text = re.sub(r'([。！？；])', r'\1 ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

def generate_audio(cid, text, outdir):
    outpath = os.path.join(outdir, f'lesson{cid}.mp3')
    if os.path.exists(outpath) and os.path.getsize(outpath) > 1000:
        return cid, outpath, os.path.getsize(outpath), True

    tmpfile = f'/tmp/mandate_tts_{cid}.txt'
    with open(tmpfile, 'w') as f:
        f.write(text)

    # Use shell=True because edge-tts has argument parsing issues in subprocess list mode
    cmd = f"edge-tts -v {shlex.quote(VOICE)} --rate={RATE} -f {shlex.quote(tmpfile)} --write-media {shlex.quote(outpath)}"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        if os.path.exists(outpath) and os.path.getsize(outpath) > 1000:
            os.remove(tmpfile)
            return cid, outpath, os.path.getsize(outpath), True
        else:
            print(f"  FAILED #{cid}: {result.stderr[:150]}", file=sys.stderr)
            if os.path.exists(tmpfile): os.remove(tmpfile)
            return cid, outpath, 0, False
    except Exception as e:
        print(f"  ERROR #{cid}: {e}", file=sys.stderr)
        if os.path.exists(tmpfile): os.remove(tmpfile)
        return cid, outpath, 0, False

def main():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    courses = extract_courses('js/courses-data.js')
    print(f"Found {len(courses)} courses")
    
    cleaned = [(cid, clean_for_speech(text)) for cid, text in courses]
    total_chars = sum(len(t) for _, t in cleaned)
    print(f"Total chars: {total_chars:,}, est. audio: ~{total_chars/250:.0f} min")
    
    completed = 0
    failed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(generate_audio, cid, text, AUDIO_DIR): cid for cid, text in cleaned}
        for future in as_completed(futures):
            cid, path, size, ok = future.result()
            if ok:
                completed += 1
                print(f"  #{cid:3d} OK  {size/1024:.0f}KB  [{completed}/{len(cleaned)}]")
            else:
                failed += 1
    print(f"\nDone: {completed} generated, {failed} failed")

if __name__ == '__main__':
    main()
