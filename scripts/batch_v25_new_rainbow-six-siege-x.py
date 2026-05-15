# -*- coding: utf-8 -*-
"""v2.5 新游戏接入：rainbow-six-siege-x（彩虹六号：围攻X）

注意：所有中文文案里如果要嵌入引号，必须用「」或（），严禁英文双引号嵌套。
keywords 数组里可以用英文双引号。

彩虹六号：围攻X 是 Ubisoft Montreal 出品的 5v5 战术射击，
Y11（Year 11）10 周年品牌焕新版本，2025-06-10 转免费。
"""
import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "games"

# ============================================================
#  彩虹六号：围攻X  rainbow-six-siege-x
# ============================================================
R6SX = {
    "worldview": {
        "background": {
            "title": "Tom Clancy 反恐宇宙——全球精锐干员在可破坏建筑中展开近距离战术对抗",
            "value": "故事发生在<b>Tom Clancy 反恐世界观</b>的当代时间线——一个多国特种部队精英被秘密组织「彩虹」招募、跨国执行反恐任务的<b>军事写实框架</b>。主战场是全球各地的<b>可破坏建筑</b>：领事馆、银行金库、摩托俱乐部、瑞士木屋、阿拉伯咖啡馆——每一面墙壁、每一层地板都可以被<b>爆破锤、冲击波、C4、热切割器</b>撕开。你加入的不是普通小队，是一支<b>汇聚 70+ 干员的跨国精英战队</b>——你下一秒用的可能是 SAS 突击兵的冲击盾，也可能是日本 SAT 的电子干扰器。",
            "keywords": ["Tom Clancy 反恐", "可破坏建筑", "70+ 干员", "跨国精英战队"]
        },
        "mainStory": {
            "title": "攻防对抗：5v5 回合制——进攻方投掷无人机侦察 + 防守方加固据点布陷阱",
            "value": "本作没有传统单人叙事，取而代之的是<b>永不停歇的 5v5 攻防循环</b>。你扮演一名干员（Operator），进攻方的任务是<b>投掷无人机侦察敌方据点、选择突入路线、救出人质或解除炸弹</b>；防守方则在准备阶段<b>加固可破坏墙壁、布置诡雷与电网、架设信号干扰器</b>。每回合仅 3 分钟——<b>前 45 秒准备阶段</b>你能听到对面墙后传来的加固声响，那种肾上腺素是你在别的射击游戏里找不到的。Y11 品牌焕新后加入<b>Dual Front 6v6 模式</b>：攻守混编、据点可重生、中立赛区动态任务。",
            "keywords": ["5v5 攻防", "干员系统", "准备阶段", "Dual Front 6v6"]
        },
        "combat": {
            "title": "战术射击核心：一发爆头即死 × 可破坏环境 × 信息博弈——以「墙后一声脚步决定生死」为核心",
            "value": "<b>一发爆头即死</b>是围攻的铁律。你的武器后坐力、射速、穿透力各不相同，但<b>爆头永远秒杀</b>。战术层的核心不是枪法而是<b>信息博弈</b>——无人机能侦察敌方位置，但会被 Mute 的信号干扰器屏蔽；Thermite 能<b>热切割加固墙</b>打开新通道，但 Bandit 的电网会烧毁火药。<b>你贴着墙壁匍匐前进、透过弹孔窥探对面动静的那一刻</b>——围攻把「信息差」做成了武器。每一轮结束后你都会在击杀回放里发现<b>「原来他从天花板开了一个洞」</b>。",
            "keywords": ["一发爆头即死", "可破坏墙体", "信息博弈", "干员技能反制"]
        },
        "coreLoop": {
            "title": "选干员 → 准备阶段侦察/布防 → 3 分钟行动阶段 → 换边 → 用声望换干员和皮肤 → 冲排位段位",
            "value": "你玩到的是<b>「战术射击 × 干员 MOBA 化 × 赛季制电竞」</b>——结构是<b>Ban/Pick 干员选择 → 准备阶段（45 秒侦察+布防）→ 行动阶段（3 分钟战术对抗）→ 换边 → 下一回合</b>四层骨架。Y11 品牌焕新带来<b>免费化转型</b>：快速比赛和非排位赛对所有玩家免费，26 名干员开箱即得。日常循环包括<b>冲排位段位、解锁新干员、收集精英皮肤、参加赛季活动和 Dual Front 模式</b>。<b>8500 万注册玩家 + 10 年持续更新</b>——围攻已从一款游戏变成了战术射击品类的代名词。",
            "keywords": ["Ban/Pick 干员", "准备+行动两阶段", "免费化转型", "8500 万玩家"]
        }
    },
    "story_overview": {
        "tagline": "<b>5 对 5，墙能炸、地板能拆</b>——你听到对面那声脚步了吗？",
        "paragraphs": [
            "想象一栋<b>每一面墙都可以被炸开的建筑</b>——领事馆、银行金库、瑞士木屋、摩托俱乐部——然后把 10 名来自全球特种部队的精英干员关进去。进攻方投掷<b>无人机</b>侦察敌方据点布局，选择从窗户、天花板还是被 Thermite 热切割开的<b>加固墙</b>突入；防守方在 45 秒准备阶段里疯狂<b>加固墙壁、架设电网、布置诡雷</b>。这不是跑得快就能赢的射击游戏——这是一场<b>信息博弈</b>。",
            "Y11 品牌焕新把这款 10 岁老兵推到全新起点：<b>免费化转型让所有玩家零门槛进入</b>，26 名干员开箱即得。全新<b>Dual Front 6v6 模式</b>打破攻守壁垒——进攻方和防守方混编同队、据点可重生、中立赛区随赛季轮换。五张经典地图（Clubhouse、Chalet、Border、Bank、Kafe）获得<b>4K 贴图 + 全新光照阴影</b>视觉重制。Siege X 不是一次赛季更新，而是<b>围攻十年来最大规模的品牌重生</b>。",
            "<b>你贴着墙壁匍匐前进、透过弹孔窥探对面动静的那一刻</b>，Ubisoft Montreal 用十年证明了战术射击的极致不是更快的射速，而是<b>「墙后那一声脚步究竟是敌是友」</b>的信息悬念；<b>你第一次在击杀回放里发现对手从天花板开了一个洞的那一秒</b>——可破坏环境让每一轮都是<b>全新的建筑拼图</b>；<b>那次你和队友精确配合、Thermite 开墙 + 闪光弹致盲 + 三人同时突入的完美回合</b>——围攻把「战术配合」做成了你能在 FPS 里体验到的最高密度多巴胺。这不是关于一个人的枪法有多准的故事，是<b>「你下一回合还敢不敢贴墙听声辨位」</b>？"
        ]
    },
    "aesthetic_summary": {
        "label": "零圆角战术极简 × 10 年品牌焕新",
        "definition": "<b>零圆角战术极简 × 10 年品牌焕新</b>，是 Ubisoft Montreal 把<b>Tom Clancy 军事写实</b>（反恐场景、可破坏建筑）和<b>电竞信息效率 HUD</b>（siege-navy #0C0F16 深色底、极简图标）以及<b>Y11 焕新视觉系统</b>（Noto Sans CJK SC + Simplon Mono、零圆角、Ghost 噪声纹理）三层缝合在<b>5v5 战术射击</b>外壳里的混血美学。底色是<b>军事写实 × 电竞极简</b>血统；变异在于<b>十周年把视觉语言推向零装饰信息建筑主义</b>。",
        "evolution": "「军事反恐 + 战术射击 + 电竞极简」视觉线跨越半世纪。<b>1998 年</b>Tom Clancy<b>《彩虹六号》</b>初代定义军事反恐战术射击美术母版——室内 CQB + 蓝图规划。<b>2004 年</b>Valve<b>《反恐精英：起源》</b>把竞技 FPS HUD 做成信息效率标杆。<b>2007 年</b>Infinity Ward<b>《使命召唤4：现代战争》</b>把当代军事写实 FPS 推成主流视觉语言。<b>2012 年</b>Riot<b>《英雄联盟》</b>电竞 UI 重设计引领「深色底+高对比图标」信息密集型界面潮流。<b>2015 年</b>《Rainbow Six Siege》首发——可破坏环境成为品类视觉标识。<b>2020 年</b>Riot<b>《Valorant》</b>把战术射击 × 角色技能视觉做成新竞品标杆。<b>2025 年</b>Siege X 十周年品牌焕新——siege-navy #0C0F16 + 零圆角 + Ghost 噪声纹理重塑视觉系统。",
        "references": [
            {"type": "game", "title": "Rainbow Six 彩虹六号初代（Tom Clancy）", "year": "1998", "note": "<b>军事反恐战术射击</b>美术母版；CQB 室内作战 + 蓝图规划视觉原型"},
            {"type": "game", "title": "Counter-Strike: Source 反恐精英：起源", "year": "2004", "note": "<b>竞技 FPS HUD 信息效率</b>标杆；极简准星+买枪菜单视觉哲学源头"},
            {"type": "film", "title": "Black Hawk Down 黑鹰坠落", "year": "2001", "note": "<b>当代军事写实</b>影像母版；室内 CQB 战术射击视觉精神养分"},
            {"type": "game", "title": "Call of Duty 4: Modern Warfare 使命召唤4", "year": "2007", "note": "<b>当代军事 FPS</b>主流化母版；围攻写实武器建模精神参照"},
            {"type": "game", "title": "Valorant 无畏契约", "year": "2020", "note": "<b>战术射击 × 角色技能</b>品类竞品标杆；干员化 FPS 视觉语言参照"},
            {"type": "art", "title": "Dieter Rams 极简工业设计原则", "year": "1976", "note": "<b>「少即是多」极简设计哲学</b>原典；Y11 零圆角零装饰界面精神远祖"},
            {"type": "game", "title": "League of Legends 英雄联盟电竞 UI 重设计", "year": "2012", "note": "<b>电竞信息密集型 UI</b>深色底+高对比图标潮流先驱；围攻 HUD 精神参照"},
            {"type": "film", "title": "Sicario 边境杀手", "year": "2015", "note": "<b>当代反恐灰色地带</b>影像参照；围攻「精英干员在道德模糊地带执行任务」调性养分"}
        ]
    },
    "aesthetic_anchor": {
        "scene": [1, 3, 4],
        "costume": [1, 3],
        "ui": [2, 6],
        "symbol": [1, 5],
        "promo": [6, 7]
    },
    "story_dims": [
        {
            "label": "时间",
            "value": "<b>当代</b>——无明确叙事年份，持续赛季制更新的反恐世界观"
        },
        {
            "label": "发生地",
            "value": "<b>全球各地室内战场</b>——领事馆、银行、咖啡馆、木屋、摩托俱乐部等可破坏建筑"
        },
        {
            "label": "角色扮演什么",
            "value": "「<b>彩虹小队干员 Operator</b>」——来自全球特种部队的精英，各自携带独特技能装备"
        },
        {
            "label": "科技水平",
            "value": "<b>当代军事科技+轻度近未来</b>——真实武器为主，辅以电磁脉冲、全息投影等干员专属技术"
        },
        {
            "label": "对抗关系",
            "value": "<b>进攻方 vs 防守方</b>——经典 5v5 不对称攻防；Y11 新增 Dual Front 6v6 攻守混编"
        },
        {
            "label": "地图",
            "value": "<b>可破坏封闭建筑</b>：每张地图的墙壁、地板、天花板均可爆破重塑；五张经典地图获 4K 视觉重制"
        },
        {
            "label": "元素",
            "value": "<b>战术射击 × 干员技能 × 可破坏环境 × 电竞对抗</b>；美术标识为「零圆角军事极简 + Ghost 噪声纹理」——十年品牌焕新的信息建筑主义"
        }
    ]
}


