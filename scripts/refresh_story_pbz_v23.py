"""按 v2.3 标准刷新影之刃零 story：删 title，重写 dims（设计师视角）"""
import json
from pathlib import Path

JSON = Path(__file__).resolve().parent.parent / "data" / "games" / "phantom-blade-zero.json"

# v2.3 dims：每条聚焦一个维度，避免与 overview 重复，加粗控制在 ≤ 30 字
# 颗粒度提升到"能指导美术执行"——具体到材质、配色、镜头、构图
new_dims = [
    {
        "label": "时间",
        "value": "<b>架空古代中国</b>——江湖秩序崩坏期，传统武林尚未瓦解、机械改造已悄然渗透；时间感像是<b>明末清初的中后期</b>叠加蒸汽工业初萌，没有明确朝代锚点，但服饰兵器走<b>晚明制式</b>"
    },
    {
        "label": "发生地",
        "value": "「<b>影境</b>」——一个被江湖称为禁地的架空地理带，地貌取材于<b>中国南方山地水乡</b>：悬崖峡谷、宝塔庭院、瀑布雾气、地下墓穴交错；色彩基调是<b>湿润灰青 + 工业锈红</b>的暗调"
    },
    {
        "label": "角色扮演",
        "value": "「<b>魂</b>」——影门最锋利的精英刺客，被自己人诬陷叛主，残命仅余 66 天；造型走<b>布衣窄袖 + 残破长袍</b>路线，腰间别多把武器，整体气质偏冷峻孤客而非英武少侠"
    },
    {
        "label": "科技水平",
        "value": "三层叠加：① 主流仍是<b>冷兵器江湖</b>（刀剑弓弩、暗器毒药）② 局部出现<b>蒸汽动力</b>（齿轮、管线、压力阀）③ 极少数顶尖人物完成<b>机械义肢改造</b>，属「局部科技越级」，非全民赛博朋克"
    },
    {
        "label": "对抗关系",
        "value": "三方角力：① 正统侠客（<b>布衣皮革</b>/水墨飘逸/冷兵器纯粹）② 机械化「<b>怪面</b>」（金属外骨骼/管线暴露/<b>工业锈蚀色</b>）③ 幕后操控势力（<b>红色丝线</b>母题/暗影符号/神秘学纹样）—— 三者材质语言彼此对立，视觉一眼分辨"
    },
    {
        "label": "地图类型",
        "value": "<b>垂直立体地形</b>是设计核心：悬崖栈道、瀑布雾气、屋顶跑酷、地下墓穴、齿轮工厂塔；Boss 战场地走<b>环形封闭竞技场</b>路线，常带机关地形；很少出现开放平原，<b>幽闭与高差</b>是关卡共性"
    },
    {
        "label": "视觉母题",
        "value": "三大反复出现的<b>视觉锚点</b>：<b>红色丝线</b>（隐喻幕后操控/宿命牵引）、<b>面具</b>（怪面阵营身份符号）、<b>齿轮咬合</b>（机械改造的视觉缩影）；色彩母题是「<b>水墨黑灰 × 锈蚀金红</b>」"
    },
    {
        "label": "美学谱系",
        "value": "灵感谱系横跨日漫与港片：《<b>铳梦</b>》（机械改造身体）+《<b>剑风传奇</b>》（暗黑武力宿命）+《<b>攻壳机动队</b>》（赛博质感）+ 邵氏武侠的招式编排；自我定位为<b>「功夫朋克」</b>这一原创美学标签"
    }
]

with open(JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

story = data.get("story", {})

# 删除 title
if "title" in story:
    del story["title"]

# 刷新 dims
story["dims"] = new_dims

# 顺序：overview -> dims
ordered = {}
if "overview" in story:
    ordered["overview"] = story["overview"]
ordered["dims"] = story["dims"]
for k, v in story.items():
    if k not in ordered:
        ordered[k] = v
data["story"] = ordered

with open(JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

import re
print("=== story 刷新自检 ===")
print("story keys:", list(data["story"].keys()))
print(f"dims 共 {len(new_dims)} 条")
for d in new_dims:
    val = d["value"]
    bolds = re.findall(r"<b>(.*?)</b>", val)
    plain = re.sub(r"<[^>]+>", "", val)
    over30 = [b for b in bolds if len(b) > 30]
    print(f"  [{d['label']}] 字数={len(plain)} <b>={len(bolds)} 超长加粗={len(over30)}")
