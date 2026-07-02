# -*- coding: utf-8 -*-
"""修复新8批自检问题：加粗超30拆分/tagline缩短/references补type/summary压缩/褒词替换/结尾问号。
只做精确字符串替换,不重写整段。"""
import json, re
from pathlib import Path
BASE = Path("d:/ecnalClaw/output/game-tracker-v2")
GDIR = BASE / "data" / "games"

def load(s): return json.load(open(GDIR/f"{s}.json", encoding="utf-8"))
def save(s,d): json.dump(d, open(GDIR/f"{s}.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)

# ---------- lost-soul-aside ----------
d = load("lost-soul-aside")
# tagline 缩短 (原35字)
d["story"]["overview"]["tagline"] = "<b>拯救世界，拯救妹妹</b>——一人一条龙，把连招打成一首诗。"
# aesthetic summary label 去"华丽剑舞"改中性; 但"华丽"作玩法术语保留在正文。summary.label 里的换掉
d["aesthetic"]["summary"]["label"] = "剑舞星旅 × 星外奇幻 Sword Odyssey"
# definition/evolution 中 "华丽爽快"→"爽快凌厉"（去褒词）
d["aesthetic"]["summary"]["definition"] = d["aesthetic"]["summary"]["definition"].replace("华丽爽快的动作演出","爽快凌厉的动作演出")
save("lost-soul-aside", d)

# ---------- onimusha ----------
d = load("onimusha-way-of-the-sword")
# tagline 35字→缩短
d["story"]["overview"]["tagline"] = "<b>剑本该只靠自己的手</b>——可要斩尽幻魔，武藏必须戴上那只不属于人的笼手。"
save("onimusha-way-of-the-sword", d)

# ---------- gujian ----------
d = load("gujian")
# tagline 35→短
d["story"]["overview"]["tagline"] = "<b>渡尽尘缘，方证生死</b>——你替满城亡魂了却执念，却记不起自己的魂丢在何处。"
# worldview.coreLoop 加粗超30字拆分
cl = d["worldview"]["coreLoop"]["value"]
cl = cl.replace("<b>沿主线引渡一个个亡魂、了却因果，穿插场景探索与法器成长，段落末尾一场 Boss 战收尾</b>",
                "<b>沿主线引渡一个个亡魂</b>、了却因果，穿插场景探索与法器成长，段落末尾一场 <b>Boss 战</b>收尾")
d["worldview"]["coreLoop"]["value"] = cl
# 引述"写实唯美风"→"写实细腻风"(去唯美)
d["aesthetic"]["summary"]["evolution"] = d["aesthetic"]["summary"]["evolution"].replace("写实唯美风","写实细腻风")
save("gujian", d)

# ---------- gui-tang ----------
d = load("gui-tang")
# tagline 41→短
d["story"]["overview"]["tagline"] = "<b>十队信使，九殁蕃戎</b>——你揣着捷报，也找着那个投军的儿子。"
# mainStory / coreLoop 加粗超30拆分
cl = d["worldview"]["coreLoop"]["value"]
cl = cl.replace("<b>沿东归之路推进剧情，穿插双人合作搬重物、钻缝隙、跑酷追逐这类经典 3A 动作冒险设计</b>",
                "<b>沿东归之路推进剧情</b>，穿插双人合作搬重物、钻缝隙、跑酷追逐这类<b>经典 3A 动作冒险设计</b>")
d["worldview"]["coreLoop"]["value"] = cl
# references 补 anime/manga (原只有 game+film) —— 把一部 film 换成 anime，再补一部
refs = d["aesthetic"]["summary"]["references"]
# 现有: 神海4(game) 最后生还者(game) 对马(game) 黑神话(game) 敦煌(film) 七武士(film) 战神(game)
# 把 敦煌(film) 保留, 七武士(film) 换成 动画《狼与香辛料》(anime,旅途护送母题) 拉 type
for r in refs:
    if r["title"]=="七武士":
        r.update({"type":"anime","title":"黄金神威","year":"2018",
                  "note":"<b>历史苦旅与硬核生存的动画母题</b>；风霜旅途与人物群像的叙事参照"})
d["aesthetic"]["summary"]["references"]=refs
# overview 末段改问号收尾
ps = d["story"]["overview"]["paragraphs"]
ps[-1] = ps[-1].replace("长风几万里，吹不散的，是你要把捷报和孩子，一起带回家的那口气。",
                        "长风几万里，吹不散的，是你要把捷报和孩子一起带回家的那口气——可这条路的尽头，等你的到底是团圆，还是史书早写好的九殁蕃戎？")
d["story"]["overview"]["paragraphs"]=ps
save("gui-tang", d)

# ---------- tides-of-annihilation ----------
d = load("tides-of-annihilation")
# tagline 41→短
d["story"]["overview"]["tagline"] = "<b>伦敦碎了，只剩你一个</b>——左手唤起圆桌亡魂，右手从半神手里抢回姐姐。"
# mainStory 加粗超30拆分
ms = d["worldview"]["mainStory"]["value"]
ms = ms.replace("<b>找回失散的姐姐/家人、修复破碎的世界、向毁灭伦敦的阿瓦隆半神复仇</b>",
                "<b>找回失散的姐姐</b>、修复破碎的世界、向毁灭伦敦的<b>阿瓦隆半神复仇</b>")
d["worldview"]["mainStory"]["value"] = ms
# references 跨度<20: 现有最早2005最晚2019=14。加一部老片。Fate2006改早期; 换"亚瑟王斗兽争霸2017"→"石中剑1963"(anime->film)拉跨度
refs=d["aesthetic"]["summary"]["references"]
for r in refs:
    if r["title"]=="亚瑟王：斗兽争霸":
        r.update({"type":"film","title":"石中剑","year":"1963",
                  "note":"<b>亚瑟王传说的经典动画影像原型</b>；圆桌与魔法的美学源头"})
d["aesthetic"]["summary"]["references"]=refs
# definition 201→压缩到180内
d["aesthetic"]["summary"]["definition"]=(
 "「骑士幻想 × 现代废墟」，是把<b>亚瑟王传说的中世纪奇幻</b>和<b>被侵蚀的现代伦敦</b>撞进同一帧的美学。"
 "底子是写实的都市废墟——扭曲的摩天楼、异化成无机物的街景；变异在于圆桌骑士、圣杯与九女巫以幽灵姿态显现其间。"
 "视觉主打<b>油画般的光影</b>与<b>镜面倒影的双世界</b>母题。色彩以废墟灰雾冷调撞骑士元素之力的金蓝红为骨，"
 "整体宏大、诗意又压抑，是国产 3A 里少见的纯西方奇幻取向。")
# evolution 301→压缩到280内
d["aesthetic"]["summary"]["evolution"]=(
 "「高速动作 + 电影级 Boss 奇观」这套美学血脉清晰。<b>2000 年代</b>《鬼泣》定义了 Stylish Action 的连招美学，"
 "《猎天使魔女》（2009）把跑酷式大场面推向极致——湮灭之潮的战斗正是这一脉，官方明确「受鬼泣启发而非魂类」。"
 "<b>2005 年</b>《旺达与巨像》用「攀爬巨型 Boss 即关卡」重定义了空间想象，成了本作巨像骑士的母版。"
 "<b>2018 年</b>《战神》示范了如何把神话史诗做成电影级单人叙事。团队里有《如龙》《刺客信条》的老兵，"
 "赌的是国产 3A 走出中国题材舒适区的这一步。")
save("tides-of-annihilation", d)

# ---------- windrose ----------
d = load("windrose")
# tagline 45→短
d["story"]["overview"]["tagline"] = "<b>你死在了黑胡子手里</b>——某种力量把你丢回荒岛，只剩一颗复仇的心。"
# mainStory 加粗超30拆分
ms=d["worldview"]["mainStory"]["value"]
ms=ms.replace("<b>从荒岛上一无所有开始，建造、锻造、招募船员、打造战船，最终向暗算你的黑胡子复仇</b>",
              "<b>从荒岛一无所有开始</b>，建造、锻造、招募船员、打造战船，最终向暗算你的<b>黑胡子复仇</b>")
d["worldview"]["mainStory"]["value"]=ms
# references type 仅2种(game+film)。把"森林2018"(game)换成动画拉type
refs=d["aesthetic"]["summary"]["references"]
for r in refs:
    if r["title"]=="森林":
        r.update({"type":"anime","title":"海贼王","year":"1999",
                  "note":"<b>海盗冒险的热血浪漫母题</b>；船员羁绊与航海自由的氛围参照"})
d["aesthetic"]["summary"]["references"]=refs
# definition 217→压缩
d["aesthetic"]["summary"]["definition"]=(
 "「海盗浪漫写实」，是把<b>加勒比黄金时代的海盗自由</b>和<b>荒岛求生的粗粝质感</b>缝进同一片开放海域的美学。"
 "底子是虚幻5的写实海洋——出色波浪建模能让最大的船显得渺小，海洋日落、精致船只、浓密丛林是最受好评的画面；"
 "变异在于建筑从鲁滨逊式荒岛小屋一路演进到加勒比庄园。氛围另一半靠<b>船歌、海浪与水手号子</b>撑起。"
 "色彩以海天蔚蓝暖阳撞诅咒沼泽阴绿为骨，整体浪漫开阔，又在内陆迷雾里透出黑暗。")
save("windrose", d)

# ---------- mistfall-hunter ----------
d = load("mistfall-hunter")
# tagline 48→短
d["story"]["overview"]["tagline"] = "<b>诸神死了，血化成金雾</b>——你被少女唤醒，一次次冲进雾里带回流金。"
# mainStory / coreLoop 加粗超30拆分
ms=d["worldview"]["mainStory"]["value"]
ms=ms.replace("<b>被神秘少女「露」用超自然力量复活、赋予不朽肉体的英雄「猎金人」</b>",
              "<b>被神秘少女「露」复活</b>、获赋不朽肉体的英雄<b>「猎金人」</b>")
ms=ms.replace("<b>猎杀被金雾腐蚀的怪物、搜集「流金」，去修复破损的「命运之网」</b>",
              "<b>猎杀被金雾腐蚀的怪物</b>、搜集「流金」，去修复破损的<b>「命运之网」</b>")
d["worldview"]["mainStory"]["value"]=ms
cl=d["worldview"]["coreLoop"]["value"]
cl=cl.replace("<b>带装备进图 → 清怪搜刮流金装备、做任务、挑战 Boss → 提防其他小队(PvP) → 携战利品撤离</b>",
              "<b>带装备进图</b> → 清怪搜刮流金装备、做任务、挑战 Boss → 提防其他小队(PvP) → <b>携战利品撤离</b>")
d["worldview"]["coreLoop"]["value"]=cl
# definition 203→压缩
d["aesthetic"]["summary"]["definition"]=(
 "「哥特黑暗奇幻」，是把<b>诸神黄昏的北欧末世</b>和<b>搜打撤的高压死亡循环</b>缝进同一片迷雾大陆的美学。"
 "底子是阴暗沉郁的写实黑暗奇幻——幽暗地牢、残破要塞、被腐蚀的生物；变异在于「<b>金色迷雾</b>」这个由神血凝成的核心母题，"
 "既是世界观来源，也是最醒目的视觉符号。色彩以幽冥暗蓝黑撞金雾的腐蚀金为骨，"
 "整体肃穆、压抑，是那种一步一杀机的哥特死亡美学。")
# evolution 328→压缩
d["aesthetic"]["summary"]["evolution"]=(
 "「黑暗奇幻 + 搜打撤」是近几年才打通的新赛道。<b>2017 年</b>《逃离塔科夫》定义了硬核搜打撤的高风险循环，"
 "让「死亡掉光一切」成为品类的紧张感来源。<b>2023 年</b>《Dark and Darker》第一个把「黑暗奇幻 + 撤离」缝在一起，"
 "是雾影猎人最直接的对标——差异在于本作走第三人称、更偏魂味流畅。战斗与氛围上，它站在《黑暗之魂》到《艾尔登法环》"
 "这条 FromSoftware 死亡美学线上。发行方 Skystone 由《暗黑破坏神》缔造者联合创立，美术血脉由此而来。")
save("mistfall-hunter", d)

print("修复完成")
