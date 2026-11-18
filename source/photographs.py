"""Gallery rows in viewing order. Descriptions are for image alternatives only."""

from typing import NamedTuple


class Photograph(NamedTuple):
    source: str
    slug: str
    width: int
    height: int
    description: tuple[str, str]


ROWS = (
    (
        Photograph("2d7cee0771be54c528c2a350d3cdbc98.jpg", "temple-reflection", 11648, 8736,
                   ("Temple towers and palm trees reflected in water beneath a pink sky.",
                    "ピンク色の空を背に、寺院の塔とヤシの木が水面に映っている。")),
        Photograph("26653ba599fb2d7ba22da9bcaf7df04f.jpg", "stone-figure", 11115, 8336,
                   ("A carved stone figure beside a lake fringed with trees.",
                    "木々に囲まれた湖のほとりに立つ石像。")),
    ),
    (
        Photograph("c375b254ace33f3d07a8a95354299ba0.jpg", "tree-and-stone", 8736, 11648,
                   ("A tall tree rises above dark stone ruins.", "石造りの遺跡を越えて伸びる高い木。")),
        Photograph("ce5f6b7023059a5796fe037a2d412864.jpg", "carved-doorways", 11253, 8440,
                   ("Carved stone doorways around a sunlit temple courtyard.",
                    "光の差す境内を囲む、彫刻を施した石の門。")),
        Photograph("d6cd00b65bd23101bcb8f11870e2a76e.jpg", "tree-lined-water", 8736, 11648,
                   ("Clouds reflected between two wooded banks.", "両岸の木々の間で水面に雲が映っている。")),
    ),
    (
        Photograph("c1e43f4e0efb253caa6f19099e25beb4.jpg", "waterway", 11648, 8736,
                   ("A view from a boat passing houses along a waterway.", "水路に並ぶ家々を船から望む。")),
        Photograph("3123cc4a59030631e56104bf0d305157.jpg", "buffalo-in-water", 2560, 1706,
                   ("A water buffalo stands in still water beside a wooded bank.",
                    "木々の茂る岸辺の静かな水に立つ水牛。")),
    ),
    (
        Photograph("_DSF3401.jpg", "blossom-grove", 11648, 8736,
                   ("Pink blossom hangs over a grove scattered with fallen petals.",
                    "地面に花びらが散り、木立には淡いピンクの花が広がっている。")),
        Photograph("_DSF2869.jpg", "snow-and-parasol", 6528, 8704,
                   ("A red parasol among vermilion gates in the snow.", "雪に包まれた朱色の鳥居と赤い傘。")),
        Photograph("_DSF3558.jpg", "bird-in-blossom", 1433, 1781,
                   ("A small green bird among pink blossoms.", "ピンクの花の間にとまる緑色の小鳥。")),
    ),
    (
        Photograph("2023-12-28 173843.jpg", "shrine-interior", 11425, 8469,
                   ("Two tassels in the shadows behind the frame of a wooden shrine.",
                    "木造の社の奥に下がる二つの房。")),
        Photograph("_DSF5020.jpg", "festival-procession", 6897, 10003,
                   ("People in white walk alongside a tall festival float on a city street.",
                    "街路を進む背の高い山鉾と、白い衣装をまとった人々。")),
        Photograph("_DSF6334.jpg", "rooftops-at-dusk", 11648, 8736,
                   ("Warm evening light over city rooftops and distant mountain ridges.",
                    "街の屋根を照らす夕日と遠くの山並み。")),
    ),
    (
        Photograph("5fa60b17fdc47a4788d14c788e7d5c39.jpg", "mountain-basin", 2560, 1706,
                   ("A rocky mountain basin seen from a high ridge beneath a clear sky.",
                    "晴れた空の下、高い尾根から岩の多い谷を見下ろす。")),
        Photograph("770c8db2ac9e62e5b42660fb833b8f3b.jpg", "autumn-ridge", 2560, 1920,
                   ("A mountain ridge above a valley of red and green foliage.",
                    "赤や緑に色づく谷を囲む山の稜線。")),
    ),
    (
        Photograph("_DSF4314.jpg", "islands-in-haze", 8099, 2815,
                   ("Low islands in a wide expanse of pale water and distant haze.",
                    "淡い色の水面の向こうに、霞んだ島影が連なっている。")),
        Photograph("_DSF5593.jpg", "moon-over-water", 2761, 3681,
                   ("A golden moon above dark hills, with a reflection on the water.",
                    "暗い山並みの上に浮かぶ金色の月が水面に映っている。")),
    ),
    (
        Photograph("_DSF7152.jpg", "sheltered-bay", 11530, 8648,
                   ("A boat and floating platforms in a blue bay between wooded hills.",
                    "緑の丘に囲まれた青い湾に浮かぶ船といかだ。")),
        Photograph("_DSF7123.jpg", "gull-over-water", 11648, 8736,
                   ("A gull in flight above sunlit blue water.", "光のきらめく青い水面の上を飛ぶカモメ。")),
        Photograph("c103c85da1ca29d49430ff1cf761ec22.jpg", "rock-offshore", 2560, 1706,
                   ("Waves break on a sandy beach in front of a rocky islet.",
                    "岩の小島の手前で、砂浜に寄せる波。")),
    ),
)
