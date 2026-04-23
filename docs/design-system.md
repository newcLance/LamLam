# Game Tracker 黑白灰设计系统

> 最后更新：2026-04-23
> 适用范围：Game Tracker 全站（首页 / 详情页 / 对比页 / 未来新增页面）
> 所有新增页面和迭代，**必须过一遍本文档评审**

---

## 1. 设计原则

| 原则 | 说明 |
|------|------|
| **纯黑白灰** | 全站零彩色。背景、文字、边框、按钮、标签、卡片——一律只用黑、白、灰三个色阶 |
| **无 Emoji** | UI 层面禁止使用任何 Emoji 图标。数据内容（如 B站视频标题）中的用户生成 Emoji 不限制 |
| **小圆角** | 圆角 ≤ 8px，体现硬核质感。禁止 rounded-2xl (16px) 以上的大圆角 |
| **截图为王** | 截图是唯一的色彩来源。UI 本身退到最低存在感，让游戏画面说话 |
| **信息密度适中** | 参考 Interface In Game 的疏密节奏：模块间大留白(56px)，模块内紧凑 |

---

## 2. 色彩系统

### 2.1 Surface 色阶（背景）

| Token | HEX | 用途 |
|-------|-----|------|
| `surface-0` | `#0c0c0c` | 页面底色、header 背景 |
| `surface-1` | `#141414` | 卡片/面板背景 |
| `surface-2` | `#1c1c1c` | 输入框/hover 态/次级面板/占位 |
| `surface-3` | `#252525` | 表头/最深层次背景 |

### 2.2 前景色（文字）

| Token | 用途 |
|-------|------|
| `text-white` | 标题、游戏名、active 状态、按钮主文字 |
| `text-neutral-300` | body 默认文字（base 层） |
| `text-neutral-400` | 次要正文、标签文字、链接按钮、来源引用 |
| `text-neutral-500` | header nav、维度标签、分类计数 |
| `text-neutral-600` | 占位文字、公司名、日期、锚点导航默认 |
| `text-neutral-700` | 无截图时的占位字母 |
| `text-black` | 白色实心按钮上的文字 |

> **禁止使用**：任何 `text-{color}-*` 彩色类（如 text-blue-400、text-amber-400 等）

### 2.3 边框

| Token | 值 | 用途 |
|-------|----|------|
| `border-bdr` | `rgba(255,255,255,.08)` | 默认边框（卡片/面板/分割线/header 底线） |
| `border-white/10` | — | 按钮边框、feature 标签边框 |
| `border-white/20` | — | hover 态边框、focus 态边框 |
| `border-white/30` | — | hover 加深态（对比按钮） |
| `border-white/[.04]` | — | 列表项分割线 |
| `border-white/[.06]` | — | feature pills 边框 |
| `border-white/[.08]` | — | story/aesthetic 卡片边框 |
| `border-white/5` | — | story 卡片内部维度分割 |

### 2.4 透明白色层级（背景叠加）

| 值 | 用途 |
|----|------|
| `bg-white/[.02]` | story/aesthetic 卡片底色 |
| `bg-white/[.04]` | 对比表格高亮行 |
| `bg-white/[.06]` | 返回按钮/feature 标签/链接按钮/对比按钮/关键词高亮 |
| `bg-white/[.08]` | B站排名第二/badge |
| `bg-white/5` | tab active 背景 / lightbox 控件 |
| `bg-white/10` | hover 态 / B站排名第一 / 共同点标签 |
| `bg-white/15` | lightbox 控件 hover / 截图放大镜 |

### 2.5 Accent 色

```
accent: #ffffff
```

accent = 白色。用于时间线圆点、模块标题竖条等需要"强调但不跳色"的场景。

---

## 3. 排版系统

