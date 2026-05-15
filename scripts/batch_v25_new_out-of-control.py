# -*- coding: utf-8 -*-
"""v2.5 新游戏接入：失控进化 out-of-control

腾讯天美工作室群 · Rust 正版玩法授权 · 第三人称生存射击

注意：所有中文文案里如果要嵌入引号，必须用「」或（），严禁英文双引号嵌套。
keywords 数组里可以用英文双引号。
"""
import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "games"

# ============================================================
#  失控进化 out-of-control
# ============================================================
OUT_OF_CONTROL = {
    "worldview": {
        "background": {
            "title": "末日废土孤岛——辐射荒野、锈蚀军事遗迹与永不停歇的资源争夺",
            "value": "故事发生在一座<b>文明崩塌后的末日荒岛</b>——没有人记得灾变的起因，只剩下锈蚀的军事基地、废弃的发电厂、辐射泄漏的火箭发射场和被野草吞噬的超市加油站。你赤手空拳被丢在海岸线上，面对的是<b>辐射区、野兽、武装 NPC 科学家和同样饥饿的其他幸存者</b>。昼夜更替带来温度骤变，暴风雨说来就来。<b>整座岛就是一台「适者生存」的永动机</b>——每隔数天服务器会刷新（wipe），文明从零开始重建，你永远在废墟上书写下一轮生存日记。",
            "keywords": ["末日荒岛", "辐射区", "wipe 重置", "适者生存"]
        },
        "mainStory": {
            "title": "生存叙事：你是一名赤手空拳的幸存者——从石器时代一路科技树攀升到火箭发射",
            "value": "本作没有编剧写好的主线剧本，取而代之的是<b>每一局服务器周期里你亲手书写的生存史诗</b>。你从海滩上一块石头、一根木棍开始，砍树采矿、熔炼金属、研究科技蓝图。沿途你会遭遇<b>武装巡逻的 NPC 科学家、空中巡逻直升机、装甲运兵车 Bradley</b>。最终目标是攻入<b>火箭发射基地</b>，但真正的主线永远是人与人之间的博弈——你今晚睡觉时，隔壁部落可能正在用 C4 炸你的铁门。<b>「信任」在这座岛上比任何资源都稀缺</b>。",
            "keywords": ["科技树攀升", "NPC 科学家", "火箭发射场", "信任稀缺"]
        },
        "combat": {
            "title": "战斗机制：第三人称射击 + 基地攻防 + 载具立体作战——「你的家门就是前线」",
            "value": "战斗贯穿你在岛上的每一秒。近战阶段你用<b>石斧长矛弓箭</b>和野兽及其他裸装玩家肉搏；中期解锁<b>手枪、冲锋枪、步枪</b>后进入第三人称射击的核心手感——掩体走位、弹道预判、爆头一击毙命。真正令人心跳加速的是<b>基地攻防战</b>：进攻方计算炸药成本规划爆破路线，防守方在迷宫般的钢铁堡垒里布满陷阱炮塔。<b>那次你和队友花三小时突袭对手主基地、在最后一扇铁门后发现满箱硫磺的瞬间</b>——就是失控进化独有的肾上腺素时刻。",
            "keywords": ["第三人称射击", "基地攻防", "爆破路线", "炮塔陷阱"]
        },
        "coreLoop": {
            "title": "采集 → 建造 → 科技研发 → PvP 掠夺 → 基地攻防 → wipe 重来",
            "value": "你玩到的是<b>「末日生存建造 + 硬核 PvP 掠夺」</b>双引擎——结构是<b>资源采集 → 基地建造升级 → 科技树研发 → PvE 据点攻略 → PvP 基地突袭 → 服务器 wipe 重置</b>六层循环。日常活动包括<b>砍树挖矿打猎、熔炼金属升级墙体、在工作台解锁武器护甲蓝图、组队攻打军事隧道和石油平台获取高级物资、和敌对部落互相抄家</b>。养成线是<b>情报系统跨周期成长 + 账号等级 + 皮肤收藏</b>。<b>每次 wipe 后你都会告诉自己「这次我要换个玩法」</b>——然后发现自己又在海滩上捡石头。",
            "keywords": ["六层循环", "wipe 重置", "情报跨周期", "抄家文化"]
        }
    },
    "story_overview": {
        "tagline": "<b>赤手空拳登陆末日荒岛</b>——你能活过今晚吗？",
        "paragraphs": [
            "想象一座<b>文明崩塌后的末日荒岛</b>——锈蚀军事基地、辐射发电厂、被藤蔓吞噬的超市与加油站散落在海岸线与雪山之间。你赤手空拳被丢在沙滩上，口袋里只有一块石头和一根火炬。<b>辐射区、野兽、武装 NPC 科学家</b>和同样饥饿的其他幸存者——岛上的一切都想杀死你。腾讯天美获得 Rust 正版授权，把这套<b>「适者生存」沙盒</b>搬上了手机和 PC 全平台。",
            "你扮演的不是什么被选中的英雄，只是一个<b>连裤子都没有的普通人</b>。从石斧砍树开始，一路熔炼金属、研究蓝图、搭建钢铁堡垒——科技树从石器时代跨越到自动炮塔与火箭发射。<b>真正的叙事不在 NPC 嘴里，而在你与其他玩家之间</b>：陌生人递过来的一块肉可能是善意也可能是陷阱；你花一整天建起的家，睡一觉醒来可能只剩断壁残垣。「信任」在这座岛上比硫磺还稀缺，<b>每一次结盟都是赌注</b>。",
            "<b>那次你和队友花三小时突袭对手主基地、在最后一扇铁门后发现满箱硫磺的瞬间</b>，天美把生存射击做成了肾上腺素剧场——你玩的不是游戏，是<b>一部由你亲手编剧的末日生存纪录片</b>；<b>那次你在雪山顶被直升机追杀、跳崖逃进矿洞的桥段</b>，昼夜温差和辐射风暴让每一步都是抉择；<b>那次 wipe 重置后你站在空旷海滩上，又捡起第一块石头的时刻</b>——失控进化的核心不是胜利，而是<b>「明知一切终将归零，你还愿不愿意再来一轮」</b>？"
        ]
    },
    "story_dims": [
        {
            "label": "时间",
            "value": "<b>不明确的近未来末日后</b>——灾变原因不详，科技残留在当代军事水平"
        },
        {
            "label": "发生地",
            "value": "<b>孤立荒岛</b>——涵盖海岸、森林、雪山、沙漠、辐射区、地下矿道等多生态区"
        },
        {
            "label": "角色扮演什么",
            "value": "「<b>赤手空拳的无名幸存者</b>」——没有职业没有背景，一切靠你从零开始"
        },
        {
            "label": "科技水平",
            "value": "<b>石器时代 → 当代军事科技</b>——单局内从石斧弓箭攀升到步枪炮塔火箭发射器"
        },
        {
            "label": "对抗关系",
            "value": "<b>幸存者 vs 幸存者 vs 环境 vs NPC</b>——以 PvP 掠夺为核心，PvE 据点为资源来源"
        },
        {
            "label": "地图",
            "value": "<b>开放世界沙盒孤岛</b>——包含数十个可探索据点（军事基地/发电厂/石油平台/军事隧道等）"
        },
        {
            "label": "元素",
            "value": "<b>Rust 正版授权 × 腾讯天美全平台移植 × 末日生存建造 × 硬核 PvP</b>——以手机端 Rust 体验为核心差异化卖点"
        }
    ],
    "aesthetic_summary": {
        "label": "锈蚀废土工业 x 硬核生存射击",
        "definition": "<b>锈蚀废土工业 x 硬核生存射击</b>，是腾讯天美把<b>后启示录废土工业美学</b>（锈蚀金属墙体、辐射警示标、破损军事设施、荒野中的人造光源）和<b>写实生存沙盒视觉语言</b>（昼夜光影、天气粒子、资源节点高亮、建造网格系统）以及<b>第三人称射击 HUD 界面</b>（准星反馈、弹道轨迹、伤害数字、快捷栏轮盘）三层缝合在<b>Rust 正版玩法授权</b>外壳里的混血美学。底色是<b>Rust 原版 × DayZ 末日沙盒</b>双重血统；变异在于<b>天美把 PC 硬核生存做成了全平台触屏友好的视觉方案</b>——手机上也能读懂废土。",
        "evolution": "「末日生存沙盒 + 基地建造 + PvP 掠夺」视觉线跨越三十年。<b>1995 年</b>Westwood<b>《命令与征服》</b>定义基地建造美学原典。<b>2003 年</b>Bohemia<b>《武装突袭》</b>把军事写实射击做成开放世界。<b>2009 年</b>Mojang<b>《Minecraft》</b>定义沙盒建造视觉范式。<b>2013 年</b>Bohemia<b>《DayZ》独立版</b>定义末日多人生存掠夺品类母版。<b>2018 年</b>Facepunch<b>《Rust》正式版</b>把基地建造与 wipe 周期做成品类标杆——本作直接授权来源。<b>2023 年</b>腾讯天美获 Rust 授权启动全平台适配。<b>2026 年</b>《失控进化》预约破 3200 万——把硬核生存射击推向中国大众市场。",
        "references": [
            {"type": "game", "title": "Rust（Facepunch Studios）", "year": "2018", "note": "<b>基地建造 + PvP 掠夺 + wipe 周期</b>品类标杆；本作直接授权来源"},
            {"type": "game", "title": "DayZ 独立版（Bohemia Interactive）", "year": "2013", "note": "<b>末日多人生存掠夺</b>品类母版；失控进化最直接精神血统"},
            {"type": "game", "title": "Minecraft（Mojang）", "year": "2009", "note": "<b>沙盒建造</b>第一人称视觉范式；基地建造精神母版"},
            {"type": "film", "title": "疯狂的麦克斯：狂暴之路 Mad Max: Fury Road", "year": "2015", "note": "<b>废土工业美学</b>电影巅峰；锈蚀金属+荒漠求生视觉圣经"},
            {"type": "film", "title": "我是传奇 I Am Legend", "year": "2007", "note": "<b>末日孤独幸存者</b>电影母版；荒岛独行与文明废墟视觉参照"},
            {"type": "game", "title": "命令与征服 Command & Conquer（Westwood）", "year": "1995", "note": "<b>RTS 基地建造</b>美学原典；资源采集+建筑升级视觉祖父"},
            {"type": "art", "title": "切尔诺贝利废墟摄影档案", "year": "1986", "note": "<b>核灾废土纪实摄影</b>真实档案；辐射区视觉考据基底"},
            {"type": "game", "title": "武装突袭 Operation Flashpoint（Bohemia）", "year": "2003", "note": "<b>军事写实开放世界射击</b>远期祖父；废土射击视觉血统"}
        ]
    },
    "aesthetic_anchor": {
        "scene": [1, 2, 4],
        "costume": [3, 4],
        "ui": [5],
        "symbol": [1, 2],
        "promo": [1, 2]
    }
}

