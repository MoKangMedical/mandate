#!/usr/bin/env python3
"""Emperor Group Chat Backend — Multi-emperor AI conversation API."""
import os, json, re, time
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx
from pathlib import Path

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
LOCAL_RESPONSES = {
    "秦始皇": "朕看此事，关键在统一号令。天下之事，最怕各行其是；制度一乱，再好的器物也会变成纷争之源。",
    "刘邦": "我看没那么玄。事情能不能成，先看人心，再看用人。会用人，粗茶淡饭也能打天下；不会用人，金山银山也守不住。",
    "项羽": "若只谈算计，未免少了气魄。大事当前，须有人敢冲在最前。只是我也承认，勇力若不能收束成法度，终究难久。",
    "汉武帝": "此题要从战略看。眼前得失不算最大，真正重要的是十年、二十年后的格局。敢不敢投入，决定能不能开疆拓土。",
    "曹操": "我更关心实际成效。名声、口号、姿态都可以放一边，能解决问题的人就用，能降低成本的法子就试。",
    "刘备": "成事不能只靠威势。人若不服，表面听命，心里未必归附。仁义不是软弱，而是让人愿意跟你走到最后。",
    "诸葛亮": "此事当分三层看：其一是目标，其二是资源，其三是执行。若三者不能相配，越勤奋越可能把局势推向失衡。",
    "孙权": "我赞成先守住基本盘。局面复杂时，不必急着争一时胜负，先稳住人、财、地，再寻找可以出手的窗口。",
    "唐太宗": "为政最忌自以为是。若能让不同意见进来，君主才不至于困在自己的判断里。以人为镜，正是为了少犯大错。",
    "武则天": "我看重的是能力和秩序。世俗成见常常把人挡在门外，但权力只问结果。谁能办事，谁就该站到台前。",
    "唐玄宗": "盛世最容易让人误判。人在顺境里会以为一切都稳固，其实危机常在繁华处发芽。此事不可只看表面光彩。",
    "宋太祖": "最好的办法，是把风险写进制度里。不要指望人人都忠诚，也不要逼人人都恐惧。让人没有必要造反，才是长久之计。",
    "王安石": "若问题已经积重难返，只靠修修补补是不够的。改革必然触动利益，若怕反对声，就永远只能守着旧病。",
    "苏轼": "诸位说得都重。我倒觉得，人也要留一点从容。制度要紧，成败要紧，但若失去通达之心，胜了也未必安稳。",
    "成吉思汗": "草原上判断很简单：能不能行动，能不能取胜，能不能让部众活下去。空谈太多，会错过最好的时机。",
    "忽必烈": "我更愿意兼收并用。不同制度、不同文化，各有可取之处。能把马背上的力量和农耕的秩序合起来，才是大格局。",
    "朱元璋": "我出身贫苦，最知道底下人怕什么。官府若只顾上头体面，不管百姓死活，迟早要出大乱子。",
    "朱棣": "天下不是守出来的。该迁都就迁都，该远航就远航，该用兵就用兵。权力若没有进取心，很快就会被人逼到墙角。",
    "康熙": "凡事不可偏激。既要有决断，也要有耐心；既要学新法，也不能轻弃根本。治理大国，贵在持久而不躁。",
    "雍正": "空话少说，账要算清，责任要压实。许多坏事不是没人知道，而是无人愿意承担执行的骂名。",
    "乾隆": "朕以为，气象也很重要。国家要有体面，制度要有章法，文化要能凝聚人心。只是自满二字，确实不可不防。",
    "慈禧": "权力场里，活下来本身就是本事。理想可以讲，但各方势力如何平衡，谁能被安抚，谁必须被压住，这些才是每日功课。",
    "孙中山": "我最关心的是天下是否为公。若制度只服务少数人，再强也不是长久之道。真正的新局面，要让普通人也有位置。",
}

class ChatRequest(BaseModel):
    topic: str
    participants: Optional[list[str]] = None
    max_responses: int = 5
    history: Optional[list[dict]] = None

class ChatResponse(BaseModel):
    messages: list[dict]
    participants: list[str]

class TurnRequest(BaseModel):
    topic: str = ""
    participants: Optional[list[str]] = None
    history: Optional[list[dict]] = None
    mode: str = "reply_to_user"

class TurnResponse(BaseModel):
    message: dict
    participants: list[str]

@app.post("/api/chat")
async def group_chat(req: ChatRequest):
    """Generate a multi-emperor conversation on a given topic."""
    # Select participants
    if req.participants and req.participants[0] == "all":
        participants = list(EMPEROR_PROFILES.keys())
    elif req.participants:
        participants = [p for p in req.participants if p in EMPEROR_PROFILES]
    else:
        participants = DEFAULT_PARTICIPANTS.copy()

    if len(participants) < 2:
        participants = DEFAULT_PARTICIPANTS.copy()

    if not DEEPSEEK_API_KEY:
        return local_chat_response(req.topic, participants, req.max_responses)

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

    except json.JSONDecodeError:
        return local_chat_response(req.topic, participants, req.max_responses)
    except Exception as e:
        return local_chat_response(req.topic, participants, req.max_responses)


