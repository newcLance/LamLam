import json

with open('data/games.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

tier1 = [
    {
        "id": 201, "name": "Baldur's Gate 3", "nameCN": "博德之门3",
        "alias": "BG3,博德之门", "company": "Larian Studios",
        "category": "已发售", "region": "欧美", "platforms": ["PC", "PS5", "Xbox"],
        "model": "买断制", "genre": "RPG", "scale": "—", "mau": "—", "games": "—",
        "established": "2023", "releaseDate": "2023.8.3",
        "desc": "Larian Studios 开发的 RPG 标杆，基于龙与地下城第五版规则。",
        "features": ["回合制战斗", "多人合作", "选择驱动叙事", "D&D 5e", "魔法系统"],
        "changes": [], "lastUpdate": "2026-04-23", "slug": "baldurs-gate-3"
    },
    {
        "id": 202, "name": "God of War", "nameCN": "战神",
        "alias": "GOW,战神2018", "company": "Santa Monica Studio",
        "category": "已发售", "region": "欧美", "platforms": ["PC", "PS4", "PS5"],
        "model": "买断制", "genre": "Action", "scale": "—", "mau": "—", "games": "—",
        "established": "2018", "releaseDate": "2022.1.14",
        "desc": "圣莫妮卡工作室北欧神话题材动作冒险，PS 旗舰级大作 PC 移植。",
        "features": ["一镜到底", "北欧神话", "父子叙事", "利维坦之斧", "开放探索"],
        "changes": [], "lastUpdate": "2026-04-23", "slug": "god-of-war"
    },
    {
        "id": 203, "name": "Ghost of Tsushima DIRECTOR'S CUT", "nameCN": "对马岛之魂：导演剪辑版",
        "alias": "对马岛,GOT", "company": "Sucker Punch Productions",
        "category": "已发售", "region": "欧美", "platforms": ["PC", "PS4", "PS5"],
        "model": "买断制", "genre": "Action-Adventure", "scale": "—", "mau": "—", "games": "—",
        "established": "2020", "releaseDate": "2024.5.16",
        "desc": "蒙古入侵时期的封建日本开放世界武士动作冒险，东方美学标杆。",
        "features": ["开放世界", "武士战斗", "和风美学", "风引导系统", "壹岐岛 DLC"],
        "changes": [], "lastUpdate": "2026-04-23", "slug": "ghost-of-tsushima"
    },
    {
        "id": 204, "name": "SILENT HILL 2", "nameCN": "寂静岭2",
        "alias": "SH2,寂静岭2重制版", "company": "Bloober Team / Konami",
        "category": "已发售", "region": "欧美", "platforms": ["PC", "PS5"],
        "model": "买断制", "genre": "Action", "scale": "—", "mau": "—", "games": "—",
        "established": "2024", "releaseDate": "2024.10.8",
        "desc": "经典心理恐怖游戏虚幻引擎5全面重制，Bloober Team 开发。",
        "features": ["心理恐怖", "UE5 重制", "雾镇探索", "多结局", "战斗系统重做"],
        "changes": [], "lastUpdate": "2026-04-23", "slug": "silent-hill-2"
    },
    {
        "id": 205, "name": "Hollow Knight: Silksong", "nameCN": "空洞骑士：丝之歌",
        "alias": "丝之歌,Silksong", "company": "Team Cherry",
        "category": "已发售", "region": "欧美", "platforms": ["PC", "Switch", "PS5", "Xbox"],
        "model": "买断制", "genre": "Action", "scale": "—", "mau": "—", "games": "—",
        "established": "2025", "releaseDate": "2025.6.12",
        "desc": "Team Cherry 独立游戏美术标杆，空洞骑士续作，类银河恶魔城。",
        "features": ["类银河恶魔城", "手绘美术", "丝绸骑士大黄蜂", "150+敌人", "全新世界"],
        "changes": [], "lastUpdate": "2026-04-23", "slug": "hollow-knight-silksong"
    },
    {
        "id": 206, "name": "Hades II", "nameCN": "哈迪斯2",
        "alias": "Hades2,黑帝斯2", "company": "Supergiant Games",
        "category": "已发售", "region": "欧美", "platforms": ["PC", "PS5", "Xbox"],
        "model": "买断制", "genre": "Action RPG", "scale": "—", "mau": "—", "games": "—",
        "established": "2025", "releaseDate": "2025.9.18",
        "desc": "Supergiant Games roguelike 续作，希腊神话题材，美学天花板。",
        "features": ["Roguelike", "希腊神话", "巫术系统", "双世界探索", "Supergiant 美术"],
        "changes": [], "lastUpdate": "2026-04-23", "slug": "hades-2"
    },
    {
        "id": 207, "name": "Persona 5 Royal", "nameCN": "女神异闻录5：皇家版",
        "alias": "P5R,女神异闻录5", "company": "Atlus / SEGA",
        "category": "已发售", "region": "日韩", "platforms": ["PC", "PS5", "Xbox", "Switch"],
        "model": "买断制", "genre": "RPG", "scale": "—", "mau": "—", "games": "—",
        "established": "2019", "releaseDate": "2022.10.21",
        "desc": "Atlus JRPG 巅峰之作，UI 设计教科书级别，全平台移植版。",
        "features": ["回合制 JRPG", "UI 设计标杆", "怪盗团", "社群系统", "认知殿堂"],
        "changes": [], "lastUpdate": "2026-04-23", "slug": "persona-5-royal"
    },
    {
        "id": 208, "name": "Hi-Fi RUSH", "nameCN": "完美音浪",
        "alias": "HiFi Rush,Hi-Fi Rush", "company": "Tango Gameworks / Krafton",
        "category": "已发售", "region": "日韩", "platforms": ["PC", "PS5", "Xbox"],
        "model": "买断制", "genre": "Action", "scale": "—", "mau": "—", "games": "—",
        "established": "2023", "releaseDate": "2023.1.25",
        "desc": "Tango Gameworks 节奏动作游戏，全球随音乐节拍律动的独特视觉。",
        "features": ["节奏动作", "卡通渲染", "音乐节拍战斗", "摇滚主题", "动态场景"],
        "changes": [], "lastUpdate": "2026-04-23", "slug": "hi-fi-rush"
    },
    {
        "id": 209, "name": "Kingdom Come: Deliverance II", "nameCN": "天国：拯救2",
        "alias": "KCD2,天国拯救2", "company": "Warhorse Studios / Deep Silver",
        "category": "已发售", "region": "欧美", "platforms": ["PC", "PS5", "Xbox"],
        "model": "买断制", "genre": "RPG", "scale": "—", "mau": "—", "games": "—",
        "established": "2025", "releaseDate": "2025.2.4",
        "desc": "写实中世纪开放世界 RPG 续作，以历史真实性著称。",
        "features": ["写实中世纪", "开放世界", "第一人称", "剑术系统", "历史考据"],
        "changes": [], "lastUpdate": "2026-04-23", "slug": "kingdom-come-deliverance-2"
    },
    {
        "id": 210, "name": "Stray", "nameCN": "迷失",
        "alias": "流浪猫", "company": "BlueTwelve Studio / Annapurna",
        "category": "已发售", "region": "欧美", "platforms": ["PC", "PS4", "PS5", "Switch"],
        "model": "买断制", "genre": "Adventure", "scale": "—", "mau": "—", "games": "—",
        "established": "2022", "releaseDate": "2022.7.19",
        "desc": "赛博朋克猫咪冒险，独特的猫视角叙事与霓虹废墟美学。",
        "features": ["猫咪视角", "赛博朋克", "霓虹废墟", "叙事冒险", "Annapurna 发行"],
        "changes": [], "lastUpdate": "2026-04-23", "slug": "stray"
    },
]

# Check for duplicates
existing_slugs = {g['slug'] for g in games}
added = 0
for g in tier1:
    if g['slug'] not in existing_slugs:
        games.append(g)
        added += 1
        print(f"  Added: {g['name']} ({g['slug']})")
    else:
        print(f"  Skip (exists): {g['name']}")

with open('data/games.json', 'w', encoding='utf-8') as f:
    json.dump(games, f, ensure_ascii=False, indent=2)

print(f"\nDone. Added {added} games. Total: {len(games)}")