### 3.1 字体

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
```

系统默认无衬线字体栈，不引入额外字体文件。

### 3.2 字号层级

| 层级 | Class | px | 用途 |
|------|-------|----|------|
| H1 | `text-4xl` | 36px | 首页标题 "Game Tracker" |
| H1（详情） | `text-3xl` | 30px | 游戏名称 |
| H2 | `text-lg` | 18px | 模块标题（官网截图、时间线...） |
| H2（对比） | `text-base` | 16px | 对比页模块标题 |
| Body | `text-sm` | 14px | 正文、描述、公司名 |
| Body（数据） | `text-[13.5px]` | 13.5px | 体验清单正文、审美偏好正文 |
| Caption | `text-xs` | 12px | 标签、来源、日期、维度标签 |
| Micro | `text-[11px]` | 11px | 卡片公司名、截图日期、维度 label |
| Nano | `text-[10px]` | 10px | story/aesthetic 分类标签（SCENE/COSTUME..） |
| Mini | `text-[9px]` | 9px | 共同点 badge |

### 3.3 字重

| Class | 用途 |
|-------|------|
| `font-extrabold` | H1 标题、品牌名 "GAME TRACKER"、story/aesthetic 分类标签 |
| `font-bold` | H2 模块标题、维度标签、体验清单标题、日期、排名序号 |
| `font-semibold` | 卡片游戏名、截图标题、对比页 header、tab 文字 |
| `font-medium` | feature 标签、lightbox 计数器、B站视频标题 |
| `font-normal` | 默认正文 |
| `font-black` | 无截图占位字母 |

### 3.4 行高

| 值 | 用途 |
|----|------|
| `leading-tight` | H1 标题 |
| `leading-relaxed` | 正文描述 |
| `leading-7` (28px) | 数据正文（体验清单/审美偏好/故事维度） |

---

## 4. 间距系统

基于 **4px 基础网格**。

### 4.1 模块间距

| 值 | Class | 用途 |
|----|-------|------|
| 56px | `mb-14` | 详情页模块间距（截图→时间线→体验→故事→审美→竞品） |
| 64px | `mb-16` | 首页品类分组间距 |

### 4.2 内部间距

| 值 | Class | 用途 |
|----|-------|------|
| 24px | `mb-6` | 模块标题与内容间距 |
| 20px | `mb-5` / `gap-5` | 子模块间距、体验清单网格 gap |
| 16px | `mb-4` / `gap-4` | 标题行与描述、截图网格 gap |
| 12px | `mb-3` / `gap-3` | 截图标题与网格、卡片网格 gap |

### 4.3 页面边距

| 值 | Class | 用途 |
|----|-------|------|
| 24px | `px-6` | 页面内容区水平 padding |
| 40px | `pt-10` | 详情页 Hero 顶部 padding |
| 64px | `pt-16` | 首页标题顶部 padding |

### 4.4 最大宽度

| 值 | Class | 用途 |
|----|-------|------|
| 1152px | `max-w-6xl` | 首页、header |
| 1024px | `max-w-5xl` | 详情页内容区 |

---

## 5. 圆角系统

全局 Tailwind config 覆盖：

| Token | 值 | 用途 |
|-------|----|------|
| `rounded` (DEFAULT) | 4px | 卡片、按钮、标签、输入框 |
| `rounded-sm` | 2px | 关键词高亮 `<b>` |
| `rounded-md` | 6px | 对比页截图缩略图 |
| `rounded-lg` | 6px | lightbox 计数器 |
| `rounded-xl` | 8px | lightbox 关闭按钮、截图容器、体验清单子卡片 |
| `rounded-2xl` | 8px | lightbox 前后翻页按钮、体验清单/竞品推荐外壳 |
| `rounded-full` | 50% | 模块标题竖条、时间线圆点、锚点导航圆点 |

> **禁止**使用超过 8px 的非 full 圆角。

---

## 6. 组件规范

### 6.1 按钮

| 类型 | 样式 | 用途 |
|------|------|------|
| **Primary（实心白）** | `bg-white text-black font-bold rounded` hover: `bg-neutral-200` | 访问官网 CTA、提交心愿 |
| **Secondary（透明白）** | `bg-white/[.06] text-neutral-400 border border-white/[.06] rounded` hover: `bg-white/10 text-white` | 返回列表、访问页面、feature 标签 |
| **Ghost（对比按钮）** | `bg-white/[.06] text-white border border-white/20 rounded-xl` hover: `bg-white/10 border-white/30` | 一键对比 |
| **回到顶部** | `bg-white text-black rounded w-10 h-10` | 固定右下角 |

### 6.2 卡片

```
bg-surface-1 border border-bdr rounded
hover: border-white/20
```

- 封面区域：`pt-[56.25%]`（16:9 固定比例）
- 信息区：`px-3 py-2.5`
- 游戏名：`font-semibold text-[13px] text-white truncate`
- 公司名：`text-[11px] text-neutral-600`

### 6.3 数据卡片（Story / Aesthetic）

```
rounded p-5 border border-white/[.08] bg-white/[.02]
```

- 分类标签：`text-[10px] font-extrabold tracking-widest uppercase text-neutral-500`
- 标题：`text-sm font-bold text-white`
- 正文：`text-[13.5px] leading-7 text-neutral-400 data-text`

### 6.4 模块标题

```html
<h2 class="text-lg font-bold flex items-center gap-2">
  <span class="w-1 h-5 rounded-full bg-white inline-block"></span>
  标题文字
