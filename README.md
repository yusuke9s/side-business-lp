# 事前登録LP 10本

広告で需要を測るための事前登録ページ（LP）です。

- `lp/` … 公開用のLP 10本（1ファイル完結。画像・アイコンはすべてHTML内に埋め込み済み）
  - pet / kaitai / eisei / koumuin / receipt / taikyo / watch / shibou / renai / souzoku
- `index.html` … 確認用の一覧ページ（公開しない）
- `build.py` … 一覧ページの生成と、各LPの文章データ（`LPS`）
- `src/` … LPを作ったときの元ファイル（現在は `lp/*.html` を直接編集しているため参考扱い）
- `DESIGN_BRIEF.md` / `ICON_BRIEF.md` … デザインの指示書
- `assets/licenses/` … 使用素材のライセンス

## 公開前に必要なこと

- 各LPの `FORM_ENDPOINT` に登録フォームの送信先（Formspree など）を設定する
- ページ下部の運営者名・連絡先を記入する
- head 内のコメント位置に計測タグを入れる
- ページ内で約束している特典（割引クーポン、無料期間など）を用意する