def local_chat_response(topic: str, participants: list[str], max_responses: int) -> ChatResponse:
    clean_topic = topic[:36] + ("..." if len(topic) > 36 else "")
    messages = []
    for name in participants[:max_responses]:
        base = LOCAL_RESPONSES.get(name, "此事不可只看一端。权力、制度、人心与时势交织在一起，判断越急，越容易失准。")
        messages.append({"emperor": name, "message": f"谈到「{clean_topic}」，{base}"})
    return ChatResponse(messages=messages, participants=participants[:10])

@app.post("/api/turn")
async def dialogue_turn(req: TurnRequest):
    """Generate one DeepSeek-powered dialogue turn."""
    participants = resolve_participants(req.participants)
    speaker = choose_next_speaker(participants, req.history or [], req.mode)

    if not DEEPSEEK_API_KEY:
        raise HTTPException(503, "DeepSeek API key not configured on chat backend")

    prompt = build_turn_prompt(
        topic=req.topic,
        participants=participants,
        history=req.history or [],
        speaker=speaker,
        mode=req.mode,
    )

    try:
        content = await call_deepseek(prompt, max_tokens=700, temperature=0.85)
        message = parse_turn_response(content, speaker)
        return TurnResponse(message=message, participants=participants)
    except Exception as e:
        raise HTTPException(502, f"DeepSeek turn generation failed: {str(e)[:200]}")


def resolve_participants(participants: Optional[list[str]]) -> list[str]:
    if participants and participants[0] == "all":
        selected = list(EMPEROR_PROFILES.keys())
    elif participants:
        selected = [p for p in participants if p in EMPEROR_PROFILES]
    else:
        selected = DEFAULT_PARTICIPANTS.copy()
    if len(selected) < 2:
        selected = DEFAULT_PARTICIPANTS.copy()
    return selected[:10]


def choose_next_speaker(participants: list[str], history: list[dict], mode: str) -> str:
    emperor_turns = [m.get("emperor") for m in history if m.get("role") == "emperor" or m.get("emperor")]
    if not emperor_turns:
        return participants[0]
    last = emperor_turns[-1]
    try:
        start = (participants.index(last) + 1) % len(participants)
    except ValueError:
        start = len(emperor_turns) % len(participants)
    if mode == "reply_to_user":
        recent = set(emperor_turns[-2:])
        for i in range(len(participants)):
            candidate = participants[(start + i) % len(participants)]
            if candidate not in recent:
                return candidate
    return participants[start]


def build_turn_prompt(topic: str, participants: list[str], history: list[dict], speaker: str, mode: str) -> str:
    profiles_text = "\n".join(f"【{name}】{EMPEROR_PROFILES[name]}" for name in participants)
    history_lines = []
    for item in history[-14:]:
        role = item.get("role")
        if role == "user":
            history_lines.append(f"【用户】{item.get('message', '')}")
        else:
            history_lines.append(f"【{item.get('emperor', '帝王')}】{item.get('message', '')}")
    history_text = "\n".join(history_lines) or "（尚无对话）"
    mode_text = "回应用户刚刚的问题，同时可以点名回应其他帝王观点。" if mode == "reply_to_user" else "接着上一位帝王的观点发言，可以赞同、反驳或补充。"

    return f"""你是 Mandate 帝王群聊中的角色扮演引擎。你只生成一轮发言，不要一次生成整场对话。

## 参与帝王
{profiles_text}

## 当前总话题
{topic or "围绕当前对话继续讨论"}

## 已有对话
{history_text}

## 本轮发言者
{speaker}

## 任务
请只让【{speaker}】发言一轮。{mode_text}
要求：
1. 必须符合该帝王的历史身份、性格和语言气质。
2. 要自然接住已有上下文，不要像独立作文。
3. 发言控制在 80 到 180 个中文字符。
4. 不要使用 emoji，不要使用网络烂梗。
5. 只输出 JSON 对象，不要 Markdown，不要解释。

输出格式：
{{"emperor":"{speaker}","message":"..."}}
"""


async def call_deepseek(prompt: str, max_tokens: int, temperature: float) -> str:
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{DEEPSEEK_BASE}/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


def parse_turn_response(content: str, speaker: str) -> dict:
    text = content.strip()
    if text.startswith("```"):
        text = re.sub(r'^```\w*\n', '', text)
        text = re.sub(r'\n```$', '', text)
    data = json.loads(text)
    if isinstance(data, list):
        data = data[0]
    if not isinstance(data, dict):
        raise ValueError("DeepSeek returned non-object turn")
    emperor = data.get("emperor") or speaker
    message = data.get("message") or ""
    if emperor not in EMPEROR_PROFILES:
        emperor = speaker
    if not message.strip():
        raise ValueError("DeepSeek returned empty message")
    return {"role": "emperor", "emperor": emperor, "message": message.strip()}

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

@app.get("/")
async def root():
    root_dir = Path(__file__).resolve().parents[1]
    return FileResponse(root_dir / "chat.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