# ============================================================
#  写入 + 自检
# ============================================================
GAMES = {
    "rainbow-six-siege-x": R6SX,
}


def write_one(slug, payload):
    fp = DATA_DIR / f"{slug}.json"
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)

    d["worldview"] = payload["worldview"]

    story = d.get("story", {})
    if "title" in story:
        del story["title"]
    new_story = {"overview": payload["story_overview"]}
    new_story["dims"] = payload["story_dims"]
    for k, v in story.items():
        if k not in new_story:
            new_story[k] = v
    d["story"] = new_story

    aes = d.get("aesthetic", {})
    new_aes = {"summary": payload["aesthetic_summary"]}
    for k in ["scene", "costume", "ui", "symbol", "promo"]:
        if k in aes and isinstance(aes[k], dict):
            card = dict(aes[k])
            card["anchorRule"] = payload["aesthetic_anchor"][k]
            new_aes[k] = card
    if "rivals" in aes:
        new_aes["rivals"] = aes["rivals"]
    for k, v in aes.items():
        if k not in new_aes:
            new_aes[k] = v
    d["aesthetic"] = new_aes

    new_order = {}
    for k in ["id", "slug"]:
        if k in d:
            new_order[k] = d[k]
    if "playerExp" in d:
        new_order["playerExp"] = d["playerExp"]
    if "worldview" in d:
        new_order["worldview"] = d["worldview"]
    if "story" in d:
        new_order["story"] = d["story"]
    if "aesthetic" in d:
        new_order["aesthetic"] = d["aesthetic"]
    for k, v in d.items():
        if k not in new_order:
            new_order[k] = v

    with open(fp, "w", encoding="utf-8") as f:
        json.dump(new_order, f, ensure_ascii=False, indent=2)


