# LPリデザイン共通ブリーフ

## 背景
事前登録LP 10本を、広告から来た人が「おっ」と思う水準に作り直す。前の版は文字だけの汎用テンプレートで、オーナーから「図も画像もSVGもない、最低以下」と強く指摘された。参考にするのは、日本の大手企業キャンペーンサイトの水準:

- **参考1（宅配便のキャンペーン）**: 全面イエロー×ブラック。人物写真のコラージュ、地図や都市名の柄を敷いた背景、黒い帯の見出しボックス、動画サムネイルのグリッド、QRコード、カレンダーなど要素がぎっしり。力強い。
- **参考2（プラント企業の採用）**: 青一色の世界観。設計図の罫線・寸法線が背景に走り、手で線を引くイラスト、写真を斜めに切ったセクション、円グラフの図解、世界地図にピン。
- **参考3（歯磨き粉GUM）**: 濃い緑の映画的なヒーロー。白衣の研究者、太い見出しを帯で強調、原因を分解した図解（菌→歯周病→口臭のフロー）、ダークトーンの中に白いカード。

共通点: 一色の強い世界観、全面を使う背景（柄・罫線・グリッド）、斜めやコラージュのレイアウト、大きな見出しを帯や箱で強調、図解で説明、人物や物のビジュアルが主役。

## 絶対条件
1. **1ファイル完結の HTML**（`<!doctype html>` から書く）。出力先は `/home/user/lp-site/lp/<slug>.html`（上書き）。
2. **画像素材は `/home/user/lp-site/assets/` にあるものを使う**（外部の画像サイトには接続できない）。ライセンスは `assets/licenses/README.md` のとおり商用利用可。
   - `assets/fluent3d/<コードポイント>.webp` : Microsoft Fluent Emoji 3D（256×256、立体的な高品質レンダリング）。ファイル名は絵文字のコードポイント（例 `1f431.webp`=猫の顔、`1f436.webp`=犬の顔、`1f3d7-fe0f.webp`=建設中のビル、`1f9fe.webp`=レシート、`1f514.webp`=ベル、`1f393.webp`=卒業帽、`1f4c5.webp`=カレンダー、`1f3db-fe0f.webp`=古典建築、`1f4ac.webp`=吹き出し、`1f381.webp`=ギフト、`1f384.webp`=ツリー、`1f3a8.webp`=パレット、`1f4e1.webp`=アンテナ、`1f440.webp`=目、`1f46a.webp`=家族、`1f4dd.webp`=メモ、`23f3.webp`=砂時計、`1f6a7.webp`=工事中、`1f69a.webp`=トラック、`1f9f1.webp`=レンガ、`1f528.webp`=ハンマー、`1f4da.webp`=本、`1f4af.webp`=100点、`1f3c6.webp`=トロフィー、`1f4f1.webp`=スマホ、`1f490.webp`=花束、`2615.webp`=コーヒー、`1f3e0.webp`=家、`1f511.webp`=鍵、`1f4f8.webp`=カメラ、`1f9f9.webp`=ほうき、`1f6aa.webp`=ドア、`1f4b0.webp`=お金の袋、`1f4c4.webp`=書類、`1f4cb.webp`=クリップボード、`2705.webp`=チェック、`1f4c8.webp`=上昇グラフ、`1f56f-fe0f.webp`=ろうそく、`1f3eb.webp`=学校、`1f4e9.webp`=封筒）。他も `ls assets/fluent3d | grep <コードポイント>` で探せる。ページからは `../assets/fluent3d/xxx.webp` の相対パスで `<img>` 参照する（`alt` を付ける、`width`/`height` 指定）。浮遊・回転・弾むなどの動きを付けて、コラージュの主役に使う。
   - `assets/undraw/<名前>.svg` : unDraw の人物・場面イラスト（1,740点、ファイル名が英語の内容。`ls assets/undraw | grep -i <キーワード>` で探す。例: pet-adoption, cat, dog, dog-walking, construction-workers, under-construction, build-your-home, exam-prep, studying, online-test, interview, job-hunt, receipt, printing-invoices, finance, personal-finance, moving, apartment-rent, house-searching, notifications, push-notifications, monitor, alert, file-search, education, graduation, essay-writing, writing-down-ideas, in-love, love-messages, chatting, texting, family, documents, calendar, checklist, signed-document）。アクセント部分は `currentColor` なので、**SVGの中身をページにインラインで貼り込み**、親要素の `color` をブランド色にすると色が合う。インラインにすると部分ごとに動かせる。
   - これに加えて、背景の柄、図解、装飾、ページ固有のモチーフ（設計図の線、地図、チャート、帯など）は自分でSVG/CSSで描く。1ページあたり大きなビジュアルを最低3つ（ヒーロー、中盤の図解、締め）。素材を貼るだけで終わらせず、コラージュ・切り抜き風の枠・影・重ね合わせで「作り込んだ」見た目にする。
