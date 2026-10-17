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

## 1. 登録フォームの受け取り先（Googleスプレッドシート）

受け取り用のスプレッドシート「事前登録（LP 10本）」は作成済み:
https://docs.google.com/spreadsheets/d/17Rl2FOktvatULDhblsSWhAqPo1OsJzz9bVN6SOHc4gQ/edit

1. スプレッドシートを開き、メニューの「拡張機能」→「Apps Script」
2. 最初から入っているコードを全部消して、`setup/apps-script.gs` の中身を貼り付けて保存
3. 右上の「デプロイ」→「新しいデプロイ」→ 種類「ウェブアプリ」
   - 次のユーザーとして実行：**自分** ／ アクセスできるユーザー：**全員**
   - 「デプロイ」を押し、アクセスを許可する（「確認されていません」と出たら「詳細」→「移動」）
4. 表示された「ウェブアプリのURL」（`https://script.google.com/macros/s/…/exec`）を
   `public/form-config.js` の `window.FORM_ENDPOINT = "";` の `""` に入れる（Claude に渡せば入れて保存します）

## 2. GitHub Pages で公開する

`.github/workflows/pages.yml` により、`main` に保存されるたびに `public/` が自動で公開される。

1. https://github.com/yusuke9s/side-business-lp/settings/pages を開く
2. 「Build and deployment」の Source を **GitHub Actions** にする
   - 非公開リポジトリで Pages が使えない（有料プランが必要）と表示された場合は、
     Settings → General の一番下「Change repository visibility」で Public にする
3. 「Custom domain」に `lp.site-forge.jp` を入れて Save、準備ができたら「Enforce HTTPS」にチェック

## 3. lp.site-forge.jp をつなぐ（DNS）

site-forge.jp の DNS を管理しているサービスで、次のレコードを1つ追加する。

| 種類 | 名前（ホスト） | 値（向き先） |
|---|---|---|
| CNAME | lp | `yusuke9s.github.io` |

数分〜数時間で `https://lp.site-forge.jp/pet` が開けるようになる。

## 4. 広告の計測タグ

各LPの `<head>` 内のコメント「計測タグ（Googleアナリティクス、Meta・TikTokのピクセル）は公開時にここへ入れる」の位置に入れる。
タグのIDを Claude に渡せば、10本まとめて入れます。

---

### 参考：Cloudflare Pages で公開する場合

GitHub Pages の代わりに Cloudflare Pages も使える。Workers & Pages → Pages → Git に接続 → `yusuke9s/side-business-lp`、
ビルドコマンドは空欄、出力ディレクトリは `public`。カスタムドメイン `lp.site-forge.jp` を追加し、DNS は CNAME `lp` → `<プロジェクト名>.pages.dev`。
