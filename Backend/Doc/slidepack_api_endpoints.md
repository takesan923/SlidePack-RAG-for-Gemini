# APIエンドポイントのレファレンス

SlidePackのHTTP APIエンドポイントのレファレンスです。

## 認証

SlidePack HTTP APIはどのエンドポイントも認証が必要です。

リクエストヘッダにAPIトークンを含むことで認証します。

### 認証付きリクエストの例

```bash
curl "https://slidepack.io/sessions" \
  -H "Authorization: Bearer {API_TOKEN}"
```

APIトークンは [ダッシュボード](https://slidepack.io/app) で作成してください。

## セッションを作成する

セッションを作成し、ファイルアップロードに必要なAWS S3 Pre-Signed POSTパラメータを返します。

セッションを新規作成すると、レンダリングを実行していない古いセッションは削除されます。

すべてのセッションは、レンダリングを実行したものも含め、24時間で有効期限が切れます。

### リクエスト

**POST** `/sessions`

```bash
curl -X POST "https://slidepack.io/sessions" \
      -H 'Authorization: Bearer {API_TOKEN}'
```

### レスポンス

**201 Created**

```json
{
  "session": {
    "uuid": "f0155f9f-d3f3-4fa9-9f8d-70f8fd2f9c36",
    "created_at": "2020-08-13T13:14:32.000000Z",
    "rendered_at": null,
    "render_succeeded": null,
    "render_slide_count": null,
    "render_message": null
  },
  "upload": {
    "action": "https://slidepack-api.s3.ap-northeast-1.amazonaws.com",
    "method": "POST",
    "enctype": "multipart/form-data",
    "params": {
      "acl": "private",
      "key": "sessions/zip/f0155f9f-d3f3-4fa9-9f8d-70f8fd2f9c36.zip",
      "Content-Type": "application/zip",
      "X-Amz-Security-Token": "***",
      "X-Amz-Credential": "***",
      "X-Amz-Algorithm": "AWS4-HMAC-SHA256",
      "X-Amz-Date": "20200813T131432Z",
      "Policy": "***",
      "X-Amz-Signature": "***"
    }
  }
}
```

#### レスポンス項目

- **session** (object): 作成されたSessionオブジェクト
- **upload** (object): 入力zipファイルアップロードに利用するパラメータ

## セッションを一覧する

セッションの一覧を取得します。

### リクエスト

**GET** `/sessions`

```bash
curl "https://slidepack.io/sessions" \
    -H 'Authorization: Bearer {API_TOKEN}'
```

### レスポンス

**200 OK**

```json
{
  "sessions": [
    {
      "uuid": "805bcdc8-4782-4673-9d69-47f7ed0696c8",
      "created_at": "2020-08-13T15:10:15.000000Z",
      "rendered_at": "2020-08-13T15:10:20.000000Z",
      "render_succeeded": true,
    },
    {
      "uuid": "f0155f9f-d3f3-4fa9-9f8d-70f8fd2f9c36",
      "created_at": "2020-08-13T13:14:32.000000Z",
      "rendered_at": null,
      "render_succeeded": null,
    }
  ]
}
```

#### レスポンス項目

- **sessions** (object[]): Sessionオブジェクトのサブセットの配列

## セッションを取得する

一つのセッションの情報を取得します。

### リクエスト

**GET** `/sessions/{uuid}`

```bash
curl "https://slidepack.io/sessions/{uuid}" \
    -H 'Authorization: Bearer {API_TOKEN}'
```

### レスポンス

**200 OK**

```json
{
  "session": {
    "uuid": "f0155f9f-d3f3-4fa9-9f8d-70f8fd2f9c36",
    "created_at": "2020-08-13T13:14:32.000000Z",
    "rendered_at": null,
    "render_succeeded": null,
    "render_slide_count": null,
    "render_message": null
  },
  "upload": {
    "action": "https://slidepack-api.s3.ap-northeast-1.amazonaws.com",
    "method": "POST",
    "enctype": "multipart/form-data",
    "params": {
      "acl": "private",
      "key": "sessions/zip/f0155f9f-d3f3-4fa9-9f8d-70f8fd2f9c36.zip",
      "Content-Type": "application/zip",
      "X-Amz-Security-Token": "***",
      "X-Amz-Credential": "***",
      "X-Amz-Algorithm": "AWS4-HMAC-SHA256",
      "X-Amz-Date": "20200813T131432Z",
      "Policy": "***",
      "X-Amz-Signature": "***"
    }
  }
}
```

#### レスポンス項目

- **session** (object): Sessionオブジェクト
- **upload** (object): 入力zipファイルアップロードに利用するパラメータ

## ファイルをアップロードする

セッションの入力zipファイルをアップロードします。Pre-signed parametersを使って、Amazon S3の専用プライベートバケットに直接アップロードを行います。

入力zipファイルの最小構成は次のとおりです。

- `template.pptx` - テンプレートとなるパワーポイントファイル
- `data.json` - テンプレートに流し込むデータ

その他、画像や動画ファイルを同梱できます。zipファイル名は何でも構いません。

次のように `multipart/form-data` リクエストを構築します。

- URLはPOST /sessionsで得られた`upload.action`
- フィールド名および値にはPOST /sessions で得られた`upload.params`の全てのキーと値を含む
- `file`フィールドを末尾に追加し、アップロードしたいファイルを示す

フォームパラメータの有効期限は1時間です。有効期限が切れた場合、GET /sessions/{uuid}で新しいパラメータを発行できます。

### リクエスト

**POST** `{可変URL}`

```bash
curl -X POST "{URL}" \
  -F "{KEY}={VALUE}" \
  -F "{KEY}={VALUE}" \
     ...
  -F "file=@{ZIP_FILE_PATH}"
```

### レスポンス

**204 No Content**

## レンダリングを実行する

セッションをレンダリングしてpptxファイルを生成し、ダウンロード用のURLを返します。

`{uuid}` はセッションUUIDで置き換えてください。

予め入力zipファイルをアップロードしておく必要があります。

### リクエスト

**POST** `/sessions/{uuid}/render`

```bash
curl -X POST "https://slidepack.io/sessions/{uuid}/render" \
     -H 'Authorization: Bearer {API_TOKEN}'
```

### レスポンス

**200 OK**

```json
{
  "session": {
    "uuid": "f0155f9f-d3f3-4fa9-9f8d-70f8fd2f9c36",
    "created_at": "2020-08-13T13:14:32.000000Z",
    "rendered_at": "2020-08-13T13:16:18.000000Z",
    "render_succeeded": true,
    "render_slide_count": 5,
    "render_message": null
  },
  "download_url": "https://slidepack-api.s3.ap-northeast-1.amazonaws.com/..."
}
```

#### レスポンス項目

- **session** (object): Sessionオブジェクト
- **download_url** (string): レンダリング済みpptxファイルのダウンロードURL

ダウンロードURLの有効期限は5分です。有効期限が切れた場合、POST /sessions/{uuid}/download_url で新しいURLを発行できます。

## ダウンロードURLを再発行する

レンダリング済みpptxファイルのダウンロードURLを再発行します。

`{uuid}` はセッションUUIDで置き換えてください。

予めレンダリングを実行しておく必要があります。

### リクエスト

**POST** `/sessions/{uuid}/download_url`

```bash
curl -X POST "https://slidepack.io/sessions/{uuid}/render" \
     -H 'Authorization: Bearer {API_TOKEN}'
```

### レスポンス

**200 OK**

```json
{
  "session": {
    "uuid": "f0155f9f-d3f3-4fa9-9f8d-70f8fd2f9c36",
    "created_at": "2020-08-13T13:14:32.000000Z",
    "rendered_at": "2020-08-13T13:16:18.000000Z",
    "render_succeeded": true,
    "render_slide_count": 5,
    "render_message": null
  },
  "download_url": "https://slidepack-api.s3.ap-northeast-1.amazonaws.com/..."
}
```

#### レスポンス項目

- **session** (object): Sessionオブジェクト
- **download_url** (string): レンダリング済みpptxファイルのダウンロードURL

ダウンロードURLの有効期限は5分です。有効期限が切れた場合、このエンドポイントで再び新しいURLを発行できます。

## Sessionオブジェクト

### プロパティ

- **uuid** (string): セッションのユニークID
- **created_at** (string): 作成日時
- **rendered_at** (string or null): レンダリング日時。未レンダリングの場合は`null`
- **render_succeeded** (boolean or null): レンダリングが成功した場合は`true`、失敗した場合は`false`。未レンダリングの場合は`null`
- **render_slide_count** (integer or null): レンダリング成功時の実績スライド枚数。未レンダリングの場合は`null`
- **render_message** (string or null): レンダリング失敗時のエラーメッセージ。未レンダリングの場合、およびレンダリングが成功した場合は`null`

### Sessionオブジェクトの例

```json
{
  "uuid": "f0155f9f-d3f3-4fa9-9f8d-70f8fd2f9c36",
  "created_at": "2020-08-13T13:14:32.000000Z",
  "rendered_at": "2020-08-13T14:16:20.000000Z",
  "render_succeeded": true,
  "render_slide_count": 5,
  "render_message": null
}
```