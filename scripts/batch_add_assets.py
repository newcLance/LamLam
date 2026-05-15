"""
批量为21款游戏写入 assets 数据
用法: python scripts/batch_add_assets.py
"""
import json, os, urllib.parse

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def xhs(keyword):
    return f"https://www.xiaohongshu.com/search_result?keyword={urllib.parse.quote(keyword)}"

def artstation_search(query):
    return f"https://www.artstation.com/search?sort_by=relevance&query={urllib.parse.quote(query)}"

def pinterest_search(query):
    return f"https://www.pinterest.com/search/pins/?q={urllib.parse.quote(query)}"

def behance_search(query):
    return f"https://www.behance.net/search/projects?search={urllib.parse.quote(query)}"

def dribbble_search(query):
    return f"https://dribbble.com/search/{urllib.parse.quote(query).replace('%20', '-')}"

def steam_store(appid):
    return f"https://store.steampowered.com/app/{appid}/"

def steam_bg(appid):
    return f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/page_bg_raw.jpg"

def igdb(slug):
    return f"https://www.igdb.com/games/{slug}"

def ps_store(concept_id):
    return f"https://store.playstation.com/en-us/concept/{concept_id}"

# ===== GAME DEFINITIONS =====
GAMES = [
    {
        "slug": "balatro",
        "nameCN": "小丑牌",
        "nameEN": "Balatro",
        "steam": 2379780,
        "twitter": "BalatroGame",
        "ps_concept": "10010334",
        "igdb_slug": "balatro",
        "artstation_artists": [],
        "extra_official": [],
    },
    {
        "slug": "vampire-survivors",
        "nameCN": "吸血鬼幸存者",
        "nameEN": "Vampire Survivors",
        "steam": 1794680,
        "twitter": "poncle_vampire",
        "ps_concept": "10004514",
        "igdb_slug": "vampire-survivors",
    },
    {
        "slug": "cult-of-the-lamb",
        "nameCN": "咩咩启示录",
        "nameEN": "Cult of the Lamb",
        "steam": 1313140,
        "twitter": "cultofthelamb",
        "ps_concept": "10004792",
        "igdb_slug": "cult-of-the-lamb",
    },
    {
        "slug": "pizza-tower",
        "nameCN": "披萨塔",
        "nameEN": "Pizza Tower",
        "steam": 2231450,
        "twitter": "PizzaTowergame",
        "ps_concept": None,
        "igdb_slug": "pizza-tower",
    },
    {
        "slug": "dredge",
        "nameCN": "疏浚",
        "nameEN": "DREDGE",
        "steam": 1562430,
        "twitter": "BSG_DREDGE",
        "ps_concept": "10006591",
        "igdb_slug": "dredge",
    },
    {
        "slug": "lethal-company",
        "nameCN": "致命公司",
        "nameEN": "Lethal Company",
        "steam": 1966720,
        "twitter": "ZeekerssRBLX",
        "ps_concept": None,
        "igdb_slug": "lethal-company",
    },
    {
        "slug": "satisfactory",
        "nameCN": "幸福工厂",
        "nameEN": "Satisfactory",
        "steam": 526870,
        "twitter": "SatisfactoryAF",
        "ps_concept": None,
        "igdb_slug": "satisfactory",
        "extra_official": [
            {"title": "Epic Games Store 商店页", "source": "Epic", "url": "https://store.epicgames.com/p/satisfactory"},
            {"title": "官方网站", "source": "官网", "url": "https://www.satisfactorygame.com"},
        ],
    },
    {
        "slug": "teardown",
        "nameCN": "拆迁",
        "nameEN": "Teardown",
        "steam": 1167630,
        "twitter": "teardowngame",
        "ps_concept": "10008489",
        "igdb_slug": "teardown",
        "extra_official": [
            {"title": "官方网站", "source": "官网", "url": "https://www.teardowngame.com"},
        ],
    },
    {
        "slug": "dyson-sphere-program",
        "nameCN": "戴森球计划",
        "nameEN": "Dyson Sphere Program",
        "steam": 1366540,
        "twitter": "DysonProgram",
        "ps_concept": None,
        "igdb_slug": "dyson-sphere-program",
    },
    {
        "slug": "the-planet-crafter",
        "nameCN": "星球工匠",
        "nameEN": "The Planet Crafter",
        "steam": 1284190,
        "twitter": "MijuGames",
        "ps_concept": "10010963",
        "igdb_slug": "the-planet-crafter",
    },
    {
        "slug": "disco-elysium",
        "nameCN": "极乐迪斯科",
        "nameEN": "Disco Elysium",
        "steam": 632470,
        "twitter": "studioZAUM",
        "ps_concept": "10002292",
        "igdb_slug": "disco-elysium--the-final-cut",
        "extra_official": [
            {"title": "官方网站（存档）", "source": "官网", "url": "https://discoelysium.com"},
        ],
    },
    {
        "slug": "eggy-party",
        "nameCN": "蛋仔派对",
        "nameEN": "Eggy Party",
        "steam": None,
        "twitter": "EggyPartyEN",
        "ps_concept": None,
        "igdb_slug": "eggy-party",
        "extra_official": [
            {"title": "官方网站", "source": "官网", "url": "https://egg.163.com"},
            {"title": "TapTap 游戏页", "source": "TapTap", "url": "https://www.taptap.cn/app/218069"},
        ],
    },
    {
        "slug": "fall-guys",
        "nameCN": "糖豆人",
        "nameEN": "Fall Guys",
        "steam": None,
        "twitter": "FallGuysGame",
        "ps_concept": "10003539",
        "igdb_slug": "fall-guys-ultimate-knockout",
        "extra_official": [
            {"title": "Epic Games Store 商店页（免费游戏）", "source": "Epic", "url": "https://store.epicgames.com/p/fall-guys"},
            {"title": "官方网站", "source": "官网", "url": "https://www.fallguys.com"},
        ],
    },
    {
        "slug": "genshin-impact",
        "nameCN": "原神",
        "nameEN": "Genshin Impact",
        "steam": None,
        "twitter": "GenshinImpact",
        "ps_concept": "10001137",
        "igdb_slug": "genshin-impact",
        "extra_official": [
            {"title": "官方网站", "source": "官网", "url": "https://genshin.hoyoverse.com"},
            {"title": "Epic Games Store 商店页", "source": "Epic", "url": "https://store.epicgames.com/p/genshin-impact"},
        ],
    },
    {
        "slug": "honkai-star-rail",
        "nameCN": "崩坏：星穹铁道",
        "nameEN": "Honkai: Star Rail",
        "steam": None,
        "twitter": "honaboreal",
        "ps_concept": "10007852",
        "igdb_slug": "honkai-star-rail",
        "extra_official": [
            {"title": "官方网站", "source": "官网", "url": "https://hsr.hoyoverse.com"},
            {"title": "Epic Games Store 商店页", "source": "Epic", "url": "https://store.epicgames.com/p/honkai-star-rail"},
        ],
    },
    {
        "slug": "zenless-zone-zero",
        "nameCN": "绝区零",
        "nameEN": "Zenless Zone Zero",
        "steam": 4162040,
        "twitter": "ZZZ_EN",
        "ps_concept": "10008540",
        "igdb_slug": "zenless-zone-zero",
        "extra_official": [
            {"title": "官方网站", "source": "官网", "url": "https://zenless.hoyoverse.com"},
        ],
    },
    {
        "slug": "neverness-to-everness",
        "nameCN": "异环",
        "nameEN": "Neverness to Everness",
        "steam": None,
        "twitter": "N2E_EN",
        "ps_concept": None,
        "igdb_slug": "neverness-to-everness",
        "extra_official": [
            {"title": "官方网站", "source": "官网", "url": "https://n2e.hotta.com"},
            {"title": "Epic Games Store 商店页", "source": "Epic", "url": "https://store.epicgames.com/p/neverness-to-everness"},
        ],
    },
    {
        "slug": "ananta",
        "nameCN": "无限大",
        "nameEN": "Ananta",
        "steam": None,
        "twitter": "Ananta_EN",
        "ps_concept": None,
        "igdb_slug": "ananta",
        "extra_official": [
            {"title": "官方网站", "source": "官网", "url": "https://ananta.gryphline.com"},
        ],
    },
    {
        "slug": "crossfire-hong",
        "nameCN": "穿越火线：虹",
        "nameEN": "CrossFire: Hong",
        "steam": None,
        "twitter": None,
        "ps_concept": None,
        "igdb_slug": None,
        "extra_official": [
            {"title": "官方网站", "source": "官网", "url": "https://cfhong.qq.com"},
        ],
    },
    {
        "slug": "out-of-control",
        "nameCN": "失控进化",
        "nameEN": "Out of Control",
        "steam": None,
        "twitter": None,
        "ps_concept": None,
        "igdb_slug": None,
        "extra_official": [
            {"title": "官方网站", "source": "官网", "url": "https://skjh.qq.com"},
        ],
    },
    {
        "slug": "rainbow-six-siege-x",
        "nameCN": "彩虹六号：围攻X",
        "nameEN": "Rainbow Six Siege X",
        "steam": None,
        "twitter": "Rainbow6Game",
        "ps_concept": "10000498",
        "igdb_slug": "tom-clancys-rainbow-six-siege",
        "extra_official": [
            {"title": "Ubisoft Store 商店页", "source": "Ubisoft", "url": "https://store.ubisoft.com/rainbow-six-siege"},
            {"title": "Steam 商店页 (Rainbow Six Siege)", "source": "Steam", "url": "https://store.steampowered.com/app/359550/"},
            {"title": "官方网站", "source": "官网", "url": "https://www.ubisoft.com/game/rainbow-six/siege"},
        ],
    },
]