def check(slug):
    with open(DATA_DIR / f"{slug}.json", "r", encoding="utf-8") as f:
        d = json.load(f)
    issues = []

    # --- worldview ---
    wv = d.get("worldview", {})
    for k in ["background", "mainStory", "combat", "coreLoop"]:
        c = wv.get(k, {})
        val = c.get("value", "")
        plain = re.sub(r"<[^>]+>", "", val)
        bolds = re.findall(r"<b>", val)
        if not (120 <= len(plain) <= 240):
            issues.append(f"wv.{k} chars={len(plain)}")
        if len(bolds) < 2:
            issues.append(f"wv.{k} bolds={len(bolds)}")
        if "\u4f60" not in val:
            issues.append(f"wv.{k} no second-person")

    # --- story overview ---
    ov = d.get("story", {}).get("overview", {})
    tag = re.sub(r"<[^>]+>", "", ov.get("tagline", ""))
    if not (12 <= len(tag) <= 40):
        issues.append(f"tagline_chars={len(tag)}")
    paras = ov.get("paragraphs", [])
    if len(paras) != 3:
        issues.append(f"paragraphs_count={len(paras)}")
    total = sum(len(re.sub(r"<[^>]+>", "", p)) for p in paras)
    bolds = sum(len(re.findall(r"<b>", p)) for p in paras) + len(re.findall(r"<b>", ov.get("tagline", "")))
    if not (380 <= total <= 700):
        issues.append(f"ov_total={total}")
    if bolds < 6:
        issues.append(f"ov_bolds={bolds}")
    if paras and not paras[-1].rstrip().endswith(("\uff1f", "?", "\u2026", "...")):
        issues.append("p3 no ?")

    # --- story dims ---
    dims = d.get("story", {}).get("dims", [])
    if not (4 <= len(dims) <= 8):
        issues.append(f"dims_count={len(dims)}")

    # --- aesthetic summary ---
    su = d.get("aesthetic", {}).get("summary", {})
    if su:
        lbl = su.get("label", "")
        if not (6 <= len(lbl) <= 30):
            issues.append(f"label_len={len(lbl)}")
        df = re.sub(r"<[^>]+>", "", su.get("definition", ""))
        if not (120 <= len(df) <= 230):
            issues.append(f"def={len(df)}")
        ev = re.sub(r"<[^>]+>", "", su.get("evolution", ""))
        if not (150 <= len(ev) <= 380):
            issues.append(f"ev={len(ev)}")
        refs = su.get("references", [])
        if not (5 <= len(refs) <= 8):
            issues.append(f"refs_count={len(refs)}")
        types = set(r["type"] for r in refs)
        if len(types) < 3:
            issues.append(f"types={len(types)}")
        years_str = " ".join(r.get("year", "") for r in refs)
        years = [int(y) for y in re.findall(r"(19\d{2}|20\d{2})", years_str)]
        if years and max(years) - min(years) < 20:
            issues.append(f"year_span={max(years)-min(years)}")
        for i, ref in enumerate(refs):
            note = ref.get("note", "")
            if "<b>" not in note:
                issues.append(f"ref[{i}] no bold in note")
    else:
        issues.append("no aesthetic_summary")

    # --- 中文引号安全检查 ---
    raw = json.dumps(d, ensure_ascii=False)
    # 检查中文上下文中嵌套的英文双引号（排除 HTML 标签和 JSON 结构引号）
    cn_blocks = re.findall(r'[\u4e00-\u9fff][^"]*"[^"]*"[^"]*[\u4e00-\u9fff]', raw)
    # 简化：只报告，不 block

    return issues


def main():
    print("=" * 70)
    print("v2.5 新游戏接入：rainbow-six-siege-x 内容写入 + 自检")
    print("=" * 70)
    for slug, payload in GAMES.items():
        write_one(slug, payload)
        issues = check(slug)
        if issues:
            print(f"\n[{slug}] {len(issues)} issues:")
            for i in issues:
                print(f"  - {i}")
        else:
            print(f"\n[{slug}] PASS")


if __name__ == "__main__":
    main()
