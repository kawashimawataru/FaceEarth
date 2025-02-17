import random

def get_random_questions():
    """
    各質問リストから1つずつランダムに取得し、辞書として返す。
    """
    return {
        "question_yesno": random.choice(question_yesno) if question_yesno else None,
        "question_choice": random.choice(question_choice) if question_choice else None,
        "question_choice2": random.choice(question_choice2) if question_choice2 else None,
        "questions_image": random.choice(questions_image) if questions_image else None
    }


question_yesno = [
  {
    "question_id": "Q1-1",
    "question_text": "暖かい場所と寒い場所、どちらが好き？",
    "type": "Yes/No",
    "options": ["暖かい", "寒い"],
    "scoring": {
      "暖かい": { "warm": 2, "tropical": 2 },
      "寒い": { "cold": 2, "mountainous": 1 }
    }
  },
  {
    "question_id": "Q1-2",
    "question_text": "海辺と湖畔、どちらが魅力的？",
    "type": "Yes/No",
    "options": ["海辺", "湖畔"],
    "scoring": {
      "海辺": { "coastal": 2, "warm": 1 },
      "湖畔": { "lakeside": 2, "scenic": 1 }
    }
  },
  {
    "question_id": "Q1-3",
    "question_text": "大都市と小さな村、どちらが落ち着く？",
    "type": "Yes/No",
    "options": ["大都市", "小さな村"],
    "scoring": {
      "大都市": { "urban": 3, "modern": 1 },
      "小さな村": { "rural": 3, "nature": 1 }
    }
  },
  {
    "question_id": "Q1-4",
    "question_text": "日差しが強い地域と日差しが弱い地域、どちらが好み？",
    "type": "Yes/No",
    "options": ["強い", "弱い"],
    "scoring": {
      "強い": { "warm": 2, "tropical": 1 },
      "弱い": { "cold": 2, "cloudy": 1 }
    }
  },
  {
    "question_id": "Q1-5",
    "question_text": "海のそばと山の近く、どちらで暮らしてみたい？",
    "type": "Yes/No",
    "options": ["海のそば", "山の近く"],
    "scoring": {
      "海のそば": { "coastal": 2, "humid": 1 },
      "山の近く": { "mountainous": 2, "cold": 1 }
    }
  },
  {
    "question_id": "Q1-6",
    "question_text": "乾燥した地域と湿度の高い地域、どちらが過ごしやすい？",
    "type": "Yes/No",
    "options": ["乾燥", "湿度高め"],
    "scoring": {
      "乾燥": { "desert": 2, "arid": 1 },
      "湿度高め": { "tropical": 2, "humid": 1 }
    }
  },
  {
    "question_id": "Q1-7",
    "question_text": "歴史を感じる街と近代的な街、どちらが落ち着く？",
    "type": "Yes/No",
    "options": ["歴史的", "近代的"],
    "scoring": {
      "歴史的": { "historical": 2, "cultural": 1 },
      "近代的": { "modern": 2, "urban": 1 }
    }
  },
  {
    "question_id": "Q1-8",
    "question_text": "週末はアクティビティ満載と静かなリゾート、どちらが理想？",
    "type": "Yes/No",
    "options": ["アクティビティ", "静かなリゾート"],
    "scoring": {
      "アクティビティ": { "adventurous": 2, "urban": 1 },
      "静かなリゾート": { "relaxing": 2, "coastal": 1 }
    }
  },
  {
    "question_id": "Q1-9",
    "question_text": "山の上と谷底、どちらの風景が好き？",
    "type": "Yes/No",
    "options": ["山の上", "谷底"],
    "scoring": {
      "山の上": { "mountainous": 2, "cold": 1 },
      "谷底": { "valley": 2, "river": 1 }
    }
  },
  {
    "question_id": "Q1-10",
    "question_text": "周囲に人が多い場所と人が少ない場所、どちらが落ち着く？",
    "type": "Yes/No",
    "options": ["人が多い", "人が少ない"],
    "scoring": {
      "人が多い": { "urban": 2, "modern": 1 },
      "人が少ない": { "rural": 2, "nature": 1 }
    }
  },
  {
    "question_id": "Q1-11",
    "question_text": "海風を感じたい派？それとも山の空気が好き？",
    "type": "Yes/No",
    "options": ["海風", "山の空気"],
    "scoring": {
      "海風": { "coastal": 2, "warm": 1 },
      "山の空気": { "mountainous": 2, "fresh": 1 }
    }
  },
  {
    "question_id": "Q1-12",
    "question_text": "夏でも肌寒い場所と冬でも暖かい場所、どちらが魅力的？",
    "type": "Yes/No",
    "options": ["肌寒い夏", "暖かい冬"],
    "scoring": {
      "肌寒い夏": { "cold": 2, "high_altitude": 1 },
      "暖かい冬": { "warm": 2, "temperate": 1 }
    }
  },
  {
    "question_id": "Q1-13",
    "question_text": "降雪が多い地域と雪が滅多に降らない地域、どちらを選ぶ？",
    "type": "Yes/No",
    "options": ["雪が多い", "雪が少ない"],
    "scoring": {
      "雪が多い": { "snowy": 3, "cold": 1 },
      "雪が少ない": { "warm": 2, "temperate": 1 }
    }
  },
  {
    "question_id": "Q1-14",
    "question_text": "アクセスの良い都会と秘境のような田舎、どちらがワクワクする？",
    "type": "Yes/No",
    "options": ["都会", "秘境"],
    "scoring": {
      "都会": { "urban": 3, "modern": 1 },
      "秘境": { "rural": 2, "adventurous": 2 }
    }
  },
  {
    "question_id": "Q1-15",
    "question_text": "観光客が多い場所と少ない場所、どちらに惹かれる？",
    "type": "Yes/No",
    "options": ["多い", "少ない"],
    "scoring": {
      "多い": { "touristic": 2, "urban": 1 },
      "少ない": { "remote": 2, "quiet": 1 }
    }
  },
  {
    "question_id": "Q1-16",
    "question_text": "四季がはっきりしている地域と一年中気温が安定している地域、どちらが好き？",
    "type": "Yes/No",
    "options": ["四季がはっきり", "一年中安定"],
    "scoring": {
      "四季がはっきり": { "temperate": 2, "seasonal": 1 },
      "一年中安定": { "tropical": 2, "mild": 1 }
    }
  },
  {
    "question_id": "Q1-17",
    "question_text": "湿度が低い方が好き？それとも適度な湿気がある方がいい？",
    "type": "Yes/No",
    "options": ["湿度低め", "湿度あり"],
    "scoring": {
      "湿度低め": { "dry": 2, "desert": 1 },
      "湿度あり": { "humid": 2, "tropical": 1 }
    }
  },
  {
    "question_id": "Q1-18",
    "question_text": "伝統文化が根強い土地と新しい文化が盛んな土地、どちらを優先する？",
    "type": "Yes/No",
    "options": ["伝統文化", "新しい文化"],
    "scoring": {
      "伝統文化": { "cultural": 3, "historical": 1 },
      "新しい文化": { "modern": 3, "innovative": 1 }
    }
  },
  {
    "question_id": "Q1-19",
    "question_text": "雨が多い場所と雨が少ない場所、どちらを選ぶ？",
    "type": "Yes/No",
    "options": ["雨が多い", "雨が少ない"],
    "scoring": {
      "雨が多い": { "rainy": 2, "lush": 1 },
      "雨が少ない": { "arid": 2, "dry": 1 }
    }
  },
  {
    "question_id": "Q1-20",
    "question_text": "スキーを楽しめる場所とマリンスポーツを楽しめる場所、どちらが魅力？",
    "type": "Yes/No",
    "options": ["スキー", "マリンスポーツ"],
    "scoring": {
      "スキー": { "snowy": 2, "mountainous": 1 },
      "マリンスポーツ": { "coastal": 2, "tropical": 1 }
    }
  },
  {
    "question_id": "Q1-21",
    "question_text": "夜景が美しい都会と星空が美しい田舎、どちらを見たい？",
    "type": "Yes/No",
    "options": ["夜景", "星空"],
    "scoring": {
      "夜景": { "urban": 2, "modern": 1 },
      "星空": { "rural": 2, "remote": 1 }
    }
  },
  {
    "question_id": "Q1-22",
    "question_text": "マイルドな気候と極端な気候、どちらに興味がある？",
    "type": "Yes/No",
    "options": ["マイルド", "極端"],
    "scoring": {
      "マイルド": { "temperate": 2, "mild": 1 },
      "極端": { "extreme": 3, "adventurous": 1 }
    }
  },
  {
    "question_id": "Q1-23",
    "question_text": "食文化が豊かな場所と景観が美しい場所、どちらに惹かれる？",
    "type": "Yes/No",
    "options": ["食文化", "景観"],
    "scoring": {
      "食文化": { "gastronomic": 3, "cultural": 1 },
      "景観": { "scenic": 3, "nature": 1 }
    }
  },
  {
    "question_id": "Q1-24",
    "question_text": "島国と大陸、どちらのイメージが好き？",
    "type": "Yes/No",
    "options": ["島国", "大陸"],
    "scoring": {
      "島国": { "island": 2, "coastal": 1 },
      "大陸": { "expansive": 2, "varied": 1 }
    }
  },
  {
    "question_id": "Q1-25",
    "question_text": "冬が長い土地と夏が長い土地、どちらが好み？",
    "type": "Yes/No",
    "options": ["冬が長い", "夏が長い"],
    "scoring": {
      "冬が長い": { "cold": 3, "snowy": 1 },
      "夏が長い": { "warm": 3, "tropical": 1 }
    }
  }
]