def build_assets(g):
    slug = g["slug"]
    nameCN = g["nameCN"]
    nameEN = g["nameEN"]
    steam = g.get("steam")
    twitter = g.get("twitter")
    ps_concept = g.get("ps_concept")
    igdb_slug = g.get("igdb_slug")
    extra_official = g.get("extra_official", [])

    # === OFFICIAL: 商店页 + 官网 ===
    store_links = []
    if steam:
        store_links.append({
            "title": f"Steam 商店页 — 截图 + Header + 背景",
            "source": "Steam",
            "url": steam_store(steam)
        })

    if ps_concept:
        store_links.append({
            "title": "PlayStation Store 商店页",
            "source": "PlayStation",
            "url": ps_store(ps_concept)
        })

    if igdb_slug:
        store_links.append({
            "title": "IGDB 游戏页 — 评分 + 媒体素材",
            "source": "IGDB",
            "url": igdb(igdb_slug)
        })

    for ex in extra_official:
        store_links.append(ex)

    if steam:
        store_links.append({
            "title": "Steam 背景图直链",
            "source": "Steam",
            "url": steam_bg(steam)
        })

    # === OFFICIAL: 角色建模 / 概念设定图 ===
    concept_links = []

    concept_links.append({
        "title": f"小红书搜索「{nameCN} 概念设定」",
        "source": "小红书",
        "url": xhs(f"{nameCN} 概念设定")
    })

    if twitter:
        concept_links.append({
            "title": f"X/Twitter 官方账号 @{twitter}",
            "source": "X/Twitter",
            "url": f"https://x.com/{twitter}"
        })

    # === INSPIRATION: 概念美术 ===
    concept_art_links = [
        {
            "title": f"ArtStation 搜索「{nameEN} concept art」",
            "source": "ArtStation",
            "url": artstation_search(f"{nameEN} concept art")
        },
        {
            "title": f"Pinterest 搜索「{nameEN} concept art」",
            "source": "Pinterest",
            "url": pinterest_search(f"{nameEN} concept art")
        },
    ]

    # === INSPIRATION: 角色设计 ===
    char_links = [
        {
            "title": f"ArtStation 搜索「{nameEN} character」",
            "source": "ArtStation",
            "url": artstation_search(f"{nameEN} character")
        },
        {
            "title": f"Pinterest 搜索「{nameEN} character design」",
            "source": "Pinterest",
            "url": pinterest_search(f"{nameEN} character design")
        },
        {
            "title": f"Behance 搜索「{nameEN}」",
            "source": "Behance",
            "url": behance_search(nameEN)
        },
    ]

    # === INSPIRATION: UI / 纹理材质 ===
    ui_links = [
        {
            "title": f"Dribbble 搜索「{nameEN} UI」",
            "source": "Dribbble",
            "url": dribbble_search(f"{nameEN} UI")
        },
        {
            "title": f"ArtStation 搜索「{nameEN} texture material」",
            "source": "ArtStation",
            "url": artstation_search(f"{nameEN} texture material")
        },
        {
            "title": f"Pinterest 搜索「{nameEN} texture」",
            "source": "Pinterest",
            "url": pinterest_search(f"{nameEN} texture")
        },
    ]

    assets = {
        "official": [
            {"cat": "商店页 + 官网", "links": store_links},
            {"cat": "角色建模 / 概念设定图", "links": concept_links},
        ],
        "inspiration": [
            {"cat": "概念美术 / Concept Art", "links": concept_art_links},
            {"cat": "角色设计", "links": char_links},
            {"cat": "UI 界面 / 纹理材质", "links": ui_links},
        ]
    }

    return assets


def count_links(assets):
    total = 0
    for section in ["official", "inspiration"]:
        for group in assets.get(section, []):
            total += len(group.get("links", []))
    return total


def main():
    results = []
    for g in GAMES:
        slug = g["slug"]
        path = f"data/games/{slug}.json"
        if not os.path.exists(path):
            print(f"[SKIP] {slug}: 文件不存在")
            continue

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "assets" in data:
            print(f"[SKIP] {slug}: 已有 assets")
            continue

        assets = build_assets(g)
        data["assets"] = assets

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        n = count_links(assets)
        print(f"[OK]   {slug}: 写入 {n} 条链接")
        results.append((slug, n))

    print(f"\n{'='*50}")
    print(f"  完成: {len(results)} 款游戏已写入 assets")
    total_links = sum(n for _, n in results)
    print(f"  总链接数: {total_links}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
