# Mandate（帝王学分析师）— 项目交接文档

> 给 Codex 的完整上下文。最后更新：2026-05-17

---

## 一、项目概览

| 项目 | 值 |
|------|-----|
| **名称** | Mandate — 帝王学分析师 |
| **定位** | 94 门中国帝王史课程的交互式学习平台 |
| **Repo** | `MoKangMedical/mandate`（GitHub） |
| **线上** | https://mokangmedical.github.io/mandate/ |
| **工作目录** | `/root/.openclaw/workspace/mandate/` |
| **分支** | `main`（开发）→ merge 到 `gh-pages`（部署） |
| **风格** | 暗黑帝王学 + 吉卜力温暖（Imperial Ghibli） |

---

## 二、技术栈

- **前端**：纯静态 HTML/CSS/JS，GitHub Pages 托管
- **数据**：单文件 `js/courses-data.js`（1.07MB, 7533 行），94 门课全在其中
- **字体**：Noto Serif SC（标题）+ Inter（正文），Google Fonts CDN
- **音频**：MP3，edge-tts + ffmpeg 生成，94 个文件 36.2MB
- **后端**：FastAPI (`backend/chat_server.py`)，端口 8003，systemd 管理
- **AI**：DeepSeek API（deepseek-chat 模型），base URL `https://api.deepseek.com/v1`

---

## 三、文件结构

```
mandate/
├── DESIGN.md               # ⭐ Google DESIGN.md 设计系统（17KB, 456行）
├── tailwind.theme.json     # Tailwind 导出
├── tokens.json             # W3C DTCG 导出
├── index.html              # 首页 — 94课程宫格 + 搜索筛选
├── courses.html            # 课程详情页 — 卡片、音频播放器、?course=N 直链
├── chat.html               # 皇帝群聊 — 23位皇帝 AI 对话
├── js/
│   ├── courses-data.js     # ⭐ 核心数据 — 94门课完整内容（1.07MB）
│   ├── courses-meta.js     # 轻量元数据（20KB）— 标题/描述/标签
│   └── data.js             # 朝代数据
├── audio/                  # 94个MP3（v2.0.0 标准）
├── data/
│   ├── emperors.json       # 皇帝资料
│   └── courses_*.json      # 备份JSON（可能过期，以 courses-data.js 为准）
├── backend/
│   └── chat_server.py      # FastAPI 群聊后端（173行，端口 8003）
└── generate_audio_v2.py    # 音频生成脚本（v2.0.0 4层管线）
```

---

## 四、课程数据格式（courses-data.js）

每门课是 `COURSES_EXTENDED` 数组中的一个对象：

```js
{
    id: 7,
    title: '秦始皇（上）：统一六国的战略与执行',
    desc: 'Short description',
    tags: "核心|45分钟",                    // string 或 array
    content: `## Title\n\n### Section...`,  // 模板字面量，多行 OK
    quiz: [{"q": "问题", "opts": ["A","B","C","D"], "answer": 0}, ...]
}
```

- **课程编号**：#7 ~ #100（共 94 门）
- **#1~#6**：概述课程，硬编码在 `courses.html` 中，不在扩展数据里

---

## 五、当前状态

### ✅ 已完成
- [x] 94 门课全部有内容
- [x] 首页宫格渲染 + 搜索 + 标签筛选
- [x] 课程详情弹窗 + 测验系统
- [x] 皇帝群聊（23 位皇帝 AI 对话）
- [x] DESIGN.md 设计系统（0 lint errors）
- [x] 94 门音频 v2.0.0 全部 A-grade（36.2MB, 105 分钟）
- [x] 部署到 gh-pages

### 📊 内容字符数分布

| 范围 | 数量 | 备注 |
|------|------|------|
| <1000 字 | 22 门 | ⚠️ 需要扩充 |
| 1000-1999 | 14 门 | ⚠️ 偏短 |
| 2000-2999 | 6 门 | 接近达标 |
| 3000-4999 | 39 门 | ✅ 达标 |
| 5000+ | 13 门 | ✅ 丰富 |

**总计**：283,736 中文字，平均 3,018 字/课  
**最短板**：#68（552字）、#85（567字）、#53（580字）、#94（580字）、#76（584字）  
**最长板**：#87 康熙（11,851字）、#17 汉武帝（6,690字）

### 📋 待办（建议 Codex 推进）
1. **扩充 42 门低于 3000 字的课程** — 优先 22 门低于 1000 字的
2. **同步 courses-meta.js** — 每次改 courses-data.js 后重新生成
3. **聊天页后端**已在运行（端口 8003），前端可能还需调优
4. **音频播放器 HTML**可在课程卡片中进一步美化

---

## 六、内容编辑安全规则（CRITICAL）

1. **绝对不要用 `replace_all=true`** 操作 `courses-data.js` — 已验证会导致文件损坏（曾经 76→96 乱码）
2. **用 Python 脚本做精准编辑**：读取文件 → 找到 `id: N,` 标记 → 定位模板字面量 → 替换内容
3. **模板字面量陷阱**：内容用反引号包裹，结束符可能是 `` `,\n `` 或 `` `,\\n ``（课程 #14 就是后者）
4. **编辑后立即全量计数**：验证所有 94 门课未被破坏

### 中文字符计数方法
```python
import re
cn_chars = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', text))
```

---

## 七、音频生成（v2.0.0）

### 4 层管线
```
L1 DeepSeek 口播稿 → L2 edge-tts → L3 ffmpeg loudnorm → L4 质量审计
   150-300字             YunyangNeural   I=-16:TP=-1.5:LRA=9   A-grade验证
                         rate -8%        24000Hz mono 48kbps
                         pitch -2Hz
