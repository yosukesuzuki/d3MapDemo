var prefectures_data = JSON.parse('{"prefectures": [{"major_island": "Honshu", "region": "Chubu", "japanese": "\u611b\u77e5\u770c", "iso": "JP-23", "capital": "Nagoya", "prefecture": "Aichi"}, {"major_island": "Honshu", "region": "Tohoku", "japanese": "\u79cb\u7530\u770c", "iso": "JP-05", "capital": "Akita", "prefecture": "Akita"}, {"major_island": "Honshu", "region": "Tohoku", "japanese": "\u9752\u68ee\u770c", "iso": "JP-02", "capital": "Aomori", "prefecture": "Aomori"}, {"major_island": "Honshu", "region": "Kanto", "japanese": "\u5343\u8449\u770c", "iso": "JP-12", "capital": "Chiba", "prefecture": "Chiba"}, {"major_island": "Shikoku", "region": "Shikoku", "japanese": "\u611b\u5a9b\u770c", "iso": "JP-38", "capital": "Matsuyama", "prefecture": "Ehime"}, {"major_island": "Honshu", "region": "Chubu", "japanese": "\u798f\u4e95\u770c", "iso": "JP-18", "capital": "Fukui", "prefecture": "Fukui"}, {"major_island": "Kyushu", "region": "Kyushu", "japanese": "\u798f\u5ca1\u770c", "iso": "JP-40", "capital": "Fukuoka", "prefecture": "Fukuoka"}, {"major_island": "Honshu", "region": "Tohoku", "japanese": "\u798f\u5cf6\u770c", "iso": "JP-07", "capital": "Fukushima", "prefecture": "Fukushima"}, {"major_island": "Honshu", "region": "Chubu", "japanese": "\u5c90\u961c\u770c", "iso": "JP-21", "capital": "Gifu", "prefecture": "Gifu"}, {"major_island": "Honshu", "region": "Kanto", "japanese": "\u7fa4\u99ac\u770c", "iso": "JP-10", "capital": "Maebashi", "prefecture": "Gunma"}, {"major_island": "Honshu", "region": "Chugoku", "japanese": "\u5e83\u5cf6\u770c", "iso": "JP-34", "capital": "Hiroshima", "prefecture": "Hiroshima"}, {"major_island": "Hokkaido", "region": "Hokkaido", "japanese": "\u5317\u6d77\u9053", "iso": "JP-01", "capital": "Sapporo", "prefecture": "Hokkaido"}, {"major_island": "Honshu", "region": "Kansai", "japanese": "\u5175\u5eab\u770c", "iso": "JP-28", "capital": "Kobe", "prefecture": "Hyogo"}, {"major_island": "Honshu", "region": "Kanto", "japanese": "\u8328\u57ce\u770c", "iso": "JP-08", "capital": "Mito", "prefecture": "Ibaraki"}, {"major_island": "Honshu", "region": "Chubu", "japanese": "\u77f3\u5ddd\u770c", "iso": "JP-17", "capital": "Kanazawa", "prefecture": "Ishikawa"}, {"major_island": "Honshu", "region": "Tohoku", "japanese": "\u5ca9\u624b\u770c", "iso": "JP-03", "capital": "Morioka", "prefecture": "Iwate"}, {"major_island": "Shikoku", "region": "Shikoku", "japanese": "\u9999\u5ddd\u770c", "iso": "JP-37", "capital": "Takamatsu", "prefecture": "Kagawa"}, {"major_island": "Kyushu", "region": "Kyushu", "japanese": "\u9e7f\u5150\u5cf6\u770c", "iso": "JP-46", "capital": "Kagoshima", "prefecture": "Kagoshima"}, {"major_island": "Honshu", "region": "Kanto", "japanese": "\u795e\u5948\u5ddd\u770c", "iso": "JP-14", "capital": "Yokohama", "prefecture": "Kanagawa"}, {"major_island": "Shikoku", "region": "Shikoku", "japanese": "\u9ad8\u77e5\u770c", "iso": "JP-39", "capital": "Kochi", "prefecture": "Kochi"}, {"major_island": "Kyushu", "region": "Kyushu", "japanese": "\u718a\u672c\u770c", "iso": "JP-43", "capital": "Kumamoto", "prefecture": "Kumamoto"}, {"major_island": "Honshu", "region": "Kansai", "japanese": "\u4eac\u90fd\u5e9c", "iso": "JP-26", "capital": "Kyoto", "prefecture": "Kyoto"}, {"major_island": "Honshu", "region": "Kansai", "japanese": "\u4e09\u91cd\u770c", "iso": "JP-24", "capital": "Tsu", "prefecture": "Mie"}, {"major_island": "Honshu", "region": "Tohoku", "japanese": "\u5bae\u57ce\u770c", "iso": "JP-04", "capital": "Sendai", "prefecture": "Miyagi"}, {"major_island": "Kyushu", "region": "Kyushu", "japanese": "\u5bae\u5d0e\u770c", "iso": "JP-45", "capital": "Miyazaki", "prefecture": "Miyazaki"}, {"major_island": "Honshu", "region": "Chubu", "japanese": "\u9577\u91ce\u770c", "iso": "JP-20", "capital": "Nagano", "prefecture": "Nagano"}, {"major_island": "Kyushu", "region": "Kyushu", "japanese": "\u9577\u5d0e\u770c", "iso": "JP-42", "capital": "Nagasaki", "prefecture": "Nagasaki"}, {"major_island": "Honshu", "region": "Kansai", "japanese": "\u5948\u826f\u770c", "iso": "JP-29", "capital": "Nara", "prefecture": "Nara"}, {"major_island": "Honshu", "region": "Chubu", "japanese": "\u65b0\u6f5f\u770c", "iso": "JP-15", "capital": "Niigata", "prefecture": "Niigata"}, {"major_island": "Kyushu", "region": "Kyushu", "japanese": "\u5927\u5206\u770c", "iso": "JP-44", "capital": "Oita", "prefecture": "Oita"}, {"major_island": "Honshu", "region": "Chugoku", "japanese": "\u5ca1\u5c71\u770c", "iso": "JP-33", "capital": "Okayama", "prefecture": "Okayama"}, {"major_island": "Ryukyu Islands", "region": "Kyushu", "japanese": "\u6c96\u7e04\u770c", "iso": "JP-47", "capital": "Naha", "prefecture": "Okinawa"}, {"major_island": "Honshu", "region": "Kansai", "japanese": "\u5927\u962a\u5e9c", "iso": "JP-27", "capital": "Osaka", "prefecture": "Osaka"}, {"major_island": "Kyushu", "region": "Kyushu", "japanese": "\u4f50\u8cc0\u770c", "iso": "JP-41", "capital": "Saga", "prefecture": "Saga"}, {"major_island": "Honshu", "region": "Kanto", "japanese": "\u57fc\u7389\u770c", "iso": "JP-11", "capital": "Saitama", "prefecture": "Saitama"}, {"major_island": "Honshu", "region": "Kansai", "japanese": "\u6ecb\u8cc0\u770c", "iso": "JP-25", "capital": "Otsu", "prefecture": "Shiga"}, {"major_island": "Honshu", "region": "Chugoku", "japanese": "\u5cf6\u6839\u770c", "iso": "JP-32", "capital": "Matsue", "prefecture": "Shimane"}, {"major_island": "Honshu", "region": "Chubu", "japanese": "\u9759\u5ca1\u770c", "iso": "JP-22", "capital": "Shizuoka", "prefecture": "Shizuoka"}, {"major_island": "Honshu", "region": "Kanto", "japanese": "\u6803\u6728\u770c", "iso": "JP-09", "capital": "Utsunomiya", "prefecture": "Tochigi"}, {"major_island": "Shikoku", "region": "Shikoku", "japanese": "\u5fb3\u5cf6\u770c", "iso": "JP-36", "capital": "Tokushima", "prefecture": "Tokushima"}, {"major_island": "Honshu", "region": "Kanto", "japanese": "\u6771\u4eac\u90fd", "iso": "JP-13", "capital": "Shinjuku", "prefecture": "Tokyo"}, {"major_island": "Honshu", "region": "Chugoku", "japanese": "\u9ce5\u53d6\u770c", "iso": "JP-31", "capital": "Tottori", "prefecture": "Tottori"}, {"major_island": "Honshu", "region": "Chubu", "japanese": "\u5bcc\u5c71\u770c", "iso": "JP-16", "capital": "Toyama", "prefecture": "Toyama"}, {"major_island": "Honshu", "region": "Kansai", "japanese": "\u548c\u6b4c\u5c71\u770c", "iso": "JP-30", "capital": "Wakayama", "prefecture": "Wakayama"}, {"major_island": "Honshu", "region": "Tohoku", "japanese": "\u5c71\u5f62\u770c", "iso": "JP-06", "capital": "Yamagata", "prefecture": "Yamagata"}, {"major_island": "Honshu", "region": "Chugoku", "japanese": "\u5c71\u53e3\u770c", "iso": "JP-35", "capital": "Yamaguchi", "prefecture": "Yamaguchi"}, {"major_island": "Honshu", "region": "Chubu", "japanese": "\u5c71\u68a8\u770c", "iso": "JP-19", "capital": "Kofu", "prefecture": "Yamanashi"}]}');