# game-tracker-v2 项目长期笔记

## 运行环境
- 构建依赖 jinja2，已装在隔离 venv：`C:/Users/lamchen.TENCENT/.workbuddy/binaries/python/envs/default/Scripts/python.exe`
- 跑 build 用该 venv 的 python：`<venv>/Scripts/python.exe build.py`（系统 python 没装 jinja2 会报 ModuleNotFoundError）

## build.py 关键行为
- build 会**清空 dist 后重建**。原写法是 `shutil.rmtree(DIST)` 整删目录，Windows 上若 dist 目录句柄被占用（预览面板/残留 http.server cd 进 dist）会 PermissionError。
- 2026-06-30 已改为「清空 dist 内容但保留目录本身」（逐项 iterdir 删 + PermissionError 跳过），规避目录锁。
- ⚠️ **非游戏站交付物不要放 dist**，会被 build 清掉。放项目根或独立目录。

## 立项（新游戏建档）标准流程
1. 逐款 WebSearch 确认准确身份（名字歧义大的如「古剑/鬼武者」必须搜实），拿 company/genre/region/platforms/model/releaseDate。
2. Steam appid：用 `store.steampowered.com/api/storesearch/?term=英文名&l=schinese&cc=CN` 拿 id；官网用 `api/appdetails?appids={id}` 的 website 字段。PS5/Switch 独占无 Steam 版则手填官网。
3. 写入 `data/games.json`，字段见 _admit_new8.py / _tier2_admit.py 模板（id/name/nameCN/alias/icon/company/category/region/platforms/model/genre/scale/mau/games/established/releaseDate/desc/features/changes/lastUpdate/slug，可选 appid/website）。
4. id 取当前 max+1 起递增，防冲突。
5. build 出详情页验证 `dist/game/{slug}.html` 存在。
- **立项 ≠ 内容生产**：立项只建元数据。worldview/story/aesthetic 三模块、Steam封面、biliVideos、assets 需另跑 game-tracker-content-pipeline skill。
- 复用脚本：`_admit_new8.py`（批量立项模板）。

## 已知站内重复检查
- 立项前必查 games.json 是否已存在（按 nameCN/alias/slug）。例：燕云十六声 = where-winds-meet(id=155) 早已立项。
- 又例：Ghost of Yotei = ghost-of-yotei(id=113) 2026-07-03 用户说"立项"时其实早已存在。

## 立项接单：查重 → 分流（**必做，2026-07-03 教训**）
用户说「立项 XXX / 做新游戏立项 XXX」时的分流：
- **已存在** → 「缺口修复模式」：查 detail 完成度、封面、B站视频数、UI 链接是否 v3 Google site:；缺哪补哪，**不重跑管线、不重写老文案**
- **不存在** → 走 6 阶段完整管线（load game-tracker-content-pipeline skill）
- 不查就重跑会浪费大量算力 + 覆盖历史内容

## story.dims 数量标准（澄清）
- **全站主流 7 维（84%）**；8 维只是 2026-06 起我这批新立项拉高的标准
- selfcheck_new8.py 里 `len(dims)<8` 只对那 7 款新立项适用，不是全站硬规则
- 老游戏 dims=7 完全 OK，不用强补

## PS5 / 无 Steam 独占游戏封面来源
- 无 Steam appid → 走 `image.api.playstation.com`
- PS 官网 og:image 常是方图（1024×1024，用于 ratings/badge），**不适合直接作封面**（裁 460×215 会砍掉大部分画面）
- 正确做法：从 PS 游戏页 HTML 里 grep 所有 `image.api.playstation.com` URL，挑 **ratio ≥ 1.6** 的是真 hero/key art（通常 3840×2160）
- 裁 460×215 webp 双写 `screenshots_local/{slug}/cover.webp` + `dist/screenshots/{slug}/cover.webp`

## screenshots.json 老条目陷阱
- 老游戏 detail 里的 screenshots.json 条目常引用 `screenshots/{slug}/home-*.webp` 但**这些文件早已不存在**（老流程遗留）→ 导致详情页破图
- 缺口修复模式必查：`for img in mod.screens[].imgs: if not os.path.exists(img.replace('screenshots/','screenshots_local/')): 剔除`
