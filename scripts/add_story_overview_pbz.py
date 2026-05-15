"""为影之刃零 story 字段补充 overview（开篇式世界观长文）"""
import json
from pathlib import Path

JSON = Path(__file__).resolve().parent.parent / "data" / "games" / "phantom-blade-zero.json"

# 开篇式宣传文 —— 像小说发售前的内封简介
# 三段式：① 世界图景 ② 主角处境 ③ 角色对抗与剧情驱动钩子
overview = {
    "tagline": "六十六天，一柄残刀，一个被江湖弃绝的名字。",
    "paragraphs": [
        "这是一个<b>失了序的江湖</b>。古塔与瀑布还立在那里，水墨意境的山河依旧，但齿轮的咬合声、蒸汽的嘶鸣、机械义肢摩擦皮肉的钝响，正一寸寸从地底渗上来。曾经的侠客为了变得更强，<b>把自己的血肉换成了钢铁</b>，他们戴上面具，以「<b>怪面</b>」的身份盘踞各方——这不再是刀光剑影的武林，是一片被欲望与工业啃噬过的<b>功夫朋克废墟</b>。",
        "你扮演的人叫「<b>魂</b>」，<b>影门</b>最锋利的刺客之一。一夜之间，你被自己人按上谋杀帝师的罪名，伤重将死，体内只剩<b>六十六天</b>气数。从你睁开眼的那一刻起，整个江湖都在追杀你——你必须在寿命燃尽之前，找到陷害你的人，问出那个你不愿相信的真相。",
        "你不是一个人在战斗，但每一个出现在你面前的人，都不会只是过客。<b>影门旧友</b>会在岔路口替你挡刀，也会在结局里举刀向你；<b>怪面首领</b>嘶哑地讲述他们为什么甘愿变成怪物；幕后那条若隐若现的<b>红色丝线</b>，缠住了天下侠客的咽喉。你怎么打、怎么选、放过谁、错信谁，<b>八个结局</b>就在这条命的尽头分岔——这不是一个关于复仇的故事，是一个关于「<b>来不及</b>」的故事。"
    ]
}

with open(JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

story = data.get("story", {})

# 把 overview 放在 story 内部，紧跟 title 之后、dims 之前
new_story = {}
for k, v in story.items():
    new_story[k] = v
    if k == "title":
        new_story["overview"] = overview

# 如果原本没有 title，直接把 overview 放最前面
if "overview" not in new_story:
    rebuilt = {"overview": overview}
    rebuilt.update(new_story)
    new_story = rebuilt

data["story"] = new_story

with open(JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("OK: story.overview added.")
print("story keys =", list(new_story.keys()))
