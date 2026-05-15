"""按五维钩子法则（v2.3）重写影之刃零 story.overview"""
import json
from pathlib import Path

JSON = Path(__file__).resolve().parent.parent / "data" / "games" / "phantom-blade-zero.json"

# 五维钩子落点自检：
# ① 高概念碰撞：tagline 直接亮出 "功夫 × 朋克"
# ② 极限处境：第 2 段 "六十六天" + "全江湖追杀"
# ③ 灰度悖论：第 3 段 "替你挡刀的旧友会举刀向你" + "甘愿变成怪物的首领"
# ④ 情绪内核：第 3 段末 "不是关于复仇，是关于来不及"
# ⑤ 信息留白：第 3 段末以问句串收尾 + 不剧透 8 结局

overview = {
    "tagline": "<b>功夫 × 朋克</b>，一柄残刀挑开江湖的第六十六天。",
    "paragraphs": [
        # 第 1 段：高概念碰撞 + 视觉奇观
        # 钩子①：水墨武侠 × 蒸汽机械（双重异质并置）
        "想象一座<b>水墨晕开的江湖</b>，下面藏着另一座<b>钢铁咬合的江湖</b>。古塔与瀑布还在，宝塔的飞檐挑着夕光；可只要你低头，就能看见<b>蒸汽从青石板缝里嘶嘶地往上冒</b>，听见齿轮在地底咬合的钝响。曾经的武林高手为了变得更强，亲手剜掉自己的血肉，换上钢铁义肢，戴上面具——他们叫「<b>怪面</b>」。这不再是刀光剑影的武林，是一片被欲望和工业啃噬过的<b>功夫朋克废墟</b>。",
        # 第 2 段：极限处境 + 第二人称代入
        # 钩子②：六十六天倒计时；体感画面
        "你叫「<b>魂</b>」——影门最锋利的那把刀。前一夜你还是组织里说一不二的精英刺客，下一夜，你就被自己人按上了谋杀帝师的罪名。剑伤穿过你的胸口，毒咬住你的心脉，体内只剩<b>六十六天气数</b>。从你睁开眼的那一刻起，整个江湖都在朝你扑过来——通缉令贴满了每一座驿站，赏金挂在每一个旧识的腰间。你必须赶在这条命燃尽之前，从他们之中找出那只动手的手；问题是，你已经不知道还能信谁了。",
        # 第 3 段：灰度悖论 + 情绪内核 + 信息留白
        # 钩子③：旧友的反差；钩子④：A/B 反差句；钩子⑤：开放式问号串收尾
        "<b>替你挡过刀的旧友</b>，会在岔路口举刀向你；面具下的怪面首领，会在断气前，嘶哑地讲完他为什么甘愿换掉那张脸。幕后那条若隐若现的<b>红色丝线</b>，缠住了天下侠客的咽喉，也缠住了你。这不是一个关于复仇的故事，是一个关于「<b>来不及</b>」的故事——你怎么打？怎么选？放过谁？错信谁？六十六天之后，<b>你想成为他们口中的哪一个魂</b>？"
    ]
}

with open(JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

data.setdefault("story", {})
data["story"]["overview"] = overview

# 保持 key 顺序：title -> overview -> dims
ordered = {}
for k in ["title", "overview", "dims"]:
    if k in data["story"]:
        ordered[k] = data["story"][k]
# 加入其它意外键
for k, v in data["story"].items():
    if k not in ordered:
        ordered[k] = v
data["story"] = ordered

with open(JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 自检报告
import re
print("=== 五维钩子自检 ===")
print(f"[tagline] {overview['tagline']}")
for i, p in enumerate(overview["paragraphs"], 1):
    bold_count = len(re.findall(r"<b>.*?</b>", p))
    char_count = len(re.sub(r"<[^>]+>", "", p))
    print(f"[第{i}段] 字数={char_count} <b>={bold_count}")
total_bold = sum(len(re.findall(r"<b>.*?</b>", p)) for p in overview["paragraphs"]) + len(re.findall(r"<b>.*?</b>", overview["tagline"]))
total_chars = sum(len(re.sub(r"<[^>]+>", "", p)) for p in overview["paragraphs"])
print(f"[总计] 总字数={total_chars} 全篇<b>={total_bold}")
print(f"[钩子⑤] 第3段末尾: ...{overview['paragraphs'][2][-30:]}")