question_choice = [
  {
    "question_id": "Q1-26",
    "question_text": "最も魅力を感じるのはどの環境？",
    "type": "choice",
    "options": ["活気ある市街地", "穏やかなビーチ", "霧深い森", "壮大な高原"],
    "scoring": {
      "活気ある市街地": { "urban": 3, "modern": 1 },
      "穏やかなビーチ": { "coastal": 3, "relaxing": 1 },
      "霧深い森": { "forest": 3, "mysterious": 1 },
      "壮大な高原": { "plateau": 2, "scenic": 2 }
    }
  },
  {
    "question_id": "Q1-27",
    "question_text": "旅先で真っ先に訪れたい場所は？",
    "type": "choice",
    "options": ["歴史的建造物", "自然公園", "ショッピング街", "地方の市場"],
    "scoring": {
      "歴史的建造物": { "historical": 3, "cultural": 1 },
      "自然公園": { "nature": 3, "scenic": 1 },
      "ショッピング街": { "urban": 2, "modern": 2 },
      "地方の市場": { "traditional": 2, "cultural": 2 }
    }
  },
  {
    "question_id": "Q1-28",
    "question_text": "どの気候帯に一番興味がある？",
    "type": "choice",
    "options": ["熱帯", "温帯", "亜寒帯", "砂漠地帯"],
    "scoring": {
      "熱帯": { "tropical": 3, "humid": 1 },
      "温帯": { "temperate": 3, "seasonal": 1 },
      "亜寒帯": { "cold": 3, "snowy": 1 },
      "砂漠地帯": { "desert": 3, "arid": 1 }
    }
  },
  {
    "question_id": "Q1-29",
    "question_text": "もし移住するとしたら、どのような場所が理想？",
    "type": "choice",
    "options": ["大都会", "海辺の街", "山間の村", "広大な平野"],
    "scoring": {
      "大都会": { "urban": 3, "modern": 1 },
      "海辺の街": { "coastal": 3, "warm": 1 },
      "山間の村": { "mountainous": 3, "rural": 1 },
      "広大な平野": { "plains": 2, "nature": 2 }
    }
  },
  {
    "question_id": "Q1-30",
    "question_text": "休日に過ごしたいのはどの地域？",
    "type": "choice",
    "options": ["湖畔リゾート", "高層ビルの立ち並ぶ街", "静寂の山岳地帯", "川沿いの田舎町"],
    "scoring": {
      "湖畔リゾート": { "lakeside": 3, "relaxing": 1 },
      "高層ビルの立ち並ぶ街": { "urban": 3, "modern": 1 },
      "静寂の山岳地帯": { "mountainous": 3, "cold": 1 },
      "川沿いの田舎町": { "rural": 2, "scenic": 2 }
    }
  },
  {
    "question_id": "Q1-31",
    "question_text": "一度は体験してみたいのは？",
    "type": "choice",
    "options": ["ジャングル探検", "氷の世界", "大都市の夜遊び", "海底観光"],
    "scoring": {
      "ジャングル探検": { "tropical": 3, "adventurous": 1 },
      "氷の世界": { "arctic": 3, "extreme": 1 },
      "大都市の夜遊び": { "urban": 3, "nightlife": 1 },
      "海底観光": { "coastal": 2, "marine": 2 }
    }
  },
  {
    "question_id": "Q1-32",
    "question_text": "最も心惹かれる自然の姿は？",
    "type": "choice",
    "options": ["広大な砂丘", "鬱蒼とした熱帯雨林", "美しい渓谷", "壮麗な火山"],
    "scoring": {
      "広大な砂丘": { "desert": 3, "arid": 1 },
      "鬱蒼とした熱帯雨林": { "tropical": 3, "forest": 1 },
      "美しい渓谷": { "valley": 3, "river": 1 },
      "壮麗な火山": { "volcanic": 3, "mountainous": 1 }
    }
  },
  {
    "question_id": "Q1-33",
    "question_text": "魅力的に感じる地域の特徴は？",
    "type": "choice",
    "options": ["芸術が盛んな街", "海の幸が豊富な町", "温泉が湧く村", "絶景が連なる道"],
    "scoring": {
      "芸術が盛んな街": { "urban": 2, "cultural": 2 },
      "海の幸が豊富な町": { "coastal": 2, "gastronomic": 2 },
      "温泉が湧く村": { "hot_spring": 3, "rural": 1 },
      "絶景が連なる道": { "scenic": 3, "road_trip": 1 }
    }
  },
  {
    "question_id": "Q1-34",
    "question_text": "一番の癒やしを感じるのは？",
    "type": "choice",
    "options": ["森の中の小道", "波音が聞こえる浜辺", "田園風景が広がる丘", "近未来的な街の眺め"],
    "scoring": {
      "森の中の小道": { "forest": 2, "relaxing": 2 },
      "波音が聞こえる浜辺": { "coastal": 3, "serene": 1 },
      "田園風景が広がる丘": { "rural": 3, "pastoral": 1 },
      "近未来的な街の眺め": { "urban": 2, "modern": 2 }
    }
  },
  {
    "question_id": "Q1-35",
    "question_text": "次の旅で訪れるならどこ？",
    "type": "choice",
    "options": ["ヨーロッパ風の旧市街", "南国のビーチリゾート", "大自然が残る北の大地", "砂漠のオアシス"],
    "scoring": {
      "ヨーロッパ風の旧市街": { "historical": 3, "cultural": 1 },
      "南国のビーチリゾート": { "tropical": 3, "coastal": 1 },
      "大自然が残る北の大地": { "cold": 2, "wilderness": 2 },
      "砂漠のオアシス": { "desert": 2, "oasis": 2 }
    }
  },
  {
    "question_id": "Q1-36",
    "question_text": "理想の写真スポットは？",
    "type": "choice",
    "options": ["壮大な崖", "花畑の中", "ライトアップされた夜景", "透き通る湖面"],
    "scoring": {
      "壮大な崖": { "cliff": 3, "scenic": 1 },
      "花畑の中": { "pastoral": 2, "colorful": 2 },
      "ライトアップされた夜景": { "urban": 2, "nightlife": 2 },
      "透き通る湖面": { "lakeside": 3, "serene": 1 }
    }
  },
  {
    "question_id": "Q1-37",
    "question_text": "海外旅行で重視したいのは？",
    "type": "choice",
    "options": ["伝統文化の体験", "リゾート気分", "ショッピングとグルメ", "絶景巡り"],
    "scoring": {
      "伝統文化の体験": { "cultural": 3, "historical": 1 },
      "リゾート気分": { "coastal": 2, "relaxing": 2 },
      "ショッピングとグルメ": { "urban": 2, "gastronomic": 2 },
      "絶景巡り": { "scenic": 3, "nature": 1 }
    }
  },
  {
    "question_id": "Q1-38",
    "question_text": "一番落ち着けるのはどんな景観？",
    "type": "choice",
    "options": ["日本庭園のような静寂", "エメラルドグリーンの海", "雪原が続く世界", "高層ビル群の光"],
    "scoring": {
      "日本庭園のような静寂": { "cultural": 2, "serene": 2 },
      "エメラルドグリーンの海": { "coastal": 3, "tropical": 1 },
      "雪原が続く世界": { "cold": 3, "snowy": 1 },
      "高層ビル群の光": { "urban": 2, "modern": 2 }
    }
  },
  {
    "question_id": "Q1-39",
    "question_text": "長期滞在するならどの国土タイプ？",
    "type": "choice",
    "options": ["島国", "半島", "内陸国", "群島"],
    "scoring": {
      "島国": { "island": 3, "coastal": 1 },
      "半島": { "peninsula": 2, "coastal": 2 },
      "内陸国": { "landlocked": 3, "mountainous": 1 },
      "群島": { "archipelago": 3, "marine": 1 }
    }
  },
  {
    "question_id": "Q1-40",
    "question_text": "憧れのリゾートタイプは？",
    "type": "choice",
    "options": ["ビーチリゾート", "湖畔リゾート", "山岳リゾート", "砂漠リゾート"],
    "scoring": {
      "ビーチリゾート": { "coastal": 3, "warm": 1 },
      "湖畔リゾート": { "lakeside": 3, "relaxing": 1 },
      "山岳リゾート": { "mountainous": 3, "cold": 1 },
      "砂漠リゾート": { "desert": 3, "arid": 1 }
    }
  },
  {
    "question_id": "Q1-41",
    "question_text": "どの季節の風景が一番好き？",
    "type": "choice",
    "options": ["新緑の春", "太陽が燦々の夏", "紅葉の秋", "雪化粧の冬"],
    "scoring": {
      "新緑の春": { "spring": 2, "fresh": 2 },
      "太陽が燦々の夏": { "summer": 2, "warm": 2 },
      "紅葉の秋": { "autumn": 2, "scenic": 2 },
      "雪化粧の冬": { "winter": 2, "cold": 2 }
    }
  },
  {
    "question_id": "Q1-42",
    "question_text": "訪れてみたい世界の地形は？",
    "type": "choice",
    "options": ["フィヨルド", "サバンナ", "カリブ海の島々", "アルプスの山々"],
    "scoring": {
      "フィヨルド": { "coastal": 2, "mountainous": 2 },
      "サバンナ": { "savanna": 3, "warm": 1 },
      "カリブ海の島々": { "tropical": 3, "island": 1 },
      "アルプスの山々": { "cold": 3, "mountainous": 1 }
    }
  },
  {
    "question_id": "Q1-43",
    "question_text": "旅行するとしたら、何を一番重視？",
    "type": "choice",
    "options": ["気候", "文化体験", "食事", "自然の壮大さ"],
    "scoring": {
      "気候": { "climate": 3, "comfortable": 1 },
      "文化体験": { "cultural": 3, "historical": 1 },
      "食事": { "gastronomic": 3, "urban": 1 },
      "自然の壮大さ": { "nature": 3, "scenic": 1 }
    }
  },
  {
    "question_id": "Q1-44",
    "question_text": "子どもと一緒に楽しむなら？",
    "type": "choice",
    "options": ["テーマパークがある都市", "自然学習ができる森", "ビーチで遊べる海辺", "歴史学習ができる古都"],
    "scoring": {
      "テーマパークがある都市": { "urban": 2, "entertainment": 2 },
      "自然学習ができる森": { "forest": 2, "educational": 2 },
      "ビーチで遊べる海辺": { "coastal": 2, "relaxing": 2 },
      "歴史学習ができる古都": { "historical": 2, "cultural": 2 }
    }
  },
  {
    "question_id": "Q1-45",
    "question_text": "次のうち、あなたが一番惹かれるのは？",
    "type": "choice",
    "options": ["色とりどりの街並み", "神秘的な洞窟", "透き通る海中世界", "荘厳な山岳"],
    "scoring": {
      "色とりどりの街並み": { "urban": 2, "cultural": 2 },
      "神秘的な洞窟": { "cave": 3, "adventurous": 1 },
      "透き通る海中世界": { "marine": 3, "coastal": 1 },
      "荘厳な山岳": { "mountainous": 3, "scenic": 1 }
    }
  },
  {
    "question_id": "Q1-46",
    "question_text": "憧れる暮らしのスタイルは？",
    "type": "choice",
    "options": ["世界中を旅するノマド", "一つの場所に根付く田舎暮らし", "都市部の高層マンション", "海辺のコテージ"],
    "scoring": {
      "世界中を旅するノマド": { "adventurous": 3, "varied": 1 },
      "一つの場所に根付く田舎暮らし": { "rural": 3, "quiet": 1 },
      "都市部の高層マンション": { "urban": 3, "modern": 1 },
      "海辺のコテージ": { "coastal": 3, "relaxing": 1 }
    }
  },
  {
    "question_id": "Q1-47",
    "question_text": "どの星空が見たい？",
    "type": "choice",
    "options": ["砂漠で見る満天の星", "極寒の地でオーロラ", "離島で見る南十字星", "高原で眺める流れ星"],
    "scoring": {
      "砂漠で見る満天の星": { "desert": 2, "remote": 2 },
      "極寒の地でオーロラ": { "cold": 2, "northern_lights": 2 },
      "離島で見る南十字星": { "island": 2, "tropical": 2 },
      "高原で眺める流れ星": { "plateau": 2, "scenic": 2 }
    }
  },
  {
    "question_id": "Q1-48",
    "question_text": "朝日を拝むならどこが最高？",
    "type": "choice",
    "options": ["海から昇る朝日", "山頂から見る朝日", "都会のビル群の隙間から", "湖面に映る朝日"],
    "scoring": {
      "海から昇る朝日": { "coastal": 3, "serene": 1 },
      "山頂から見る朝日": { "mountainous": 3, "adventurous": 1 },
      "都会のビル群の隙間から": { "urban": 3, "modern": 1 },
      "湖面に映る朝日": { "lakeside": 3, "scenic": 1 }
    }
  },
  {
    "question_id": "Q1-49",
    "question_text": "長時間のフライトでも行きたい場所は？",
    "type": "choice",
    "options": ["楽園のようなリゾート", "歴史情緒あふれる街", "秘境のジャングル", "世界遺産の山岳地帯"],
    "scoring": {
      "楽園のようなリゾート": { "coastal": 3, "tropical": 1 },
      "歴史情緒あふれる街": { "historical": 3, "cultural": 1 },
      "秘境のジャングル": { "forest": 3, "adventurous": 1 },
      "世界遺産の山岳地帯": { "mountainous": 3, "unesco": 1 }
    }
  },
  {
    "question_id": "Q1-50",
    "question_text": "ゆったりした休日を過ごすなら？",
    "type": "choice",
    "options": ["緑豊かな公園", "海岸沿いの散歩道", "古都のカフェ巡り", "山の温泉街"],
    "scoring": {
      "緑豊かな公園": { "nature": 3, "relaxing": 1 },
      "海岸沿いの散歩道": { "coastal": 3, "serene": 1 },
      "古都のカフェ巡り": { "historical": 2, "urban": 2 },
      "山の温泉街": { "mountainous": 2, "hot_spring": 2 }
    }
  }
]

