# OpenCALM-chat-api


サイバーエージェントが公開した日本語LLM(OpenCALM)をHTTP APIから使うためのプログラムです。

https://www.cyberagent.co.jp/news/detail/id=28817

## 前提
GPUサーバ上でOpenCALMが動く環境が既に存在している必要があります。

以下の記事の手順を参考に構築してください。

https://qiita.com/tar_xzvf/items/09ee2bf146c4a3319492

## 設定
動作時に以下の設定値を適切に設定してください。 

| 項目名                 | 説明                      | 備考                       |
|---------------------|-------------------------|--------------------------|
| BASIC_AUTH_USERNAME | Basic認証のユーザ名            ||
| BASIC_AUTH_PASSWORD | Basic認証のパスワード           ||
| RUNNING_ON_GPU      | GPUがない環境で動作確認するためのオプション | GPUに関わらない部分の実装をするときなどに使う |

## 動作方法
```shell
git clone https://github.com/tar-xzvff/OpenCALM-chat-api.git
cd OpenCALM-chat-api
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0
```

curlでのリクエスト例です、Basic認証があるため認証した上でリクエストしてください。
```shell
$ curl -i -X POST \
>    -H "Content-Type:application/json" \
>    -H "Authorization:Basic dXNlcjpQQGFzc1cwcmQ=" \
>    -d \
> '{
>   "body": "Hello"
> }' \
>  'http://127.0.0.1:8000/api/chat'
HTTP/1.1 200 OK
date: Sun, 21 May 2023 00:12:17 GMT
server: uvicorn
content-length: 34
content-type: application/json

{"body":"This is dummy response."}
```