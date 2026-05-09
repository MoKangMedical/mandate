"""Mandate Backend — Emperor Digital Avatar API Proxy"""
import os
import json
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Mandate API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", os.getenv("OPENAI_API_KEY", ""))
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# Load emperor data
import pathlib
DATA_PATH = pathlib.Path(__file__).parent.parent / "data" / "emperors.json"
try:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        EMPERORS = {e["id"]: e for e in json.load(f)}
except (FileNotFoundError, json.JSONDecodeError):
    EMPERORS = {}
    print(f"Warning: Could not load emperors from {DATA_PATH}")


class ChatRequest(BaseModel):
    emperor_id: str
    message: str
    history: list[dict] = []


class ChatResponse(BaseModel):
    reply: str
    emperor_name: str


@app.get("/api/health")
async def health():
    return {"status": "ok", "emperors": len(EMPERORS)}


@app.get("/api/emperors")
async def list_emperors():
    return [{"id": e["id"], "name": e["name"], "temple": e["temple"],
             "dynasty": e["dynasty"], "era": e["reign"][:4]} for e in EMPERORS.values()]


@app.get("/api/emperors/{emperor_id}")
async def get_emperor(emperor_id: str):
    emp = EMPERORS.get(emperor_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Emperor not found")
    return emp


def build_system_prompt(emp: dict) -> str:
    """Build the emperor's digital avatar system prompt."""
    dynasty_map = {
        "xia":"夏","shang":"商","zhou-w":"西周","zhou-e":"东周","qin":"秦",
        "han-w":"西汉","xin":"新","han-e":"东汉","sanguo":"三国","jin-w":"西晋",
        "jin-e":"东晋","nanbei":"南北朝","sui":"隋","tang":"唐","wudai":"五代",
        "song-n":"北宋","song-s":"南宋","liao":"辽","jin":"金","xixia":"西夏",
        "yuan":"元","ming":"明","qing":"清"
    }
    dynasty = dynasty_map.get(emp.get("dynasty",""), emp.get("dynasty",""))

    p = emp.get("avatar", {})
    return f"""你是{emp['name']}（{emp.get('temple','')}），{dynasty}时期的皇帝，在位时间{emp.get('reign','')}。

{p.get('prompt','')}

重要规则：
- 你是{emp['name']}本人，用第一人称说话（根据你的性格选择用"朕"或"我"）
- 你只知道你活着时发生的事（{emp.get('reign','')}及之前），不知道后世发生的事情
- 如果有人提到后世的事件、评价或科技，你会感到困惑、好奇或质疑
- 保持你的性格特点：{p.get('personality','')}
- 说话风格：{p.get('style','')}
- 回复长度控制在2-5句话，言简意赅
- 你是古代帝王，不要使用现代网络用语、表情符号或英文"""


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    emp = EMPERORS.get(req.emperor_id) if EMPERORS else None

    if not emp:
        emp = {"id": req.emperor_id, "name": "未知帝王", "temple": "",
               "dynasty": "", "reign": "", "avatar": {
                   "personality": "未知", "style": "常规",
                   "prompt": "你是一位中国古代帝王。"}}

    if not DEEPSEEK_API_KEY:
        raise HTTPException(status_code=503, detail="DeepSeek API key not configured")

    system_prompt = build_system_prompt(emp)
    messages = [{"role": "system", "content": system_prompt}]

    for h in req.history[-10:]:
        role = "user" if h.get("role") == "user" else "assistant"
        messages.append({"role": role, "content": h.get("content", "")})

    messages.append({"role": "user", "content": req.message})

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": DEEPSEEK_MODEL,
                "messages": messages,
                "temperature": 0.8,
                "max_tokens": 600
            }
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    data = resp.json()
    reply = data["choices"][0]["message"]["content"]

    return ChatResponse(reply=reply, emperor_name=emp["name"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
