"""按 v2.4 五大美术原则刷新影之刃零 aesthetic 模块"""
import json
import re
from pathlib import Path

JSON = Path(__file__).resolve().parent.parent / "data" / "games" / "phantom-blade-zero.json"

# 五大原则编号：1=80/20  2=色彩刺客  3=剪影定生死  4=信息磨损  5=UI即世界
new_aesthetic_main = {
    "scene": {
        "title": "暗黑水墨 × 蒸汽锈蚀 — 一眼锁死的双色江湖",
        # 命中：① 80/20（水墨×蒸汽）② 色彩刺客（暗黑底色 + 高对比锈红）④ 信息磨损（雾气/锈蚀/裂痕）
        "value": "公式 = <b>80% 中式水墨山地</b>（飞檐古塔、悬崖峡谷、雾气浮岚）×<b>20% 蒸汽工业废墟</b>（锈蚀管道、齿轮塔、漏油的金属裂缝）。色彩极简到只剩两种：环境主色是<b>低明度墨黑灰青</b>，情绪色是<b>高饱和锈红</b>（火把、丝线、血迹），其他颜色被压到几乎无声。墙面有风化、栈道有断裂、机关有焦痕——任何一帧画面都<b>带着被时间和暴力啃过的痕迹</b>，自带末世故事感。",
        "anchorRule": [1, 2, 4]
    },
    "costume": {
        "title": "流线布衣 vs 张狂铁甲 — 涂黑也能秒辨敌我",
        # 命中：① 80/20（布衣武侠×机械义肢）③ 剪影定生死（流线 vs 张狂、布料 vs 钢铁）④ 信息磨损（残破/缺口）
        "value": "主角「魂」走<b>流线收敛剪影</b>：深色布衣 + 皮甲，<b>残破长袍</b>带焦痕缺口，腰间多刀；线条利落、对称、轻盈。机械化「<b>怪面</b>」走<b>张狂不对称剪影</b>：金属外骨骼 + 暴露管线，肩甲与义肢做出戏剧性的<b>非对称突出</b>，沉重冰冷。两者一个是<b>布料/皮革的有机柔感</b>，一个是<b>黑铁/黄铜的工业硬感</b>——把所有人涂成纯黑剪影，谁是主角、谁是 Boss 一秒看穿。",
        "anchorRule": [1, 3, 4]
    },
    "ui": {
        "title": "极简到几乎隐身的战斗 HUD",
        # 命中：⑤ UI即世界（极简 + 部分 Diegetic + 信息密度低）
        "value": "走<b>极简 + 半 Diegetic</b>路线：常态战斗几乎没有满屏 HUD，核心信息只压在屏幕底部一条窄带（HP/杀意/武器）。伤害反馈不靠跳红字，靠<b>喷血量、衣甲破损、敌人受击硬直</b>还原打击感；菜单和 Loading 全部用<b>水墨晕染 + 书法字型</b>，把 UI 溶进世界观。整体信息密度被刻意压到<b>「能不显示就不显示」</b>，让美术 100% 占领屏幕。",
        "anchorRule": [5]
    },
    "symbol": {
        "title": "红色丝线 × 齿轮 × 面具 — 三件套锚定双色母题",
        # 命中：① 80/20（武侠符号×机械符号）② 色彩刺客（暗底+锈红母题）
        "value": "三大反复出现的<b>视觉锚点</b>：<b>红色丝线</b>（命运/操控的隐喻，连带血液与执念）、<b>齿轮咬合</b>（蒸汽机械改造的身份标记）、<b>面具</b>（人性与机械化的分界线）。次级符号包括刀光剑影的弧线、墨迹飞溅、符文暗纹——传统武侠语汇 × 工业机械语汇严格按 80/20 配比并置。色彩母题被锁死在<b>「墨黑灰青 × 高饱和锈红」</b>双色之中，缩到邮票大小也能被认出。",
        "anchorRule": [1, 2]
    },
    "promo": {
        "title": "「功夫朋克」一词锁死品类，双色影调贯穿物料",
        # 命中：① 80/20（功夫×朋克 高概念）② 色彩刺客（双色影调统一）
        "value": "宣发用一个原创词「<b>功夫朋克</b>」（Kungfu Punk）一刀切死品类——80% 是李小龙/成龙的<b>功夫熟悉感</b>，20% 是机械蒸汽的<b>朋克变异感</b>。预告片剪辑极快，主打招式华丽度 + 打击反馈的瞬时冲击；Key Art 构图固定在<b>暗黑底色 + 高对比锈红光</b>的双色影调里，所有物料、海报、社媒头图共用同一组色彩 DNA。短视频环境下的辨识度被刻意拉到 0.5 秒级。",
        "anchorRule": [1, 2]
    }
}

with open(JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

# 保留 rivals
rivals = data.get("aesthetic", {}).get("rivals", [])
data["aesthetic"] = {**new_aesthetic_main, "rivals": rivals}

with open(JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# === v2.4 五大原则自检 ===
print("=== v2.4 aesthetic 自检 ===\n")

KEYWORDS = {
    1: ["×", "+", "与", "混合"],  # 80/20 碰撞
    2: ["主色", "底色", "基调", "情绪色", "高饱和", "母题", "双色", "对比"],  # 色彩刺客
    3: ["vs", "对比", "对立", "反差", "剪影", "轮廓", "材质", "流线", "张狂", "对称", "不对称"],  # 剪影
    4: ["磨损", "战损", "锈蚀", "残破", "风化", "缺口", "血污", "焦痕", "裂痕", "修补", "漏油", "啃"],  # 信息磨损
    5: ["极简", "Diegetic", "留白", "隐藏", "融入", "沉浸", "minimal", "信息密度"]  # UI即世界
}

for key, card in new_aesthetic_main.items():
    val = card["value"]
    plain = re.sub(r"<[^>]+>", "", val)
    bolds = re.findall(r"<b>(.*?)</b>", val)
    declared = card["anchorRule"]
    hits = []
    for rule_id, kws in KEYWORDS.items():
        if any(k in val for k in kws):
            hits.append(rule_id)
    declared_set = set(declared)
    hit_set = set(hits)
    missing = declared_set - hit_set
    extra = hit_set - declared_set
    
    print(f"[{key}] anchorRule声明={declared} 实际命中={sorted(hits)}")
    print(f"  字数={len(plain)} <b>={len(bolds)}")
    if missing:
        print(f"  ⚠️ 声明但未命中关键词: {sorted(missing)}")
    if extra:
        print(f"  ℹ️ 命中但未声明: {sorted(extra)}")
    over30 = [b for b in bolds if len(b) > 30]
    if over30:
        print(f"  ❌ 超长加粗 {len(over30)} 处")
    print()

print("rivals 保留:", len(rivals), "条")