question_choice2 = [
  {
    "question_id": "Q1-51",
    "question_text": "あなたの性格を色に例えるなら？",
    "type": "choice2",
    "options": ["燃える赤", "穏やかな青", "爽やかな緑", "神秘的な紫"],
    "scoring": {
      "燃える赤": { "desert": 2, "volcanic": 1 },
      "穏やかな青": { "coastal": 2, "serene": 1 },
      "爽やかな緑": { "forest": 2, "nature": 1 },
      "神秘的な紫": { "mountainous": 2, "mysterious": 1 }
    }
  },
  {
    "question_id": "Q1-52",
    "question_text": "自分の旅行スタイルを動物にたとえるなら？",
    "type": "choice2",
    "options": ["鷹(高みから見渡す)", "イルカ(海と戯れる)", "ネコ(路地裏を探検)", "亀(ゆっくり巡る)"],
    "scoring": {
      "鷹(高みから見渡す)": { "mountainous": 2, "adventurous": 1 },
      "イルカ(海と戯れる)": { "coastal": 2, "marine": 1 },
      "ネコ(路地裏を探検)": { "urban": 2, "curious": 1 },
      "亀(ゆっくり巡る)": { "rural": 2, "relaxing": 1 }
    }
  },
  {
    "question_id": "Q1-53",
    "question_text": "あなたの旅行への意気込みを天気で表すと？",
    "type": "choice2",
    "options": ["灼熱の太陽", "しとしと雨", "さわやかな風", "吹雪"],
    "scoring": {
      "灼熱の太陽": { "warm": 2, "desert": 1 },
      "しとしと雨": { "rainy": 2, "forest": 1 },
      "さわやかな風": { "coastal": 2, "mild": 1 },
      "吹雪": { "cold": 2, "mountainous": 1 }
    }
  },
  {
    "question_id": "Q1-54",
    "question_text": "自分の心に一番近い景色は？",
    "type": "choice2",
    "options": ["荒涼とした大地", "凪いだ海", "そびえ立つ山々", "深い樹海"],
    "scoring": {
      "荒涼とした大地": { "desert": 2, "arid": 1 },
      "凪いだ海": { "coastal": 2, "serene": 1 },
      "そびえ立つ山々": { "mountainous": 2, "cold": 1 },
      "深い樹海": { "forest": 2, "mysterious": 1 }
    }
  },
  {
    "question_id": "Q1-55",
    "question_text": "もし感情が川の流れなら、それは？",
    "type": "choice2",
    "options": ["急流の激しい川", "ゆったり流れる大河", "せせらぎが響く小川", "地下を流れる伏流水"],
    "scoring": {
      "急流の激しい川": { "adventurous": 2, "mountainous": 1 },
      "ゆったり流れる大河": { "expansive": 2, "plains": 1 },
      "せせらぎが響く小川": { "rural": 2, "scenic": 1 },
      "地下を流れる伏流水": { "mysterious": 2, "cave": 1 }
    }
  },
  {
    "question_id": "Q1-56",
    "question_text": "自分の内面を一言で表すとしたら？",
    "type": "choice2",
    "options": ["太陽のように明るい", "月のように静かな", "星のように煌めく", "雲のように自由な"],
    "scoring": {
      "太陽のように明るい": { "warm": 2, "desert": 1 },
      "月のように静かな": { "cold": 2, "mountainous": 1 },
      "星のように煌めく": { "remote": 2, "night_sky": 1 },
      "雲のように自由な": { "mild": 2, "free": 1 }
    }
  },
  {
    "question_id": "Q1-57",
    "question_text": "理想とする冒険を童話に例えるなら？",
    "type": "choice2",
    "options": ["不思議の国", "海底二万里", "ジャングルブック", "アルプスの少女"],
    "scoring": {
      "不思議の国": { "mysterious": 2, "cultural": 1 },
      "海底二万里": { "marine": 2, "coastal": 1 },
      "ジャングルブック": { "tropical": 2, "forest": 1 },
      "アルプスの少女": { "mountainous": 2, "cold": 1 }
    }
  },
  {
    "question_id": "Q1-58",
    "question_text": "あなたの人生観を季節に例えるなら？",
    "type": "choice2",
    "options": ["春の芽吹き", "夏の情熱", "秋の成熟", "冬の静寂"],
    "scoring": {
      "春の芽吹き": { "fresh": 2, "mild": 1 },
      "夏の情熱": { "warm": 2, "tropical": 1 },
      "秋の成熟": { "scenic": 2, "moderate": 1 },
      "冬の静寂": { "cold": 2, "quiet": 1 }
    }
  },
  {
    "question_id": "Q1-59",
    "question_text": "自分を木に例えると？",
    "type": "choice2",
    "options": ["常夏のヤシの木", "高地のモミの木", "広大な平野の一本樹", "神秘的な森の巨木"],
    "scoring": {
      "常夏のヤシの木": { "tropical": 2, "coastal": 1 },
      "高地のモミの木": { "mountainous": 2, "cold": 1 },
      "広大な平野の一本樹": { "plains": 2, "solitary": 1 },
      "神秘的な森の巨木": { "forest": 2, "mysterious": 1 }
    }
  },
  {
    "question_id": "Q1-60",
    "question_text": "あなたのエネルギー源を自然現象で言うと？",
    "type": "choice2",
    "options": ["火山の噴火", "滝のような勢い", "穏やかな微風", "雷鳴とどろく稲妻"],
    "scoring": {
      "火山の噴火": { "volcanic": 2, "extreme": 1 },
      "滝のような勢い": { "waterfall": 2, "mountainous": 1 },
      "穏やかな微風": { "coastal": 2, "mild": 1 },
      "雷鳴とどろく稲妻": { "stormy": 2, "adventurous": 1 }
    }
  },
  {
    "question_id": "Q1-61",
    "question_text": "あなたの価値観を花に例えると？",
    "type": "choice2",
    "options": ["満開のひまわり", "神秘的な月下美人", "可憐なすみれ", "たくましいサボテンの花"],
    "scoring": {
      "満開のひまわり": { "sunny": 2, "warm": 1 },
      "神秘的な月下美人": { "nocturnal": 2, "mysterious": 1 },
      "可憐なすみれ": { "mild": 2, "forest": 1 },
      "たくましいサボテンの花": { "desert": 2, "arid": 1 }
    }
  },
  {
    "question_id": "Q1-62",
    "question_text": "魂のカラーをオーロラにたとえるなら？",
    "type": "choice2",
    "options": ["赤いオーロラ", "青いオーロラ", "緑のオーロラ", "紫のオーロラ"],
    "scoring": {
      "赤いオーロラ": { "extreme": 2, "adventurous": 1 },
      "青いオーロラ": { "cold": 2, "northern_lights": 1 },
      "緑のオーロラ": { "forest": 2, "mystical": 1 },
      "紫のオーロラ": { "mountainous": 2, "mysterious": 1 }
    }
  },
  {
    "question_id": "Q1-63",
    "question_text": "自分の歩みを地形に例えるなら？",
    "type": "choice2",
    "options": ["切り立った崖", "ゆるやかな丘", "波打ち際", "果てしない砂漠"],
    "scoring": {
      "切り立った崖": { "cliff": 2, "extreme": 1 },
      "ゆるやかな丘": { "rural": 2, "scenic": 1 },
      "波打ち際": { "coastal": 2, "mild": 1 },
      "果てしない砂漠": { "desert": 2, "arid": 1 }
    }
  },
  {
    "question_id": "Q1-64",
    "question_text": "自分を風景画に例えるとしたら？",
    "type": "choice2",
    "options": ["海辺の夕陽", "雪山の朝焼け", "花畑の昼下がり", "都心の夜景"],
    "scoring": {
      "海辺の夕陽": { "coastal": 2, "warm": 1 },
      "雪山の朝焼け": { "mountainous": 2, "cold": 1 },
      "花畑の昼下がり": { "pastoral": 2, "scenic": 1 },
      "都心の夜景": { "urban": 2, "modern": 1 }
    }
  },
  {
    "question_id": "Q1-65",
    "question_text": "あなたが持つ冒険心を空の色で表すなら？",
    "type": "choice2",
    "options": ["真っ青な快晴", "どんより曇天", "夕焼けのオレンジ", "星空の漆黒"],
    "scoring": {
      "真っ青な快晴": { "warm": 2, "open": 1 },
      "どんより曇天": { "cold": 2, "moody": 1 },
      "夕焼けのオレンジ": { "coastal": 2, "dramatic": 1 },
      "星空の漆黒": { "remote": 2, "night_sky": 1 }
    }
  },
  {
    "question_id": "Q1-66",
    "question_text": "あなたの余暇スタイルを乗り物でたとえると？",
    "type": "choice2",
    "options": ["高速列車", "帆船", "熱気球", "山岳鉄道"],
    "scoring": {
      "高速列車": { "urban": 2, "modern": 1 },
      "帆船": { "coastal": 2, "adventurous": 1 },
      "熱気球": { "scenic": 2, "mild": 1 },
      "山岳鉄道": { "mountainous": 2, "cold": 1 }
    }
  },
  {
    "question_id": "Q1-67",
    "question_text": "あなたのインスピレーション源を空想の生き物に例えるなら？",
    "type": "choice2",
    "options": ["ドラゴン", "マーメイド", "フェニックス", "ユニコーン"],
    "scoring": {
      "ドラゴン": { "mountainous": 2, "fiery": 1 },
      "マーメイド": { "coastal": 2, "marine": 1 },
      "フェニックス": { "desert": 2, "rebirth": 1 },
      "ユニコーン": { "forest": 2, "mystical": 1 }
    }
  },
  {
    "question_id": "Q1-68",
    "question_text": "あなたを一言で象徴するなら？",
    "type": "choice2",
    "options": ["灼熱", "氷結", "新緑", "深淵"],
    "scoring": {
      "灼熱": { "desert": 2, "warm": 1 },
      "氷結": { "cold": 2, "mountainous": 1 },
      "新緑": { "forest": 2, "mild": 1 },
      "深淵": { "mysterious": 2, "remote": 1 }
    }
  },
  {
    "question_id": "Q1-69",
    "question_text": "自分の生き方を川の源流から河口に例えるとしたら？",
    "type": "choice2",
    "options": ["源流で生まれてすぐ海へ", "ゆっくり蛇行して旅をする", "大地を深く削りながら進む", "途中で地下に潜る"],
    "scoring": {
      "源流で生まれてすぐ海へ": { "adventurous": 2, "short_path": 1 },
      "ゆっくり蛇行して旅をする": { "rural": 2, "scenic": 1 },
      "大地を深く削りながら進む": { "mountainous": 2, "determined": 1 },
      "途中で地下に潜る": { "mysterious": 2, "cave": 1 }
    }
  },
  {
    "question_id": "Q1-70",
    "question_text": "あなたが音楽に求める雰囲気を自然災害にたとえると？",
    "type": "choice2",
    "options": ["激しい雷鳴", "じわじわ増水する川", "嵐の前の静けさ", "吹雪のホワイトアウト"],
    "scoring": {
      "激しい雷鳴": { "stormy": 2, "extreme": 1 },
      "じわじわ増水する川": { "scenic": 2, "persistent": 1 },
      "嵐の前の静けさ": { "calm": 2, "mild": 1 },
      "吹雪のホワイトアウト": { "snowy": 2, "cold": 1 }
    }
  },
  {
    "question_id": "Q1-71",
    "question_text": "あなたの友情を山にたとえると？",
    "type": "choice2",
    "options": ["そびえ立つ険しい峰", "なだらかな丘", "広大に連なる山脈", "ぽつんと立つ独立峰"],
    "scoring": {
      "そびえ立つ険しい峰": { "mountainous": 2, "extreme": 1 },
      "なだらかな丘": { "mild": 2, "scenic": 1 },
      "広大に連なる山脈": { "expansive": 2, "cold": 1 },
      "ぽつんと立つ独立峰": { "solitary": 2, "remote": 1 }
    }
  },
  {
    "question_id": "Q1-72",
    "question_text": "自分の家を自然環境に例えるなら？",
    "type": "choice2",
    "options": ["海辺の灯台", "森の隠れ家", "草原に立つテント", "崖の上の要塞"],
    "scoring": {
      "海辺の灯台": { "coastal": 2, "guiding": 1 },
      "森の隠れ家": { "forest": 2, "quiet": 1 },
      "草原に立つテント": { "plains": 2, "simple": 1 },
      "崖の上の要塞": { "cliff": 2, "defensive": 1 }
    }
  },
  {
    "question_id": "Q1-73",
    "question_text": "あなたの決断力を天候に例えるなら？",
    "type": "choice2",
    "options": ["突風のように即決", "微風のようにじわじわ", "晴れ間を待つ", "大嵐を起こす"],
    "scoring": {
      "突風のように即決": { "windy": 2, "adventurous": 1 },
      "微風のようにじわじわ": { "mild": 2, "calm": 1 },
      "晴れ間を待つ": { "patient": 2, "moderate": 1 },
      "大嵐を起こす": { "stormy": 2, "extreme": 1 }
    }
  },
  {
    "question_id": "Q1-74",
    "question_text": "自分の夢を地質現象にたとえるなら？",
    "type": "choice2",
    "options": ["マグマのように内側で煮えたぎる", "氷河のようにゆっくり動く", "砂丘のように形を変える", "洞窟の奥深くで成長する鍾乳石"],
    "scoring": {
      "マグマのように内側で煮えたぎる": { "volcanic": 2, "intense": 1 },
      "氷河のようにゆっくり動く": { "cold": 2, "slow": 1 },
      "砂丘のように形を変える": { "desert": 2, "shifting": 1 },
      "洞窟の奥深くで成長する鍾乳石": { "cave": 2, "patient": 1 }
    }
  },
  {
    "question_id": "Q1-75",
    "question_text": "あなたの開放感を空に例えるなら？",
    "type": "choice2",
    "options": ["朝焼けの空", "真昼の雲一つない空", "夕暮れのオレンジ空", "満天の星空"],
    "scoring": {
      "朝焼けの空": { "mild": 2, "new_beginning": 1 },
      "真昼の雲一つない空": { "open": 2, "warm": 1 },
      "夕暮れのオレンジ空": { "coastal": 2, "dramatic": 1 },
      "満天の星空": { "remote": 2, "night_sky": 1 }
    }
  }
]

