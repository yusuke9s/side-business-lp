# 事前登録LP 10本

広告で需要を測るための事前登録ページ（LP）です。

- `public/` … 公開するフォルダ（Cloudflare Pages の出力ディレクトリ）
  - LP 10本：pet / kaitai / eisei / koumuin / receipt / taikyo / watch / shibou / renai / souzoku（1ファイル完結。画像・アイコンはHTML内に埋め込み済み）
  - `privacy.html` … プライバシーポリシー
  - `form-config.js` … 登録フォームの送信先（全LP共通）
- `setup/` … 公開の手順（`SETUP.md`）と、フォーム受付用の Google Apps Script
- `index.html` … 確認用の一覧ページ（公開しない）
- `build.py` … 一覧ページの生成と、各LPの文章データ（`LPS`）
- `src/` … LPを作ったときの元ファイル（現在は `public/*.html` を直接編集しているため参考扱い）
- `DESIGN_BRIEF.md` / `ICON_BRIEF.md` … デザインの指示書
- `assets/licenses/` … 使用素材のライセンス

## 公開前に必要なこと

手順は `setup/SETUP.md` にまとめています。

- `public/form-config.js` に登録フォームの送信先（Google Apps Script のURL）を設定する
- Cloudflare Pages で公開し、`lp.site-forge.jp` をつなぐ
- head 内のコメント位置に計測タグを入れる
- ページ内で約束している特典（割引クーポン、無料期間など）を用意する
