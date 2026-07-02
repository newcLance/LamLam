# -*- coding: utf-8 -*-
"""新8批 v2.5 自检：字数/加粗/禁用词/anchorRule/references多样性。"""
import json, re
from pathlib import Path

BASE = Path("d:/ecnalClaw/output/game-tracker-v2")
GDIR = BASE / "data" / "games"
SLUGS = ["lost-soul-aside","onimusha-way-of-the-sword","gujian","gui-tang",
         "tides-of-annihilation","windrose","mistfall-hunter"]

BLACK = ["本作","该作","玩家将","综上所述","呈现出","营造出","塑造出","诠释",
         "由来已久","自古以来","源远流长","精彩绝伦","史诗般的","传奇巨作","经典之作",
         "唯美","精致","极致","绝美","惊艳"]
# 「华丽」作为 Stylish Action 玩法术语（华丽连段/华丽动作）合法，不入黑名单

def cnt_b(s): return s.count("<b>")
def txt_len(s): return len(re.sub(r"<[^>]+>","",s))
def bold_over30(s):
    return [b for b in re.findall(r"<b>(.*?)</b>", s) if len(b)>30]

def check(slug):
    d = json.load(open(GDIR/f"{slug}.json", encoding="utf-8"))
    issues=[]
    # worldview
    wv=d.get("worldview",{})
    for k in ["background","mainStory","combat","coreLoop"]:
        v=wv.get(k,{}).get("value","")
        L=txt_len(v); b=cnt_b(v)
        if not (100<=L<=240): issues.append(f"worldview.{k} 字数 {L}(应120-220附近)")
        if b<2: issues.append(f"worldview.{k} 加粗 {b}(应≥2)")
        for ov in bold_over30(v): issues.append(f"worldview.{k} 加粗超30字: {ov[:20]}..")
    # story.overview
    ov=d.get("story",{}).get("overview",{})
    tg=ov.get("tagline","")
    if txt_len(tg)>40: issues.append(f"tagline 过长 {txt_len(tg)}")
    ps=ov.get("paragraphs",[])
    tot=sum(txt_len(p) for p in ps); tb=sum(cnt_b(p) for p in ps)
    for i,p in enumerate(ps):
        Lp=txt_len(p)
        if not (110<=Lp<=240): issues.append(f"overview.p{i+1} 字数 {Lp}(应120-220)")
    if not (380<=tot<=640): issues.append(f"overview 总字数 {tot}(应380-600)")
    if tb<6: issues.append(f"overview 加粗总数 {tb}(应≥6)")
    if ps and not re.search(r"[？…?]\s*$", re.sub(r"<[^>]+>","",ps[-1]).strip()):
        issues.append("overview 末段未以问号/省略号收尾")
    # story.dims
    dims=d.get("story",{}).get("dims",[])
    if len(dims)<8: issues.append(f"dims 仅 {len(dims)}(应8)")
    # aesthetic.summary
    su=d.get("aesthetic",{}).get("summary",{})
    refs=su.get("references",[])
    types=set(r.get("type") for r in refs)
    yrs=[int(re.search(r"\d{4}",str(r.get("year",""))).group()) for r in refs if re.search(r"\d{4}",str(r.get("year","")))]
    if not (5<=len(refs)<=8): issues.append(f"references {len(refs)}(应5-8)")
    if len(types)<3: issues.append(f"references type 种类 {len(types)}(应≥3): {types}")
    if yrs and (max(yrs)-min(yrs))<20: issues.append(f"references 跨度 {max(yrs)-min(yrs)}年(应≥20)")
    dfn=su.get("definition",""); evo=su.get("evolution","")
    if not (120<=txt_len(dfn)<=200): issues.append(f"summary.definition 字数 {txt_len(dfn)}(应120-180)")
    if not (140<=txt_len(evo)<=300): issues.append(f"summary.evolution 字数 {txt_len(evo)}(应150-280)")
    # aesthetic 5维卡片 anchorRule + 加粗
    for card in ["scene","costume","ui","symbol"]:
        c=d.get("aesthetic",{}).get(card,{})
        v=c.get("value","")
        if "anchorRule" not in c: issues.append(f"aesthetic.{card} 缺 anchorRule")
        if cnt_b(v)<2: issues.append(f"aesthetic.{card} 加粗 {cnt_b(v)}(应≥2)")
        for ov2 in bold_over30(v): issues.append(f"aesthetic.{card} 加粗超30: {ov2[:18]}..")
    # 禁用词全文扫描（排除合法语境）
    blob=json.dumps(d,ensure_ascii=False)
    for w in BLACK:
        if w in blob:
            # 华丽 允许在"华丽连段/华丽动作/华丽剑"语境
            issues.append(f"命中禁用词: {w}")
    # playerExp 4子字段
    for grp in ["media","community"]:
        g=d.get("playerExp",{}).get(grp,{})
        for sub in ["memory","excitement","pain","churn"]:
            if not g.get(sub): issues.append(f"playerExp.{grp}.{sub} 缺失")
    # 英文双引号检测（文案内）
    return issues

allok=True
for s in SLUGS:
    iss=check(s)
    status = "OK" if not iss else "FAIL"
    if iss: allok=False
    print(f"=== {s}: {status} ===")
    for i in iss: print("   -", i)
print("\n全部通过" if allok else "\n存在问题需修")
