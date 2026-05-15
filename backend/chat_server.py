#!/usr/bin/env python3
"""Emperor Group Chat Backend — Multi-emperor AI conversation API."""
import os, json, re, time
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI(title="Mandate Emperor Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# DeepSeek API config
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "") or os.environ.get("OPENAI_API_KEY", "")
DEEPSEEK_BASE = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"

# Emperor character profiles
EMPEROR_PROFILES = {
    "秦始皇": "嬴政，统一六国的始皇帝。霸气威严，喜欢谈论统一、制度、法治。说话简短有力，常用「朕」。性格：果决、多疑、控制欲强。代表名言：「朕为始皇帝，后世以计数。」",
    "刘邦": "汉高祖，从亭长到皇帝的草根逆袭。豁达大度，善于用人，幽默风趣。说话接地气，爱用大白话。性格：务实、灵活、慷慨。口头禅：大丈夫当如此也！",
    "项羽": "西楚霸王，力能扛鼎的悲剧英雄。骄傲、自负、重情义。说话充满豪气，爱谈勇武。性格：刚愎、浪漫、至死不认输。名言：力拔山兮气盖世。",
    "汉武帝": "刘彻，北逐匈奴的开疆帝王。雄心勃勃，好大喜功。喜欢谈战略和开疆拓土。性格：激进、好战、晚年悔悟。",
    "曹操": "魏武帝，乱世枭雄。多谋善断，实用主义。爱谈兵法、权谋和人才。性格：多疑、务实、文学气质。名言：宁我负人，毋人负我。",
    "刘备": "蜀汉昭烈帝，仁义之君。以德服人，重视感情。说话常带泪，重情重义。性格：坚韧、仁义、善于凝聚人心。名言：勿以善小而不为。",
    "诸葛亮": "蜀汉丞相，智慧的化身。说话引经据典，条理分明。性格：忠诚、谨慎、鞠躬尽瘁。名言：非淡泊无以明志。",
    "孙权": "吴大帝，守成之主。善于识人用人，年轻有为。说话务实，爱谈经营之道。性格：沉稳、善断、识人。",
    "唐太宗": "李世民，贞观之治的缔造者。善于纳谏，以史为镜。说话谦逊有涵养。性格：理性、善于反思、从善如流。名言：以铜为镜可以正衣冠。",
    "武则天": "中国唯一女皇帝。自信、果敢、不服传统。说话气场强大，不容置疑。性格：强势、聪慧、善于权谋。",
    "唐玄宗": "李隆基，开元盛世的缔造者和毁灭者。前半生英明后半生昏聩。说话带艺术气质。性格：多才、多情、晚节不保。",
    "宋太祖": "赵匡胤，杯酒释兵权的温和开创者。说话温和但坚定。性格：仁厚、重文轻武、善于用制度。名言：卧榻之侧岂容他人鼾睡。",
    "王安石": "北宋改革家，拗相公。说话激进，充满理想主义。性格：固执、清廉、不畏人言。名言：天命不足畏，祖宗不足法。",
    "苏轼": "苏东坡，千古第一文人。说话风趣幽默，乐观豁达。性格：旷达、多才、乐天知命。名言：一蓑烟雨任平生。",
    "成吉思汗": "铁木真，世界征服者。说话简短直接，充满力量。性格：雄才大略、冷酷、重视忠诚。名言：不要因为路远而踌躇。",
    "忽必烈": "元世祖，马背与农耕之间的帝王。说话务实，东西方思维兼具。性格：开放、务实、善于学习。",
    "朱元璋": "明太祖，乞丐皇帝。说话直白粗犷，爱用大白话。性格：勤政、多疑、狠辣。名言：朕本淮右布衣。",
    "朱棣": "明成祖永乐大帝，篡位者与开拓者。说话充满不安全感。性格：好大喜功、勤政、急于证明自己。名言：天子守国门。",
    "康熙": "清圣祖，千古一帝。说话沉稳老练，有国际视野。性格：博学、理性、善于学习。名言：凡事必躬亲。",
    "雍正": "清世宗，最孤独的皇帝。说话直接，不爱废话。性格：勤政、严苛、孤独。名言：为君难。",
    "乾隆": "清高宗，十全老人。说话自信满满，爱炫耀。性格：骄傲、好大喜功、自恋。名言：十全武功。",
    "慈禧": "慈禧太后，统治中国47年的女人。说话精明老练。性格：权术高超、保守、善于平衡。",
    "孙中山": "国父，民主革命先行者。说话充满理想和激情。性格：理想主义、坚韧、天下为公。",
}

