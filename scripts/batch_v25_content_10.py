# -*- coding: utf-8 -*-
"""v2.5 第十批 2 款 Party 游戏：eggy-party / fall-guys

注意：所有中文文案里如果要嵌入引号，必须用「」或（），严禁英文双引号嵌套。
keywords 数组里可以用英文双引号。

派对游戏没有传统叙事，因此：
- worldview.mainStory 改写为「赛事循环 / 关卡循环」
- worldview.combat 改写为「对抗机制 / 大逃杀循环」
- story_overview 写「游戏文化现象 / 社交意义」
"""
import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "games"

# ============================================================
#  蛋仔派对 eggy-party
# ============================================================
EGGY = {
    "worldview": {
        "background": {
            "title": "永恒欢乐的蛋仔宇宙——色彩斑斓的蛋仔岛 Eggy Island 机关派对乐园",
            "value": "故事发生在<b>永恒欢乐的蛋仔宇宙 Eggyverse</b>——一片没有时间线、没有黑夜、不会真正受伤的<b>色彩斑斓派对世界</b>。主舞台是漂浮在云海中的<b>蛋仔岛 Eggy Island</b>——糖果色山丘、棉花糖云、果冻海滩之间散落着<b>弹射器、旋转锤、传送带、蜜糖陷阱、大风扇、香蕉皮、巨型保龄球</b>等玩具化机关。整座岛由<b>UGC 关卡库（蛋仔工坊）</b>持续扩张——你下一秒踩进的关卡可能是哪位中国玩家昨晚才搭出的奇思妙想。",
            "keywords": ["Eggyverse", "Eggy Island", "玩具化机关", "蛋仔工坊"]
        },
        "mainStory": {
            "title": "赛事循环：你是 Eggy 蛋仔——在 32 人派对赛上靠运气与小聪明抢到最后王冠",
            "value": "本作没有传统主线，取而代之的是<b>永不落幕的派对赛事循环</b>。你扮演<b>一颗会蹦跳的可爱蛋形角色 Eggy</b>，圆滚滚没有手脚却能滚跳推抓。每场派对最多<b>32 颗蛋仔</b>同台，按<b>巅峰对决/团队竞技/休闲玩法/工坊地图</b>分流：<b>巅峰赛多轮淘汰只剩一颗摘王冠、团队赛抢蛋仔/守城/捉迷藏、休闲赛在工坊里玩你画我猜与狼人杀变体</b>。网易把<b>问卷调研</b>嵌进运营——你今天玩到的新模式很可能源自某次中国 7-15 岁玩家票选。",
            "keywords": ["32 人派对赛", "巅峰王冠", "团队竞技", "网易问卷运营"]
        },
        "combat": {
            "title": "对抗机制：弹射陷阱+互相推抓+运气抽奖——以「滚下平台时还能笑出声」为核心",
            "value": "「对抗」不是暴力战斗，而是<b>玩具化物理喜剧</b>。你能依赖的招式只有<b>跳、扑抓、翻滚、抱起队友/对手再往陷阱里一扔</b>——抓人有 1 秒读条，被抓方可以挣脱。地图机关才是真正的对手：<b>突然旋转的大锤、定时升起的尖刺、缩小的浮岛、随机风向的传送门</b>。<b>那次你领先一步即将冲线、却被旋转锤一甩飞回起点的瞬间</b>就是蛋仔的反内卷哲学——<b>「滚下平台时还能笑出声」</b>。胜负重要，但更重要的是和朋友连麦时那阵共同的笑声。",
            "keywords": ["扑抓推搡", "旋转锤陷阱", "反内卷喜剧", "连麦欢笑"]
        },
        "coreLoop": {
            "title": "组队 → 选派对模式 → 闯关淘汰 → 摘王冠 → 用蛋币换皮肤捏脸 → 进工坊造关卡",
            "value": "你玩到的是<b>「移动端国民级派对 + UGC 强生态」</b>——结构是<b>派对赛对局 + 蛋仔广场社交 + 工坊创作 + 蛋仔捏捏</b>四层骨架。日常活动包括<b>组队进巅峰赛/团队赛、刷蛋币换皮肤与挂件、在蛋仔广场和好友贴贴跳舞、进工坊用积木编辑器搭关卡发布给全国玩家试玩、参加 KOL 主播开的房间</b>。养成线是<b>赛季手册+段位系统+蛋仔捏脸+皮肤盲盒+工坊作者粉丝数</b>。<b>2022 年内测 → 2023 年全民爆款</b>，蛋仔成为中国 7-15 岁孩子放学后默认的社交平台。",
            "keywords": ["32 人对局", "蛋仔工坊", "蛋仔广场", "KOL 直播间"]
        }
    },
    "story_overview": {
        "tagline": "<b>32 颗蛋仔挤在彩虹平台上</b>——下一颗摔下去的会不会是你？",
        "paragraphs": [
            "想象一片<b>永恒欢乐的蛋仔宇宙 Eggyverse</b>——一片没有时间线、没有黑夜、不会真正受伤的色彩斑斓派对世界。主舞台是漂浮在云海中的<b>蛋仔岛 Eggy Island</b>——糖果色山丘、棉花糖云、果冻海滩之间散落着<b>弹射器、旋转锤、传送带、蜜糖陷阱、大风扇、巨型保龄球</b>等玩具化机关。整座岛由<b>蛋仔工坊 UGC</b>持续扩张——你下一秒踩进的关卡可能是某位中国玩家昨晚才搭出的奇思妙想。",
            "本作没有主角和反派——你扮演一颗会蹦跳的<b>蛋形角色 Eggy</b>，圆滚滚没有手脚却能滚跳推抓。每场派对最多 32 颗蛋仔同台，按巅峰对决/团队竞技/休闲玩法/工坊地图分流。网易把<b>问卷调研</b>嵌进日常运营——你今天玩到的新模式很可能源自某次中国 7-15 岁玩家票选。蛋仔的真正特殊性在于<b>它不是单机，而是放学后默认的社交平台</b>——同班同学连麦组队，比 QQ 群还热闹。",
            "<b>那次你领先一步即将冲线、却被旋转锤一甩飞回起点的瞬间</b>，网易把派对游戏做成中国 7-15 岁孩子的童年坐标——你玩的不是游戏，是<b>「滚下平台时还能笑出声」这道反内卷快乐主义</b>；<b>那场你和好友连麦在蛋仔广场互相贴贴拍照的桥段</b>——蛋仔捏脸 + 皮肤让你明白<b>「派对的核心从来不是赢，而是和谁一起摔倒」</b>；<b>那次你进入某位陌生工坊作者搭的奇葩关卡笑到肚子疼的时刻</b>，UGC 强生态让蛋仔从一款游戏变成了一个文化现象。这不是关于打败别人的故事，是<b>「你下一次摔下平台时，是更想笑出来，还是想再来一局」</b>？"
        ]
    },
    "aesthetic_summary": {
        "label": "糖果色玩具乐园 × UGC 社交派对",
        "definition": "<b>糖果色玩具乐园 × UGC 社交派对</b>，是网易把<b>潮流玩具盲盒美学</b>（圆润蛋形、马卡龙糖果色、Q 弹手感、蛋仔捏脸自定义）和<b>儿童游乐园机关玩具传统</b>（弹射器、旋转锤、传送带、蜜糖陷阱）以及<b>移动端社交派对界面</b>（连麦小窗、表情贴贴、广场聚会、工坊编辑器）三层缝合在<b>32 人派对竞技</b>外壳里的混血美学。底色是<b>糖豆人 × 中国潮玩盲盒</b>双重血统；变异在于<b>把 UGC 关卡编辑器做成日常入口</b>——蛋仔工坊本身就是一座永远长大的乐园。",
        "evolution": "「派对乐园 + 玩具机关 + UGC 社交」视觉线跨越百年。<b>1955 年</b>迪士尼<b>加州迪士尼乐园</b>开园定义现代主题乐园糖果色机关美学母版。<b>1989 年</b>日本电视综艺<b>《Takeshi's Castle 风云！武铁城》</b>定义巨型机关闯关综艺范式——蛋仔派对赛的精神祖父。<b>2003 年</b>任天堂<b>《超级马里奥派对》</b>把派对游戏做成主机国民玩法。<b>2009 年</b><b>Roblox</b>把 UGC 关卡库做成欧美儿童社交平台母版。<b>2017 年</b>泡泡玛特<b>Molly 盲盒</b>把潮流玩具盲盒做成中国年轻人收藏母版。<b>2020 年</b>Mediatonic<b>《糖豆人 Fall Guys》</b>定义现代派对大逃杀品类母版——蛋仔最直接对标作品。<b>2022 年</b>《蛋仔派对》全平台公测+网易问卷调研驱动迭代。<b>2023 年</b>蛋仔派对 DAU 破 4000 万——把派对游戏推到中国 7-15 岁国民级现象。",
        "references": [
            {"type": "show", "title": "Takeshi's Castle 风云！武铁城（日本综艺）", "year": "1989", "note": "<b>巨型机关闯关综艺</b>电视范式；蛋仔派对赛精神祖父"},
            {"type": "show", "title": "Wipeout 美版终极挑战（ABC 综艺）", "year": "2008", "note": "<b>超现实障碍赛</b>真人秀普及版；可对照蛋仔多人淘汰调性"},
            {"type": "game", "title": "Fall Guys 糖豆人", "year": "2020", "note": "<b>现代派对大逃杀</b>品类母版；蛋仔最直接对标作品"},
            {"type": "game", "title": "超级马里奥派对 Mario Party", "year": "2003", "note": "<b>主机派对游戏</b>国民玩法母版；本作 32 人多模式精神参照"},
            {"type": "game", "title": "Roblox", "year": "2009", "note": "<b>UGC 关卡库儿童社交平台</b>母版；蛋仔工坊精神血统"},
            {"type": "art", "title": "泡泡玛特 Molly 盲盒手办", "year": "2017", "note": "<b>潮流玩具盲盒</b>当代收藏母版；蛋仔皮肤捏脸视觉精神养分"},
            {"type": "film", "title": "小美人鱼 The Little Mermaid 海底世界", "year": "1989", "note": "<b>糖果色梦幻动画美术</b>电影母版；Eggy Island 调色精神参照"},
            {"type": "art", "title": "南瓜派对软糖玩具广告档案", "year": "1995", "note": "<b>儿童糖果玩具广告美学</b>真实档案；蛋仔 Q 弹手感视觉血统养分"}
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
#  糖豆人 fall-guys
# ============================================================
FALL_GUYS = {
    "worldview": {
        "background": {
            "title": "无叙事永恒综艺时空——超现实综艺障碍赛道里果冻豆永远在排队上场",
            "value": "故事发生在<b>无叙事时间线的永恒综艺时空</b>——整个游戏世界是一档<b>永远不会停播的超现实电视综艺</b>。主舞台是<b>漂浮在粉紫色云海中的巨型障碍赛道</b>——糖果色平台、黏液池、旋转锤、巨型滚球、跷跷板、风扇墙、蜂巢门<b>组成的几十张赛道地图，全部漂在没有地平线的天空里</b>。Mediatonic 把<b>儿童电视综艺布景 + 拉斯维加斯霓虹灯</b>缝合成一台永远循环的电视秀，你和 59 颗豆子永远在排队等下一回合。",
            "keywords": ["永恒综艺", "漂浮赛道", "黏液池", "60 豆排队"]
        },
        "mainStory": {
            "title": "赛事循环：你是一颗果冻豆 Fall Guy——60 人开局只为活到最后一轮戴上王冠",
            "value": "本作没有传统主线，取而代之的是<b>每局 60 人豆豆大逃杀循环</b>。你扮演一颗<b>圆鼓鼓的果冻豆 Fall Guy</b>——形似一根会蹦跳的彩色软糖，戴着千奇百怪的 cosplay 皮肤（从恐龙到热狗到皮卡丘联动）。每场比赛分<b>4-5 轮淘汰</b>：第一轮通常是 60 人狂奔的赛跑赛或团队赛，每轮按门槛淘汰一批。最终轮 1-6 颗豆子角逐<b>黄金王冠</b>。Mediatonic（已被 Epic Games 收购）把综艺节目玩法浓缩成<b>10 分钟极致的紧张+滑稽</b>。",
            "keywords": ["60 豆开局", "黄金王冠", "Mediatonic", "Epic 收购"]
        },
        "combat": {
            "title": "大逃杀循环：滑倒+拉扯+黏液+尖刺——以「摔得越惨笑得越响」为核心的物理喜剧",
            "value": "「对抗」不是真正的战斗，而是<b>果冻豆物理喜剧大逃杀</b>。你的招式极其有限：<b>跑、跳、扑（潜水扑倒）、抓（拽住对手或物体）</b>。地图机关才是真正的杀手——<b>旋转锤把你抡进黏液池、风扇墙把你刮下平台、尖刺门夹断队伍、滚动巨球把整排豆子撞飞</b>。<b>那次你最后一秒被一颗陌生豆子从背后抱住、两个人一起滚下悬崖的瞬间</b>就是糖豆人的派对哲学——<b>「摔得越惨笑得越响」</b>。胜负只是借口，60 颗豆豆同时上演的物理喜剧才是真正的节目。",
            "keywords": ["扑倒拉扯", "旋转锤", "黏液池", "果冻豆物理喜剧"]
        },
        "coreLoop": {
            "title": "排队 60 人 → 多轮淘汰赛 → 最终王冠争夺 → 用王冠/Kudos 换 cosplay 皮肤 → 再排队",
            "value": "你玩到的是<b>「派对节目大逃杀 + cosplay 皮肤秀」</b>——结构是<b>排队 60 人房 → 4-5 轮淘汰 → 王冠争夺 → 装扮房间</b>四层循环。日常活动包括<b>狂奔赛跑、团队抢尾巴/守门/堆球、Boss 关躲机关、最终王冠决赛、连麦组队、用 Kudos 换 cosplay 皮肤</b>。养成线是<b>赛季手册+联动皮肤库（恐龙/海绵宝宝/索尼克）+ Crown Rank + Show Bucks</b>。<b>2020 年 8 月发售即爆款 → 2022 年免费化 + Epic 收购</b>。",
            "keywords": ["4-5 轮淘汰", "cosplay 皮肤", "免费转型", "疫情爆款"]
        }
    },
    "story_overview": {
        "tagline": "<b>60 颗果冻豆挤在起跑线上</b>——这一轮你能不能活到最后？",
        "paragraphs": [
            "想象一档<b>永远不会停播的超现实电视综艺</b>——整个游戏世界是一片漂浮在粉紫色云海中的<b>巨型障碍赛道</b>。糖果色平台、黏液池、旋转锤、巨型滚球、跷跷板、风扇墙、蜂巢门组成的几十张赛道地图，全部漂在没有地平线的天空里。Mediatonic 把<b>儿童电视综艺布景 + 拉斯维加斯霓虹灯</b>缝合成一台永远循环的电视秀。你和 59 颗豆子永远在排队等下一回合，这里没有日夜，只有<b>下一档节目</b>。",
            "你扮演一颗<b>圆鼓鼓的果冻豆 Fall Guy</b>——形似一根会蹦跳的彩色软糖，戴着千奇百怪的 cosplay 皮肤。每场比赛分 4-5 轮淘汰：第一轮通常是 60 人狂奔赛跑赛，每轮按门槛淘汰一批，最终轮 1-6 颗豆子角逐黄金王冠。<b>2020 年 8 月发售时正赶上全球疫情封锁</b>——大家在家宅着没事干，糖豆人因此成为<b>那个夏天的社交媒体奇迹</b>，YouTube/Twitch/微博朋友圈被果冻豆截图刷屏，PSN 当月免费下载创历史纪录。",
            "<b>那次你最后一秒被一颗陌生豆子从背后抱住、两个人一起滚下悬崖的瞬间</b>，Mediatonic 把派对游戏拽回主流——你打的不是怪，是<b>「摔得越惨笑得越响」这道果冻豆物理喜剧哲学</b>；<b>那场你和朋友连麦在最终决赛跷跷板上死命挣扎的桥段</b>——cosplay 皮肤让你明白<b>「重要的不是你赢了，而是你戴着皮卡丘皮肤被旋转锤打飞那一刻有人录下来发了 TikTok」</b>；<b>那次免费化转型后糖豆人重回热门榜的对话节点</b>，疫情时代社交媒体爆款不是偶然。这不是关于打败对手的故事，是<b>「你下一次摔下平台时，是更想笑出来，还是想再来一局</b>？"
        ]
    },
    "aesthetic_summary": {
        "label": "综艺节目布景 × 果冻豆大逃杀",
        "definition": "<b>综艺节目布景 × 果冻豆大逃杀</b>，是 Mediatonic 把<b>儿童电视综艺障碍赛布景</b>（致敬 Wipeout 旋转锤、Takeshi's Castle 黏液池、巨型滚球关）和<b>糖果色霓虹派对视觉</b>（粉紫云海、马卡龙糖色、霓虹荧光招牌）以及<b>果冻豆 cosplay 时尚</b>（圆鼓软糖身材、皮卡丘/恐龙/索尼克联动皮肤）三层缝合在<b>60 人大逃杀</b>外壳里的混血美学。底色是<b>Wipeout 综艺 × 任天堂派对游戏</b>双重血统；变异在于<b>把果冻豆做成联动 IP 载体</b>——皮肤即社交货币。",
        "evolution": "「综艺障碍赛 + 派对大逃杀」视觉线跨越六十年。<b>1965 年</b>《It's a Knockout》欧洲电视综艺把儿童化巨型障碍赛带入欧洲电视——综艺布景视觉源头。<b>1989 年</b>日本<b>《Takeshi's Castle 风云！武铁城》</b>定义巨型机关闯关综艺范式——糖豆人精神祖父。<b>2008 年</b>ABC<b>《Wipeout 终极挑战》</b>把超现实障碍赛真人秀做成全球热门——糖豆人最直接电视母版。<b>2009 年</b>BBC<b>《Total Wipeout》</b>把英国版巨型机关秀普及。<b>2014 年</b>Mediatonic 在伦敦成立。<b>2017 年</b>任天堂<b>《超级马里奥派对》</b>定义主机派对游戏底色。<b>2020 年 8 月</b>《Fall Guys》在 Devolver Digital 发行下登场——疫情封锁催化全球爆款，PSN 月度下载王。<b>2022 年</b>转免费 + Epic 收购把糖豆人推到派对大逃杀品类常青树。",
        "references": [
            {"type": "show", "title": "Wipeout 终极挑战（ABC 综艺）", "year": "2008", "note": "<b>超现实障碍赛真人秀</b>电视母版；糖豆人最直接美术血统来源"},
            {"type": "show", "title": "Takeshi's Castle 风云！武铁城（日本综艺）", "year": "1989", "note": "<b>巨型机关闯关综艺</b>电视祖父；黏液池+巨球关精神血统"},
            {"type": "show", "title": "Total Wipeout（BBC 综艺）", "year": "2009", "note": "<b>英国版超现实障碍赛</b>电视普及版；糖豆人欧洲调性参照"},
            {"type": "show", "title": "海绵宝宝 SpongeBob SquarePants", "year": "1999", "note": "<b>糖果色卡通水下幽默</b>动画范式；可对照粉紫云海与软糖身材调性"},
            {"type": "art", "title": "果冻软糖广告档案（Haribo/Jell-O 商业海报）", "year": "1980", "note": "<b>果冻软糖 Q 弹视觉</b>商业广告原典；Fall Guy 身材材质考据基底"},
            {"type": "show", "title": "疫情期间社交媒体爆款实录（YouTube/Twitch 2020）", "year": "2020", "note": "<b>糖豆人现象级传播</b>真实档案；本作文化意义直接见证"},
            {"type": "game", "title": "超级马里奥派对 Mario Party", "year": "2003", "note": "<b>主机派对游戏</b>国民玩法母版；糖豆人多人淘汰精神参照"},
            {"type": "show", "title": "It's a Knockout（欧洲电视综艺）", "year": "1965", "note": "<b>儿童化巨型障碍赛</b>电视源头；综艺布景视觉远期祖父"}
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
    "eggy-party": EGGY,
    "fall-guys":  FALL_GUYS,
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
    if "dims" in story:
        new_story["dims"] = story["dims"]
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

    ov = d.get("story", {}).get("overview", {})
    tag = re.sub(r"<[^>]+>", "", ov.get("tagline", ""))
    if not (12 <= len(tag) <= 40):
        issues.append(f"tagline_chars={len(tag)}")
    paras = ov.get("paragraphs", [])
    total = sum(len(re.sub(r"<[^>]+>", "", p)) for p in paras)
    bolds = sum(len(re.findall(r"<b>", p)) for p in paras) + len(re.findall(r"<b>", ov.get("tagline", "")))
    if not (380 <= total <= 700):
        issues.append(f"ov_total={total}")
    if bolds < 6:
        issues.append(f"ov_bolds={bolds}")
    if paras and not paras[-1].rstrip().endswith(("\uff1f", "?", "\u2026", "...")):
        issues.append("p3 no ?")

    su = d.get("aesthetic", {}).get("summary", {})
    if su:
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
        years = [int(y) for y in re.findall(r"(19\d{2}|20\d{2}|18\d{2}|17\d{2}|16\d{2}|15\d{2}|14\d{2})", years_str)]
        if years and max(years) - min(years) < 20:
            issues.append(f"year_span={max(years)-min(years)}")

    return issues


def main():
    print("=" * 70)
    print("v2.5 第十批 2 款 Party 游戏：内容写入 + 自检")
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
