import json

fp = 'd:/ecnalClaw/output/game-tracker-v2/data/games/resident-evil-requiem.json'

with open(fp, 'r', encoding='utf-8') as f:
    d = json.load(f)

playerExp = {
    "media": {
        "memory": [
            {
                "text": "IGN 评测把<b>开场 Rhodes Hill 慢性病疗养中心几小时</b>形容为系列至今最惊悚的段落，戴上耳机关灯玩会让人发现自己身上还有没绷紧过的肌肉。",
                "src": "IGN Resident Evil Requiem Review",
                "url": "https://www.ign.com/articles/resident-evil-requiem-review"
            },
            {
                "text": "Polygon 把流程拆成<b>「Grace 的脆弱潜行 + Leon 的残躯救赎」双主角对照</b>，并指出 Leon 的整段戏建立在他作为浣熊市菜鸟警员留下的幸存者愧疚上。",
                "src": "Polygon Resident Evil Requiem Endings",
                "url": "https://www.polygon.com/resident-evil-requiems-endings-explained/"
            },
            {
                "text": "游民星空给出 9.2 分，称 Wrenwood Hotel 与浣熊市废墟的复刻<b>把场景做成了叙事本身</b>，老玩家光是路过警局残骸就会被戳中。",
                "src": "游民星空 评测",
                "url": "https://www.gamersky.com/news/202602/2096887_2.shtml"
            },
            {
                "text": "Outlook Respawn 报道 Metacritic 用户均分 9.5、Steam 同时在线峰值 344,214，<b>成为系列史上口碑最高、Steam 同时在线最高的正传作品</b>，超过《生化危机 4 重制版》一倍以上。",
                "src": "Outlook Respawn",
                "url": "https://respawn.outlookindia.com/gaming/gaming-news/resident-evil-requiem-breaks-metacritic-record-with-highest-score"
            }
        ],
        "excitement": [
            {
                "text": "IGN 把 Grace 段落里<b>用「血液收集器」吸取丧尸尸液合成单次溶血针</b>列为系列最爽的潜行处决，扎进背脊后整具尸体会膨胀爆裂。",
                "src": "IGN Resident Evil Requiem Review",
                "url": "https://www.ign.com/articles/resident-evil-requiem-review"
            },
            {
                "text": "游民星空认为 Leon 的<b>手斧 + 完美格挡反击</b>能让高手无伤通关大部分战斗，「卡肉感」反击与「皇家守卫」式弹反让动作流畅度直追《生化危机 4 重制版》。",
                "src": "游民星空 评测",
                "url": "https://www.gamersky.com/news/202602/2096887_2.shtml"
            },
            {
                "text": "Metacritic 媒体评测用「the most enjoyably bad one-liners in the business」形容 Leon 的台词，加上<b>原生 PS5 不掉 60、PS5 Pro 4K + 路径追踪</b>的演出，被多家媒体并列为「20 年来最让人乐在其中的生化新作」。",
                "src": "Metacritic Resident Evil Requiem PS5",
                "url": "https://www.metacritic.com/game/playstation-5/resident-evil-requiem"
            },
            {
                "text": "IGN 中国指出 Leon 进入<b>东浣熊市半开放地图</b>的爽感来自「战斗手环」积分系统：杀敌换点数购入新枪与改装件，配合废墟中的崩塌高楼战斗，是系列罕有的立体战场。",
                "src": "IGN 中国 评测",
                "url": "https://www.ign.com.cn/re9/58781/review/sheng-hua-wei-ji-an-hun-qu-ping-ce-9-fen-ign-zhong-guo"
            }
        ],
        "pain": [
            {
                "text": "游民星空指出<b>双线切换太频繁</b>，Leon 刚打爽就被切回 Grace 潜行，情绪反复被打断；后期剧情靠浣熊市怀旧桥段硬串，关键转折铺垫不足。",
                "src": "游民百相 游民星空",
                "url": "https://club.gamersky.com/m/activity/1539358?club=1468"
            },
            {
                "text": "IGN 中国吐槽<b>BOSS 战设计套路化</b>，匹配不上整体精彩的动作体验；同时半开放浣熊市地图除了倒塌高楼桥段外平平无奇，缺少 RE4 重制湖区的灵性。",
                "src": "IGN 中国 评测",
                "url": "https://www.ign.com.cn/re9/58781/review/sheng-hua-wei-ji-an-hun-qu-ping-ce-9-fen-ign-zhong-guo"
            },
            {
                "text": "Region Free 仅给出 60 分，作为 M 站当下最低分指出谜题<b>陈旧到部分被过场动画直接跳过</b>，跑回头路换钥匙的设计像在做功课，最终 Boss 战草草收场。",
                "src": "游民星空 转载 Region Free",
                "url": "https://www.gamersky.com/news/202602/2096927.shtml"
            },
            {
                "text": "Metacritic 法语用户长评指出 Grace 段落第一人称视角下<b>战斗辨识度不足</b>，加上配乐与音效偏内敛，没有给关键场面留下记忆点。",
                "src": "Metacritic User Review",
                "url": "https://www.metacritic.com/game/playstation-5/resident-evil-requiem"
            }
        ],
        "churn": [
            {
                "text": "ComicBook 与 Screen Rant 指出<b>非正史「坏结局」里 Leon 被 Zeno 一枪爆头</b>，整段没有最终 Boss 战，玩家普遍觉得突兀且廉价，让首次通关情绪极差。",
                "src": "ComicBook.com",
                "url": "https://comicbook.com/gaming/feature/resident-evil-requiems-non-canon-ending-feels-like-a-complete-waste/"
            },
            {
                "text": "biggo 财经报道 PC 版同时挂着<b>Denuvo + Capcom 自家 DRM + Enigma</b> 三层壳，评测者一天只能换 5 次 CPU 授权，玩家也可能因 Windows 更新或驱动变动被锁出游戏。",
                "src": "biggo Finance",
                "url": "https://finance.biggo.com/news/202602271823_Resident_Evil_Requiem_PC_Performance_Review"
            },
            {
                "text": "Steam 商店页显示<b>「豪华包」拆出 5 套外观、4 把武器涂装与 1998 年来信文件</b>额外卖 78 元，多家媒体批评 30 周年纪念作把怀旧元素切片当 DLC。",
                "src": "Steam 商店页 Resident Evil Requiem",
                "url": "https://store.steampowered.com/app/3764200/Resident_Evil_Requiem/"
            }
        ]
    },
    "community": {
        "memory": [
            {
                "text": "Steambase 统计 Steam 总评 14.8 万条<b>「好评如潮」、好评率 96%</b>，简体中文区也是 90% 好评，社区普遍把开场疗养院段落称为「peak Resident Evil」。",
                "src": "Steambase Resident Evil Requiem Reviews",
                "url": "https://steambase.io/games/resident-evil-requiem/reviews"
            },
            {
                "text": "Metacritic PS5 用户区充斥「The most entertaining new Resident Evil game in over two decades」之类长评，<b>用户均分 9.5 创系列纪录</b>，被频繁拿来与《生化危机 4 重制版》《村庄》对比。",
                "src": "Metacritic Resident Evil Requiem PS5",
                "url": "https://www.metacritic.com/game/playstation-5/resident-evil-requiem"
            },
            {
                "text": "游民百相用户长评把游戏总结成「<b>一场精心准备的粉丝聚会</b>」，认为重返浣熊市警局残骸、双线联动设计与 RE Engine 升级版的湿润材质是最直接的留念点。",
                "src": "游民百相 玩家评测",
                "url": "https://club.gamersky.com/m/activity/1539358?club=1468"
            }
        ],
        "excitement": [
            {
                "text": "Screen Rant 整理 YouTube 频道 Sirloin 的坏结局视频评论，玩家「<b>哭崩</b>」「<b>看完直接发疯</b>」的留言占满评论区，确认这是 30 年系列里情感冲击最强的一次假死。",
                "src": "Screen Rant",
                "url": "https://screenrant.com/resident-evil-requiem-leon-death-bad-ending-reactions/"
            },
            {
                "text": "FandomWire 长帖回顾真结局里<b>Sherry Birkin 出现并暗示 Elpis 可治愈所有浣熊市后遗症患者</b>，社区把这段彩蛋视为承接生化 10 复仇者集结的最大爽点。",
                "src": "FandomWire 结局解析",
                "url": "https://fandomwire.com/all-resident-evil-requiem-endings-explained"
            },
            {
                "text": "Steam 社区讨论区把<b>「Grace 在线声敏丧尸 → Leon 进同一区无怪可刷」的连锁反应</b>当作多周目必玩理由，证明双线 AI 真的会互相吃掉敌人。",
                "src": "Steam 社区讨论",
                "url": "https://steamcommunity.com/app/3764200/discussions/"
            },
            {
                "text": "Outlook Respawn 把 Steam 同时在线 344,214 写成「比 RE4 重制翻倍、和《艾尔登法环》同等量级」，<b>社区把这数据截图洗版</b>当作生化系列复兴的实锤。",
                "src": "Outlook Respawn",
                "url": "https://respawn.outlookindia.com/gaming/gaming-news/resident-evil-requiem-breaks-metacritic-record-with-highest-score"
            }
        ],
        "pain": [
            {
                "text": "游民星空转载 IGN 专栏，指出社区分裂成两派——<b>「Leon 一出恐怖全无」</b>派与「30 周年就该照顾不同口味」派吵成一片，老粉认为后期被强行做成加强版生化 6。",
                "src": "游民星空 转载 IGN",
                "url": "https://www.gamersky.com/news/202603/2101776.shtml"
            },
            {
                "text": "Metacritic 用户长评出现「<b>Leon feels about as engaging as a protagonist as rotten cheese</b>」之类差评，吐槽 50% 后剧情放弃 Grace 这条更有趣的线。",
                "src": "Metacritic 用户评测",
                "url": "https://www.metacritic.com/game/resident-evil-requiem"
            },
            {
                "text": "游民百相多位玩家提到<b>缺少佣兵模式</b>，通关后除了多周目收集没什么刷的动力；首发还遇到偶发闪退与 Steam 版小型优化问题，等着补丁。",
                "src": "游民百相 玩家评测",
                "url": "https://club.gamersky.com/m/activity/1539358?club=1468"
            },
            {
                "text": "Steam 社区一篇日文长评归纳三条结构性差评：<b>「Leon 一枪爆头 vs Grace 一弹匣还杀不死同种怪」物理逻辑割裂、射击手感不及《最后生还者》、丧尸断头后变异让斩首失去价值</b>。",
                "src": "Metacritic 日语用户评测",
                "url": "https://www.metacritic.com/game/resident-evil-requiem"
            }
        ],
        "churn": [
            {
                "text": "Steam 综合讨论区围绕 Denuvo + Capcom DRM + Enigma 吵翻天，差评里反复出现「<b>5 次硬件授权上限 + Enigma 限制 mod</b>」两条，让 PC mod 玩家直接退款。",
                "src": "Steam 综合讨论",
                "url": "https://steamcommunity.com/app/3764200/discussions/0/762934064830303899/"
            },
            {
                "text": "Steam 商店页热门差评点名<b>「豪华包 78 元卖五套外观、滤镜与 1998 年来信」</b>，认为 30 周年纪念作把情怀彩蛋切片付费，吃相难看。",
                "src": "Steam 商店页 Resident Evil Requiem",
                "url": "https://store.steampowered.com/app/3764200/Resident_Evil_Requiem/"
            },
            {
                "text": "Steam 配置门槛讨论中，老硬件用户反映<b>GTX 1660 / RX 5500 XT 推荐档需开启 DLSS/FSR 才能稳 1080p 60</b>，加上 SSD 强制要求，劝退一批仍在用机械硬盘的核心粉。",
                "src": "Steam 商店页 系统需求",
                "url": "https://store.steampowered.com/app/3764200/Resident_Evil_Requiem/"
            }
        ]
    },
    "biliVideos": []
}

d['playerExp'] = playerExp

with open(fp, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print('OK: playerExp written')
print('media.memory[0].src:', playerExp['media']['memory'][0]['src'])
print('media.excitement[0].src:', playerExp['media']['excitement'][0]['src'])
print('media.pain[0].src:', playerExp['media']['pain'][0]['src'])
print('media.churn[0].src:', playerExp['media']['churn'][0]['src'])
print('community.memory[0].src:', playerExp['community']['memory'][0]['src'])
print('community.excitement[0].src:', playerExp['community']['excitement'][0]['src'])
print('community.pain[0].src:', playerExp['community']['pain'][0]['src'])
print('community.churn[0].src:', playerExp['community']['churn'][0]['src'])
