# 公開の手順

公開するのは `public/` フォルダの中身だけです（LP 10本、プライバシーポリシー、フォームの設定ファイル）。
リポジトリ直下の `index.html`（確認用の一覧）などは公開されません。

公開後のURL（予定）:

| サービス | URL |
|---|---|
| うちの子アトリエ | https://lp.site-forge.jp/pet |
| 解体見積メーカー | https://lp.site-forge.jp/kaitai |
| 衛生管理者 合格ドリル | https://lp.site-forge.jp/eisei |
| 公務員面接トレーナー | https://lp.site-forge.jp/koumuin |
| レシートまるごと申告 | https://lp.site-forge.jp/receipt |
| 退去前チェックパック | https://lp.site-forge.jp/taikyo |
| ページ見張り番 | https://lp.site-forge.jp/watch |
| 志望理由書コーチ | https://lp.site-forge.jp/shibou |
| メンズ恋愛ナビ | https://lp.site-forge.jp/renai |
| 相続やることナビ | https://lp.site-forge.jp/souzoku |
| プライバシーポリシー | https://lp.site-forge.jp/privacy |

---

## 1. 登録フォームの受け取り先を作る（Googleスプレッドシート・約3分）

1. Googleスプレッドシートを新しく作る（名前は「事前登録」など）
2. メニューの「拡張機能」→「Apps Script」を開く
3. 最初から入っているコードを全部消して、`setup/apps-script.gs` の中身を貼り付けて保存
4. 右上の「デプロイ」→「新しいデプロイ」
   - 種類の選択（歯車）→「ウェブアプリ」
   - 次のユーザーとして実行：**自分**
   - アクセスできるユーザー：**全員**
   - 「デプロイ」を押し、Googleアカウントへのアクセスを許可する
     （「このアプリは確認されていません」と出たら「詳細」→「（安全ではないページ）に移動」）
5. 表示された「ウェブアプリのURL」（`https://script.google.com/macros/s/…/exec`）をコピーする
6. そのURLを `public/form-config.js` の `window.FORM_ENDPOINT = "";` の `""` の中に入れる
   （URLを Claude に渡せば、こちらで入れて保存します）

登録があると、スプレッドシートの「登録」シートに1行ずつ追加されます。
「ページ」「URLパラメータ」の列で、どの広告から来た登録かが分かります（広告のURLに `?utm_source=instagram` などを付ける）。

## 2. Cloudflare Pages で公開する（約5分）

1. https://dash.cloudflare.com にログイン（アカウントが無ければ無料で作る）
2. 左メニュー「Workers & Pages」→「作成」→「Pages」→「Git に接続」
3. GitHub を連携し、リポジトリ `yusuke9s/side-business-lp` を選ぶ
4. ビルドの設定
   - フレームワーク プリセット：**なし**
   - ビルド コマンド：**空欄**
   - ビルド出力ディレクトリ：**public**
5. 「保存してデプロイ」→ `https://<プロジェクト名>.pages.dev/pet` で表示を確認

以後、GitHub の `main` に保存されるたびに自動で公開ページが更新されます。

## 3. lp.site-forge.jp をつなぐ

1. Cloudflare Pages のプロジェクト →「カスタムドメイン」→「カスタムドメインを設定」→ `lp.site-forge.jp` を入力
2. site-forge.jp の DNS を管理しているサービスで、次のレコードを追加する
   （DNS を Cloudflare で管理している場合は、この手順は自動で行われる）

   | 種類 | 名前（ホスト） | 値（向き先） |
   |---|---|---|
   | CNAME | lp | `<プロジェクト名>.pages.dev` |

3. 数分〜数時間で `https://lp.site-forge.jp/pet` が開けるようになる（SSL は自動）

## 4. 広告の計測タグ

各LPの `<head>` 内のコメント「計測タグ（Googleアナリティクス、Meta・TikTokのピクセル）は公開時にここへ入れる」の位置に入れます。
タグのIDが用意できたら Claude に渡せば、10本まとめて入れます。