3. 外部リソースは Google Fonts（日本語フォント）と、必要なら cdnjs の GSAP（`https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js` と `ScrollTrigger.min.js`）だけ。使わなくても良い（素の CSS アニメーション＋IntersectionObserver で十分）。
4. **動きをふんだんに**。最低でも:
   - ヒーローの入場アニメーション（要素が順番に出る、イラストのパーツが動く）
   - SVGの線が描かれるアニメーション（stroke-dasharray / dashoffset）
   - スクロールで要素が出てくる演出（フェード＋スライド、斜めのワイプなど）
   - 常に動いている要素（ループ: 浮遊、点滅、回転、流れるテキスト帯＝マーキー）
   - 数字のカウントアップか、順番に表示されるシーケンス
   - ボタンやカードのホバー
   - `prefers-reduced-motion: reduce` のときは動きを止める
   - **アニメーションの初期状態（opacity:0 など）は JS が `html` に `.js` クラスを付けたときだけ適用**し、JS が無くても全部見える状態にする
5. **スマホ（幅390px）で横スクロールが出ないこと**。ヒーローはスマホでも迫力を保つ（イラストを縮めるだけでなく配置を組み替える）。
6. 明るい背景でも暗い背景でも、文字のコントラストを確保する。
7. **嘘を書かない**: 架空のお客様の声、架空の利用者数・実績、架空の企業ロゴ、架空の受賞は禁止。画面の例や数字の例には「表示例」と書く。メディア掲載なども書かない。
8. 文章（見出し・説明・悩み・機能・使い方・料金・特典・FAQ）は `/home/user/lp-site/build.py` の `LPS` に入っている内容を使う。見せ方に合わせて短く言い換えたり、図解用のラベルを足すのは良いが、**料金・特典・FAQの約束ごとは変えない**（特に免責のFAQ）。
9. **登録フォームは今の仕組みをそのまま使う**: `/home/user/lp-site/_template/<slug>.html` の `<section ... id="signup">` 内のフォーム（id: `signup-form`, `signup-email`, `signup-q`, `signup-error`, `signup-thanks`, `signup-preview`）と、末尾の `<script>`（FORM_ENDPOINT の処理）を流用する。見た目はページに合わせて作り直して良い。ページ内のCTAボタンはすべて `#signup` へ。ページ下部の運営者・連絡先のプレースホルダーも残す。
10. ヘッダーにロゴ（サービス名をSVGか文字で）と「事前登録受付中」。スマホではCTAが常に押せる追従ボタン（画面下固定、セーフエリア考慮）を付ける。
11. 計測タグ用のコメント `<!-- 計測タグ（Googleアナリティクス、Meta・TikTokのピクセル）は公開時にここへ入れる -->` を head に残す。
12. 写真に差し替えやすいよう、主役イラストを置いた箇所には `<!-- 写真差し替え候補: ○○ -->` とコメントを残す。
13. 最後に、ページで実際に参照した素材ファイルのパス一覧（`assets/...`）を報告に含める（公開時にそのファイルだけ一緒に出すため）。

## 仕上げの確認
書き終えたら、Playwright で1回だけ確認する（`NODE_PATH=$(npm root -g) node script.js`、ブラウザは `executablePath: '/opt/pw-browsers/chromium'`）。
- 幅1280と390で、ファーストビューと全体（fullPage）のスクリーンショットを撮って目で見る
- 390幅で `document.documentElement.scrollWidth` が390を超えないこと
- コンソールエラーが無いこと
見つかった崩れは1回直す。スクリプトとスクリーンショットは `/tmp/claude-0/-home-user/ad4455f4-46cf-5930-83c4-b27dc7020475/scratchpad/` に置く。

## 報告
最後に、作ったページごとに「世界観・主なイラスト・動きの演出」を3〜5行で、確認結果（横スクロール・コンソールエラー）とともに報告する。