```

### 关键参数
- **语音**：`zh-CN-YunyangNeural`（沉稳新闻腔，适合帝王学）
- **文件**：`audio/lesson{N}.mp3`，每段 50-70 秒，~350KB
- **总大小**：36.2MB（旧版 184MB，压缩 80%）
- **生成脚本**：`generate_audio_v2.py`（支持 `--force` 重生成、`--courses 7,8,9` 指定课程）
- **DeepSeek API Key**：从 `~/.hermes/config.yaml` 读取

### 音频嵌入 HTML
```html
<audio controls preload="none">
  <source src="audio/lesson7.mp3" type="audio/mpeg">
</audio>
```

---

## 八、设计系统（DESIGN.md）

### 核心规则（AI 生成 UI 时必须遵守）
1. **金色 `#e2b64f`** 是唯一交互强调色 — 红色 `#c43a31` 仅用于印章/紧急
2. **绝不纯黑** — 最深色 `#09090b`（深墨色）
3. **萤火虫光晕** `{shadows.firefly-glow}` 用于所有浮层元素
4. **径向渐变**偏移到边缘，不居中
5. **Hover** = 上浮 `translateY(-4px)` + 金色阴影
6. **字体**：Noto Serif SC（标题）、Inter（正文）

### 设计 Token 文件
- `DESIGN.md` — 权威规范（22色, 9级字体, 4级圆角, 7级间距, 6级阴影, 15组件）
- `tailwind.theme.json` — Tailwind 导出
- `tokens.json` — W3C DTCG 格式

---

## 九、聊天后端

- **文件**：`backend/chat_server.py`（173 行 FastAPI）
- **端口**：8003
- **Systemd**：`mandate-chat.service`（active, auto-restart）
- **环境变量**：`DEEPSEEK_API_KEY` 在 `/etc/systemd/system/mandate-chat.service.d/` 中配置
- **端点**：`POST /chat`，23 位皇帝角色扮演对话
- **重启**：`systemctl restart mandate-chat.service`

---

## 十、部署流程

```bash
cd /root/.openclaw/workspace/mandate

# 开发在 main 分支
git add -A && git commit -m "描述改动"
git push origin main

# 部署到 gh-pages
git checkout gh-pages
git merge main -m "deploy: 描述"
git push origin gh-pages
git checkout main

# 验证
curl -sL -o /dev/null -w "%{http_code}" "https://mokangmedical.github.io/mandate/"
# 应返回 200
```

---

## 十一、已知陷阱

| 陷阱 | 说明 |
|------|------|
| **patch replace_all** | 在 courses-data.js 上使用会导致文件损坏，绝对禁用 |
| **模板字面量结束符** | 有 `` `,\n `` 和 `` `,\\n `` 两种变体（#14 是后者） |
| **courses-meta.js 不同步** | 改 courses-data.js 后必须重新生成 courses-meta.js |
| **音频 extra 文件** | 旧版 184MB，新版 36.2MB，注意磁盘空间 |
| **首页不载入 courses-data.js** | 首页只用 courses-meta.js（20KB），完整数据在 courses.html 中按需加载 |

---

## 十二、下一步建议

1. **扩充 22 门低于 1000 字的课程**到 3000+ 字（最重要）
2. 扩充剩余 20 门 1000-2999 字的课程
3. 每次扩充后重新生成 `courses-meta.js`
4. 每次扩充后重新生成对应课程的音频（`python3 generate_audio_v2.py --force --courses N`）
5. 为课程卡片添加更精致的音频播放器 UI（参考 DESIGN.md 组件规范）
6. 聊天页前端可能需要移动端适配优化

---

*生成时间：2026-05-17 · 工作目录：/root/.openclaw/workspace/mandate/*
