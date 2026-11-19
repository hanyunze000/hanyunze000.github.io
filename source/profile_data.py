"""Public academic profile. Each (English, Japanese) pair follows this order."""

NAME = "Yunze Han"
NAME_JA = "韓 運澤"
MASKED_EMAIL = "hanyunze19981203*outlook.com"
RESEARCHMAP = "https://researchmap.jp/yunzehan"


def presentation_heading(meetings):
    count = len(meetings)
    return f"Presentations of this paper ({count})", f"この論文の報告先（{count}件）"


PUBLICATIONS = [
    {
        "id": "taobao-villages",
        "title": "Does Rural E-Commerce Reduce Street Crime? Evidence From Taobao Villages in China",
        "authors": [NAME, "Qing Sun", "Kei Kajisa"],
        "corresponding": "Qing Sun",
        "journal": "Bulletin of Economic Research",
        "year": "2026",
        "doi": "10.1111/boer.70090",
        "summary": (
            "Using data from 2,872 counties in China, we find that property-related street and neighborhood crime fell in counties where Taobao Villages emerged.",
            ("中国の2,872県のデータを分析したところ、", "淘宝村が形成された県では、",
             "路上や住宅地での", "財産犯罪が減少しました。"),
        ),
    },
    {
        "id": "medical-care",
        "title": "Beyond medical care: public health insurance, caloric intake, and labor productivity in rural China",
        "authors": [NAME, "Kei Kajisa"],
        "corresponding": NAME,
        "journal": "Health Economics Review",
        "year": "2026",
        "doi": "10.1186/s13561-026-00833-w",
        "summary": (
            "In rural China, participants in the New Rural Cooperative Medical Scheme consumed more calories than nonparticipants. Higher caloric intake was also associated with higher earnings per working day the following year.",
            ("中国農村部では、", "新型農村合作医療制度の加入者は", "非加入者よりも摂取カロリーが高く、",
             "摂取カロリーが高い人ほど、", "翌年の就労日1日当たりの所得も", "高い傾向にありました。"),
        ),
        "meetings": [
            {
                "name": ("2025 Annual Conference of the Agricultural Economics Society of Japan", "2025年度日本農業経済学会大会"),
                "date": ("Mar 2025", "2025年3月"),
                "url": "https://researchmap.jp/yunzehan/presentations/55076457",
            },
            {
                "name": "Kyoto Development Economic Research (KDER) Student Workshop",
                "date": ("Feb 2025", "2025年2月"),
                "url": "https://www.econ.kyoto-u.ac.jp/en/about/seminars/42094/",
            },
        ],
    },
]

WORKING_PAPERS = [
    {
        "id": "collective-labor",
        "title": "Early-life exposure to Mao-era rural collective labor persistently reshapes how people invest in social capital",
        "authors": [NAME, "Kei Kajisa"],
        "meetings": [
            {
                "name": ("Japanese Economic Association 2026 Autumn Meeting", "日本経済学会2026年度秋季大会"),
                "date": ("Sep 2026", "2026年9月"),
                "url": "https://researchmap.jp/yunzehan/presentations/55076526",
            },
            {
                "name": ("1st Annual Conference of the Community Mechanism Research Association", "共同体メカニズム研究学会 第1回大会"),
                "date": ("Jun 2026", "2026年6月"),
                "note": ("Session chair", "座長兼任"),
                "url": "https://researchmap.jp/yunzehan/presentations/55076516",
            },
            {
                "name": "20th International Convention of the East Asian Economic Association",
                "date": ("Nov 2025", "2025年11月"),
                "earlier_title": "Mandatory Resettlement and Social Capital: The Lasting Effects of China’s Send-Down Movement",
                "url": "https://researchmap.jp/yunzehan/presentations/55076489",
            },
        ],
    },
    {
        "id": "irrigation-lotteries",
        "title": "The Hidden Social Costs of “Fair” Lotteries: Evidence from a Fifteen-Year Natural Experiment in a Sri Lankan Irrigation Project",
        "authors": [NAME, "Kei Kajisa"],
    },
    {
        "id": "motorway-expansion",
        "title": "The Unintended Consequences of Motorway Expansion for Street and Neighborhood Crime in China",
        "authors": [NAME, "Kei Kajisa"],
        "meetings": [
            {
                "name": "21st International Convention of the East Asian Economic Association",
                "date": ("Nov 2026", "2026年11月"),
                "url": "https://eaea21.pfm.gov.kh/293-program-and-speaker",
            },
        ],
    },
    {
        "id": "one-child-policy",
        "title": "Born Under the One-Child Policy: Fertility Restrictions and Gender Differences in Long-Run Health Behaviors and Health Status",
        "authors": [NAME, "Qing Sun"],
    },
    {
        "id": "parental-loss",
        "title": "Parental Loss in Adulthood and Personal Income in Rural China",
        "authors": [NAME, "Kei Kajisa"],
    },
    {
        "id": "land-titling",
        "title": "Land Titling and Property Crime: Evidence from Rural China",
        "authors": [NAME, "Qing Sun"],
    },
    {
        "id": "housing-wealth",
        "title": "More Spending or Different Choices? Housing Wealth Gains and Household Carbon Emissions in China",
        "authors": ["Qing Sun", NAME, "Shinichi Kitano"],
        "corresponding": NAME,
    },
]

