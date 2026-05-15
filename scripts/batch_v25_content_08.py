# -*- coding: utf-8 -*-
"""v2.5 第八批 4 款 Survival 游戏：
dying-light-the-beast / metroid-prime-4-beyond / high-on-life-2 / dave-the-diver

注意：所有中文文案里如果要嵌入引号，必须用「」或（），严禁英文双引号嵌套。
keywords 数组里可以用英文双引号。
"""
import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "games"

# ============================================================
#  消逝的光芒：野兽 dying-light-the-beast
# ============================================================
DLB = {
    "worldview": {
        "background": {
            "title": "Harran 病毒爆发后数年——欧式被隔离的乡村区域 Castor Woods",
            "value": "故事发生在<b>Harran 病毒爆发后数年的末世</b>——一座被铁丝网与河流隔离的<b>欧式乡村「Castor Woods」</b>。你穿过<b>松木镇区、被遗弃的城堡、伐木厂、葡萄园、铁路隧道、玉米地</b>——白天像田园牧歌的旅游明信片，太阳一落山就变成丧尸狩猎场。Techland 把<b>波兰乡村真实地貌</b>缝进末世里——<b>晾衣绳还在风里飘、教堂钟还在夜里响、葡萄藤爬上倒塌的拖拉机</b>。这是<b>欧式末世田园 × 跑酷剪影夜恐</b>反差缝合，不再是中东 Harran 的烈日，而是更冷的北方光线。",
            "keywords": ["Harran 病毒", "Castor Woods", "欧式末世田园", "昼夜反差恐怖"]
        },
        "mainStory": {
            "title": "你是 Kyle Crane——一代主角逃脱多年囚禁后获得超自然力量回归",
            "value": "你扮演<b>Kyle Crane（凯尔·克雷恩）</b>——初代《消逝的光芒》主角，被某神秘组织囚禁实验多年，<b>体内的 Harran 病毒被强行培育成可控状态</b>。你逃脱后流落到 Castor Woods 这片被隔离区域，遇到<b>幸存者社区与残暴反派 Baron 男爵</b>。剧情核心是<b>「人还是兽」</b>——Crane 可以随时切换成<b>半丧尸形态「The Beast」</b>狂暴战斗，但每次释放都让他离人性更远。一边追查囚禁他的实验真相、一边帮社区对抗 Baron，<b>那道选择从十年前 Harran 一直延续到现在</b>。",
            "keywords": ["Kyle Crane 回归", "The Beast 形态", "Baron 男爵", "人兽抉择"]
        },
        "combat": {
            "title": "跑酷+紫外线对抗+野兽形态狂暴+末世 DIY 武器——以「昼夜节奏」为核心的硬核动作",
            "value": "战斗延续系列招牌<b>第一人称跑酷+近战</b>——<b>翻墙、蹬墙、抓檐、滑铲、空中处决</b>一气呵成。武器全是<b>末世 DIY 拼凑感</b>——绑钉子的棒球棍、电锯改装、火焰瓶、十字弓。白天对手主要是慢速行尸，到夜里<b>Volatile 高速变异体</b>会成群追杀你，必须靠<b>UV 紫外线手电筒</b>烧退它们才能保命。新增的<b>Beast Mode 野兽形态</b>是 Crane 独有——血量低时按键释放，<b>双臂变形+力量爆表+痛击成群丧尸</b>但理智值会反噬。整套战斗哲学是<b>「白天玩跑酷、夜里玩生存、绝境放野兽」</b>。",
            "keywords": ["第一人称跑酷", "UV 紫外线", "Beast 野兽形态", "夜行 Volatile"]
        },
        "coreLoop": {
            "title": "据点接任务 → 白天搜刮跑酷 → 夜里冒险高回报 → 升级技能 → 推进主线",
            "value": "你玩到的是<b>「跑酷开放世界 × 末日生存动作 RPG」</b>——Castor Woods 是一片连通的乡村开放世界。日常活动包括<b>从据点出发跑酷穿越城镇与森林、白天搜刮医疗用品与汽车零件、夜里前往高警戒区取稀有蓝图、协助幸存者据点抵御袭击</b>。养成线是<b>跑酷/战斗/野兽三大技能树+Beast Mode 充能槽</b>。Techland 把<b>独立发行</b>当成赌注——这是不再隶属 2 代续作的独立故事，主打一代老粉回归。",
            "keywords": ["乡村开放世界", "昼夜节奏", "三大技能树", "幸存者据点"]
        }
    },
    "story_overview": {
        "tagline": "<b>Kyle Crane 在 Castor Woods 醒来</b>——你还是当年那个人吗？",
        "paragraphs": [
            "想象一片<b>Harran 病毒爆发后数年的末世</b>——但镜头不再在中东烈日下，而是切到欧洲被铁丝网与河流隔离的乡村「Castor Woods」。你穿过<b>松木镇区、被遗弃的城堡、伐木厂、葡萄园、铁路隧道、玉米地</b>——白天像田园牧歌的旅游明信片，太阳一落山变成丧尸狩猎场。<b>晾衣绳在风里飘、教堂钟在夜里响、葡萄藤爬上倒塌的拖拉机</b>。Techland 把波兰乡村真实地貌缝进末世里——这一作走向<b>独立发售</b>，不再是 2 代 DLC，而是一代主角的回归之作。",
            "你扮演<b>Kyle Crane</b>——初代主角，被某神秘组织囚禁实验多年，<b>体内 Harran 病毒被强行培育成可控状态</b>。你逃脱后流落 Castor Woods，遇到幸存者社区与残暴反派<b>Baron 男爵</b>。新机制 <b>The Beast</b> 让 Crane 可以切换成半丧尸狂暴形态——双臂变形、力量爆表、痛击成群丧尸，但每次释放都让他离人性更远。白天玩跑酷、夜里玩生存、绝境放野兽。",
            "<b>那次你第一次在夜里被 Volatile 群体追上铁路天桥、UV 手电筒电池见底、按键释放 Beast Mode 把六只丧尸打成血雾的瞬间</b>，Techland 把第一人称跑酷+末日动作做到系列十年新巅峰——你打的不是怪，是<b>「人还是兽」这道一代留下的旧题</b>；<b>那场你在葡萄园教堂看到 Baron 男爵处决幸存者的桥段</b>——欧式末世让你明白<b>「换个地图，人性还是这副样子」</b>；<b>那次你在被囚禁的实验档案里读到自己十年来发生过什么的对话节点</b>，回归不再是宣发噱头，是 Crane 自己的执念。这不是关于打败丧尸的故事，是<b>「Kyle Crane 还是当年那个人吗」</b>的故事——下一段夜路你要不要放出野兽？"
        ]
    },
    "aesthetic_summary": {
        "label": "末世乡村田园 × 跑酷昼夜恐怖",
        "definition": "<b>末世乡村田园 × 跑酷昼夜恐怖</b>，是 Techland 把<b>欧洲（波兰/巴尔干）真实乡村地貌</b>（松木镇、葡萄园、教堂尖顶、伐木厂、铁路隧道）和<b>Harran 病毒末世跑酷恐怖</b>（成群丧尸、UV 紫外线、夜行 Volatile、DIY 武器、第一人称翻墙蹬墙）反差融合在<b>一代主角 Kyle Crane 回归 + Beast 野兽形态</b>外壳里的混血美学。底色是<b>《28 天后》× 罗梅罗活死人三部曲</b>双重血统；变异在于<b>把镜头从 Harran 烈日切到欧洲冷光线</b>。",
        "evolution": "「丧尸末世+乡村田园+跑酷」视觉线跨越半世纪。<b>1968 年</b>乔治·罗梅罗<b>《活死人之夜》</b>定义现代丧尸电影母版——本作精神祖父之一。<b>1978 年</b>罗梅罗<b>《活死人黎明》</b>把丧尸做到末世社会隐喻巅峰。<b>2002 年</b>丹尼·博伊尔<b>《28 天后》</b>定义高速变异感染者品类——本作 Volatile 直接精神来源。<b>1979 年</b>乔治·米勒<b>《疯狂麦克斯》</b>定义末日 DIY 武器视觉母版。<b>2015 年</b>Techland <b>《消逝的光芒》初代</b>定义第一人称跑酷+昼夜节奏品类骨架。<b>2022 年</b>Techland<b>《消逝的光芒 2》</b>把跑酷开放世界推到次世代工业级。<b>2025 年</b>《消逝的光芒：野兽》在 C-Engine 下登场——欧式乡村+一代回归+Beast Mode 把跑酷恐怖推到独立发售新阶段。",
        "references": [
            {"type": "film", "title": "28 天后 28 Days Later", "year": "2002", "note": "<b>高速变异感染者</b>电影母版；本作 Volatile 与夜行恐怖最深底色"},
            {"type": "film", "title": "活死人之夜（罗梅罗）", "year": "1968", "note": "<b>现代丧尸电影</b>母版；本作 Harran 病毒末世精神祖父"},
            {"type": "film", "title": "活死人黎明（罗梅罗）", "year": "1978", "note": "<b>丧尸末世社会隐喻</b>电影巅峰；可对照 Castor Woods 据点张力"},
            {"type": "film", "title": "疯狂麦克斯 Mad Max", "year": "1979", "note": "<b>末日 DIY 武器</b>视觉母版；本作绑钉棒球棍考据来源"},
            {"type": "show", "title": "极限跑酷纪录片 Parkour: From Margin to Mainstream", "year": "2013", "note": "<b>Free Running 跑酷</b>真实档案；本作第一人称翻墙蹬墙考据基底"},
            {"type": "game", "title": "消逝的光芒 Dying Light 1", "year": "2015", "note": "<b>第一人称跑酷+昼夜节奏</b>品类骨架；本作直接前作"},
            {"type": "game", "title": "消逝的光芒 2 Dying Light 2", "year": "2022", "note": "<b>跑酷开放世界次世代工业级</b>标杆；本作系统直接演进"},
            {"type": "art", "title": "波兰/巴尔干乡村风光纪录片", "year": "2018", "note": "<b>欧式松木镇+葡萄园+教堂</b>真实档案；Castor Woods 美术考据基底"}
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
#  银河战士 Prime 4：超越 metroid-prime-4-beyond
# ============================================================
MP4 = {
    "worldview": {
        "background": {
            "title": "遥远未来银河联邦时代——未知外星星球上的 Chozo 遗迹与太空海盗基地",
            "value": "故事发生在<b>遥远未来银河联邦时代</b>——人类与多种外星种族组成<b>Galactic Federation</b>松散统治银河，但太空海盗与 Phazon 灾变阴影从未散去。本作主舞台是<b>一颗未知外星星球</b>——你穿过<b>外星生态丛林、Chozo 鸟人族失落遗迹、太空海盗深矿基地、能量结晶溶洞、漂浮空中神殿</b>。三层科技堆叠：<b>联邦舰队枪械、Chozo 古文明能量符文、太空海盗 Phazon 改造生体武器</b>。Retro Studios 七年磨一作。",
            "keywords": ["Galactic Federation", "Chozo 遗迹", "Space Pirates", "Phazon 灾变"]
        },
        "mainStory": {
            "title": "你是萨姆斯·阿兰——银河系最强赏金猎人独自踏入未知星球的 Chozo 秘密",
            "value": "你扮演<b>萨姆斯·阿兰（Samus Aran）</b>——银河系最强女性赏金猎人，由 Chozo 鸟人族抚养长大，身披<b>Chozo 动力铠甲</b>。开场联邦军舰被未知敌人击落，萨姆斯单舱坠入这颗陌生星球，发现<b>新的 Chozo 文明分支与好战鸟人族 Mawkin</b>。剧情核心是<b>「Chozo 留给萨姆斯的不只是铠甲，还有她不知道的旧账」</b>——一支古代 Chozo 派系制造能量威胁，萨姆斯独自深入解开身世第二层秘密。<b>整作零对白靠环境叙事推进</b>。",
            "keywords": ["Samus Aran", "Chozo 身世", "Mawkin 派系", "环境叙事"]
        },
        "combat": {
            "title": "Morph Ball 变形球+光束切换+导弹+第一人称扫描——以「孤独探索」为核心的银河城射击",
            "value": "战斗延续 Metroid Prime 招牌<b>第一人称视角射击 + 银河城探索</b>——<b>Power/Wave/Ice/Plasma Beam</b>四种光束切换，每种对特定敌人有效。<b>Morph Ball 变形球</b>让你压缩成弹珠钻入管道、放置炸弹。新增<b>Beyond 精神感应</b>——隔空操控外星机关、读取 Chozo 古文残留意识、远距离操控敌人。Boss 包括<b>巨型外星生物机械、Chozo 守护幽灵、Phazon 队长</b>。整套战斗哲学是<b>「扫描+切光束+变形球，独自面对外星深渊」</b>。",
            "keywords": ["四种光束", "Morph Ball", "Beyond 精神感应", "扫描机制"]
        },
        "coreLoop": {
            "title": "降落星球 → 扫描环境 → 探索遗迹 → 解锁新能力 → 回访已知区域 → 推进主线",
            "value": "你玩到的是<b>「3D 银河城 × 第一人称射击探索」</b>——这是 Metroid Prime 系列招牌玩法。星球地图是<b>互联多区域</b>：丛林表层、Chozo 遗迹深层、太空海盗基地、能量结晶溶洞、漂浮空中神殿。日常活动包括<b>沿管道用 Morph Ball 穿越、对环境物体扫描积累 Lore 数据库、搜集导弹箱与能量罐升级、解锁新能力后回访早期区域开启隐藏区</b>——<b>Backtracking 是核心，不是缺点</b>。Retro Studios 七年等待没有白费。",
            "keywords": ["3D 银河城", "扫描数据库", "Backtracking", "能力门解锁"]
        }
    },
    "story_overview": {
        "tagline": "<b>萨姆斯独自坠入陌生星球</b>——Chozo 留给你的旧账，你敢翻吗？",
        "paragraphs": [
            "想象一片<b>遥远未来银河联邦时代</b>——人类与多种外星种族组成 Galactic Federation 松散统治银河，但太空海盗与 Phazon 灾变阴影从未散去。本作主舞台是一颗未知外星星球——你穿过<b>外星生态丛林、Chozo 鸟人族失落遗迹、太空海盗深矿基地、能量结晶溶洞、漂浮空中神殿</b>。三层科技堆叠：<b>联邦舰队枪械、Chozo 古文明能量符文、太空海盗 Phazon 改造生体武器</b>。Retro Studios 与任天堂联合开发<b>七年磨一作</b>。",
            "你扮演<b>萨姆斯·阿兰</b>——银河系最强女性赏金猎人，由 Chozo 鸟人族抚养长大。开场联邦军舰被未知敌人击落，萨姆斯单舱坠入这颗陌生星球，发现<b>新的 Chozo 文明分支与好战鸟人族 Mawkin</b>。新机制 <b>Beyond 精神感应</b>让你隔空操控外星机关、读取 Chozo 古文残留意识、甚至从远距离操控敌人。整作零对白靠环境叙事推进——萨姆斯一个人，是银河战士品牌最纯粹的孤独。",
            "<b>那次你第一次在 Chozo 神殿扫描古文符号、Beyond 精神感应让符文活过来的瞬间</b>，Retro Studios 把 H.R. 吉格生物机械美学推到任天堂工业级——你打的不是怪，是<b>「Chozo 留给萨姆斯不只是铠甲」这道悬了二十年的旧账</b>；<b>那场你被 Phazon 改造的太空海盗队长围困、第一次切到 Plasma Beam 把它烧穿的桥段</b>——四种光束让你明白<b>「孤独探索从来不是无聊，是节奏」</b>；<b>那次你回访初始丛林、新解锁能力打开早期看不见隐藏区域的对话节点</b>，七年等待终于回报。这不是关于打败反派的故事，是<b>「Chozo 留给你的旧账你敢翻吗」</b>的故事——下一颗能量罐藏在哪面墙后？"
        ]
    },
    "aesthetic_summary": {
        "label": "外星生物机械 × 银河城孤独探索",
        "definition": "<b>外星生物机械 × 银河城孤独探索</b>，是 Retro Studios 把<b>H.R. 吉格生物机械视觉传统</b>（外骨骼+管线+液态金属+生体融合机械）和<b>Chozo 鸟人族古文明遗迹</b>（高耸石柱+羽翼符文+漂浮神殿+能量结晶）以及<b>外星生态自然主义</b>（陌生植被+液态河流+能量风暴）三层缝合在<b>第一人称银河城探索</b>外壳里的混血美学。底色是<b>《异形》× 旧 Metroid Prime 三部曲</b>双重血统；变异在于<b>萨姆斯零对白孤独镜头</b>。",
        "evolution": "「外星生物机械+孤独探索」视觉线跨越半世纪。<b>1968 年</b>库布里克<b>《2001 太空漫游》</b>定义太空孤独探索哲学母版——本作精神祖父。<b>1979 年</b>雷德利·斯科特<b>《异形》</b>定义太空生物机械恐怖电影母版——H.R. 吉格美学起点。<b>1986 年</b><b>《异形 2》</b>把外星殖民地工业级化。<b>1986 年</b>任天堂<b>《Metroid》初代</b>开辟银河城品类。<b>1994 年</b><b>《超级银河战士》</b>把银河城做到 SFC 神作。<b>2002 年</b>Retro Studios<b>《Metroid Prime》</b>开辟 3D 第一人称银河城品类——本作直接前作。<b>2007 年</b><b>《Metroid Prime 3：腐化》</b>把 Phazon 灾变叙事画上句号。<b>2025 年</b>《Metroid Prime 4：Beyond》在 Switch 2 平台登场——七年等待+精神感应+次世代生物机械把外星孤独探索推到任天堂工业级新巅峰。",
        "references": [
            {"type": "film", "title": "异形 Alien", "year": "1979", "note": "<b>太空生物机械恐怖</b>电影母版；H.R. 吉格美学起点与本作生物机械最深底色"},
            {"type": "film", "title": "2001 太空漫游 2001: A Space Odyssey", "year": "1968", "note": "<b>太空孤独探索哲学</b>母版；本作零对白环境叙事精神祖父"},
            {"type": "art", "title": "H.R. 吉格画册 Necronomicon", "year": "1977", "note": "<b>生物机械视觉</b>原典；本作外骨骼与管线美学直接来源"},
            {"type": "game", "title": "Metroid Prime 三部曲", "year": "2002", "note": "<b>3D 第一人称银河城</b>品类母版；本作直接前作与系统骨架"},
            {"type": "game", "title": "超级银河战士 Super Metroid", "year": "1994", "note": "<b>银河城品类 SFC 神作</b>；本作精神 DNA"},
            {"type": "film", "title": "异形 2 Aliens", "year": "1986", "note": "<b>外星殖民地工业级</b>电影范式；可对照太空海盗深矿基地调性"},
            {"type": "art", "title": "Chozo 鸟人族神话设定档案", "year": "1986", "note": "<b>羽翼+石柱+能量符文</b>系列原典；萨姆斯身世美术考据基底"},
            {"type": "film", "title": "普罗米修斯 Prometheus", "year": "2012", "note": "<b>外星古文明遗迹</b>电影范式；可对照 Chozo 神殿调性"}
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
#  嗨皮人生 2 high-on-life-2
# ============================================================
HOL2 = {
    "worldview": {
        "background": {
            "title": "架空科幻当代——外星人已公开接触地球的银河系第二乐章",
            "value": "故事发生在<b>架空科幻当代</b>——外星人已公开接触地球，跨星球传送门成日常基础设施。1 代之后的银河系格局再次洗牌——<b>新一波外星黑帮、宗教邪教、跨维度怪兽涌入</b>。你穿过<b>Blim City 霓虹外星都市、暗黑星球地下角斗场、有机体星球肉墙隧道、节日嘉年华星际游乐园、跨维度购物中心</b>。科技是<b>跨星球传送门 + 外星生物武器化</b>——你的枪是真的活着，会说脏话、会吐槽你、会在死亡时哭。Squanch Games 把<b>Justin Roiland 离开后的成人卡通 FPS</b>赌在续作上。",
            "keywords": ["Blim City", "跨星球传送门", "活体外星枪", "成人卡通 FPS"]
        },
        "mainStory": {
            "title": "你是回归赏金猎人——手持新一代会说话的外星枪械对抗跨维度威胁",
            "value": "你扮演<b>回归的赏金猎人主角</b>——1 代之后名声大噪，新雇主联系你处理<b>一波跨维度入侵 Blim City 的诡异威胁</b>。剧情核心是<b>「老搭档+新搭档的成人嘴炮喜剧」</b>——你手持几把<b>会说话的活体外星枪 Gatlian</b>——它们各有性格：刻薄毒舌的、神经质胆小的、嗨过头的、忧郁存在主义的。整作主基调是<b>不间断对白嘴炮</b>，台词密度比 1 代再翻倍。Squanch Games 在 Justin Roiland 离开后承诺<b>「保留瑞克与莫蒂式怪味喜剧但走向新作者表达」</b>——续作是这家工作室的赌注。",
            "keywords": ["Gatlian 活枪", "成人嘴炮喜剧", "跨维度入侵", "Squanch 续作"]
        },
        "combat": {
            "title": "活体外星枪+花式技能+敌人变种 Boss 战+霓虹卡通视觉——以「嘴炮陪玩」为核心的彩色 FPS",
            "value": "战斗是<b>第一人称射击 + 活体外星枪技能</b>——每把 Gatlian 都有<b>独特技能与不间断对白</b>。Kenny（手枪型）能发射黏弹固定敌人、Sweezy（突击步枪型）能慢镜头时停、Gus（霰弹型）会自动射出锯片回旋镖。新增<b>2 代专属枪种</b>带跨维度异常技能。敌人是<b>外星黑帮、邪教徒、变种生物、跨维度怪兽</b>。Boss 战每场都有完整<b>剧场式嘴炮 + 多阶段机制</b>——典型瑞克与莫蒂式胡闹关卡设计。整套战斗哲学是<b>「打不过别紧张，你的枪会替你嘴炮反派」</b>。",
            "keywords": ["Gatlian 技能", "时停慢镜头", "黏弹锯片", "剧场式 Boss"]
        },
        "coreLoop": {
            "title": "Blim City 接赏金 → 传送门跳星球 → FPS 战斗+嘴炮 → 回城刷店升级 → 推主线",
            "value": "你玩到的是<b>「成人卡通彩色 FPS × 银河系赏金喜剧」</b>——结构沿用 1 代<b>Blim City 中枢 + 多星球任务关卡</b>骨架。日常活动包括<b>从 Blim City 公寓接赏金、跨星球传送门跳跃、第一人称跑射、收集外星垃圾、回城购买装备和装饰、看外星电视吐槽节目</b>。养成线是<b>每把 Gatlian 单独升级 + 主角防具与跳跃强化</b>。<b>那次你和 Kenny 一起在角斗场吐槽一段三分钟、被解说员打断三次的瞬间</b>是 Squanch 嘴炮密度峰值。",
            "keywords": ["Blim City 中枢", "多星球关卡", "外星电视台", "嘴炮节奏"]
        }
    },
    "story_overview": {
        "tagline": "<b>Blim City 又来了一波跨维度入侵</b>——你的活体外星枪准备好嘴炮了吗？",
        "paragraphs": [
            "想象一片<b>架空科幻当代</b>——外星人已公开接触地球，跨星球传送门成日常基础设施。1 代之后银河系格局再次洗牌——<b>新一波外星黑帮、宗教邪教、跨维度怪兽涌入</b>。你穿过<b>Blim City 霓虹外星都市、暗黑星球地下角斗场、有机体星球肉墙隧道、节日嘉年华星际游乐园</b>。科技是跨星球传送门 + 外星生物武器化——你的枪是真的活着，会说脏话、吐槽你、死亡时哭。Squanch Games 把 Justin Roiland 离开后的成人卡通 FPS 续作赌在 2 代上。",
            "你扮演<b>回归的赏金猎人主角</b>——1 代之后名声大噪，新雇主联系你处理一波跨维度入侵 Blim City 的诡异威胁。你手持几把<b>会说话的活体外星枪 Gatlian</b>——刻薄毒舌的、神经质胆小的、嗨过头的、忧郁存在主义的。整作主基调是<b>不间断对白嘴炮</b>，台词密度比 1 代再翻倍。Squanch 承诺保留瑞克与莫蒂式怪味喜剧但走向新作者表达——这是工作室的赌注。",
            "<b>那次你第一次和 Kenny 在角斗场被解说员打断三次的脱口秀小品瞬间</b>，Squanch Games 把成人卡通 FPS 嘴炮密度推到峰值——你打的不是怪，是<b>「Roiland 离开后喜剧灵魂能不能延续」这道续作大考</b>；<b>那场你被跨维度怪兽追到购物中心、Sweezy 时停慢镜头让你边吐槽边收割的桥段</b>——活体外星枪让你明白<b>「打不过别紧张，你的枪会替你嘴炮反派」</b>；<b>那次你回 Blim City 公寓打开外星电视台看完整段三分钟黑色小品的对话节点</b>，喜剧不止在关卡里。这不是关于打败反派的故事，是<b>「你的活体外星枪准备好嘴炮了吗」</b>的故事——下一道传送门通向哪个怪味星球？"
        ]
    },
    "aesthetic_summary": {
        "label": "外星卡通嘉年华 × 成人喜剧 FPS",
        "definition": "<b>外星卡通嘉年华 × 成人喜剧 FPS</b>，是 Squanch Games 把<b>瑞克与莫蒂式成人卡通视觉</b>（粗线条角色+夸张表情+怪味黑色幽默+涂鸦感装饰）和<b>赛博朋克霓虹外星都市</b>（Blim City 全息广告+多种族 NPC+霓虹小巷）以及<b>有机体生物世界</b>（肉墙隧道+脉搏管道+活体武器）反差融合在<b>第一人称射击 + 活体枪嘴炮</b>外壳里的混血美学。底色是<b>《瑞克与莫蒂》× 《银河系漫游指南》</b>双重血统；变异在于<b>武器具有完整对白演员阵容</b>。",
        "evolution": "「成人卡通+银河系喜剧+FPS」视觉线跨越半世纪。<b>1979 年</b>道格拉斯·亚当斯<b>《银河系漫游指南》</b>定义银河系荒诞喜剧文学母版——本作精神祖父。<b>1981 年</b><b>《Heavy Metal》成人动画电影</b>定义成人卡通视觉传统。<b>1997 年</b>Mike Judge<b>《King of the Hill》</b>定义美式低俗成人卡通范式。<b>1999 年</b><b>《南方公园》</b>把成人卡通做到电视黄金时代标杆。<b>2013 年</b>Justin Roiland<b>《瑞克与莫蒂》</b>定义跨维度怪味喜剧动画品类——本作直接精神血统。<b>2007 年</b><b>《传送门 Portal》</b>定义喜剧 FPS 关卡设计范式。<b>2020 年</b>Squanch Games<b>《嗨皮人生 1》</b>开辟活体外星枪嘴炮 FPS 子类——本作直接前作。<b>2025 年</b>《嗨皮人生 2》在虚幻 5 引擎下登场——Roiland 离场后第一作 Squanch 续作赌注。",
        "references": [
            {"type": "show", "title": "瑞克与莫蒂 Rick and Morty", "year": "2013", "note": "<b>跨维度怪味喜剧动画</b>品类母版；本作精神血统最深底色"},
            {"type": "novel", "title": "银河系漫游指南 The Hitchhiker's Guide", "year": "1979", "note": "<b>银河系荒诞喜剧</b>文学母版；本作精神祖父"},
            {"type": "show", "title": "南方公园 South Park", "year": "1997", "note": "<b>成人卡通电视黄金时代</b>标杆；可对照本作低俗喜剧调性"},
            {"type": "game", "title": "嗨皮人生 1 High on Life", "year": "2020", "note": "<b>活体外星枪嘴炮 FPS</b>子类母版；本作直接前作与系统骨架"},
            {"type": "game", "title": "传送门 Portal", "year": "2007", "note": "<b>喜剧 FPS 关卡设计</b>范式；可对照本作 Boss 战剧场感"},
            {"type": "game", "title": "赛博朋克 2077", "year": "2020", "note": "<b>霓虹未来都市</b>视觉远期参照；可对照 Blim City 街景调性"},
            {"type": "film", "title": "Heavy Metal 重金属动画电影", "year": "1981", "note": "<b>成人卡通视觉传统</b>电影源头；本作怪味卡通血统精神养分"},
            {"type": "show", "title": "Beavis and Butt-Head", "year": "1993", "note": "<b>美式低俗成人卡通</b>范式；可对照外星电视台小品调性"}
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
#  潜水员戴夫 dave-the-diver
# ============================================================
DAVE = {
    "worldview": {
        "background": {
            "title": "当代普通人的夏日海洋冒险——神秘蓝洞 + 班乔寿司店",
            "value": "故事发生在<b>当代世界一片普通海域</b>——但海面下有一个<b>每日地形都会随海流变换的神秘蓝洞 The Blue Hole</b>。你穿过<b>表层珊瑚礁阳光区、中层暗礁洞穴、深层荧光发光鱼群、海底古代亚特兰蒂斯遗迹、岸上的班乔寿司店</b>。科技是<b>当代潜水装备 + 轻奇幻海底古文明</b>——氧气表、鱼叉、麻醉枪并置亚特兰蒂斯能量水晶。<b>白天潜水 + 夜里经营寿司店</b>是日复一日的循环，圆润潜水员 Dave 帮朋友 Cobra 大叔的店渡过一个奇幻夏天。",
            "keywords": ["The Blue Hole", "班乔寿司店", "亚特兰蒂斯遗迹", "白天潜水夜里经营"]
        },
        "mainStory": {
            "title": "你是 Dave——圆润潜水员帮朋友把濒临倒闭的寿司店做成网红名店",
            "value": "你扮演<b>Dave the Diver（戴夫）</b>——一名<b>圆润、佛系、嗜睡的资深潜水员</b>。开场你被老朋友 Cobra 大叔从沙滩躺椅上叫起来：他在 Blue Hole 旁的<b>班乔寿司店</b>濒临倒闭，需要你白天潜水捕新鲜食材、夜里上阵当主厨救店。剧情核心是<b>「Dave 一个普通中年大叔在夏天发现一片海底古代文明」</b>——从开寿司店的小目标，逐渐卷入<b>亚特兰蒂斯人鱼族、海洋制药公司、海底邪教、远洋怪物</b>等连环冒险，TGA 2023 提名独立游戏。",
            "keywords": ["Dave 大叔", "Cobra 老板", "班乔寿司店", "亚特兰蒂斯人鱼"]
        },
        "combat": {
            "title": "鱼叉+麻醉枪+突击步枪+海底 Boss—以「白天捕鱼+夜里上菜」为核心的双轨循环",
            "value": "战斗是<b>白天潜水捕鱼 + 偶发 Boss 战</b>——日常用<b>鱼叉、麻醉枪、捕鱼网</b>击晕鱼类活捉，对体型大的稀有鱼用<b>突击步枪、鱼雷</b>击杀。氧气有限，潜得越深氧气消耗越快，必须在氧气见底前升回水面。Boss 战包括<b>巨型大白鲨、海底蜥蜴人、亚特兰蒂斯守卫、海洋制药公司武装鱼雷艇</b>。<b>夜里在班乔寿司店</b>切换玩法——做寿司是节奏小游戏，端菜是限时跑动游戏，给客人捏寿司+续茶+收银，<b>仿佛你白天打 Boss 晚上打工</b>。整套战斗哲学是<b>「能麻醉就别杀，活鱼上桌价格更高」</b>。",
            "keywords": ["氧气管理", "麻醉活捉", "Boss 鲨鱼", "寿司节奏小游戏"]
        },
        "coreLoop": {
            "title": "白天 Blue Hole 潜水捕鱼 → 收集食材 → 夜里寿司店做菜 → 升级装备 → 推剧情副本",
            "value": "你玩到的是<b>「潜水探索 + 餐厅经营双轨循环」</b>——结构是<b>白天潜水 vs 夜里上菜</b>对照玩法。日常活动包括<b>白天到 Blue Hole 三层潜水（每天地形随海流变化）、捕鱼+采珍珠+发掘亚特兰蒂斯遗迹道具、回岸上交给 Cobra 处理、夜里制定寿司菜单+做菜+管理服务员、雇佣员工+升级厨房+扩展菜单</b>。养成线是<b>潜水装备升级+寿司店等级+鱼图鉴+员工技能</b>。<b>钓一条鱼一个寿司也能做出史诗感</b>。",
            "keywords": ["双轨循环", "随机海流地形", "寿司经营", "鱼图鉴"]
        }
    },
    "story_overview": {
        "tagline": "<b>Cobra 大叔又把 Dave 从沙滩躺椅上叫醒了</b>——今晚客人吃什么寿司？",
        "paragraphs": [
            "想象一片<b>当代普通海域</b>——但海面下有一个每日地形都会随海流变换的<b>神秘蓝洞 The Blue Hole</b>。你穿过<b>表层珊瑚礁阳光区、中层暗礁洞穴、深层荧光发光鱼群、海底古代亚特兰蒂斯遗迹、岸上的班乔寿司店</b>。科技是当代潜水装备+轻奇幻海底古文明——氧气表、鱼叉、麻醉枪并置亚特兰蒂斯能量水晶。<b>白天潜水 + 夜里经营寿司店</b>是日复一日的循环。Mintrocket（Nexon 子工作室）把治愈与冒险塞进 6.5 像素 + 3D 镜头里——TGA 2023 提名最佳独立游戏，口碑爆款。",
            "你扮演<b>Dave the Diver</b>——一名圆润、佛系、嗜睡的资深潜水员。开场老朋友 Cobra 把你从沙滩躺椅上叫醒：他的<b>班乔寿司店</b>濒临倒闭，需要你白天潜水捕新鲜食材、夜里上阵当主厨救店。从开寿司店的小目标，<b>Dave 这个普通中年大叔逐渐卷入亚特兰蒂斯人鱼族、海洋制药公司、海底邪教、远洋怪物等连环冒险</b>——反差萌+治愈冒险缝合得严丝合缝。",
            "<b>那次你第一次潜到 200 米深处、氧气见底、却看到亚特兰蒂斯人鱼水晶神殿的瞬间</b>，Mintrocket 把像素 3D 混搭+反差萌做到 indie 治愈神作高度——你打的不是怪，是<b>「Dave 这个圆润大叔为什么夏天卷入了海底古文明」这道反差萌</b>；<b>那场你白天捕的稀有鱼晚上被店里食客差评 Cobra 跟你掰扯账本的桥段</b>——双轨循环让你明白<b>「能麻醉就别杀，活鱼上桌价格更高」</b>；<b>那次你深夜关店和 Cobra 在码头喝啤酒看星星的对话节点</b>，明亮海洋配温馨餐厅，治愈不只是宣发标签。这不是关于打败反派的故事，是<b>「今晚客人吃什么寿司」</b>的故事——下一潜你抓鳗鱼还是金枪鱼？"
        ]
    },
    "aesthetic_summary": {
        "label": "像素 3D 混搭 × 海洋寿司治愈",
        "definition": "<b>像素 3D 混搭 × 海洋寿司治愈</b>，是 Mintrocket 把<b>16 位时代像素角色</b>（圆润 Dave 颗粒度低面、Cobra 卡通脸、像素表情符号弹幕）和<b>3D 实时光照海洋场景</b>（蓝洞折射阳光、深海荧光鱼群、亚特兰蒂斯水晶神殿）混搭融合在<b>白天潜水 + 夜里寿司店双轨循环</b>外壳里的混血美学。底色是<b>《海底两万里》× 海绵宝宝</b>双重血统；变异在于<b>角色像素 + 环境 3D 的反差萌镜头</b>——亚洲独立工作室对像素美学的现代演绎。",
        "evolution": "「海洋冒险+餐厅经营+像素萌系」视觉线跨越百年。<b>1870 年</b>儒勒·凡尔纳<b>《海底两万里》</b>定义海底奇幻文学母版——本作精神祖父。<b>1989 年</b>迪士尼<b>《小美人鱼》</b>定义当代海洋亚特兰蒂斯流行视觉。<b>1999 年</b><b>《海绵宝宝 SpongeBob》</b>定义海底卡通治愈喜剧——Cobra 与寿司店调性精神参照。<b>2003 年</b>皮克斯<b>《海底总动员》</b>把海洋多彩 3D 推到电影工业级。<b>1996 年</b><b>《牧场物语》</b>定义经营养成日式像素品类。<b>2017 年</b><b>《塞尔达：旷野之息》</b>把开放世界自由探索做到当代标杆——本作蓝洞海流地形日变精神参照。<b>2016 年</b><b>《Stardew Valley》</b>把像素经营独立游戏推到口碑神作。<b>2023 年</b>《潜水员戴夫》在 Mintrocket 打磨下登场——像素 3D 混搭+双轨循环+反差萌把海洋治愈推到 indie 现象级口碑爆款。",
        "references": [
            {"type": "show", "title": "海绵宝宝 SpongeBob SquarePants", "year": "1999", "note": "<b>海底卡通治愈喜剧</b>动画母版；Cobra 与寿司店调性精神参照"},
            {"type": "novel", "title": "海底两万里（凡尔纳）", "year": "1870", "note": "<b>海底奇幻文学</b>母版；本作亚特兰蒂斯遗迹精神祖父"},
            {"type": "film", "title": "海底总动员 Finding Nemo", "year": "2003", "note": "<b>海洋多彩 3D 工业级</b>电影标杆；本作蓝洞海洋色彩养分"},
            {"type": "film", "title": "小美人鱼 The Little Mermaid", "year": "1989", "note": "<b>当代海洋亚特兰蒂斯</b>流行视觉；可对照人鱼族水晶神殿调性"},
            {"type": "game", "title": "牧场物语 Story of Seasons", "year": "1996", "note": "<b>经营养成日式像素</b>品类母版；本作经营骨架精神养分"},
            {"type": "game", "title": "Stardew Valley", "year": "2016", "note": "<b>像素经营独立神作</b>口碑标杆；本作 indie 血统直接参照"},
            {"type": "game", "title": "塞尔达传说：旷野之息", "year": "2017", "note": "<b>开放世界自由探索</b>当代标杆；本作蓝洞海流地形日变精神参照"},
            {"type": "show", "title": "海洋探险纪录片 Blue Planet", "year": "2001", "note": "<b>真实海洋多层生态</b>真实档案；蓝洞表层中层深层考据基底"}
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
    "dying-light-the-beast":   DLB,
    "metroid-prime-4-beyond":  MP4,
    "high-on-life-2":          HOL2,
    "dave-the-diver":          DAVE,
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
    print("v2.5 第八批 4 款 Survival 游戏：内容写入 + 自检")
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