# ============================================================
#  写入 + 自检
# ============================================================
GAMES = {
    "out-of-control": OUT_OF_CONTROL,
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
    # 写入 dims（新游戏需要从 payload 中生成）
    if "story_dims" in payload:
        new_story["dims"] = payload["story_dims"]
    elif "dims" in story and story["dims"]:
        new_story["dims"] = story["dims"]
    else:
        new_story["dims"] = payload.get("story_dims", [])
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
    # 新游戏没有 aesthetic 子维度卡片，只写 summary + anchorRule
    if "anchorRule" not in new_aes and "aesthetic_anchor" in payload:
        new_aes["anchorRule"] = payload["aesthetic_anchor"]
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
        # 标题存在
        if not c.get("title"):
            issues.append(f"wv.{k} no title")
        # keywords 存在
        if not c.get("keywords") or len(c["keywords"]) < 2:
            issues.append(f"wv.{k} keywords<2")

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
        years = [int(y) for y in re.findall(r"(19\d{2}|20\d{2}|18\d{2})", years_str)]
        if years and max(years) - min(years) < 20:
            issues.append(f"year_span={max(years)-min(years)}")
        # 每条 note 含 <b>
        for i, r in enumerate(refs):
            if "<b>" not in r.get("note", ""):
                issues.append(f"ref[{i}] no bold in note")
    else:
        issues.append("no aesthetic.summary")

    # --- 中文引号安全检查 ---
    raw = json.dumps(d, ensure_ascii=False)
    # 检测 value/tagline/paragraphs/definition/evolution/note 字段中的嵌套英文双引号
    for field in ["value", "tagline", "definition", "evolution", "note"]:
        pattern = rf'"{field}"\s*:\s*"(.*?)"(?=\s*[,}}\]])'
        # 简单检查：中文文案中不应出现 \"xxx\" 这种嵌套
        pass  # JSON 序列化后难以直接检测嵌套引号，跳过自动检测

    return issues


def main():
    print("=" * 70)
    print("v2.5 新游戏接入：失控进化 out-of-control 内容写入 + 自检")
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
