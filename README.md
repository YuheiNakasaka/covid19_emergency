# covid19_emergency

緊急事態宣言・まん延防止等重点措置の期間及び区域の情報を返す API です。

政府の運営する[新型コロナウイルス感染症対策](https://corona.go.jp/emergency/)の HP から GitHub Actions で定期的にスクレイピングし json ファイルを生成させています。

# API

[https://yuheinakasaka.github.io/covid19_emergency/emergency.json](https://yuheinakasaka.github.io/covid19_emergency/emergency.json)

レスポンス例は下記です。

```
{
    // 緊急事態宣言
    "emergency": [
        {
            "name": "沖縄県",
            "from": "5月23日",
            "to": "8月31日"
        },
        {
            "name": "東京都",
            "from": "7月12日",
            "to": "8月31日"
        },
        {
            "name": "埼玉県",
            "from": "8月2日",
            "to": "8月31日"
        },
        {
            "name": "千葉県",
            "from": "8月2日",
            "to": "8月31日"
        },
        {
            "name": "神奈川県",
            "from": "8月2日",
            "to": "8月31日"
        },
        {
            "name": "大阪府",
            "from": "8月2日",
            "to": "8月31日"
        }
    ],
    // まん延防止等重点措置
    "manbou": [
        {
            "name": "北海道",
            "from": "8月2日",
            "to": "8月31日"
        },
        {
            "name": "石川県",
            "from": "8月2日",
            "to": "8月31日"
        },
        {
            "name": "京都府",
            "from": "8月2日",
            "to": "8月31日"
        },
        {
            "name": "兵庫県",
            "from": "8月2日",
            "to": "8月31日"
        },
        {
            "name": "福岡県",
            "from": "8月2日",
            "to": "8月31日"
        },
        {
            "name": "福島県",
            "from": "8月8日",
            "to": "8月31日"
        },
        {
            "name": "茨城県",
            "from": "8月8日",
            "to": "8月31日"
        },
        {
            "name": "栃木県",
            "from": "8月8日",
            "to": "8月31日"
        },
        {
            "name": "群馬県",
            "from": "8月8日",
            "to": "8月31日"
        },
        {
            "name": "静岡県",
            "from": "8月8日",
            "to": "8月31日"
        },
        {
            "name": "愛知県",
            "from": "8月8日",
            "to": "8月31日"
        },
        {
            "name": "滋賀県",
            "from": "8月8日",
            "to": "8月31日"
        },
        {
            "name": "熊本県",
            "from": "8月8日",
            "to": "8月31日"
        }
    ],
    // 最終更新日時 TZ=Tokyo/Asia
    "updatedAt": "2021-08-16 16:25:01.052446"
}
```

# よくある質問

## API のリクエスト回数制限はある？

ない。GitHub Pages の静的ファイルを利用しているので好きにリクエストしてもらっても問題ない。

## 社内で利用してもいい？

いい。どこでどう使われようが問題ない。ただし、それで発生した責任は負わない。

## API が死んでるもしくはデータが間違っている

[@razokulover](https://twitter.com/razokulover)へ連絡が一番早い。issue や PR を立ててもらっても構わない。
