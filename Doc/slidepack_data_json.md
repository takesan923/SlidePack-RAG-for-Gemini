# data.json レファレンス

`data.json`はSlidePackの入力zipファイルに必要な要素の一つで、流し込むデータやそのプロパティを定義します。

ここでは`data.json`で使用する各種オブジェクトの詳細を確認いただけます。各種オブジェクトの具体的な使い方に関しては[レンダリング例](https://docs.slidepack.io/ja/examples)も併せてご覧ください。

## rootオブジェクト

`data.json`のトップレベルはこのように構成してください。

### プロパティ

- **slides** (object[]・必須): Slideオブジェクトの配列。各要素がレンダリング結果PPTXで一枚のスライドになります。複数のSlideオブジェクトが同じテンプレートスライド番号を指すことができ、その場合、同じテンプレートスライドが複数回使用されます。
- **theme** (object・任意): プレゼンテーション全体に適用されるThemeオブジェクト。

### data.jsonのルートオブジェクト

```json
{
  "slides": [
    {
      "template": 1,
      "some_text": "配置する文章"
    },
    {
      "template": 2,
      "some_table": {
        "type": "table",
        "rows": [
          ["この", "行は", "ヘッダー"],
          ["この", "行は", "内容一行目"]
        ]
      }
    }
  ],
  "theme": {
    "colors": {
      "dk1": "#6c685f",
      "lt1": "#f5f2e3"
    }
  }
}
```

**注意**: 初期バージョンではJSONのトップレベルに直接スライドの配列を記述していました。現在でもその形式は利用可能ですが、次期バージョンで廃止予定です。

## Slideオブジェクト

Slideオブジェクト１つが、レンダリング後に１枚のスライドになります。

個々のSlideオブジェクトは辞書（マップ）であり、キーはプレースホルダー名、値はそこに流し込むデータです。

各キーごとに、SlidePackはスライド内の該当プレースホルダを探し、見つかれば値を埋めます。

`template`キーは必須です。このスライドのテンプレートとして利用すべきテンプレートスライド番号を指定します。

### プロパティ

- **template** (integer・必須): テンプレートスライド番号。

### Slideオブジェクト

```json
{
  "template": 1,
  "my_text": "配置したい文章",
  "more_text": {
    "type": "text",
    "value": "他の位置に配置したい文章",
    "hyperlink": "https://slidepack.io/"
  },
  "my_table": {
    "type": "table",
    "rows": [
      ["この", "行は", "ヘッダー"],
      ["この", "行は", "内容一行目"]
    ]
  }
}
```

## Textオブジェクト

Textオブジェクトはひとかたまりのテキストを表します。

主にこのような場面で利用します。

• テキストボックス内のプレースホルダ {placeholder} を置き換えるとき
• 表組みのセル内に流し込む文字列を指定するとき
• 箇条書きの項目として

### 文字列での簡易表現

オプション指定が不要の場合、Textオブジェクトの代わりに文字列を使用することができます。下記は同等です。

```json
"my_text": "我輩は猫である。"
```

```json
"my_text": {
  "type": "text",
  "value": "我輩は猫である。"
}
```

### プロパティ

- **type** (string "text"・必須)
- **value** (string・必須): 文字列の内容。
- **styles** (object・任意): Stylesオブジェクト。既存のスタイルを指定の値で上書きします。`styles.font`は文字列部分に適用され、`styles.shape`はシェイプ全体に適用されます。
- **hyperlink** (string・任意): URLを指定するとハイパーリンク化します。
- **level** (integer・任意): 箇条書き内でのインデントレベル。`0`（デフォルト）から`8`まで。Listオブジェクトの要素として使われたときのみ有効です。

### Textオブジェクト（最小の例）

```json
"my_placeholder": {
  "type": "text",
  "value": "吾輩は猫である。"
}
```

### Textオブジェクト（オプションつきの例）

```json
"my_placeholder": {
  "type": "text",
  "value": "吾輩は猫である。",
  "styles": {
    "font": {
      "size": 28,
      "color": "#000000",
      "underline": true,
      "italic": true
    },
    "shape": {
      "fill": "#E2E9F4",
      "outline": "758AA5",
      "align": "center",
      "vertical_align": "top"
    }
  },
  "hyperlink": "https://slidepack.io/"
}
```

## Tableオブジェクト

表組みにデータを流し込むときに使用します。

SlidePackはスライド内の表の代替テキストを読み取り、指定のキーと一致する表にデータを流し込みます。代替テキストを編集するには、PowerPointで表を右クリックし、代替テキストを編集を選びます。

各セルの値はTextオブジェクトまたは文字列です。

テンプレート側の表組みと配列の大きさが異なる場合、表組みの行や列が追加・削除されます。

### プロパティ

- **type** (string "table"・必須)
- **rows** (string[][] or object[][]・必須): セルの値の二次元配列。各値はTextオブジェクトあるいは文字列（混合でも問題ありません）。
- **rows[n][m]** (string or object・任意): n行m列のセルの値。
- **rows[n][m].databar** (object・任意): 指定するとセルにデータバーを描画します。
- **rows[n][m].databar.ratio** (number・任意): データバーの長さ。`0.0`から`1.0`。
- **rows[n][m].databar.color** (number・任意): データバーの色。
- **horizontal_sizing** (string enum・任意): セル増減時の水平方向のリサイズ挙動。
  - `fixed`（デフォルト） - 表組みの幅を維持し、収まるように各セルの横幅を調整します。
  - `anchor_left` - 表組みの左端の位置を維持し、右方向に伸縮します。
  - `anchor_right` - 表組みの右端のいちを維持し、左方向に伸縮します。
- **vertical_sizing** (string enum・任意): セル増減時の垂直方向のリサイズ挙動。
  - `fixed` - 表組みの高さを維持し、収まるように各セルの高さを調整します。
  - `anchor_top`（デフォルト） - 表組みの上端の位置を維持し、下方向に伸縮します。
  - `anchor_bottom` - 表組みの下端の位置を維持し、上方向に伸縮します。

### Tableオブジェクト（最小の例）

```json
"my_table_alt_text": {
  "type": "table",
  "rows": [
    ["タイトル", "アーティスト", "アルバム"],
    ["So What", "Miles Davis", "Kind of Blue"],
    ["Take Five", "Dave Brubeck", "Time Out"]
  ]
}
```

### Tableオブジェクト（オプションつきの例）

```json
"my_table_alt_text": {
  "type": "table",
  "rows": [
    ["タイトル", "アーティスト", "アルバム"],
    [
      {
        "type": "text",
        "value": "So What",
        "styles": {
          "font": {
            "bold": true
          },
          "shape": {
            "align": "justified"
          }
        }
      },
      { "type": "text", "value": "Miles Davis" },
      { "type": "text", "value": "Kind of Blue" }
    ],
    [
      { "type": "text", "value": "Take Five" },
      { "type": "text", "value": "Dave Brubeck" },
      { "type": "text", "value": "Time Out" }
    ]
  ],
  "horizontal_sizing": "fixed",
  "vertical_sizing": "anchor_top"
}
```

## Chartオブジェクト

グラフ（チャート）に系列データを流し込むときに使用します。

現在対応している表の種類は棒グラフ、線グラフ、面グラフ、円グラフです。

散布図にも対応していますが、データ形式が異なります。

SlidePackはスライド内のグラフの代替テキストを読み取り、指定のキーと一致するグラフにデータを流し込みます。代替テキストを編集するには、PowerPointでグラフを右クリックし、代替テキストを編集を選びます。

### プロパティ

- **type** (string "chart"・必須)
- **labels** (string[]・任意): 項目ラベルとして表示する文字列の配列。通常、横軸沿いに表示されます。
- **labels_interval** (integer・任意): 文字列型項目ラベルの表示間隔。例えば`3`の場合、`labels`のうち3つに1つだけが表示され、残りはスキップされます。
- **date_labels** (integer[]・任意): 項目ラベルとして表示する日付を数値で表した配列。`labels`の代わりにこちらを指定することで、日付軸項目ラベルに切り替わります。各値はExcelの日付数値、つまり1900年1月1日からの日数を表した整数です。例えば2022年11月11日は`44881`になります。
- **date_labels_format** (string・任意): 日付軸項目ラベルの表示形式コード。`"yyyy/mm/dd"` など。詳細は[MS Officeのドキュメント](https://support.microsoft.com/ja-JP/search/results?query=%E6%97%A5%E4%BB%98%20%E6%99%82%E5%88%BB%20%E6%95%B0%E5%80%A4%E3%81%AE%E6%9B%B8%E5%BC%8F)を参照ください。
- **date_labels_major_unit** (int・任意): 日付軸項目ラベルの表示間隔を`date_labels_major_time_unit`との組み合わせで指定します。例えば `2` と `"months"` なら二ヶ月おきにラベルが表示されます。
- **date_labels_major_time_unit** (string enum・任意): `"days"`, `"months"`, `"years"` のいずれか。
- **axis1** (object・必須): 第1軸のデータ。
- **axis1.series** (object・必須): 系列データのコレクション。キーは系列名、値は系列データ。
- **axis1.series.{key}** (object・任意): 系列データ。テンプレートのグラフにキーと同名の系列がある場合、その系列が上書きされます。ない場合は新たな系列が作成されます。
- **axis1.series.{key}.name** (string・必須): 系列の新しい名前。凡例などに反映されます。
- **axis1.series.{key}.values** (number[]・必須): 系列の数値の配列。
- **axis1.series.{key}.styles** (object・任意): 系列全体に適用するStylesオブジェクト。
- **axis1.series.{key}.data_point_styles** (object[]・任意): 個々のデータポイントに適用するStylesオブジェクトの配列。`values`配列の同インデックスの値にスタイルを適用します。元のスタイルを維持したい要素については `null` を指定します。
- **axis1.bounds** (object・任意): 値軸の表示範囲。
- **axis1.bounds.minimum** (number・任意): 値軸の表示範囲の最小値。
- **axis1.bounds.maximum** (number・任意): 値軸の表示範囲の最大値。
- **axis1.format** (string・任意): 値軸のラベルの表示形式コード。`"0.0%"` and `"#,#0.0"`など。詳細は[MS Officeのドキュメント](https://support.microsoft.com/ja-JP/search/results?query=%E8%A1%A8%E7%A4%BA%E5%BD%A2%E5%BC%8F%E3%81%AE%E6%9B%B8%E5%BC%8F%E8%A8%98%E5%8F%B7)を参照ください。
- **axis1.major_unit** (number・任意): 値軸のラベルの表示間隔。
- **axis2** (object・任意): 第2軸のデータ。形式は`axis1`と同じです。

### styles と data_point_styles の効果対象

| グラフの種類 | shape.fill | shape.outline |
|------------|-----------|---------------|
| 棒グラフ | 棒の塗り | 棒の枠線 |
| 線グラフ | マーカーの塗り | グラフ線とマーカーの枠線 |
| 面グラフ | 面の塗り | 面の枠線 |

### Chartオブジェクト（最小の例）

```json
"my_chart_alt_text": {
  "type": "chart",
  "labels": ["Q1", "Q2", "Q3", "Q4"],
  "axis1": {
    "series": {
      "my_series_key": {
        "name": "売上",
        "values": [100, 130, 120, 130]
      }
    }
  }
}
```

### Chartオブジェクト（オプションつきの例）

```json
"my_chart_alt_text": {
  "type": "chart",
  "labels": ["Q1", "Q2", "Q3", "Q4"],
  "labels_interval": 2,
  "axis1": {
    "bounds": {
      "minimum": 50,
      "maximum": 150
    },
    "format": "#,#.0",
    "interval": 20,
    "series": {
      "ser1": {
        "name": "売上",
        "values": [100, 130, 120, 130]
      },
      "ser2": {
        "name": "経費",
        "values": [85, 90, 80, 75]
      }
    }
  },
  "axis2": {
    "series": {
      "ser3": {
        "name": "利益率",
        "values": [0.15, 0.3, 0.33, 0.42],
        "styles": {
          "shape": { "fill": "ffdd99", "outline": "ffaa55" }
        },
        "data_point_styles": [
          null,
          null,
          { "shape": { "fill": "ff0000" } },
          null
        ]
      }
    }
  }
}
```

## Scatter Chart オブジェクト

散布図に系列データを流し込むときに使用します。

SlidePackはスライド内のグラフの代替テキストを読み取り、指定のキーと一致するグラフにデータを流し込みます。代替テキストを編集するには、PowerPointでグラフを右クリックし、代替テキストを編集を選びます。

### プロパティ

- **type** (string "scatter-chart"・必須)
- **axis1** (object・必須): 第1軸のデータ。
- **axis1.series** (object・必須): 系列データのコレクション。キーは系列名、値は系列データ。
- **axis1.series.{key}** (object・任意): 系列データ。テンプレートグラフ内にキーと同名の系列がある場合、その系列データが上書きされます。ない場合は新たな系列が作成されます。
- **axis1.series.{key}.name** (string・必須): 系列の新しい名前。凡例などに反映されます。
- **axis1.series.{key}.values** ([number, number][]・必須): 系列の数値の配列。個々の要素は `[x値, y値]` のタプルです。
- **axis1.series.{key}.styles** (object・任意): 系列全体に適用するStylesオブジェクト。
- **axis1.series.{key}.data_point_styles** (object[]・任意): 個々のデータポイントに適用するStylesオブジェクトの配列。`values`配列の同インデックスの値にスタイルを適用します。元のスタイルを維持したい要素については `null` を指定します。
- **axis1.x_bounds** (object・任意): X軸の表示範囲。
- **axis1.x_bounds.minimum** (number・任意): X軸の表示範囲の最小値。
- **axis1.x_bounds.maximum** (number・任意): X軸の表示範囲の最大値。
- **axis1.x_format** (string・任意): X軸のラベルの表示形式コード。`0.0%` and `#,#0.0`など。詳細は[MS Officeのドキュメント](https://support.microsoft.com/ja-JP/search/results?query=%E8%A1%A8%E7%A4%BA%E5%BD%A2%E5%BC%8F%E3%81%AE%E6%9B%B8%E5%BC%8F%E8%A8%98%E5%8F%B7)を参照ください。
- **axis1.x_major_unit** (number・任意): X軸のラベルの表示間隔。
- **axis1.y_bounds** (object・任意): Y軸の表示範囲。
- **axis1.y_bounds.minimum** (number・任意): Y軸の表示範囲の最小値。
- **axis1.y_bounds.maximum** (number・任意): Y軸の表示範囲の最大値。
- **axis1.y_format** (string・任意): Y軸のラベルの表示形式コード。`0.0%` and `#,#0.0`など。詳細は[MS Officeのドキュメント](https://support.microsoft.com/ja-JP/search/results?query=%E8%A1%A8%E7%A4%BA%E5%BD%A2%E5%BC%8F%E3%81%AE%E6%9B%B8%E5%BC%8F%E8%A8%98%E5%8F%B7)を参照ください。
- **axis1.y_major_unit** (number・任意): Y軸のラベルの表示間隔。
- **axis2** (object・任意): 第2軸のデータ。形式は`axis1`と同じです。

### Scatter Chartオブジェクト（最小の例）

```json
"my_scatter_chart_alt_text": {
  "type": "scatter-chart",
  "axis1": {
    "series": {
      "my_series_key": {
        "name": "発生値",
        "values": [
          [7.1, 5.1],
          [3.4, 6.9],
          [2.6, 2.6],
          [4.0, 8.1],
          [2.8, 4.5]
        ]
      }
    }
  }
}
```

### Scatter Chartオブジェクト（オプションつきの例）

```json
"my_scatter_chart_alt_text": {
  "type": "scatter-chart",
  "axis1": {
    "x_bounds": { "minimum": 0, "maximum": 10 },
    "x_format": "#,#0.00",
    "x_major_unit": 1.0,
    "y_bounds": { "minimum": 0, "maximum": 10 },
    "series": {
      "my_series_one": {
        "name": "天然",
        "values": [
          [7.1, 5.1],
          [3.4, 6.9],
          [2.6, 2.6],
          [4.0, 8.1],
          [2.8, 4.5]
        ]
      }
    }
  },
  "axis2": {
    "series": {
      "my_series_two": {
        "name": "養殖",
        "values": [
          [4.6, 5.3],
          [5.2, 3.6],
          [6.0, 2.8],
          [6.3, 6.5],
          [8.2, 4.4]
        ],
        "styles": {
          "shape": { "fill": "ffdd99", "outline": "ffaa55" }
        },
        "data_point_styles": [
          null,
          null,
          { "shape": { "fill": "ff0000" } },
          null,
          null
        ]
      }
    }
  }
}
```

## Listオブジェクト

箇条書きにデータを流し込むのに使います。

テキストボックス内のプレースホルダ {placeholders} を箇条書きに変換します。

個々の項目はTextオブジェクトまたは文字列です。フォントスタイルを `values[n].styles.font` で設定できます。`values[n].styles.shape` は無視されます。

### プロパティ

- **type** (string "list"・必須)
- **values** (string[] or object[]・必須): 箇条書きの項目の配列。各値はTextオブジェクトあるいは文字列（混合でも問題ありません）。
- **values[n].level** (integer・任意): 箇条書き内でのインデントレベル。`0`（デフォルト）から`8`まで。

### Listオブジェクト（最小の例）

```json
"my-list-placeholder": {
  "type": "list",
  "values": [
    "吾輩は猫である",
    "坊っちゃん",
    "三四郎"
  ]
}
```

### Listオブジェクト（オプションつきの例）

```json
"my-list-placeholder": {
  "type": "list",
  "values": [
    {
      "value": "吾輩は猫である",
      "level": 1
    },
    {
      "value": "坊っちゃん",
      "level": 2
    },
    {
      "value": "三四郎",
      "level": 2,
      "styles": {
        "font": {
          "bold": true,
          "color": "#2a4598"
        }
      }
    }
  ]
}
```

## Imageオブジェクト

スライドに画像を埋め込むのに使います。

スライド内のプレースホルダ {placeholders} を含むテキストボックスや図形を画像で置換します。

### プロパティ

- **type** (string "image"・必須)
- **src** (string・必須): 画像ファイルをzip内に格納し、`data.json`があるディレクトリからの相対パスを指定してください。対応形式は `jpg`, `jpeg`, `gif`, `png` です。
- **scaling** (string enum・任意): 画像の配置サイズ挙動。
  - `none`（デフォルト） - 画像本来の大きさのまま配置します。
  - `contain` - 画像全体が置換先の図形いっぱいに収まる大きさで配置します。
  - `cover` - 画像が置換先の図形を覆い隠す大きさで配置します。図形から画像がはみ出すことがあります。
- **overflow** (string enum・任意): 画像のはみ出しの挙動。
  - `visible`（デフォルト） - 画像を切り取りません。置換先の図形からはみ出した部分も表示されます。
  - `hidden` - 置換先の図形からはみ出した部分は切り取られ非表示になります。

### Imageオブジェクト

```json
"my-image-placeholder": {
  "type": "image",
  "src": "images/home-office.jpg",
  "scaling": "contain",
  "overflow": "hidden"
}
```

## Videoオブジェクト

スライドに動画を埋め込むのに使います。

プレースホルダ {placeholders} を含むテキストボックスや図形を、指定の動画で置換します。

動画のコーデックよってはPowerPointで再生できない可能性があります。Microsoftによる推奨コーデックはH.264動画及びAAC音声です。

### プロパティ

- **type** (string "video"・必須)
- **src** (string・必須): 動画ファイルへのパスまたはYouTubeの動画URL。動画ファイルの場合、zip内に格納し、`data.json`があるディレクトリからの相対パスを指定してください。対応形式は `mp4`, `m4v`, `mov` です。
- **thumbnail** (string・任意): 動画が再生されるまでの間に表示される画像。ローカル動画ファイルの場合は必須。動画自体と同じ縦横比の画像を使用してください。画像ファイルをzip内に格納し、`data.json`があるディレクトリからの相対パスを指定してください。対応形式は `jpg`, `jpeg`, `gif`, `png` です。
- **scaling** (string enum・任意): 動画の配置サイズ挙動。
  - `contain`（デフォルト） - 動画全体が置換先の図形いっぱいに収まる大きさで配置します。
  - `cover` - 動画が置換先の図形を覆い隠す大きさで配置します。図形から動画がはみ出すことがあります。

### Videoオブジェクト

```json
"my-video-placeholder": {
  "type": "video",
  "src": "demo-reel.mp4",
  "thumbnail": "thumb.png",
  "scaling": "contain"
}
```

## Stylesオブジェクト

様々な要素に色やフォントスタイルを適用するのに使います。

実際の効果は対象のオブジェクトによって異なります。例えばTextオブジェクトに対して `shape.outline` を指定するとそのテキストが入った図形の枠線の色が変わりますが、棒グラフのChartオブジェクトに対してだとグラフのバーの枠線の色が変わります。

対象によっては効果がないプロパティもあります。例えばグラフのデータポイントに対して `shape.align` を指定しても効果がありません。

詳細は各オブジェクトの説明を御覧ください。

### プロパティ

- **font** (object・任意): フォントに関するスタイル。
- **font.typeface** (string・任意): 文字の書体。`"Arial"` や `"Calibri"`など。
- **font.size** (number・任意): 文字の大きさ（単位はポイント）。
- **font.color** (string・任意): 文字の色。
- **font.underline** (boolean・任意): 文字に下線を引きます。
- **font.bold** (boolean・任意): 文字を太字にします。
- **font.italic** (boolean・任意): 文字を斜体にします。
- **font.strike** (boolean・任意): 文字に打ち消し線を引きます。
- **shape** (object・任意): 図形に関するスタイル。
- **shape.outline** (string・任意): 図形の枠線の色。
- **shape.fill** (string・任意): 図形の塗りの色。
- **shape.align** (string enum・任意): 図形内の横方向の文字揃え。`left`, `center`, `right`, `justified`, `distributed` のいずれか。
- **shape.vertical_align** (string enum・任意): 図形内の縦方向の文字揃え。`top`, `center`, `bottom` のいずれか。

### Stylesを指定したTextオブジェクトの例

```json
"my-text-placeholder": {
  "type": "text",
  "value": "吾輩は猫である",
  "styles": {
    "font": {
      "typeface": "Times New Roman",
      "size": 28,
      "color": "#000000",
      "underline": true,
      "italic": true,
      "bold": true,
      "strike": true
    },
    "shape": {
      "outline": "accent1",
      "fill": "lavender",
      "align": "center",
      "vertical_align": "bottom"
    }
  }
}
```

## Themeオブジェクト

全スライドに適用されるテーマの色設定を変更するのに使います。

PowerPointのテーマには12の名前付きの色があります。

それぞれが指し示す色をThemeオブジェクトで指定できます。

ここでは `"#ff0000"` のようなHexカラーコードまたは `"snow"` のような色名を使ってください。テーマカラーを指定するのにテーマカラー名を使うことはできません。

無指定のもの、空文字列 `""` を指定したもの、`null`を指定したものはテンプレートでの色設定が維持されます。

### プロパティ

- **colors** (object・任意): テーマの色設定
- **colors.lt1** (string・任意): テーマの色「テキスト/背景: 淡色 1」。通常はこれがスライド背景色です。
- **colors.dk1** (string・任意): テーマの色「テキスト/背景: 濃色 1」。通常はこれが文字色です。
- **colors.lt2** (string・任意): テーマの色「テキスト/背景: 淡色 2」。
- **colors.dk2** (string・任意): テーマの色「テキスト/背景: 濃色 2」。
- **colors.accent1** (string・任意): テーマの色「アクセント 1」。
- **colors.accent2** (string・任意): テーマの色「アクセント 2」。
- **colors.accent3** (string・任意): テーマの色「アクセント 3」。
- **colors.accent4** (string・任意): テーマの色「アクセント 4」。
- **colors.accent5** (string・任意): テーマの色「アクセント 5」。
- **colors.accent6** (string・任意): テーマの色「アクセント 6」。
- **colors.hlink** (string・任意): テーマの色「ハイパーリンク」。
- **colors.folHlink** (string・任意): テーマの色「表示済みのハイパーリンク」。

### Themeオブジェクト

```json
{
  "colors": {
    "lt1": "F5F2E3",
    "dk1": "6c685f",
    "lt2": "#CAD9EA",
    "dk2": "#5c6875",
    "accent1": "6b95a4",
    "accent2": "c9747f",
    "accent3": "7e9a62",
    "accent4": "tan",
    "accent5": "",
    "accent6": null,
    "hlink": "858499"
  }
}
```

## 要素の削除

プレースホルダーのキーに対して`{ "delete": true }`をアサインすることで、スライド内の要素を削除できます。

### スライドからオブジェクトを削除する

```json
"my_placeholder": {
  "delete": true
}
```

• プレースホルダがテキストボックス内にある場合、テキストボックス自体が削除されます。
• プレースホルダが表組み内にある場合、そのセルが空になります。
• 該当する代替テキストを持つ表組みやグラフがある場合、削除されます。

## 色

文字や塗りの色を指定するときにはHexカラーコードか色名が使用できます。

**Hexカラーコード** は `#f6ad5c` や `FF0000` のような文字列です。先頭の `#` はあってもなくても構いません。大文字小文字の区別はありません。

**色名** は `lt1`, `dk1`, `lt2`, `dk2`, `accent1`, `accent2`, `accent3`, `accent4`, `accent5`, `accent6`, `hlink`, `folHlink` のいずれかで、テーマで設定された12色に相当します。それぞれの名前が指し示す具体的な色をカスタマイズするには、rootオブジェクトで `theme` を設定してください。

また、下記のカラーコードが使用可能です。これらのコードは [HTMLの色名](https://ja.wikipedia.org/wiki/%E3%82%A6%E3%82%A7%E3%83%96%E3%82%AB%E3%83%A9%E3%83%BC#HTML%E3%81%A7%E3%81%AE%E8%89%B2%E5%90%8D%E7%A7%B0) と似ていますが、大文字小文字の区別など細かい点が異なるので注意してください。

black dkSlateGray dimGray slateGray gray ltSlateGray dkGray silver ltGray gainsboro mistyRose antiqueWhite linen beige whiteSmoke lavenderBlush oldLace aliceBlue ltCyan seaShell ghostWhite honeydew floralWhite azure mintCream snow ivory white medVioletRed deepPink paleVioletRed hotPink ltPink pink dkRed red firebrick crimson indianRed ltCoral salmon dkSalmon ltSalmon orangeRed tomato dkOrange coral orange dkKhaki gold khaki peachPuff yellow paleGoldenrod moccasin papayaWhip ltGoldenrodYellow lemonChiffon ltYellow maroon brown saddleBrown sienna chocolate dkGoldenrod peru rosyBrown goldenrod sandyBrown tan burlyWood wheat navajoWhite bisque blanchedAlmond cornsilk dkGreen green dkOliveGreen forestGreen seaGreen olive oliveDrab medSeaGreen limeGreen lime springGreen medSpringGreen dkSeaGreen medAquamarine yellowGreen lawnGreen chartreuse ltGreen greenYellow paleGreen teal dkCyan ltSeaGreen cadet