"""为影之刃零 aesthetic 顶部新增 summary 综述（美学定调 + 共识发展 + 借鉴谱系）"""
import json
import re
from pathlib import Path

JSON = Path(__file__).resolve().parent.parent / "data" / "games" / "phantom-blade-zero.json"

summary = {
    # 美学一词锚定（海报级标语）
    "label": "功夫朋克 Kungfu Punk",

    # Q1: 是什么美学？
    "definition": (
        "<b>功夫朋克</b>是一种把<b>东方武侠</b>与<b>蒸汽朋克</b>硬碰硬撞在一起的混血美学。"
        "它的底色仍然是水墨气质的中式江湖——飞檐斗笠、刀光墨迹、云雾山涧；"
        "但你随时会在画面里撞见一颗咬合中的齿轮、一截嘶嘶漏气的管线、或者一只贴着皮肉的金属义肢。"
        "色彩被锁死在<b>墨黑灰青 × 高饱和锈红</b>的双色 DNA 里，"
        "整体调性介于<b>港片武侠的硬朗</b>和<b>赛博朋克的反乌托邦</b>之间——既古老，又脏；既写意，又压迫。"
    ),

    # Q2: 审美共识如何一步步发展出来？
    "evolution": (
        "这种审美不是凭空出现的，它是<b>三十年视觉文化的复合产物</b>。"
        "1980-90 年代，香港武侠电影（徐克、王家卫、李连杰一代）把"
        "<b>水墨意境 + 飞檐打斗 + 残破侠客</b>定型为东方动作美学的全球标签；"
        "与此同时，日漫《<b>铳梦</b>》《<b>攻壳机动队</b>》《<b>剑风传奇</b>》"
        "把<b>机械改造身体</b>的视觉冲击推到大众视野，催生了赛博/蒸汽朋克的群众基础。"
        "进入 2010 年代后，《<b>只狼</b>》《<b>对马岛之魂</b>》"
        "《<b>双人成行</b>》一类作品又证明了「东方题材也能在国际市场跑通暗黑动作风格」。"
        "影之刃零踩在这条线上，把武侠的骨与蒸汽朋克的肉并到同一具身体里，"
        "顺势收获了一批<b>同时吃中式审美和工业暗黑审美</b>的核心观众。"
    ),

    # Q3: 美术设计可参考借鉴的谱系
    # type: game / film / anime / manga / show
    "references": [
        {
            "type": "manga",
            "title": "铳梦 (GUNNM)",
            "year": "1990",
            "note": "<b>机械义肢嫁接血肉</b>的视觉范式起源；脏感金属 × 有机肌肉的材质碰撞"
        },
        {
            "type": "anime",
            "title": "攻壳机动队",
            "year": "1995",
            "note": "<b>赛博身体观</b>的视觉教科书；机械改造下的存在主义气质"
        },
        {
            "type": "manga",
            "title": "剑风传奇 (Berserk)",
            "year": "1989",
            "note": "<b>暗黑武力宿命</b>美学母版；血污残刀、巨大反派、命运齿轮意象"
        },
        {
            "type": "film",
            "title": "卧虎藏龙 / 一代宗师",
            "year": "2000 / 2013",
            "note": "<b>水墨意境 + 飞檐打斗</b>的电影级东方动作语言；写意构图与光雾质感"
        },
        {
            "type": "game",
            "title": "只狼：影逝二度",
            "year": "2019",
            "note": "<b>暗调东方</b>动作游戏的全球范式；战损质感 + 极简战斗 HUD 的成功验证"
        },
        {
            "type": "film",
            "title": "邵氏武侠 / 龙门客栈系列",
            "year": "1960s-70s",
            "note": "<b>港式武侠</b>构图与色彩传统；高对比度、雾气江湖、招式编排"
        },
        {
            "type": "anime",
            "title": "吸血鬼猎人 D",
            "year": "1985",
            "note": "<b>哥特机械</b>美学；冷峻孤客造型 + 机械幻想生物的混搭传统"
        }
    ]
}

with open(JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

aesthetic = data.get("aesthetic", {})

# 重组顺序：summary -> scene/costume/ui/symbol/promo -> rivals
new_aesthetic = {"summary": summary}
for key in ["scene", "costume", "ui", "symbol", "promo"]:
    if key in aesthetic:
        new_aesthetic[key] = aesthetic[key]
if "rivals" in aesthetic:
    new_aesthetic["rivals"] = aesthetic["rivals"]
# 兜底：若有其它键也带上
for k, v in aesthetic.items():
    if k not in new_aesthetic:
        new_aesthetic[k] = v

data["aesthetic"] = new_aesthetic

with open(JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# === 自检 ===
print("=== aesthetic.summary 自检 ===\n")
print(f"label: {summary['label']}")
for fkey in ["definition", "evolution"]:
    text = summary[fkey]
    plain = re.sub(r"<[^>]+>", "", text)
    bolds = re.findall(r"<b>(.*?)</b>", text)
    print(f"\n[{fkey}] 字数={len(plain)} <b>={len(bolds)}")

print(f"\nreferences 共 {len(summary['references'])} 条")
type_dist = {}
for r in summary["references"]:
    t = r["type"]
    type_dist[t] = type_dist.get(t, 0) + 1
print(f"  类型分布: {type_dist}")
print(f"\naesthetic keys (顺序): {list(new_aesthetic.keys())}")