# Predefined emperor groups for common topics
DEFAULT_PARTICIPANTS = ["秦始皇", "刘邦", "唐太宗", "康熙", "曹操"]

class ChatRequest(BaseModel):
    topic: str
    participants: Optional[list[str]] = None
    max_responses: int = 5
    history: Optional[list[dict]] = None

class ChatResponse(BaseModel):
    messages: list[dict]
    participants: list[str]

@app.post("/api/chat")
async def group_chat(req: ChatRequest):
    """Generate a multi-emperor conversation on a given topic."""
    if not DEEPSEEK_API_KEY:
        raise HTTPException(500, "DeepSeek API key not configured")

    # Select participants
    if req.participants and req.participants[0] == "all":
        participants = list(EMPEROR_PROFILES.keys())
    elif req.participants:
        participants = [p for p in req.participants if p in EMPEROR_PROFILES]
    else:
        participants = DEFAULT_PARTICIPANTS.copy()

    if len(participants) < 2:
        participants = DEFAULT_PARTICIPANTS.copy()

    # Build system prompt
    profiles_text = "\n".join([
        f"【{name}】{EMPEROR_PROFILES[name]}" 
        for name in participants[:10]  # Limit to 10 for quality
    ])

    history_text = ""
    if req.history:
        history_text = "\n## 之前的对话\n" + "\n".join([
            f"【{m['emperor']}】{m['message']}" for m in req.history[-10:]
        ])

    prompt = f"""你是一个帝王群聊的模拟器。以下是参与群聊的帝王角色设定：

{profiles_text}

{history_text}

## 当前话题
{req.topic}

## 要求
请让以上帝王围绕话题展开一场自然、有趣的群聊对话。每个帝王发言一次，展现其独特的性格和观点。帝王之间可以相互回应、争论或赞同。
对话要有历史依据，但可以用现代语言表达。每个帝王的发言要符合其性格特点和时代背景。
可以用现代词汇（如「改革」「战略」等），但不要用过于现代的梗。
输出格式为JSON数组，每个元素包含emperor（帝王名）和message（发言内容）两个字段。
只输出JSON，不要其他内容。

示例格式：
[{{"emperor":"秦始皇","message":"朕认为..."}},{{"emperor":"唐太宗","message":"以史为镜..."}}]"""

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                f"{DEEPSEEK_BASE}/chat/completions",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.9,
                    "max_tokens": 2000,
                }
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]

        # Parse JSON from response
        content = content.strip()
        if content.startswith("```"):
            content = re.sub(r'^```\w*\n', '', content)
            content = re.sub(r'\n```$', '', content)

        messages = json.loads(content)
        if not isinstance(messages, list):
            messages = [messages]

        return ChatResponse(
            messages=messages[:req.max_responses],
            participants=participants[:10]
        )

    except json.JSONDecodeError as e:
        raise HTTPException(500, f"Failed to parse AI response: {str(e)[:200]}")
    except Exception as e:
        raise HTTPException(500, f"Chat generation failed: {str(e)[:200]}")

@app.get("/api/emperors")
async def list_emperors():
    """List all available emperors for chat."""
    return {
        "emperors": [
            {"name": name, "preview": profile[:60] + "..."}
            for name, profile in EMPEROR_PROFILES.items()
        ]
    }

@app.get("/health")
async def health():
    return {"status": "ok", "emperors": len(EMPEROR_PROFILES)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