</h2>
```

左侧 1×5px 白色竖条 + 18px 加粗标题。

### 6.5 Lightbox

- 背景：`bg-black/95`
- 控件：`bg-white/5` hover `bg-white/15`
- 图片：`max-w-[94vw] max-h-[88vh] rounded-xl shadow-2xl`
- 过渡：fade in 200ms / fade out 150ms
- 交互：← → 键盘翻页、ESC 关闭、点击背景关闭
- 打开时锁 `body.style.overflow = 'hidden'`

### 6.6 Hero Banner（详情页）

- 背景：首张截图 `blur(40px) brightness(0.35) saturate(1.3)` + `scale(1.15)`
- 叠加：`bg-gradient-to-t from-surface-0 via-surface-0/60 to-transparent` + `bg-gradient-to-r from-surface-0/80 to-transparent`
- 最小高度：340px
- 返回按钮在游戏名上方

### 6.7 锚点导航

- 位置：`fixed right-5 top-1/2 -translate-y-1/2`（仅 xl 屏显示）
- 容器：`bg-surface-1/95 backdrop-blur-xl border border-bdr rounded`
- Active：`bg-white/10 text-white` + `bg-white` 圆点
- Default：`text-neutral-600` + `bg-neutral-700` 圆点

---

## 7. 禁止清单 (Checklist)

新页面/迭代提交前，必须逐条检查：

- [ ] **零彩色**：搜索模板中是否存在 `amber`/`emerald`/`rose`/`cyan`/`violet`/`orange`/`blue`/`red`/`sky`/`indigo`/`green`/`yellow`/`purple`/`pink`/`teal` 等彩色关键词（`slate` 和 `neutral` 允许）
- [ ] **零 Emoji**：UI 文本中是否存在任何 Emoji 字符（搜索 Unicode 范围 U+1F300-U+1FAFF）
- [ ] **圆角 ≤ 8px**：检查是否有 `rounded-3xl` 或更大的圆角
- [ ] **文字层级正确**：标题用 `text-white`，正文用 `text-neutral-300~400`，次要用 `text-neutral-500~600`
- [ ] **按钮样式复用**：只用 Primary/Secondary/Ghost 三种按钮类型
- [ ] **间距一致**：模块间 `mb-14`（详情页）或 `mb-16`（首页），不随意用其他值

---

## 8. 技术栈

| 依赖 | 版本 |
|------|------|
| Tailwind CSS | CDN Play Mode |
| Alpine.js | 3.x CDN |
| Jinja2 | Python SSG |
| 构建 | `python build.py` |
| 部署 | GitHub → Cloudflare Pages（dist/ 目录） |

---

*本文档是 Game Tracker 的唯一视觉规范来源。任何视觉决策有分歧时，以本文档为准。*
