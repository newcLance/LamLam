# -*- coding: utf-8 -*-
"""v2.5 第七批 5 款 Adventure 游戏：
stray / signalis / split-fiction / days-gone / dredge

注意：所有中文文案里如果要嵌入引号，必须用「」或（），严禁英文双引号嵌套。
keywords 数组里可以用英文双引号。
"""
import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "games"

# ============================================================
#  迷失 stray
# ============================================================
STRAY = {
    "worldview": {
        "background": {
            "title": "遥远未来——人类灭绝后只剩机器人居住的地下赛博废墟",
            "value": "故事发生在<b>遥远的未来</b>——人类文明已经彻底消亡，地球表面被某种未明灾难抹去，只剩<b>地下封闭城市</b>里一群<b>仍以人类生活方式活下去的机器人</b>。你穿过<b>贫民窟铁皮棚户、蚁村霓虹中文招牌、中城蒸汽管道走廊、下水道祖玛菌、控制室冰冷服务器</b>。这是一座九龙城寨式的<b>赛博朋克废墟</b>——<b>霓虹灯还亮着，门口机器人猫贩子还在叫卖，但天花板上的雨水还在滴</b>。BlueTwelve 工作室把<b>猫的微观视角 × 后人类城市衰败</b>反差缝合成一种独特的孤独诗意。",
            "keywords": ["后人类未来", "九龙城寨赛博废墟", "机器人社会", "猫视角微观"]
        },
        "mainStory": {
            "title": "你是一只流浪橘猫——与无人机 B-12 搭档寻找回到地面的路",
            "value": "你扮演一只<b>普通的流浪橘猫</b>——开场你和三只伙伴在地表废墟玩耍，一脚踩空跌入地下封闭城市，与同伴失散。你独自醒来，遇到一只随身漂浮的小型无人机<b>B-12</b>——它有人类记忆碎片、能翻译机器人语言、能黑入终端。你们组队穿越机器人贫民窟、蚁村、中城、下水道，去寻找传说中<b>能回到地面的出口</b>。剧情核心是<b>「猫与机器人的双向救赎」</b>——B-12 慢慢拼回自己是谁，而你只是想回家、回到阳光下、回到伙伴身边。<b>那一段你在蚁村屋顶看着两只机器人下围棋的瞬间</b>，孤独被一只猫的好奇心治愈。",
            "keywords": ["流浪橘猫", "B-12 无人机", "机器人社会", "回到地面"]
        },
        "combat": {
            "title": "祖玛菌追逐 + 防御机器人潜行 + UV 灯光武器——以「不擅长战斗」为核心的猫式应对",
            "value": "战斗几乎不存在——<b>你是一只猫，不是战士</b>。主要威胁是<b>祖玛菌（Zurks）</b>——一种从下水道蔓延出来的<b>变异活体细菌生物</b>，会成群扑咬。面对祖玛菌你只能<b>狂奔、跳上高处、按节奏甩掉身上的菌团</b>。后期解锁<b>UV 紫外线灯</b>——你帮 B-12 照射菌群让它们瞬间汽化，节奏类似<b>猫式音乐节拍游戏</b>。还有<b>哨兵防御机器人</b>——它们会用激光锁定你，必须利用箱子掩体潜行。整套战斗哲学是<b>「猫不打架，猫躲、猫跳、猫绕」</b>。",
            "keywords": ["祖玛菌追逐", "UV 灯节拍", "哨兵潜行", "猫式逃跑"]
        },
        "coreLoop": {
            "title": "城区探索 → 跳跃攀爬 → 与机器人 NPC 互动 → 收集回忆 → 推进章节",
            "value": "你玩到的是<b>「线性章节式 3D 平台跳跃 + 微型解谜」</b>——结构是<b>贫民窟 → 死城 → 蚁村 → 下水道 → 中城 → 控制室</b>线性推进，每章一个微型城市切片。日常活动包括<b>沿着空调管道与霓虹招牌跳跃攀爬、用 B-12 翻译机器人对话、给居民送信送货、收集 Memory 回忆碎片</b>。你还可以<b>蹭机器人腿脚、把桌上东西扒到地上、在沙发上睡觉、对着乐谱按琴键</b>——<b>所有「猫做的蠢事」都被设计成专门按键</b>。养成线几乎不存在，<b>这只猫始终是这只猫</b>，但 B-12 的人类记忆一点点拼回完整。",
            "keywords": ["3D 平台跳跃", "猫式互动", "Memory 收集", "线性章节"]
        }
    },
    "story_overview": {
        "tagline": "<b>地下九龙城寨里走丢的橘猫</b>——你还想回到阳光下吗？",
        "paragraphs": [
            "想象一片<b>遥远未来人类彻底消亡后的地球</b>——表面被某种未明灾难抹去，只剩地下封闭城市里一群仍以人类生活方式活下去的机器人。你穿过<b>贫民窟铁皮棚户、蚁村霓虹中文招牌、中城蒸汽管道走廊、下水道祖玛菌、控制室冰冷服务器</b>。这是一座九龙城寨式的赛博朋克废墟——<b>霓虹灯还亮着、门口机器人猫贩子还在叫卖、晾在外的电缆像植物一样蔓延、天花板的雨水滴在生锈空调外机上</b>。法国 BlueTwelve 工作室把猫的微观视角和后人类城市衰败反差缝合成一种独特的孤独诗意，由 Annapurna Interactive 发行。",
            "你是一只<b>普通的流浪橘猫</b>——开场你和三只伙伴在地表废墟玩耍，一脚踩空跌入地下封闭城市，与同伴失散。你独自醒来，遇到一只随身漂浮的小型无人机<b>B-12</b>——它有人类记忆碎片、能翻译机器人语言、能黑入终端。你们组队穿越机器人贫民窟、蚁村、中城、下水道，去寻找传说中<b>能回到地面的出口</b>。一路上你蹭机器人居民的腿脚、把桌上的瓶子扒到地上、跳上沙发睡觉、对着乐谱按琴键——<b>每一件猫做的蠢事都成了治愈机器人的善意</b>。",
            "<b>那次你第一次在蚁村屋顶看到两只机器人坐在霓虹下围棋的瞬间</b>，BlueTwelve 把九龙城寨赛博废墟做到了猫眼能看到的最温柔高度——你打的不是怪，是<b>整代赛博朋克审美的尺度反转</b>；<b>那场你被祖玛菌追到下水道死路、B-12 第一次为你照亮 UV 灯的桥段</b>——猫式逃跑让你明白<b>「这世界没有人类，但温度还在」</b>；<b>那次你在控制室看 B-12 拼回自己是谁的对话节点</b>，孤独被一只猫的好奇心彻底治愈。这不是关于打败反派的故事，是<b>「橘猫还想不想回到阳光下」</b>的故事——蚁村霓虹还在闪，下一段管道往哪里跳？"
        ]
    },
    "aesthetic_summary": {
        "label": "九龙城寨赛博废墟 × 猫视角微观",
        "definition": "<b>九龙城寨赛博废墟 × 猫视角微观</b>，是 BlueTwelve 把<b>香港九龙城寨真实老龄化都市质感</b>（铁皮棚户、晾衣绳、霓虹中文招牌、蒸汽管道、生锈空调外机）和<b>赛博朋克 × 后人类机器人社会</b>（机器人居民、全息广告、老化电路、灯泡式眼睛）反差缝合在<b>一只猫的微观视角</b>外壳里的混血美学。底色是<b>银翼杀手 × 九龙城寨</b>双重视觉血统；变异在于<b>把镜头压低到地面 30 厘米</b>——所有空间被猫的尺度重新丈量。色彩锁定<b>霓虹粉紫蓝 + 生锈棕 + 暖黄电灯</b>三色组合。",
        "evolution": "猫视角赛博废墟视觉线跨越半世纪。<b>1982 年</b>雷德利·斯科特<b>《银翼杀手》</b>定义赛博朋克都市基础视觉——本作精神祖父之一。<b>1993 年</b>九龙城寨被拆迁前的纪实摄影集<b>《City of Darkness》</b>定义高密度老龄化都市档案——美术参考核心。<b>1988 年</b>大友克洋<b>《阿基拉》</b>定义霓虹+管道+反乌托邦动画范式。<b>1995 年</b>押井守<b>《攻壳机动队》</b>把香港式赛博废墟做成动画工业级。<b>2008 年</b>皮克斯<b>《机器人总动员 WALL·E》</b>定义后人类小机器人孤独诗意。<b>2001 年</b><b>《猫狗大战》系列</b>开启猫视角动物电影范式。<b>2017 年</b>《<b>银翼杀手 2049</b>》刷新赛博废墟工业级视觉。<b>2022 年</b>《迷失 Stray》在 Unreal 引擎下登场——猫视角 + 九龙城寨美术 + 机器人社会孤独诗意把赛博朋克推到「微观尺度」的全新工业级高度。",
        "references": [
            {"type": "film", "title": "银翼杀手 2049", "year": "2017", "note": "<b>赛博废墟工业级视觉</b>电影标杆；本作霓虹色温与雨夜蒸汽的最深底色"},
            {"type": "film", "title": "银翼杀手 Blade Runner", "year": "1982", "note": "<b>赛博朋克都市</b>视觉源头；本作精神祖父之一"},
            {"type": "art", "title": "九龙城寨纪实摄影集 City of Darkness", "year": "1993", "note": "<b>高密度老龄化都市</b>真实档案；本作美术考据核心来源"},
            {"type": "anime", "title": "攻壳机动队（押井守）", "year": "1995", "note": "<b>香港式赛博废墟</b>动画工业级范式；可对照中城走廊调性"},
            {"type": "anime", "title": "阿基拉 AKIRA（大友克洋）", "year": "1988", "note": "<b>霓虹+管道+反乌托邦</b>动画范式；本作色彩血统精神养分"},
            {"type": "film", "title": "机器人总动员 WALL·E", "year": "2008", "note": "<b>后人类小机器人孤独诗意</b>电影母版；可对照 B-12 与橘猫双向救赎调性"},
            {"type": "film", "title": "猫狗大战 Cats & Dogs", "year": "2001", "note": "<b>猫视角动物电影</b>范式；猫尺度世界观的远期参照"},
            {"type": "game", "title": "Tokyo Jungle", "year": "2012", "note": "<b>后人类动物视角</b>独立游戏先驱；可对照本作猫式微观叙事"}
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
#  信号 signalis
# ============================================================
SIGNALIS = {
    "worldview": {
        "background": {
            "title": "遥远未来——人类殖民外星但仍困在冷战式极权下的太空采矿殖民地",
            "value": "故事发生在<b>遥远未来人类已殖民外星的时代</b>——但社会形态没有进步，仍是<b>冷战式东欧极权国家「Eusan Nation」</b>，监视、配给、政治审查、磁带档案、CRT 屏幕统治日常。你穿过<b>失事飞船 Penrose 残骸、雪原下方深处的 Sierpinski-23 采矿设施、教育中心走廊、红色异空间走廊、神秘高塔</b>。科技刻意低保真——<b>磁带、CRT 显像管、笨重金属操作台、纸质打孔卡、模拟仪表盘</b>。这不是常规未来，这是<b>太空时代的东德 × PS1 时代的恐怖</b>——一座用工业蓝灰构筑的极权幽灵船。",
            "keywords": ["Eusan Nation", "冷战太空殖民", "PS1 低保真恐怖", "Sierpinski-23"]
        },
        "mainStory": {
            "title": "你是 Elster——LSTR 型 Replika 机器人，在外星雪原寻找丢失的同伴",
            "value": "你扮演<b>Elster</b>——一台<b>LSTR 型 Replika 仿生人形机器人</b>，与人类技术员 Ariane 搭档深空勘探。开场飞船 Penrose 在冰雪行星坠毁，Ariane 失踪，你独自醒来沿雪原走向地下采矿设施 Sierpinski-23 寻找她。剧情核心是<b>「机器人对人类的执着算不算爱情」</b>——你与 Ariane 之间暧昧、隐忍、超越制造目的。一路 Replika 同型号发狂袭来，红色异空间渗入现实，<b>Eusan 极权真相浮现</b>。这是关于记忆、身份、性别与执念的<b>德式硬核诡异叙事</b>。",
            "keywords": ["Elster LSTR", "Ariane 失踪", "Replika 同型异化", "执念叙事"]
        },
        "combat": {
            "title": "受限弹药 + 多种 Replika 怪物 + 笔记解谜——以「资源稀缺」为核心的生存恐怖",
            "value": "战斗是经典<b>固定视角生存恐怖</b>——<b>子弹永远不够、血包永远不够、库存永远不够</b>。武器包括<b>左轮、木柄手雷、突击步枪、霰弹枪、火焰喷射器</b>。敌人是<b>各种异化 Replika 型号</b>——LSTR/STAR/MNHR/EULR 行为模式不同。Replika 倒下后会<b>缓慢复活</b>，你必须用火焰彻底烧掉或绕开。库存只有 6 格，逼你每秒在权衡舍弃。<b>红色异空间</b>会突然渗入——走廊变形、墙面流血、敌人增殖。整套战斗哲学是<b>「能跑就跑、能不开枪就别开枪」</b>。",
            "keywords": ["6 格库存", "Replika 复活", "红色异空间", "固定视角恐怖"]
        },
        "coreLoop": {
            "title": "采矿设施探索 → 笔记线索 → 解谜（密码/星象/磁带）→ Replika 战斗 → 多结局",
            "value": "你玩到的是<b>「PS1 复古固定视角生存恐怖 + 文学解谜」</b>——结构沿用<b>初代寂静岭 + Resident Evil</b>骨架，但叙事密度像一本德式现代小说。日常活动包括<b>探索采矿设施、用门禁卡推进、解 6 位密码、对照笔记本破解钢琴乐谱、读 Eusan 政府公文与私人日记拼真相</b>。你会反复在<b>现实/红色异空间/记忆闪回</b>之间切换。Elster 不会变强，但你对真相的认知一点点崩溃。结局多达 4 种以上，取决你<b>怎么对待 Ariane 的记忆</b>。",
            "keywords": ["固定视角探索", "笔记解谜", "红色异空间切换", "多结局"]
        }
    },
    "story_overview": {
        "tagline": "<b>Elster 在雪原醒来</b>——你还记得自己答应过 Ariane 什么吗？",
        "paragraphs": [
            "想象一片<b>遥远未来人类已殖民外星的时代</b>——但社会形态没有进步，仍是冷战式东欧极权 Eusan Nation，监视、配给、政治审查、磁带档案统治日常。你穿过<b>失事飞船 Penrose 残骸、Sierpinski-23 采矿设施、教育中心走廊、红色异空间、神秘高塔</b>。科技刻意低保真——磁带、CRT、笨重金属操作台、纸质打孔卡、模拟仪表盘。这是<b>太空时代的东德 × PS1 时代的恐怖</b>。德国 rose-engine 双人独立六年磨一剑。",
            "你是<b>Elster</b>——LSTR 型号 Replika 仿生人形机器人，与人类技术员 Ariane 搭档深空勘探。开场飞船 Penrose 在冰雪行星坠毁，Ariane 失踪，你沿雪原走向地下采矿设施 Sierpinski-23 寻找她。一路上你遇到<b>大量发狂的 Replika 同型号</b>——LSTR/STAR/MNHR/EULR 行为模式不同，倒下还会复活，必须火焰烧掉或绕开。<b>红色异空间频繁渗入，Eusan 极权真相浮现</b>。",
            "<b>那次你第一次走进红色异空间对称走廊、磁带杂音里听见自己名字的瞬间</b>，rose-engine 把 PS1 复古恐怖做到 indie 工业新巅峰——你打的不是怪，是<b>「机器人执着算不算爱情」</b>这道题；<b>那场你在档案室翻到 Ariane 病历、第一次意识到自己执念的桥段</b>——红色异空间让你明白<b>「这条信号已响了多少次」</b>；<b>那次你在塔顶面对 Replika 同型自己复活体的对话节点</b>，性别、身份、记忆、爱情、政治极权五条线被一刀切开。这不是关于打败怪物的故事，是<b>「Elster 还记得答应过 Ariane 什么吗」</b>的故事——下一台 Replika 你烧还是不烧？"
        ]
    },
    "aesthetic_summary": {
        "label": "冷战太空 × PS1 恐怖红色",
        "definition": "<b>冷战太空 × PS1 恐怖红色</b>，是 rose-engine 把<b>东德苏联冷战极权工业美学</b>（CRT 显像管、磁带、笨重金属操作台、Replika 制服与东德军装）和<b>PS1 低多边形恐怖</b>（粗糙模型、固定视角、像素化贴图、噪点滤镜）反差融合在<b>太空殖民幽灵船叙事</b>外壳里的混血美学。底色是<b>1995 年代 PS1 寂静岭+生化危机</b>视觉血统；变异在于<b>红色异空间</b>——超现实正红走廊+对称构图把恐怖推到大都会几何高度。色彩锁定<b>工业蓝灰 + 极权红 + CRT 黄绿</b>三色。",
        "evolution": "「冷战太空 + 低保真恐怖」视觉线跨越百年。<b>1927 年</b>弗里茨·朗<b>《大都会》</b>定义工业极权未来都市视觉源头——本作精神祖父。<b>1979 年</b><b>《异形》</b>定义太空蓝领工业恐怖电影。<b>1982 年</b>约翰·卡朋特<b>《怪形》</b>定义雪原幽闭+身份替换恐怖电影母版。<b>1989 年</b>东德人民军日常生活纪录片为 Eusan 制服符号提供视觉档案。<b>1996 年</b><b>《生化危机》</b>定义固定视角生存恐怖游戏品类。<b>1999 年</b><b>《寂静岭》</b>定义心理投射 PS1 恐怖游戏品类——本作直接精神前作。<b>2002 年</b>新海诚<b>《星之声》</b>定义太空+失联+执念叙事范式。<b>2022 年</b>《SIGNALIS》在 rose-engine 双人独立打磨下登场——固定视角 PS1 像素+Replika 执念把冷战太空恐怖推到 indie 神作高度。",
        "references": [
            {"type": "film", "title": "大都会 Metropolis（弗里茨·朗）", "year": "1927", "note": "<b>工业极权未来都市</b>视觉源头；本作 Eusan 极权美学最深底色"},
            {"type": "film", "title": "异形 Alien", "year": "1979", "note": "<b>太空蓝领工业恐怖</b>电影母版；可对照 Penrose 飞船与采矿设施调性"},
            {"type": "film", "title": "怪形 The Thing（约翰·卡朋特）", "year": "1982", "note": "<b>雪原幽闭+身份替换</b>恐怖电影母版；可对照 Replika 同型异化"},
            {"type": "game", "title": "寂静岭 Silent Hill（PS1 原版）", "year": "1999", "note": "<b>心理投射 PS1 恐怖</b>游戏品类母版；本作精神前作"},
            {"type": "game", "title": "生化危机 Resident Evil（PS1 原版）", "year": "1996", "note": "<b>固定视角生存恐怖</b>游戏品类母版；本作系统骨架直接来源"},
            {"type": "anime", "title": "新海诚《星之声》", "year": "2002", "note": "<b>太空+失联+执念</b>叙事范式；可对照 Elster 与 Ariane 关系调性"},
            {"type": "art", "title": "东德人民军日常生活纪实摄影", "year": "1989", "note": "<b>冷战极权制服与符号</b>视觉档案；Replika 制服考据来源"},
            {"type": "art", "title": "苏联未来主义海报与字体设计", "year": "1960", "note": "<b>极权未来主义</b>平面设计档案；本作 UI 与档案文件视觉养分"}
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
#  分裂虚构 split-fiction
# ============================================================
SPLIT = {
    "worldview": {
        "background": {
            "title": "当代框架 + 虚构小说世界——科幻与奇幻双轨无限时空",
            "value": "故事发生在<b>当代地球一家叫 Rader Publishing 的出版科技公司</b>——CEO J.D. Rader 发明了一台叫<b>Mind's Eye</b>的机器，能把作家未发表的小说世界<b>实体化</b>。两位作家在试机过程中<b>意外被困在彼此的小说世界里</b>。你穿越的世界包括<b>赛博朋克都市霓虹街、太空站零重力、机械义肢黑帮巢穴</b>（科幻轨）和<b>魔法森林、中世纪城堡、巨龙巢穴、童话糖果国</b>（奇幻轨）——<b>每一章一个完全不同的美术世界</b>。Hazelight 把双轨万花筒做到游戏史最奢侈关卡密度。",
            "keywords": ["Rader Publishing", "Mind's Eye 机器", "科幻 × 奇幻双轨", "万花筒关卡"]
        },
        "mainStory": {
            "title": "你是 Mio 与 Zoe——科幻作家与奇幻作家被困在自己创作的小说里",
            "value": "你扮演<b>Mio Hudson（科幻作家）</b>与<b>Zoe Foster（奇幻作家）</b>——两位风格完全相反、互看不顺眼的作家。开场你们都签了 Rader 合同准备试 Mind's Eye，意外被困进机器内部，<b>科幻作家被丢进奇幻世界、奇幻作家被丢进科幻世界</b>，必须互相扶持才能逃出。剧情核心是<b>「两个互不喜欢的女人在彼此创作里学会理解对方」</b>——最终发现各自都在用作品逃避童年伤痛。Hazelight 招牌<b>双人合作必玩</b>设计让没有第二位玩家就不能推进任何关卡。",
            "keywords": ["Mio 科幻", "Zoe 奇幻", "强制双人合作", "互救成长"]
        },
        "combat": {
            "title": "双人协同 + 章节限定能力 + Boss 战 + 即兴小游戏——Hazelight 招牌玩法万花筒",
            "value": "战斗是<b>每章一套全新机制</b>——Hazelight 把<b>《双人成行》</b>的设计哲学推到极致。一章你是赛博朋克黑客<b>用未来武器射穿义肢黑帮</b>，下一章你变成<b>骑龙的魔法师 + 持剑的女骑士</b>，再下一章你变成<b>太空站零重力机甲与会喷火的小猪</b>。每章 30-40 分钟一套机制，<b>从不复用</b>。Boss 战包含<b>巨型机甲、暴风雪巨龙、变形糖果怪、AI 反派 Rader 化身</b>。玩法穿插<b>即兴双人小游戏</b>——节奏对决、跳台竞速、推箱解谜、QTE 配合。整套战斗哲学是<b>「玩你从没想过会出现在同一个游戏里的 50 种玩法」</b>。",
            "keywords": ["每章新机制", "强制配合", "30+ 章节玩法", "即兴小游戏"]
        },
        "coreLoop": {
            "title": "进入小说章节 → 双人解谜 → Boss 战 → 切换到对方小说 → 元叙事互动",
            "value": "你玩到的是<b>「电影章节式双人合作」</b>——结构是<b>科幻关卡 ⇄ 奇幻关卡</b>交替，全程<b>分屏</b>显示两位玩家视角。日常活动包括<b>双人协同推进解谜（按钮同步、绳索拉扯、镜像对称解锁）、即兴小游戏（节奏跳跃、跑酷竞速、对战球类）、Boss 战分工配合、跨小说章节互相吐槽彼此创作的烂梗</b>。养成线几乎不存在——<b>能力随章节切换、不带回前章</b>。<b>那一段 Mio 用科幻黑客技能侵入 Zoe 奇幻王国数据塔</b>是 Hazelight 元叙事的最高峰。<b>这是 2025 年最不孤独的游戏</b>——没有第二个人，你连开始都开始不了。",
            "keywords": ["分屏双人", "章节切换", "元叙事互动", "强制合作"]
        }
    },
    "story_overview": {
        "tagline": "<b>Mio 与 Zoe 被困在彼此小说里</b>——你愿意陪一个完全相反的人冒险吗？",
        "paragraphs": [
            "想象一家叫 Rader Publishing 的当代出版科技公司——CEO J.D. Rader 发明了一台叫 Mind's Eye 的机器，能把作家未发表的小说世界<b>实体化</b>，但他的真实目的是窃取作家创意。你穿越的世界包括<b>赛博朋克都市霓虹街、太空站零重力、机械义肢黑帮巢穴</b>（科幻轨）和<b>魔法森林、中世纪城堡、巨龙巢穴、童话糖果国</b>（奇幻轨）——每章一个完全不同的美术世界，<b>分屏左右像两本完全不同画册同时翻开</b>。Hazelight 把双轨万花筒做到游戏史最奢侈关卡密度。",
            "你扮演<b>Mio Hudson（科幻作家）</b>与<b>Zoe Foster（奇幻作家）</b>——风格相反、互看不顺眼的两位作家。开场你们都签了 Rader 合同试 Mind's Eye，意外被困——科幻作家被丢进奇幻世界、奇幻作家被丢进科幻世界，必须互相扶持才能逃出。<b>最终发现各自都在用作品逃避童年伤痛</b>。Hazelight 强制双人合作让没有第二位玩家就不能推进任何关卡。",
            "<b>那次你和搭档第一次操控龙与机甲在分屏两侧同时起飞、视角合二为一的瞬间</b>，Hazelight 把<b>《双人成行》</b>设计哲学推到游戏史万花筒高度——你打的不是怪，是<b>「合作」在 30+ 完全不同机制里的极限测试</b>；<b>那场 Mio 用科幻黑客侵入 Zoe 魔法王国数据塔、两个世界元素第一次混合的桥段</b>——元叙事让你明白<b>「我笔下英雄和你笔下公主原来可以同框」</b>；<b>那次你在终点看到 Rader 黑幕、Mio 与 Zoe 决定一起把作品要回来的对话节点</b>，互相不喜欢的两个女人成为彼此最重要合著者。这不是关于打败反派的故事，是<b>「你愿意陪一个完全相反的人冒险吗」</b>的故事——下一章去科幻还是奇幻？"
        ]
    },
    "aesthetic_summary": {
        "label": "多风格万花筒 × 双人合作分屏",
        "definition": "<b>多风格万花筒 × 双人合作分屏</b>，是 Hazelight 把<b>科幻视觉传统</b>（赛博朋克霓虹、太空站零重力、机械义肢、AI 反乌托邦）和<b>奇幻视觉传统</b>（中世纪城堡、巨龙、魔法森林、糖果童话国）以章节为单位高频反差切换在<b>双人合作分屏强制叙事</b>外壳里的混血美学。底色是<b>《双人成行》It Takes Two</b>万花筒玩法美学血统；变异在于<b>每章一套世界观</b>，整作 30+ 美术风格无缝缝合。色彩锁定<b>科幻冷蓝紫 + 奇幻暖金红 + 分屏白线</b>三色组合。",
        "evolution": "「双人合作 + 风格万花筒」视觉线跨越四十年。<b>1979 年</b>《<b>无尽的故事</b>》小说定义书中世界实体化叙事母版——本作精神祖父。<b>1984 年</b><b>《无尽的故事》电影版</b>把书中世界电影化。<b>2009 年</b><b>《阿凡达》</b>定义当代科幻奇幻视觉巅峰。<b>2018 年</b>斯皮尔伯格<b>《头号玩家》</b>定义虚构世界混搭流行 IP 范式——本作元叙事调性精神参照。<b>2013 年</b>Hazelight 创始人<b>《Brothers》</b>开辟双角色操控范式。<b>2018 年</b>Hazelight<b>《A Way Out》</b>开辟分屏强制双人合作品类。<b>2021 年</b>Hazelight<b>《双人成行》</b>把万花筒玩法做到 TGA 年度。<b>2025 年</b>《分裂虚构》在虚幻 5 引擎下登场——双轨科幻奇幻+30+ 章节玩法把双人合作万花筒推到工业级新巅峰。",
        "references": [
            {"type": "film", "title": "头号玩家 Ready Player One", "year": "2018", "note": "<b>虚构世界混搭流行 IP</b>电影范式；本作元叙事调性精神参照"},
            {"type": "novel", "title": "无尽的故事 The NeverEnding Story", "year": "1979", "note": "<b>书中世界实体化</b>叙事母版；本作 Mind's Eye 机器精神祖父"},
            {"type": "game", "title": "双人成行 It Takes Two", "year": "2021", "note": "<b>双人合作万花筒玩法</b>TGA 年度母版；本作直接前作与系统骨架"},
            {"type": "game", "title": "A Way Out", "year": "2018", "note": "<b>分屏强制双人合作</b>品类母版；Hazelight 设计哲学起点"},
            {"type": "game", "title": "Brothers: A Tale of Two Sons", "year": "2013", "note": "<b>双角色操控</b>范式起点；Josef Fares 个人创作精神前史"},
            {"type": "film", "title": "无尽的故事电影版", "year": "1984", "note": "<b>书中世界电影化</b>视觉范式；可对照本作小说世界跳转调性"},
            {"type": "film", "title": "阿凡达 Avatar", "year": "2009", "note": "<b>当代科幻奇幻视觉</b>巅峰；本作奇幻轨色彩养分"},
            {"type": "film", "title": "捉鬼敢死队 Ghostbusters", "year": "1984", "note": "<b>反差风格混搭</b>美式冒险电影范式；可对照分屏吐槽喜剧调性"}
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
#  往日不再 days-gone
# ============================================================
DAYSGONE = {
    "worldview": {
        "background": {
            "title": "病毒爆发后约 2 年——俄勒冈州末日松林与高速公路废墟",
            "value": "故事发生在<b>近未来美国西北俄勒冈州——一种神秘病毒爆发约 2 年后的末日</b>。感染者被称为<b>Freakers</b>（变异人/狂尸），<b>夜行/怕水/数百只组成「尸潮 Horde」</b>是它们的招牌。你穿过<b>太平洋西北温带雨林、火山湖国家公园 Crater Lake、被遗弃的小镇 Farewell、山间高速公路</b>——苔藓爬上加油站招牌、苔原覆盖锈蚀皮卡、松林里偶尔传来摩托车引擎声。这是<b>太平洋西北自然纪录片 × 飞车党公路片</b>反差缝合。SIE Bend Studio 把俄勒冈做成北美最美的末日。",
            "keywords": ["Freakers 尸潮", "俄勒冈末日", "Crater Lake", "飞车党摩托"]
        },
        "mainStory": {
            "title": "你是 Deacon St. John——前飞车党成员骑摩托寻找失散的妻子 Sarah",
            "value": "你扮演<b>Deacon St. John（迪肯·圣约翰）</b>——病毒爆发前是<b>「Mongrels MC」飞车党</b>成员，疫情爆发当夜他和兄弟 Boozer 把妻子 Sarah 送上撤离直升机，自己留下处理事务——<b>那架直升机消失在末日浓烟里再没回来</b>。两年后他靠摩托车在俄勒冈替营地接赏金、清剿尸潮维生。剧情核心是<b>「我妻子真的死了吗」</b>这道执念——Deacon 拒绝承认 Sarah 已死，每条线索都让他骑得更远。<b>Deacon 粗鲁、自私、不讨喜，但 Sarah 那份执念让他像个真实的人</b>。",
            "keywords": ["Deacon 飞车党", "Sarah 失踪", "Boozer 兄弟", "公路赏金"]
        },
        "combat": {
            "title": "尸潮防御 + 摩托追逐 + 拼凑武器 + 营地阵营——以「移动据点」为核心的开放世界生存",
            "value": "战斗核心是<b>尸潮 Horde 防御战</b>——<b>200-500 只 Freakers 同时奔袭你</b>，必须靠<b>地形+陷阱+诱饵+燃烧瓶+土制炸药+自动武器</b>组合作战，是当代游戏少见的<b>真群体 AI 高峰体验</b>。其他威胁包括 Rippers 邪教徒、Marauders 流寇、Newts 变异儿童。武器都是<b>末日拼凑感</b>——绑铁钉的棒球棍、改装猎枪、自制燃烧瓶。你的<b>摩托车是核心据点</b>——没油就走不动、没零件得推、撞坏要去最近营地修。",
            "keywords": ["Horde 尸潮防御", "摩托车据点", "营地阵营", "拼凑武器"]
        },
        "coreLoop": {
            "title": "营地接任务 → 加油修摩托 → 奔袭目标点 → 清尸潮 → 卖人头换信用",
            "value": "你玩到的是<b>「公路片开放世界 × 末日生存 RPG」</b>——俄勒冈是无缝大世界，你的所有移动都靠摩托。日常活动包括<b>营地领赏金任务（清尸潮/解救人质/猎杀 Marauders）、加油站补汽油、修车铺换零件、剥 Freaker 耳朵换信用、清剿野外营地为营地解锁装备</b>。声望分别在三大营地累积，决定能买到的武器、配件、摩托升级。养成线是<b>近战/枪法/生存三大技能树 + 摩托燃料/血量/储物</b>。<b>那次你第一次清掉一支 300 头规模尸潮的瞬间</b>是 PS4 末期开放世界设计教科书。",
            "keywords": ["公路开放世界", "三营地声望", "摩托修养", "尸潮清剿"]
        }
    },
    "story_overview": {
        "tagline": "<b>Deacon 没承认 Sarah 死了</b>——两年了，你还在等谁回信吗？",
        "paragraphs": [
            "想象一片<b>近未来美国西北俄勒冈州——病毒爆发约 2 年后的末日</b>。感染者被称为 Freakers，<b>夜行、怕水、数百只组成尸潮 Horde 一起奔袭活人</b>。你穿过<b>太平洋西北温带雨林、火山湖国家公园 Crater Lake、被遗弃的小镇 Farewell、山间高速公路</b>——苔藓爬上加油站招牌、苔原覆盖锈蚀皮卡、松林里偶尔传来摩托引擎。这是太平洋西北自然纪录片 × 飞车党公路片反差缝合。SIE Bend Studio 把俄勒冈做成北美最美的末日。",
            "你扮演<b>Deacon St. John</b>——病毒爆发前是 Mongrels MC 飞车党。爆发当夜他和兄弟 Boozer 把妻子 Sarah 送上撤离直升机，自己留下处理事务——<b>那架直升机消失在末日浓烟里再没回来</b>。两年后他靠摩托车在俄勒冈替营地接赏金、清剿尸潮维生。Deacon 粗鲁、自私、不讨喜，但他对 Sarah 那份执念让他像个真实的人——<b>每条线索都让他骑得更远</b>。",
            "<b>那次你第一次在加油站院子被 300 头规模尸潮围住、土制炸药+自动步枪+最后一滴汽油同时燃尽的瞬间</b>，SIE Bend Studio 把开放世界尸潮 AI 做到 PS4 末期工业级——你打的不是怪，是<b>整代飞车党公路片末日精神状态的具象化</b>；<b>那场你跟旧无线电信号穿越 Crater Lake 找到 Sarah 名字的桥段</b>——执念让你明白<b>「我妻子真的死了吗」这道题，Deacon 自己都不敢回答</b>；<b>那次你在 Lost Lake 营地夜里和 Boozer 喝完最后一罐啤酒的对话节点</b>，太平洋西北末日终于露出温柔。这不是关于打败尸潮的故事，是<b>「Deacon 还在等谁回信吗」</b>的故事——下一段山路去哪个营地？"
        ]
    },
    "aesthetic_summary": {
        "label": "太平洋西北末世 × 飞车党公路美学",
        "definition": "<b>太平洋西北末世 × 飞车党公路美学</b>，是 SIE Bend Studio 把<b>美国西北温带雨林真实地貌</b>（道格拉斯冷杉松林、火山湖、苔藓岩壁、山间高速、加油站小镇）和<b>飞车党亚文化视觉传统</b>（皮夹克 + 络腮胡 + 摩托引擎 + Mongrels MC 队徽）反差融合在<b>近未来病毒末日 + 尸潮防御</b>外壳里的混血美学。底色是<b>《最后的我们》× 《疯狂麦克斯》</b>双重血统；变异在于<b>把摩托车做成生存核心</b>——加油修车推车都是叙事。色彩锁定<b>松林墨绿 + 苔藓灰 + 引擎油锈红</b>三色。",
        "evolution": "「飞车党 + 末日公路」视觉线跨越半世纪。<b>1969 年</b><b>《逍遥骑士》</b>定义美国摩托公路片视觉源头——本作精神祖父。<b>1979 年</b>乔治·米勒<b>《疯狂麦克斯》</b>定义末日公路飞车党视觉母版。<b>1981 年</b><b>《疯狂麦克斯 2》</b>把末日公路推到电影巅峰。<b>2010 年</b>剧集<b>《行尸走肉》</b>定义当代尸潮叙事流行化。<b>2008 年</b>剧集<b>《飞车党》</b>把美国摩托俱乐部文化做到剧集工业级——Mongrels MC 直接精神参照。<b>2015 年</b>俄勒冈州 PBS 纪录片让太平洋西北温带雨林+Crater Lake 成为大众视觉档案。<b>2013 年</b><b>《最后的我们》</b>定义当代叙事驱动末日生存品类。<b>2019 年</b>《往日不再》在虚幻 4 引擎下登场——尸潮 AI+摩托车据点把太平洋西北末日工业级化，2025 年凭口碑逆转翻身。",
        "references": [
            {"type": "film", "title": "疯狂麦克斯 2 The Road Warrior", "year": "1981", "note": "<b>末日公路飞车党</b>电影母版；本作飞车党+公路末世视觉最深底色"},
            {"type": "film", "title": "逍遥骑士 Easy Rider", "year": "1969", "note": "<b>美国摩托公路片</b>视觉源头；Deacon 个人公路精神祖父"},
            {"type": "show", "title": "飞车党 Sons of Anarchy", "year": "2008", "note": "<b>美国摩托俱乐部</b>剧集工业级母版；Mongrels MC 直接精神参照"},
            {"type": "show", "title": "行尸走肉 The Walking Dead", "year": "2010", "note": "<b>当代尸潮叙事</b>流行化标杆；可对照本作 Freakers 与营地张力"},
            {"type": "show", "title": "俄勒冈州 PBS 自然纪录片", "year": "2015", "note": "<b>太平洋西北温带雨林+Crater Lake</b>真实地貌档案；本作美术考据来源"},
            {"type": "game", "title": "最后的我们 The Last of Us", "year": "2013", "note": "<b>叙事驱动末日生存</b>品类母版；本作系统设计远期参照"},
            {"type": "film", "title": "末日危途 The Road（科马克·麦卡锡）", "year": "2009", "note": "<b>末日父子公路</b>电影范式；可对照 Deacon 与 Sarah 执念调性"},
            {"type": "art", "title": "Harley-Davidson 飞车党文化档案", "year": "1947", "note": "<b>美式飞车党亚文化</b>视觉档案；皮夹克+队徽考据来源"}
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
#  疏浚 dredge
# ============================================================
DREDGE = {
    "worldview": {
        "background": {
            "title": "模糊当代——被神秘力量笼罩的群岛 The Marrows",
            "value": "故事发生在<b>一片叫 The Marrows 的孤立群岛</b>——时代模糊像 20 世纪某个北方海域。你的地图由五区域组成：<b>Greater Marrow、Gale Cliffs、Stellar Basin、Twisted Strand、Devil's Spine</b>。白天是平凡的低多边形北欧渔村——海鸥、灯塔、木屋、码头。<b>夜晚变质</b>——海雾包船身、深海冒出畸形鱼、远方传来诡异歌声、视野出现不该存在的礁石。Black Salt Games 把<b>萌系渔村 × 克苏鲁深海</b>反差缝合。",
            "keywords": ["The Marrows 群岛", "五大区域", "克苏鲁深海", "低多边形萌系"]
        },
        "mainStory": {
            "title": "你是无名渔夫——被神秘信件引到群岛的新来者",
            "value": "你扮演一位<b>无名渔夫</b>——开场你的小船在风暴中触礁，被 Greater Marrow 镇长救起。镇长说他需要新渔夫接替前任失踪者，你欠他一艘新船的债，于是开始为他打工。剧情核心是<b>「Collector 老收藏家到底想集齐什么」</b>——他陆续要求你前往五大区域<b>取回五件古怪文物</b>，每一件都让海上异象加剧、镇民开始噩梦。你逐步发现<b>群岛每位 NPC 都背负秘密</b>。最终选择是<b>把文物交给 Collector 还是扔回海里</b>——克苏鲁式不可挽回的代价摆在你面前。",
            "keywords": ["无名渔夫", "Collector 收藏家", "五件文物", "二选一结局"]
        },
        "combat": {
            "title": "深海异变鱼追逐 + 理智值 + 灯光武器 + 时间管理——以「不要在夜里出海」为核心的克苏鲁恐怖",
            "value": "战斗几乎不存在——<b>你只是个渔夫，不是战士</b>。主要威胁是<b>夜里出现的深海怪物</b>：<b>海怪触手、幽灵船、巨型海蛇、噩梦鱼群</b>。面对它们你只能<b>开启探照灯快速撤回港口</b>。核心机制是<b>理智值（Panic Meter）</b>——夜越深、海越深，理智越低，画面开始扭曲、出现幻觉礁石。<b>钓鱼是核心活动</b>——白天钓鱼、夜里冒险拉变异鱼，每条鱼按贪婪/匆忙程度可能<b>变异</b>，变异鱼卖更高价但增加噩梦。整套战斗哲学是<b>「天黑前必须回港、贪心一定有代价」</b>——克苏鲁与渔夫的合同。",
            "keywords": ["理智值 Panic", "深海怪物", "变异鱼", "天黑回港"]
        },
        "coreLoop": {
            "title": "白天钓鱼 → 港口卖鱼 → 升级船与渔具 → 接镇民委托 → 夜里冒险取文物",
            "value": "你玩到的是<b>「克苏鲁渔船管理 × 时间循环开放世界」</b>——结构是<b>白天稳赚 vs 夜晚高风险高回报</b>对赌循环。日常活动包括<b>选择鱼竿/渔笼/拖网安装在船上格子（俄罗斯方块式空间管理）、识别鱼种钓法（拍键节奏小游戏）、回 Greater Marrow 卖鱼换钱、升级船体/引擎/储物舱、接 NPC 委托、夜里前往五大区域取文物</b>。养成线是<b>船升级 + 钓具配置 + 钓鱼研究图鉴</b>。<b>那次你第一次在夜里看到幽灵船跟着你、理智值跌到 0 的瞬间</b>是 indie 克苏鲁神来之笔。<b>钓一条鱼也能心跳加速。</b>",
            "keywords": ["白天 vs 夜晚对赌", "船舱方块管理", "钓鱼节奏", "图鉴收集"]
        }
    },
    "story_overview": {
        "tagline": "<b>The Marrows 群岛的灯塔又灭了</b>——天黑前你回得了港吗？",
        "paragraphs": [
            "想象一片叫 <b>The Marrows 的孤立群岛</b>——时代模糊像 20 世纪中期某个北方海域。地图由五区域组成：<b>Greater Marrow 主镇、Gale Cliffs 风暴悬崖、Stellar Basin、Twisted Strand、Devil's Spine</b>。白天是平凡的低多边形北欧渔村——海鸥、灯塔、木屋、码头、镇长在码头点烟斗。<b>夜晚一切变质</b>——海雾包裹船身、深海冒出畸形鱼、远方传来诡异歌声、视野出现不该存在的礁石。Black Salt Games 把萌系渔村和克苏鲁深海反差缝合。",
            "你扮演一位<b>无名渔夫</b>——开场你的小船在风暴中触礁，被 Greater Marrow 镇长救起。镇长说他需要新渔夫接替前任失踪者，你欠他一艘新船的债，开始为他打工。<b>名为 Collector 的老收藏家</b>陆续要你前往五大区域取回<b>五件古怪文物</b>——每一件都让海上异象加剧、镇民噩梦、灯塔逐一熄灭。你逐步发现每位 NPC 都背秘密：<b>失踪的妻子、被诅咒的灯塔守、变成乌贼的渔夫</b>。",
            "<b>那次你第一次在夜里看到幽灵船跟着你、理智值 Panic Meter 跌到 0、画面扭曲出现幻觉礁石的瞬间</b>，Black Salt Games 把克苏鲁恐怖塞进萌系低多边形渔船里——你打的不是怪，是<b>「贪心一定有代价」这道渔夫合同</b>；<b>那场你为了多卖几个金币把第十条鱼塞进船舱、回港路上鱼变异成不明生物的桥段</b>——理智值让你明白<b>「天黑前必须回港」从来不是建议而是诅咒</b>；<b>那次你在第五件文物前面对 Collector 与海洋两个选择的对话节点</b>，钓鱼不再只是钓鱼。这不是关于打败邪神的故事，是<b>「无名渔夫天黑前回得了港吗」</b>的故事——下一网你撒还是不撒？"
        ]
    },
    "aesthetic_summary": {
        "label": "低多边形渔村 × 克苏鲁深海",
        "definition": "<b>低多边形渔村 × 克苏鲁深海</b>，是 Black Salt Games 把<b>低多边形萌系北欧渔村视觉</b>（小镇木屋、码头灯塔、低面渔船、Q 版海鸥、画风简洁可爱）和<b>克苏鲁深海恐怖叙事</b>（海雾、变异鱼、幽灵船、海怪触手、噩梦幻觉）反差缝合在<b>渔船管理 × 时间对赌</b>外壳里的混血美学。底色是<b>霍华德·洛夫克拉夫特 × 老人与海</b>双重血统；变异在于<b>白天萌系 vs 夜晚惊悚的二象性</b>——同一座岛在 24 小时内变成两个游戏。色彩锁定<b>白天天蓝木黄 + 夜晚墨蓝紫红 + 灯塔暖橙</b>三色。",
        "evolution": "「低多边形 + 克苏鲁渔村」视觉线跨越百年。<b>1928 年</b>洛夫克拉夫特<b>《克苏鲁的呼唤》</b>定义深海邪神恐怖文学母版——本作精神祖父。<b>1931 年</b>洛夫克拉夫特<b>《印斯茅斯的阴霾》</b>定义渔村+变异+海洋邪教叙事范式。<b>1952 年</b>海明威<b>《老人与海》</b>定义独自渔夫与大海对峙文学母版——本作叙事节奏精神养分。<b>1996 年</b>PS1 时代低多边形美学成为 indie 怀旧视觉源头。<b>2009 年</b><b>《恐怖游轮》</b>定义海上时间循环+心理恐怖范式。<b>2015 年</b><b>《Sunless Sea》</b>开辟深海克苏鲁航海 RPG 品类。<b>2018 年</b><b>《Subnautica》</b>把深海恐怖做到 3D 工业级。<b>2023 年</b>《疏浚 Dredge》在 Black Salt Games 四人独立打磨下登场——低多边形萌系+克苏鲁夜晚+渔船方块管理把渔船管理时间对赌推到 indie 神作高度。",
        "references": [
            {"type": "novel", "title": "克苏鲁的呼唤（洛夫克拉夫特）", "year": "1928", "note": "<b>深海邪神恐怖</b>文学母版；本作克苏鲁血统最深精神祖父"},
            {"type": "novel", "title": "印斯茅斯的阴霾（洛夫克拉夫特）", "year": "1931", "note": "<b>渔村+变异+海洋邪教</b>叙事范式；可对照 The Marrows 居民秘密调性"},
            {"type": "novel", "title": "老人与海（海明威）", "year": "1952", "note": "<b>独自渔夫与大海对峙</b>文学母版；本作叙事节奏精神养分"},
            {"type": "film", "title": "恐怖游轮 Triangle", "year": "2009", "note": "<b>海上时间循环+心理恐怖</b>电影范式；可对照夜晚理智值崩溃调性"},
            {"type": "game", "title": "Sunless Sea", "year": "2015", "note": "<b>深海克苏鲁航海 RPG</b>品类母版；本作系统设计直接前作精神养分"},
            {"type": "game", "title": "Subnautica", "year": "2018", "note": "<b>深海恐怖 3D 工业级</b>品类标杆；可对照本作深海异变鱼调性"},
            {"type": "art", "title": "PS1 时代低多边形美学档案", "year": "1996", "note": "<b>低多边形 indie 怀旧</b>视觉源头；本作画风血统直接来源"},
            {"type": "show", "title": "挪威/冰岛北欧渔村风光纪录片", "year": "2010", "note": "<b>北欧小港口+灯塔+木屋</b>真实档案；本作美术考据基底"}
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
    "stray":         STRAY,
    "signalis":      SIGNALIS,
    "split-fiction": SPLIT,
    "days-gone":     DAYSGONE,
    "dredge":        DREDGE,
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

    # worldview checks
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

    # story overview checks
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

    # aesthetic summary checks
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
    print("v2.5 第七批 5 款 Adventure 游戏：内容写入 + 自检")
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