JICA = (
    "JICA Ogata Sadako Research Institute for Peace and Development",
    "JICA緒方貞子平和開発研究所",
)
FIELDWORK = [
    {
        "country": ("Sri Lanka", "スリランカ"),
        "title": ("Walawe Left Bank Irrigation Upgrading and Extension Project", ("ワラウェ川左岸", "灌漑改修拡張事業")),
        "detail": (
            "I managed field data collection covering about 900 households, 300 agricultural markets, "
            "200 farmer organizations, and more than 100 irrigation canals. I also organized public goods, "
            "ultimatum, and trust games as part of the project evaluation.",
            ("約900世帯、", "約300の農産物市場、", "約200の農民組織、", "100本を超える用水路を対象に、",
             "現地でのデータ収集を取りまとめました。", "事業評価の一環として、", "公共財ゲーム、",
             "最後通牒ゲーム、", "信頼ゲームの実施も担当しました。"),
        ),
    },
    {
        "country": ("Uganda", "ウガンダ"),
        "title": ("Northern Uganda Farmers’ Livelihood Improvement Project", ("北部ウガンダ", "生計向上支援プロジェクト")),
        "detail": (
            "Working remotely, I analyzed baseline data and helped design the random assignment for the evaluation. "
            "I also supported the analysis of farm income, production, and other indicators of household livelihoods.",
            ("ベースライン調査のデータを遠隔で分析し、", "効果検証に用いる",
             "無作為割付の設計に参加しました。", "農家の所得や生産など、",
             "生計に関する指標の分析も支援しました。"),
        ),
    },
]

# Each CV row consists of a date, a qualification or role, and an institution.
# A date range with a note gives its start, end and note in each language.
def education_title(level, field):
    level_en, level_ja = level
    field_en, field_ja = field
    return f"{level_en} in {field_en}", f"{field_ja}専攻 {level_ja}"


NATURAL_RESOURCE_ECONOMICS = ("Natural Resource Economics", "生物資源経済学")
KYOTO_AGRICULTURE = (
    "Graduate School of Agriculture, Kyoto University",
    "京都大学大学院農学研究科",
)
EDUCATION = [
    ((("Oct 2024", "Sep 2027", "(expected)"), ("2024年10月", "2027年9月", "（予定）")),
     education_title(("Doctoral program", "博士後期課程"), NATURAL_RESOURCE_ECONOMICS),
     KYOTO_AGRICULTURE),
    (("Oct 2022 – Sep 2024", "2022年10月 – 2024年9月"),
     education_title(("Master’s degree", "修士課程"), NATURAL_RESOURCE_ECONOMICS),
     KYOTO_AGRICULTURE),
    (("Sep 2017 – Jun 2021", "2017年9月 – 2021年6月"),
     education_title(("Bachelor’s degree", "学士課程"), ("Financial Management", "財務管理")),
     ("Glorious Sun School of Business and Management, Donghua University", "東華大学 旭日工商管理学院")),
]
APPOINTMENTS = [
    (("Jan 2024 – present", "2024年1月 – 現在"),
     ("Part-time research assistant", "非常勤研究助手"), JICA),
    (("May – Sep 2024", "2024年5月 – 9月"),
     ("Teaching assistant", "ティーチング・アシスタント"), ("Kyoto University", "京都大学")),
    (("Oct 2023", "2023年10月"),
     ("New student orientation tutor", "新入生チューター"), ("Kyoto University", "京都大学")),
    (("Apr – Sep 2023", "2023年4月 – 9月"),
     ("Office assistant", "オフィス・アシスタント"), ("Kyoto University", "京都大学")),
]
AWARDS = [
    (("Oct 2024 – Sep 2027", "2024年10月 – 2027年9月"),
     ("DoGS Fellow (JST SPRING)", "大学院教育支援機構奨励研究員（JST SPRING）"),
     ("Division of Graduate Studies, Kyoto University", "京都大学大学院教育支援機構")),
    (("Nov 2022", "2022年11月"),
     ("MEXT Honors Scholarship for Privately Financed International Students", "文部科学省外国人留学生学習奨励費"),
     ("Japan Student Services Organization (JASSO)", "日本学生支援機構（JASSO）")),
    (("Jan 2021", "2021年1月"),
     ("Outstanding Thesis Award", "優秀論文賞"), ("Donghua University", "東華大学")),
]
MEMBERSHIPS = [
    ("2026", ("Japanese Association for Development Economics", "開発経済学会")),
    ("2026", ("Community Mechanism Research Association", "共同体メカニズム研究学会")),
    ("2026", ("Japanese Economic Association", "日本経済学会")),
    ("2025", ("East Asian Economic Association", "東アジア経済学会（EAEA）")),
    ("2025", ("Agricultural Economics Society of Japan", "日本農業経済学会")),
]
OTHER_EXPERIENCE = [
    (("Aug 2024 – present", "2024年8月 – 現在"),
     ("Contract photographer", "契約フォトグラファー"), ("Visual China Group (VCG)", "Visual China Group（VCG）")),
]