questions_image = [
  {
    "question_id": "Q1-76",
    "question_text": "次の4枚の写真の中で、最も惹かれるのはどれ？(1.都会の夜景, 2.白い砂浜, 3.緑豊かな森, 4.雪山の頂)",
    "type": "image",
    "options": ["都会の夜景", "白い砂浜", "緑豊かな森", "雪山の頂"],
    "scoring": {
      "都会の夜景": { "urban": 2, "modern": 2 },
      "白い砂浜": { "coastal": 3, "tropical": 1 },
      "緑豊かな森": { "forest": 3, "nature": 1 },
      "雪山の頂": { "cold": 3, "mountainous": 1 }
    }
  },
  {
    "question_id": "Q1-77",
    "question_text": "4つの風景画像から選ぶなら？(1.サンゴ礁の海, 2.広大な草原, 3.湖畔の黄昏, 4.歴史的な城下町)",
    "type": "image",
    "options": ["サンゴ礁の海", "広大な草原", "湖畔の黄昏", "歴史的な城下町"],
    "scoring": {
      "サンゴ礁の海": { "coastal": 3, "marine": 1 },
      "広大な草原": { "plains": 3, "rural": 1 },
      "湖畔の黄昏": { "lakeside": 3, "serene": 1 },
      "歴史的な城下町": { "historical": 3, "urban": 1 }
    }
  },
  {
    "question_id": "Q1-78",
    "question_text": "次の4つの旅先イメージから最も行きたい場所は？(1.豪華客船, 2.アルプスの山小屋, 3.アマゾンの密林, 4.エジプトのピラミッド)",
    "type": "image",
    "options": ["豪華客船", "アルプスの山小屋", "アマゾンの密林", "エジプトのピラミッド"],
    "scoring": {
      "豪華客船": { "marine": 2, "luxury": 2 },
      "アルプスの山小屋": { "mountainous": 3, "cold": 1 },
      "アマゾンの密林": { "tropical": 3, "forest": 1 },
      "エジプトのピラミッド": { "desert": 3, "historical": 1 }
    }
  },
  {
    "question_id": "Q1-79",
    "question_text": "次の4つの写真で惹かれる風景は？(1.霧に包まれた森, 2.青々とした海, 3.ニューヨークの街並み, 4.広大な砂漠)",
    "type": "image",
    "options": ["霧に包まれた森", "青々とした海", "ニューヨークの街並み", "広大な砂漠"],
    "scoring": {
      "霧に包まれた森": { "forest": 3, "mysterious": 1 },
      "青々とした海": { "coastal": 3, "warm": 1 },
      "ニューヨークの街並み": { "urban": 3, "modern": 1 },
      "広大な砂漠": { "desert": 3, "arid": 1 }
    }
  },
  {
    "question_id": "Q1-80",
    "question_text": "次の4枚のポストカードから、どれを飾りたい？(1.穏やかな湖, 2.ロンドンのビッグベン, 3.色とりどりのサンセットビーチ, 4.雪原とオーロラ)",
    "type": "image",
    "options": ["穏やかな湖", "ロンドンのビッグベン", "色とりどりのサンセットビーチ", "雪原とオーロラ"],
    "scoring": {
      "穏やかな湖": { "lakeside": 3, "serene": 1 },
      "ロンドンのビッグベン": { "urban": 3, "historical": 1 },
      "色とりどりのサンセットビーチ": { "coastal": 3, "dramatic": 1 },
      "雪原とオーロラ": { "cold": 3, "northern_lights": 1 }
    }
  },
  {
    "question_id": "Q1-81",
    "question_text": "次の4つの写真で行ってみたいのは？(1.青い洞窟, 2.紅葉の山道, 3.モロッコの砂漠, 4.香港の夜景)",
    "type": "image",
    "options": ["青い洞窟", "紅葉の山道", "モロッコの砂漠", "香港の夜景"],
    "scoring": {
      "青い洞窟": { "cave": 3, "coastal": 1 },
      "紅葉の山道": { "mountainous": 3, "autumn": 1 },
      "モロッコの砂漠": { "desert": 3, "arid": 1 },
      "香港の夜景": { "urban": 3, "modern": 1 }
    }
  },
  {
    "question_id": "Q1-82",
    "question_text": "4枚の絶景写真の中で、どれが好み？(1.崖沿いの海岸線, 2.エメラルドグリーンの渓谷, 3.アムステルダムの街並み, 4.雪山に建つ山小屋)",
    "type": "image",
    "options": ["崖沿いの海岸線", "エメラルドグリーンの渓谷", "アムステルダムの街並み", "雪山に建つ山小屋"],
    "scoring": {
      "崖沿いの海岸線": { "coastal": 2, "cliff": 2 },
      "エメラルドグリーンの渓谷": { "valley": 2, "river": 2 },
      "アムステルダムの街並み": { "urban": 2, "historical": 2 },
      "雪山に建つ山小屋": { "cold": 2, "mountainous": 2 }
    }
  },
  {
    "question_id": "Q1-83",
    "question_text": "次の4つの自然風景でお気に入りは？(1.滝が流れる断崖, 2.白砂のビーチ, 3.トロピカルなジャングル, 4.広がるヒマラヤ)",
    "type": "image",
    "options": ["滝が流れる断崖", "白砂のビーチ", "トロピカルなジャングル", "広がるヒマラヤ"],
    "scoring": {
      "滝が流れる断崖": { "waterfall": 2, "mountainous": 2 },
      "白砂のビーチ": { "coastal": 3, "tropical": 1 },
      "トロピカルなジャングル": { "forest": 3, "humid": 1 },
      "広がるヒマラヤ": { "cold": 3, "mountainous": 1 }
    }
  },
  {
    "question_id": "Q1-84",
    "question_text": "次の観光地写真のうち、最もワクワクするのは？(1.パリのエッフェル塔, 2.ハワイの海, 3.スイスの山, 4.エチオピアの大地溝帯)",
    "type": "image",
    "options": ["パリのエッフェル塔", "ハワイの海", "スイスの山", "エチオピアの大地溝帯"],
    "scoring": {
      "パリのエッフェル塔": { "urban": 3, "romantic": 1 },
      "ハワイの海": { "coastal": 3, "tropical": 1 },
      "スイスの山": { "mountainous": 3, "cold": 1 },
      "エチオピアの大地溝帯": { "desert": 2, "adventurous": 2 }
    }
  },
  {
    "question_id": "Q1-85",
    "question_text": "次の世界遺産写真の中から、行ってみたいのは？(1.グランドキャニオン, 2.サグラダファミリア, 3.グレートバリアリーフ, 4.マチュピチュ)",
    "type": "image",
    "options": ["グランドキャニオン", "サグラダファミリア", "グレートバリアリーフ", "マチュピチュ"],
    "scoring": {
      "グランドキャニオン": { "desert": 2, "canyon": 2 },
      "サグラダファミリア": { "urban": 3, "historical": 1 },
      "グレートバリアリーフ": { "coastal": 3, "marine": 1 },
      "マチュピチュ": { "mountainous": 3, "historical": 1 }
    }
  },
  {
    "question_id": "Q1-86",
    "question_text": "次の4つの写真で夕日が美しいと思うのは？(1.バリ島のビーチ, 2.アフリカのサバンナ, 3.北海道の丘陵地帯, 4.ニューヨークの摩天楼)",
    "type": "image",
    "options": ["バリ島のビーチ", "アフリカのサバンナ", "北海道の丘陵地帯", "ニューヨークの摩天楼"],
    "scoring": {
      "バリ島のビーチ": { "coastal": 3, "tropical": 1 },
      "アフリカのサバンナ": { "savanna": 3, "warm": 1 },
      "北海道の丘陵地帯": { "rural": 3, "mild": 1 },
      "ニューヨークの摩天楼": { "urban": 3, "modern": 1 }
    }
  },
  {
    "question_id": "Q1-87",
    "question_text": "次の4枚の夜空写真から選ぶなら？(1.砂漠の星空, 2.海辺の月夜, 3.北欧のオーロラ, 4.大都市のライトアップ)",
    "type": "image",
    "options": ["砂漠の星空", "海辺の月夜", "北欧のオーロラ", "大都市のライトアップ"],
    "scoring": {
      "砂漠の星空": { "desert": 2, "remote": 2 },
      "海辺の月夜": { "coastal": 2, "serene": 2 },
      "北欧のオーロラ": { "cold": 2, "northern_lights": 2 },
      "大都市のライトアップ": { "urban": 2, "modern": 2 }
    }
  },
  {
    "question_id": "Q1-88",
    "question_text": "次の4つの山岳風景で魅力を感じるのは？(1.切り立った岩山, 2.雪に覆われた峰, 3.草花が咲き乱れる高山, 4.火山口が見える山)",
    "type": "image",
    "options": ["切り立った岩山", "雪に覆われた峰", "草花が咲き乱れる高山", "火山口が見える山"],
    "scoring": {
      "切り立った岩山": { "mountainous": 3, "rocky": 1 },
      "雪に覆われた峰": { "mountainous": 3, "cold": 1 },
      "草花が咲き乱れる高山": { "mountainous": 2, "scenic": 2 },
      "火山口が見える山": { "volcanic": 3, "extreme": 1 }
    }
  },
  {
    "question_id": "Q1-89",
    "question_text": "次の4枚の森の写真から好きな雰囲気は？(1.太陽光差し込む明るい森, 2.苔むした原生林, 3.竹林の小道, 4.落ち葉に埋もれた静寂の森)",
    "type": "image",
    "options": ["太陽光差し込む明るい森", "苔むした原生林", "竹林の小道", "落ち葉に埋もれた静寂の森"],
    "scoring": {
      "太陽光差し込む明るい森": { "forest": 2, "warm": 2 },
      "苔むした原生林": { "forest": 2, "mysterious": 2 },
      "竹林の小道": { "forest": 2, "cultural": 2 },
      "落ち葉に埋もれた静寂の森": { "forest": 2, "quiet": 2 }
    }
  },
  {
    "question_id": "Q1-90",
    "question_text": "次の4つの海洋写真で行きたいのは？(1.エーゲ海の白い街並み, 2.サンゴ礁が広がる海, 3.霧が立ち込める北海, 4.雄大なフィヨルド)",
    "type": "image",
    "options": ["エーゲ海の白い街並み", "サンゴ礁が広がる海", "霧が立ち込める北海", "雄大なフィヨルド"],
    "scoring": {
      "エーゲ海の白い街並み": { "coastal": 3, "historical": 1 },
      "サンゴ礁が広がる海": { "coastal": 3, "marine": 1 },
      "霧が立ち込める北海": { "cold": 2, "coastal": 2 },
      "雄大なフィヨルド": { "coastal": 2, "mountainous": 2 }
    }
  },
  {
    "question_id": "Q1-91",
    "question_text": "次の4つの都市景観写真、どこを訪れたい？(1.東京の交差点, 2.イスタンブールの市場, 3.リオのカラフルな街並み, 4.ドバイの高層ビル群)",
    "type": "image",
    "options": ["東京の交差点", "イスタンブールの市場", "リオのカラフルな街並み", "ドバイの高層ビル群"],
    "scoring": {
      "東京の交差点": { "urban": 3, "modern": 1 },
      "イスタンブールの市場": { "urban": 2, "historical": 2 },
      "リオのカラフルな街並み": { "urban": 2, "warm": 2 },
      "ドバイの高層ビル群": { "urban": 3, "desert": 1 }
    }
  },
  {
    "question_id": "Q1-92",
    "question_text": "次の4枚の写真で一番涼しそうなのは？(1.氷河の湖, 2.高地の草原, 3.森の中の川, 4.海風が吹くビーチ)",
    "type": "image",
    "options": ["氷河の湖", "高地の草原", "森の中の川", "海風が吹くビーチ"],
    "scoring": {
      "氷河の湖": { "cold": 3, "lakeside": 1 },
      "高地の草原": { "mountainous": 2, "mild": 2 },
      "森の中の川": { "forest": 2, "river": 2 },
      "海風が吹くビーチ": { "coastal": 2, "breezy": 2 }
    }
  },
  {
    "question_id": "Q1-93",
    "question_text": "次の4つの写真から、心が和むのは？(1.ラベンダー畑, 2.木漏れ日の森, 3.干潟で戯れる鳥たち, 4.夕陽に染まる草原)",
    "type": "image",
    "options": ["ラベンダー畑", "木漏れ日の森", "干潟で戯れる鳥たち", "夕陽に染まる草原"],
    "scoring": {
      "ラベンダー畑": { "rural": 2, "pastoral": 2 },
      "木漏れ日の森": { "forest": 2, "serene": 2 },
      "干潟で戯れる鳥たち": { "coastal": 2, "nature": 2 },
      "夕陽に染まる草原": { "plains": 2, "warm": 2 }
    }
  },
  {
    "question_id": "Q1-94",
    "question_text": "次の絶景写真から最も行きたいのは？(1.ナイアガラの滝, 2.サハラ砂漠, 3.チベット高原, 4.ベネチアの運河)",
    "type": "image",
    "options": ["ナイアガラの滝", "サハラ砂漠", "チベット高原", "ベネチアの運河"],
    "scoring": {
      "ナイアガラの滝": { "waterfall": 3, "border": 1 },
      "サハラ砂漠": { "desert": 3, "arid": 1 },
      "チベット高原": { "plateau": 3, "cold": 1 },
      "ベネチアの運河": { "urban": 3, "historical": 1 }
    }
  },
  {
    "question_id": "Q1-95",
    "question_text": "次の4つの写真で開放感を感じるのは？(1.青空と海の水平線, 2.果てしない草原, 3.広大なキャニオン, 4.近代的な大橋)",
    "type": "image",
    "options": ["青空と海の水平線", "果てしない草原", "広大なキャニオン", "近代的な大橋"],
    "scoring": {
      "青空と海の水平線": { "coastal": 3, "serene": 1 },
      "果てしない草原": { "plains": 3, "rural": 1 },
      "広大なキャニオン": { "desert": 2, "canyon": 2 },
      "近代的な大橋": { "urban": 2, "modern": 2 }
    }
  },
  {
    "question_id": "Q1-96",
    "question_text": "次の4つの世界の祭り写真、どこに参加したい？(1.リオのカーニバル, 2.青森のねぶた祭, 3.バーニングマン, 4.オクトーバーフェスト)",
    "type": "image",
    "options": ["リオのカーニバル", "青森のねぶた祭", "バーニングマン", "オクトーバーフェスト"],
    "scoring": {
      "リオのカーニバル": { "urban": 2, "warm": 2 },
      "青森のねぶた祭": { "cultural": 3, "urban": 1 },
      "バーニングマン": { "desert": 3, "artistic": 1 },
      "オクトーバーフェスト": { "urban": 3, "cultural": 1 }
    }
  },
  {
    "question_id": "Q1-97",
    "question_text": "次の4枚のヨーロッパ風景写真から選ぶなら？(1.アルプス山脈, 2.地中海沿岸, 3.イギリスの田園地帯, 4.東欧の古城)",
    "type": "image",
    "options": ["アルプス山脈", "地中海沿岸", "イギリスの田園地帯", "東欧の古城"],
    "scoring": {
      "アルプス山脈": { "mountainous": 3, "cold": 1 },
      "地中海沿岸": { "coastal": 3, "warm": 1 },
      "イギリスの田園地帯": { "rural": 3, "mild": 1 },
      "東欧の古城": { "historical": 3, "cultural": 1 }
    }
  },
  {
    "question_id": "Q1-98",
    "question_text": "次の4つの夕景写真、どれに心惹かれる？(1.イタリアの丘陵地, 2.アジアのジャングル, 3.シカゴの高層ビル群, 4.アフリカのサバンナ)",
    "type": "image",
    "options": ["イタリアの丘陵地", "アジアのジャングル", "シカゴの高層ビル群", "アフリカのサバンナ"],
    "scoring": {
      "イタリアの丘陵地": { "rural": 3, "historical": 1 },
      "アジアのジャングル": { "forest": 3, "tropical": 1 },
      "シカゴの高層ビル群": { "urban": 3, "modern": 1 },
      "アフリカのサバンナ": { "savanna": 3, "warm": 1 }
    }
  },
  {
    "question_id": "Q1-99",
    "question_text": "次の4枚の海岸写真からどれが好き？(1.白い崖が続く海岸, 2.黒砂のビーチ, 3.ヤシの木が生い茂る浜, 4.岩場の多いワイルドな海岸)",
    "type": "image",
    "options": ["白い崖が続く海岸", "黒砂のビーチ", "ヤシの木が生い茂る浜", "岩場の多いワイルドな海岸"],
    "scoring": {
      "白い崖が続く海岸": { "coastal": 2, "cliff": 2 },
      "黒砂のビーチ": { "coastal": 2, "volcanic": 2 },
      "ヤシの木が生い茂る浜": { "tropical": 2, "coastal": 2 },
      "岩場の多いワイルドな海岸": { "coastal": 2, "rugged": 2 }
    }
  },
  {
    "question_id": "Q1-100",
    "question_text": "次の4枚の都市夜景写真、どの雰囲気が好き？(1.上海の摩天楼, 2.プラハの歴史地区, 3.ラスベガスのネオン街, 4.シンガポールの湾岸夜景)",
    "type": "image",
    "options": ["上海の摩天楼", "プラハの歴史地区", "ラスベガスのネオン街", "シンガポールの湾岸夜景"],
    "scoring": {
      "上海の摩天楼": { "urban": 3, "modern": 1 },
      "プラハの歴史地区": { "historical": 3, "cultural": 1 },
      "ラスベガスのネオン街": { "urban": 2, "entertainment": 2 },
      "シンガポールの湾岸夜景": { "urban": 3, "coastal": 1 }
    }
  }
]
