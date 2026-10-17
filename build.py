"""事前登録LP 10本を生成するスクリプト。

使い方: python3 build.py
出力: lp/*.html（公開用のLP）と index.html（確認用の一覧）

フォームの送信先は FORM_ENDPOINT に設定する（Formspree などの URL）。
空のままだと送信はせず、完了メッセージだけ表示する。
"""

from pathlib import Path
from html import escape

ROOT = Path(__file__).parent
FORM_ENDPOINT = ""  # 例: "https://formspree.io/f/xxxxxxx"
OPERATOR = "運営者名（公開前に記入）"
CONTACT = "連絡先メールアドレス（公開前に記入）"

# ---------------------------------------------------------------------------
# 商品画像の代わりに置く、各サービスの画面イメージ
# ---------------------------------------------------------------------------

CAT_FACE = """<svg viewBox="0 0 120 120" aria-hidden="true">
<polygon points="20,46 30,8 54,32" fill="{ear}"/><polygon points="100,46 90,8 66,32" fill="{ear}"/>
<circle cx="60" cy="68" r="40" fill="{face}"/>
<circle cx="45" cy="64" r="5.5" fill="{eye}"/><circle cx="75" cy="64" r="5.5" fill="{eye}"/>
<path d="M54 78 L66 78 L60 85 Z" fill="{nose}"/>
<path d="M60 85 Q60 92 52 92 M60 85 Q60 92 68 92" stroke="{eye}" stroke-width="2" fill="none" stroke-linecap="round"/>
</svg>"""

MOCK_PET = f"""
<div class="mock mock-pet" aria-label="写真がイラストになり、アクリルスタンドになるまでの例">
  <div class="pet-step">
    <div class="pet-tile pet-photo">{CAT_FACE.format(ear="#8d8a86", face="#a8a49f", eye="#3d3a36", nose="#6e6a65")}</div>
    <span>スマホの写真</span>
  </div>
  <div class="pet-arrow" aria-hidden="true">→</div>
  <div class="pet-step">
    <div class="pet-tile pet-illust">{CAT_FACE.format(ear="#f2a541", face="#ffd28a", eye="#2b2b2b", nose="#e8735a")}</div>
    <span>AIでイラストに</span>
  </div>
  <div class="pet-arrow" aria-hidden="true">→</div>
  <div class="pet-step">
    <div class="pet-tile pet-acsta">
      <div class="acsta-plate">{CAT_FACE.format(ear="#f2a541", face="#ffd28a", eye="#2b2b2b", nose="#e8735a")}<b>MUGI</b></div>
      <div class="acsta-base"></div>
    </div>
    <span>アクスタでお届け</span>
  </div>
</div>"""

MOCK_KAITAI = """
<div class="mock mock-doc">
  <div class="doc-head"><b>御見積書</b><span>表示例</span></div>
  <p class="doc-sub">木造2階建て　延床30坪</p>
  <div class="scroll-x"><table class="doc-table">
    <thead><tr><th>項目</th><th>数量</th><th>単価</th><th>金額</th></tr></thead>
    <tbody>
      <tr><td>建物解体（木造）</td><td>30 坪</td><td>32,000</td><td>960,000</td></tr>
      <tr><td>廃材運搬（4t車）</td><td>6 台</td><td>35,000</td><td>210,000</td></tr>
      <tr><td>木くず処分</td><td>18 m³</td><td>6,000</td><td>108,000</td></tr>
      <tr><td>コンクリートがら処分</td><td>12 t</td><td>5,000</td><td>60,000</td></tr>
      <tr><td>ブロック塀撤去</td><td>15 m</td><td>4,000</td><td>60,000</td></tr>
    </tbody>
    <tfoot>
      <tr><td colspan="3">小計</td><td>1,398,000</td></tr>
      <tr><td colspan="3">消費税（10%）</td><td>139,800</td></tr>
      <tr class="total"><td colspan="3">合計</td><td>¥1,537,800</td></tr>
    </tfoot>
  </table></div>
  <p class="mock-note">※金額は表示例です。単価はご自身で設定します。</p>
</div>"""

MOCK_EISEI = """
<div class="mock mock-quiz">
  <div class="quiz-head"><span class="tag">関係法令</span><span>問 12 / 20</span></div>
  <p class="quiz-q">衛生管理者を選任しなければならない事業場の規模として、正しいものはどれか。</p>
  <ol class="quiz-opts">
    <li>常時10人以上</li><li>常時30人以上</li><li class="is-right">常時50人以上</li><li>常時100人以上</li><li>常時300人以上</li>
  </ol>
  <div class="quiz-exp"><b>解説</b>常時50人以上の労働者を使用する事業場では、衛生管理者の選任が必要です。<cite>労働安全衛生法施行令 第4条</cite></div>
  <div class="quiz-bars">
    <div><span>関係法令</span><i style="--v:62%"></i><b>62%</b></div>
    <div><span>労働衛生</span><i style="--v:78%"></i><b>78%</b></div>
    <div><span>労働生理</span><i style="--v:85%"></i><b>85%</b></div>
  </div>
  <p class="mock-note">※正答率は表示例です。</p>
</div>"""

MOCK_KOUMUIN = """
<div class="mock mock-chat">
  <div class="chat-row ai"><span class="who">面接官AI・深掘り 2/5</span><p>子育て支援に関心があるとのことですが、〇〇市の施策で特に注目しているものは何ですか。</p></div>
  <div class="chat-row me"><span class="who">あなた</span><p>待機児童の解消に向けた、保育所の整備です。</p></div>
  <div class="chat-row ai"><span class="who">面接官AI・深掘り 3/5</span><p>他の自治体ではなく、〇〇市でそれに取り組みたい理由は何ですか。</p></div>
  <div class="chat-score"><span>具体性 <b>B</b></span><span>一貫性 <b>A</b></span><span>自治体理解 <b>C</b></span></div>
</div>"""

MOCK_RECEIPT = """
<div class="mock mock-list">
  <div class="list-head"><b>読み取り結果</b><span>表示例</span></div>
  <ul class="rows">
    <li><span class="d">1/12</span><span class="s">ガソリンスタンド</span><span class="a">¥4,820</span><span class="k">旅費交通費（候補）</span></li>
    <li><span class="d">2/03</span><span class="s">家電量販店</span><span class="a">¥1,280</span><span class="k">消耗品費（候補）</span></li>
    <li><span class="d">3/18</span><span class="s">カフェ</span><span class="a">¥690</span><span class="k">会議費（候補）</span></li>
    <li><span class="d">4/02</span><span class="s">書店</span><span class="a">¥2,420</span><span class="k">新聞図書費（候補）</span></li>
  </ul>
  <div class="list-foot"><span>読み取り済み 286枚 ・ 確認中 12枚</span></div>
  <div class="chips"><span>freee 形式</span><span>マネーフォワード 形式</span><span>弥生 形式</span></div>
</div>"""

MOCK_TAIKYO = """
<div class="mock mock-check">
  <div class="list-head"><b>立ち会い前チェック</b><span>表示例</span></div>
  <ul class="checks">
    <li class="done">入居時の写真を部屋ごとに整理した</li>
    <li class="done">傷や汚れの位置を、日付入りで撮影した</li>
    <li>立ち会いでは、その場でサインしない</li>
    <li>請求の内訳（単価・面積）を書面でもらう</li>
  </ul>
  <div class="calc">
    <span>壁紙（クロス）・入居4年</span>
    <b>残存価値の目安 約33%</b>
    <i style="--v:33%"></i>
    <small>国土交通省ガイドラインの一般的な考え方（耐用年数6年）による目安です</small>
  </div>
</div>"""

MOCK_WATCH = """
<div class="mock mock-notice">
  <div class="notice">
    <div class="notice-top"><b>ページ見張り番</b><span>10:12</span></div>
    <p class="notice-title">【更新あり】〇〇県 産業支援課「公募情報」</p>
    <p class="notice-diff"><span class="plus">追加</span>令和9年度 小規模事業者 設備導入補助金（公募要領.pdf）</p>
    <p class="notice-diff"><span class="plus">追加</span>申請締切：令和9年5月30日</p>
    <p class="notice-link">変更箇所を見る</p>
  </div>
  <p class="mock-note">※通知の表示例です。</p>
</div>"""

MOCK_SHIBOU = """
<div class="mock mock-essay">
  <div class="list-head"><b>下書き</b><span>表示例</span></div>
  <p class="essay">私は貴学の国際協力の学びに惹かれました。<mark>高校時代のボランティア経験から</mark>、困っている人の立場に立って考える大切さを学びました。</p>
  <div class="essay-q"><b>問い</b>そのボランティアで、あなたが一番迷ったことは何でしたか。その時どう考え、どう動きましたか。</div>
  <div class="chips"><span>ポリシーとの合い方 ◯</span><span>具体性 △</span><span>構成 ◯</span></div>
</div>"""

MOCK_RENAI = """
<div class="mock mock-line">
  <div class="line-bubble them">今週ちょっとバタバタしてて、また連絡するね</div>
  <div class="line-ai">
    <span class="who">返信の案</span>
    <ol>
      <li><b>気づかう</b>忙しい時期なんだね。無理しないでね、落ち着いたらまた話そう</li>
      <li><b>次につなぐ</b>了解！落ち着いたら、前に話してたカレー屋さん行こう</li>
      <li><b>短く</b>了解、おつかれさま！</li>
    </ol>
    <p class="tip">返事を急かす言葉は避けて、相手のペースに合わせましょう。</p>
  </div>
</div>"""

MOCK_SOUZOKU = """
<div class="mock mock-time">
  <div class="list-head"><b>やることと期限</b><span>表示例</span></div>
  <ol class="timeline">
    <li class="done"><span class="when">7日以内</span><span class="what">死亡届の提出</span><span class="st">完了</span></li>
    <li class="next"><span class="when">3か月以内</span><span class="what">相続放棄・限定承認の期限</span><span class="st">担当：兄</span></li>
    <li><span class="when">4か月以内</span><span class="what">準確定申告</span><span class="st">未着手</span></li>
    <li><span class="when">10か月以内</span><span class="what">相続税の申告・納付</span><span class="st">未着手</span></li>
    <li><span class="when">3年以内</span><span class="what">相続登記</span><span class="st">未着手</span></li>
  </ol>
</div>"""

# ---------------------------------------------------------------------------
# 10本のLPの中身
# ---------------------------------------------------------------------------

LPS = [
    dict(
        slug="pet", no=1, brand="うちの子アトリエ",
        idea="ペットの写真からオリジナルグッズ",
        font=("Zen Maru Gothic", "Zen+Maru+Gothic:wght@500;700;900"),
        colors=dict(bg="#f4f8f6", soft="#e1f1ea", brand="#1f7a62", brand_ink="#ffffff", accent="#f2a541"),
        eyebrow="ペットの写真から、世界にひとつのグッズを",
        title="うちの子の写真が、<br>イラストのアクスタに。",
        sub="スマホの写真を1枚送るだけ。AIがイラストにして、注文前に仕上がりを無料で確認できます。アクリルスタンドやポスターにしてお届けします。",
        mock=MOCK_PET,
        pains=["似顔絵を頼むと、仕上がりまで何日も待つ", "完成するまで、どんな絵になるか分からない", "写真をそのまま印刷するだけでは物足りない"],
        features=[
            ("注文前に無料プレビュー", "写真を送って約30秒で仕上がりを表示します。気に入ってから注文できます。"),
            ("画風を選べる", "水彩、ゆるかわ、和風など。年賀状やカレンダーに合う画風も用意します。"),
            ("グッズにしてお届け", "アクリルスタンド、A4ポスター、2027年カレンダー。受注生産で1点から作ります。"),
            ("修正は1回無料", "目の色や模様など、気になるところは注文前に1回まで無料で直せます。"),
        ],
        steps=["写真をアップロード", "画風を選んで、無料プレビューを確認", "グッズを選んで注文。ご自宅にお届け"],
        price=[("アクリルスタンド", "3,980円〜"), ("アクスタ＋A4ポスター", "5,480円")],
        price_note="いずれも税込・予定価格です。",
        perk="先行登録の方には、公開時に使える割引クーポンをお送りします。",
        faq=[
            ("AIで描くのですか？", "はい、AIでイラストにしています。ご注文前に仕上がりを確認でき、気に入らなければ注文の必要はありません。"),
            ("どんな写真が向いていますか？", "顔がはっきり写った、明るい写真がおすすめです。"),
            ("クリスマスに間に合いますか？", "受注生産のため、お届けまで1〜2週間ほどかかる見込みです。締切日は公開時にお知らせします。"),
            ("返品はできますか？", "1点ずつ受注生産するため、お客様都合の返品はお受けできません。初期不良の場合は交換します。"),
        ],
        q_label="飼っているペット", q_opts=["犬", "猫", "うさぎ・小動物", "その他"],
    ),
    dict(
        slug="kaitai", no=2, brand="解体見積メーカー",
        idea="業種特化の見積書作成（解体工事）",
        font=("BIZ UDPGothic", "BIZ+UDPGothic:wght@700"),
        colors=dict(bg="#f4f4f1", soft="#fdf1c7", brand="#f2b705", brand_ink="#1d1f22", accent="#1d1f22", brand_text="#7a5a00"),
        eyebrow="解体工事の見積書を、現場でつくる",
        title="坪数と構造を入れるだけ。<br>内訳つきの解体見積書。",
        sub="木造・鉄骨・RCの構造と坪数、付帯工事、産廃の品目を選ぶと、内訳つきの見積書PDFができあがります。現地調査のその場でスマホから作って、LINEで送れます。",
        mock=MOCK_KAITAI,
        pains=["見積書を、夜にExcelで作っている", "「一式」ではなく内訳を出してほしいと言われる", "産廃の品目ごとの計算が面倒"],
        features=[
            ("解体専用の項目", "建物解体、運搬、産廃処分（木くず・コンクリートがら・石膏ボードなど）、付帯工事を最初から用意しています。"),
            ("自社の単価を登録", "よく使う単価を一度登録すれば、次からは自動で計算されます。"),
            ("見積から請求書へ", "受注したら、ワンタップで請求書に変換。インボイスの登録番号にも対応予定です。"),
            ("スマホで完結", "現地でそのまま入力し、PDFをLINEやメールで送れます。"),
        ],
        steps=["構造・坪数・付帯工事を選ぶ", "単価を確認して調整", "PDFを作ってLINEで送る"],
        price=[("月額", "4,980円"), ("年払い", "49,800円")],
        price_note="いずれも税込・予定価格です。",
        perk="先行登録の方は、公開後14日間無料でお試しいただけます。",
        faq=[
            ("塗装やリフォームにも使えますか？", "まずは解体工事向けに作っています。外壁塗装向けも検討中です。"),
            ("今使っているExcelの単価表は使えますか？", "単価の一括取り込みに対応する予定です。"),
            ("パソコンがなくても使えますか？", "スマホだけで作成と送付ができます。"),
        ],
        q_label="主な工事", q_opts=["解体工事", "外壁・屋根塗装", "リフォーム", "その他"],
    ),
    dict(
        slug="eisei", no=3, brand="衛生管理者 合格ドリル",
        idea="資格のAI問題集（衛生管理者）",
        font=("M PLUS 1p", "M+PLUS+1p:wght@500;700;800"),
        colors=dict(bg="#f8f5f1", soft="#fde4d3", brand="#d9480f", brand_ink="#ffffff", accent="#2b8a3e", brand_text="#b33c0b"),
        eyebrow="第一種・第二種衛生管理者の試験対策",
        title="試験日から逆算して、<br>毎日の出題を自動で。",
        sub="法令の条文にもとづいた一問一答と五肢択一。分野ごとの正答率から弱点を見つけて、試験日までに解くべき問題を毎日出します。",
        mock=MOCK_EISEI,
        pains=["会社から取るように言われたが、勉強の時間がない", "問題を解いても、なぜ間違えたのか分からない", "どこが弱点で、あと何をやればいいか分からない"],
        features=[
            ("条文つきの解説", "すべての解説に、根拠となる法令の条文を示します。"),
            ("弱点を自動で分析", "関係法令・労働衛生・労働生理の分野ごとに正答率を表示します。"),
            ("試験日から逆算", "受験日を入れると、毎日の問題数と範囲を自動で決めます。"),
            ("スキマ時間に", "スマホで1問から解けます。通勤中でも続けられます。"),
        ],
        steps=["受験日と種別を登録", "無料の20問診断で弱点をチェック", "毎日の出題をこなす"],
        price=[("試験日まで使い放題", "4,980円")],
        price_note="税込・予定価格です。会社でまとめての導入にも対応予定です。",
        perk="先行登録の方は、公開時に無料診断を先行してお試しいただけます。",
        faq=[
            ("過去問は収録されていますか？", "過去問そのものではなく、法令と出題範囲をもとにしたオリジナル問題です。"),
            ("第二種にも対応しますか？", "はい。第一種・第二種の両方に対応予定です。"),
            ("会社でまとめて購入できますか？", "複数名分の一括購入に対応予定です。登録フォームでお知らせください。"),
        ],
        q_label="受験の予定", q_opts=["第一種", "第二種", "まだ決めていない", "会社でまとめて導入したい"],
    ),
    dict(
        slug="koumuin", no=4, brand="公務員面接トレーナー",
        idea="公務員試験の面接練習",
        font=("Zen Kaku Gothic New", "Zen+Kaku+Gothic+New:wght@500;700;900"),
        colors=dict(bg="#f3f5f9", soft="#dfe6f3", brand="#1e3a6e", brand_ink="#ffffff", accent="#2f9e44"),
        eyebrow="公務員試験の面接カード添削と模擬面接",
        title="面接カードから、<br>深掘り質問をAIが連続で。",
        sub="面接カードと志望先の自治体を入れると、面接官が聞きそうな質問を「なぜ」「具体的には」と5段階で深掘りします。回答を入力すると、具体性や志望先との一貫性を評価します。",
        mock=MOCK_KOUMUIN,
        pains=["面接カードを書いたが、何を聞かれるか分からない", "予備校の面接対策は高い", "一人では深掘りの練習ができない"],
        features=[
            ("自治体ごとの質問", "志望先の総合計画や重点施策をふまえた質問を出します。"),
            ("5段階の深掘り", "なぜ、具体的には、他の自治体との違い、困難、入庁後、の順に掘り下げます。"),
            ("食い違いをチェック", "面接カードの内容と回答のずれを指摘します。"),
            ("社会人経験者採用にも", "職務経験をふまえた質問にも対応します。"),
        ],
        steps=["面接カードを貼り付ける", "志望先を選ぶ", "質問に答えて、評価レポートを受け取る"],
        price=[("3ヶ月パス", "4,980円")],
        price_note="税込・予定価格です。",
        perk="先行登録の方は、公開時に3問を無料でお試しいただけます。",
        faq=[
            ("面接カードをAIが書いてくれますか？", "いいえ。書くのはご自身です。このサービスは、書いた内容で面接の練習をするためのものです。"),
            ("音声で練習できますか？", "最初は文字で回答する形です。音声は今後の対応を検討しています。"),
            ("どの自治体に対応しますか？", "国家一般職、特別区、主な県・政令市から順に対応します。"),
        ],
        q_label="受験区分", q_opts=["大卒程度（新卒）", "社会人経験者採用", "高卒程度", "その他"],
    ),
    dict(
        slug="receipt", no=5, brand="レシートまるごと申告",
        idea="確定申告のレシート整理",
        font=("BIZ UDPGothic", "BIZ+UDPGothic:wght@700"),
        colors=dict(bg="#f2f7f8", soft="#d5ecf0", brand="#0e7490", brand_ink="#ffffff", accent="#f59f00"),
        eyebrow="副業・個人事業主の確定申告準備",
        title="1年分のレシート、<br>まとめて撮ればデータに。",
        sub="ためこんだレシートや領収書を、スマホでまとめて撮影。AIが日付・金額・お店を読み取り、スタッフが確認したうえで、freee・マネーフォワード・弥生に取り込めるデータにします。",
        mock=MOCK_RECEIPT,
        pains=["レシートが袋にたまったまま、手をつけていない", "会計ソフトの使い方を覚えるのが面倒", "申告期限の直前にあわてたくない"],
        features=[
            ("まとめて撮影", "1枚ずつ入力する必要はありません。続けて撮るだけです。"),
            ("AIが読み取り、人が確認", "読み取った内容を、スタッフが目で確認します。"),
            ("会計ソフトに取り込める", "freee・マネーフォワード・弥生の取り込み形式で出力します。"),
            ("経費の集計表つき", "収支内訳書の経費欄に写しやすい集計表もお渡しします。"),
        ],
        steps=["レシートをまとめて撮影", "読み取り結果をスタッフが確認", "会計ソフト用のデータを受け取る"],
        price=[("1シーズン（レシート500枚まで）", "9,800円")],
        price_note="税込・予定価格です。",
        perk="先行登録の方には、年明けの受付開始を優先してお知らせします。",
        faq=[
            ("申告書も作ってくれますか？", "いいえ。申告書の作成や提出、税務相談は行いません。経費のデータ化までのお手伝いです。"),
            ("勘定科目は決めてくれますか？", "候補を表示します。最終的にはご自身で確認して決めてください。"),
            ("手書きの領収書も読めますか？", "読み取れますが、精度が下がる場合があります。その分はスタッフが確認します。"),
        ],
        q_label="申告の種類", q_opts=["副業（会社員）", "個人事業主（白色申告）", "個人事業主（青色申告）", "まだ分からない"],
    ),
    dict(
        slug="taikyo", no=6, brand="退去前チェックパック",
        idea="退去費用で損しないための準備",
        font=("Zen Kaku Gothic New", "Zen+Kaku+Gothic+New:wght@500;700;900"),
        colors=dict(bg="#f5f7f2", soft="#e3ecd5", brand="#4d7c0f", brand_ink="#ffffff", accent="#e67700"),
        eyebrow="賃貸の退去、立ち会いの前に",
        title="退去費用で損しないために、<br>立ち会いの前にやること。",
        sub="国土交通省のガイドラインをもとに、退去前に準備しておくことをまとめたチェックパックです。入居年数を入れると、壁紙などの残存価値の目安も計算できます。",
        mock=MOCK_TAIKYO,
        pains=["退去の立ち会いで、言われるままサインしてしまいそう", "どこまでが自分の負担なのか分からない", "入居時の状態を示せるものがない"],
        features=[
            ("立ち会い前のチェックリスト", "部屋ごとの撮影ポイント、確認すること、その場でサインしないための手順をまとめています。"),
            ("負担の目安を計算", "入居年数から、壁紙などの残存価値の目安を計算します（ガイドラインの一般的な考え方にもとづきます）。"),
            ("管理会社に聞く質問集", "請求の内訳を確認するための質問のテンプレートです。"),
        ],
        steps=["退去日と入居年数を入力", "チェックリストに沿って撮影・確認", "立ち会いに臨む"],
        price=[("チェックパック", "980円")],
        price_note="税込・予定価格です。",
        perk="先行登録の方には、公開時にお知らせします。",
        faq=[
            ("請求額が正しいか判断してもらえますか？", "個別の請求が妥当かどうかの判断や、管理会社との交渉は行いません。相談が必要な場合は、消費者ホットライン（188）や弁護士にご相談ください。"),
            ("すでに請求書が届いています", "請求の内訳を確認するための質問集はお使いいただけます。"),
            ("ガイドラインとは何ですか？", "国土交通省の「原状回復をめぐるトラブルとガイドライン」です。"),
        ],
        q_label="退去の予定", q_opts=["1か月以内", "3か月以内", "半年以内", "まだ決まっていない"],
    ),
    dict(
        slug="watch", no=7, brand="ページ見張り番",
        idea="サイト更新のLINE通知",
        font=("Zen Kaku Gothic New", "Zen+Kaku+Gothic+New:wght@500;700;900"),
        colors=dict(bg="#f7f4f6", soft="#f7dbe6", brand="#c2255c", brand_ink="#ffffff", accent="#1c7ed6"),
        eyebrow="Webページの更新を、LINEでお知らせ",
        title="見ておきたいページの更新を、<br>LINEに届けます。",
        sub="URLを登録するだけ。補助金の公募ページや自治体のお知らせが更新されたら、変わった部分を抜き出してLINEとメールでお知らせします。",
        mock=MOCK_WATCH,
        pains=["補助金の公募に気づくのが遅れた", "毎日同じページを見に行くのが面倒", "LINE Notifyが終わって、通知の仕組みがなくなった"],
        features=[
            ("変わった部分だけ", "ページ全体ではなく、追加・変更された部分を抜き出して届けます。"),
            ("PDFの追加も検知", "公募要領などのPDFが追加されたらお知らせします。"),
            ("キーワードで絞り込み", "「公募」「締切」など、指定した言葉を含む更新だけを通知できます。"),
            ("LINEとメールで", "難しい設定は要りません。友だち追加だけで届きます。"),
        ],
        steps=["見張りたいページのURLを登録", "通知の条件を選ぶ", "更新があればLINEに届く"],
        price=[("フリー（3ページまで）", "無料"), ("スタンダード（50ページまで）", "月1,980円")],
        price_note="税込・予定価格です。",
        perk="先行登録の方は、公開時にスタンダードを1か月無料でお試しいただけます。",
        faq=[
            ("どれくらいの間隔で確認しますか？", "1〜6時間ごとに確認します。相手のサイトに負担をかけないよう、間隔に下限を設けています。"),
            ("ログインが必要なページも見張れますか？", "対応していません。誰でも見られるページが対象です。"),
            ("どんなページに向いていますか？", "補助金・助成金の公募、自治体のお知らせ、入札情報、求人ページなどです。"),
        ],
        q_label="使いたい用途", q_opts=["補助金・公募の情報", "入札情報", "仕事での情報収集", "個人的な用途"],
    ),
    dict(
        slug="shibou", no=8, brand="志望理由書コーチ",
        idea="志望理由書の添削",
        font=("Shippori Mincho", "Shippori+Mincho:wght@600;800"),
        colors=dict(bg="#f4f5f8", soft="#efdde3", brand="#7a1f3d", brand_ink="#ffffff", accent="#1971c2"),
        eyebrow="総合型選抜・学校推薦型選抜の志望理由書に",
        title="書き直さない。<br>考えるための問いを返す添削。",
        sub="下書きと志望校のアドミッション・ポリシーを入れると、AIがポリシーとの合い方、具体性、構成をチェックします。直した文章ではなく、自分の言葉で書き直すための問いと、想定される面接の質問を返します。",
        mock=MOCK_SHIBOU,
        pains=["先生に見てもらう時間が足りない", "塾の添削は高い", "AIに書かせると、自分の文章ではなくなる"],
        features=[
            ("アドミッション・ポリシーと照合", "志望校が求める学生像と、下書きの内容が合っているかを確認します。"),
            ("問いかけ型の添削", "文章を書き換えず、「それはいつ、どんな経験ですか？」と問い返します。"),
            ("想定面接質問", "志望理由書から、面接で聞かれそうな質問を10問出します。"),
            ("保護者とも共有", "進み具合を保護者と共有できます。"),
        ],
        steps=["志望校・学部とポリシーを入力", "下書きを貼り付ける", "問いと面接質問を受け取り、自分で書き直す"],
        price=[("受験まで使い放題", "9,800円")],
        price_note="税込・予定価格です。",
        perk="先行登録の方には、公開時にお知らせします。",
        faq=[
            ("AIを使った志望理由書を出しても大丈夫ですか？", "このサービスは文章を代わりに書きません。大学によっては生成AIの利用にルールがあるため、必ず志望校の募集要項を確認してください。"),
            ("推薦入試にも使えますか？", "はい。学校推薦型選抜の志望理由書にも使えます。"),
            ("誰が申し込めますか？", "高校生ご本人、または保護者の方がお申し込みいただけます。"),
        ],
        q_label="ご登録者", q_opts=["高校生本人", "保護者", "学校・塾の先生"],
    ),
    dict(
        slug="renai", no=9, brand="メンズ恋愛ナビ",
        idea="男性向けの恋愛AIコーチ",
        font=("Zen Kaku Gothic New", "Zen+Kaku+Gothic+New:wght@500;700;900"),
        colors=dict(bg="#f6f4f9", soft="#ebdcf3", brand="#862e9c", brand_ink="#ffffff", accent="#0ca678"),
        eyebrow="男性のための、恋愛と婚活の相談相手",
        title="このLINE、どう返す？<br>いつでも相談できるAIコーチ。",
        sub="やりとりのスクリーンショットを貼るだけで、返信の案を3パターン出します。デートの誘い方、マッチングアプリのプロフィール、2回目につなげるコツまで、人には聞きにくいことを匿名で相談できます。",
        mock=MOCK_RENAI,
        pains=["返事が来なくて、次に何を送ればいいか分からない", "デートに誘うタイミングが分からない", "プロフィールの写真や文章に自信がない"],
        features=[
            ("スクショで返信相談", "トーク画面を貼ると、流れをふまえた返信案を出します。"),
            ("プロフィール添削", "写真の選び方と、自己紹介文を改善します。"),
            ("デートの相談", "誘い方、お店選び、当日の会話のヒントまで。"),
            ("匿名で何度でも", "人に話しにくいことも、24時間いつでも相談できます。"),
        ],
        steps=["トーク画面やプロフィールを貼る", "状況をひとこと書く", "返信案やアドバイスを受け取る"],
        price=[("月額", "1,480円")],
        price_note="税込・予定価格です。",
        perk="先行登録の方は、公開時に初月無料でお試しいただけます。",
        faq=[
            ("相手の個人情報は大丈夫ですか？", "名前などはスクリーンショットから隠して使えます。送った画像は相談のあとに削除します。"),
            ("必ずうまくいきますか？", "結果を約束するものではありません。相手を尊重したコミュニケーションをお手伝いするサービスです。"),
            ("女性も使えますか？", "まずは男性向けに作っていますが、どなたでもお使いいただけます。"),
        ],
        q_label="主な相談", q_opts=["マッチングアプリ", "職場・知人", "婚活（結婚相談所など）", "その他"],
    ),
    dict(
        slug="souzoku", no=10, brand="相続やることナビ",
        idea="相続手続きナビ",
        font=("Zen Old Mincho", "Zen+Old+Mincho:wght@600;700"),
        colors=dict(bg="#f3f5f6", soft="#dde4ea", brand="#3d5266", brand_ink="#ffffff", accent="#9c6b2f"),
        eyebrow="ご家族を亡くされた方へ",
        title="相続の手続き、<br>いつまでに何をすればいいか。",
        sub="いくつかの質問に答えると、あなたのご家族に必要な手続きと期限を一覧にします。期限が近づいたらお知らせし、家族で分担して進められます。",
        mock=MOCK_SOUZOKU,
        pains=["何から手をつければいいか分からない", "期限のある手続きを見落としそうで不安", "兄弟姉妹で、誰が何をするか決まらない"],
        features=[
            ("やることリスト", "状況に合わせて、必要な手続きだけを一覧にします。"),
            ("期限をお知らせ", "相続放棄（3か月）、準確定申告（4か月）、相続税の申告（10か月）など、期限が近づくと通知します。"),
            ("家族で分担", "家族を招待して手続きを割り振り、進み具合を共有できます。"),
            ("必要書類の案内", "手続きごとに、一般的に必要な書類と窓口を案内します。"),
        ],
        steps=["いくつかの質問に答える", "やることと期限の一覧を受け取る", "家族と分担して進める"],
        price=[("相続やることナビ", "4,980円")],
        price_note="税込・予定価格です。",
        perk="先行登録の方には、公開時にお知らせします。",
        faq=[
            ("書類を作ってもらえますか？", "書類の作成や申請の代行、個別の税務・法律相談は行いません。必要に応じて、司法書士・税理士・弁護士にご相談ください。"),
            ("自治体の無料の案内と何が違いますか？", "役所の手続きに加えて、金融機関や相続税などの期限を通知し、家族で分担できる点が違います。"),
            ("生前の準備にも使えますか？", "はい。今後必要になる手続きの確認にもお使いいただけます。"),
        ],
        q_label="今の状況", q_opts=["亡くなってから3か月以内", "3か月〜1年", "1年以上前", "生前の準備として"],
    ),
]

# ---------------------------------------------------------------------------
# LP共通のスタイル
# ---------------------------------------------------------------------------

LP_CSS = """
:root {
  --bg: __BG__; --surface: #ffffff; --ink: #1d232b; --muted: #59636f; --line: #dde2e8;
  --soft: __SOFT__; --brand: __BRAND__; --brand-text: __BRAND_TEXT__; --brand-ink: __BRAND_INK__; --accent: __ACCENT__;
  --font-display: "__FONT__", "Hiragino Sans", "Yu Gothic", sans-serif;
  --font-body: "Noto Sans JP", "Hiragino Sans", "Yu Gothic", "Meiryo", sans-serif;
  color-scheme: light;
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--font-body); font-size: 16px; line-height: 1.8; }
img, svg { max-width: 100%; }
.wrap { max-width: 1060px; margin: 0 auto; padding-left: max(18px, env(safe-area-inset-left, 0px)); padding-right: max(18px, env(safe-area-inset-right, 0px)); }
h1, h2, h3 { font-family: var(--font-display); line-height: 1.4; margin: 0; text-wrap: balance; word-break: auto-phrase; }
p { margin: 0; }
.topbar { padding-block: 16px; }
.topbar .wrap { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
.logo { font-family: var(--font-display); font-weight: 800; font-size: 19px; letter-spacing: 0.02em; }
.badge { font-size: 12.5px; font-weight: 700; color: var(--brand-ink); background: var(--brand); padding: 4px 12px; border-radius: 999px; }
.hero { padding-block: 28px 56px; }
.hero .wrap { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr); gap: 44px; align-items: center; }
.eyebrow { font-size: 14px; font-weight: 700; color: var(--brand-text); letter-spacing: 0.04em; }
.hero h1 { font-size: clamp(27px, 3.6vw, 40px); font-weight: 800; margin-top: 10px; }
.hero .sub { margin-top: 18px; color: var(--muted); max-width: 34em; }
.cta { display: inline-flex; align-items: center; justify-content: center; gap: 8px; margin-top: 26px; background: var(--brand); color: var(--brand-ink); font-weight: 700; font-size: 16px; text-decoration: none; padding: 15px 28px; border-radius: 12px; border: 0; cursor: pointer; font-family: inherit; }
.cta:hover { filter: brightness(1.06); }
.cta:focus-visible, input:focus-visible, select:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
.cta-note { display: block; margin-top: 10px; font-size: 13px; color: var(--muted); }
section.block { padding-block: 56px; }
section.alt { background: var(--surface); }
.sec-title { font-size: clamp(22px, 3vw, 28px); font-weight: 800; }
.sec-lead { color: var(--muted); margin-top: 8px; }
.pains { margin: 26px 0 0; padding: 0; list-style: none; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
.pains li { background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 18px 20px; font-weight: 500; }
.pains li::before { content: "「"; color: var(--brand-text); font-weight: 800; }
.pains li::after { content: "」"; color: var(--brand-text); font-weight: 800; }
.features { margin-top: 28px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px 28px; }
.feature { display: grid; gap: 6px; padding-top: 16px; border-top: 3px solid var(--brand); min-width: 0; }
.feature h3 { font-size: 18px; }
.feature p { color: var(--muted); font-size: 15px; }
.steps { margin: 28px 0 0; padding: 0; list-style: none; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; counter-reset: step; }
.steps li { counter-increment: step; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 18px 20px; display: grid; gap: 8px; align-content: start; font-weight: 700; }
.steps li::before { content: "STEP " counter(step); font-size: 12px; letter-spacing: 0.12em; color: var(--brand-text); font-weight: 800; }
.price-box { margin-top: 26px; background: var(--surface); border: 2px solid var(--brand); border-radius: 18px; padding: 24px 26px; display: grid; gap: 14px; max-width: 640px; }
.price-row { display: flex; align-items: baseline; justify-content: space-between; gap: 16px; flex-wrap: wrap; border-bottom: 1px dashed var(--line); padding-bottom: 12px; }
.price-row:last-of-type { border-bottom: 0; padding-bottom: 0; }
.price-row span { font-weight: 500; }
.price-row b { font-family: var(--font-display); font-size: 28px; font-weight: 800; color: var(--brand-text); font-variant-numeric: tabular-nums; }
.price-note { font-size: 13px; color: var(--muted); }
.perk { background: var(--soft); border-radius: 12px; padding: 12px 16px; font-weight: 700; font-size: 15px; }
.faq { margin-top: 24px; display: grid; gap: 10px; max-width: 780px; }
.faq details { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; }
.faq summary { cursor: pointer; padding: 16px 18px; font-weight: 700; list-style: none; display: flex; justify-content: space-between; gap: 12px; }
.faq summary::-webkit-details-marker { display: none; }
.faq summary::after { content: "+"; color: var(--brand-text); font-weight: 800; }
.faq details[open] summary::after { content: "−"; }
.faq details p { padding: 0 18px 16px; color: var(--muted); font-size: 15px; }
.signup { background: var(--brand); color: var(--brand-ink); }
.signup .wrap { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 36px; align-items: center; }
.signup .sec-title { color: var(--brand-ink); }
.signup .sec-lead { color: var(--brand-ink); opacity: 0.9; }
form.card { background: var(--surface); color: var(--ink); border-radius: 18px; padding: 26px; display: grid; gap: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.12); }
form.card label { display: grid; gap: 6px; font-weight: 700; font-size: 14px; }
form.card input, form.card select { font: inherit; font-size: 16px; padding: 12px 14px; border: 1px solid var(--line); border-radius: 10px; background: #fff; color: var(--ink); width: 100%; }
form.card .cta { margin-top: 4px; width: 100%; }
form.card .err { color: #c92a2a; font-size: 13px; font-weight: 500; }
form.card .privacy { font-size: 12.5px; color: var(--muted); font-weight: 400; }
.thanks { background: var(--surface); color: var(--ink); border-radius: 18px; padding: 30px 26px; display: grid; gap: 8px; }
.thanks h3 { font-size: 20px; color: var(--brand-text); }
.thanks small { color: var(--muted); }
footer { padding-block: 32px 48px; font-size: 13px; color: var(--muted); }
footer .wrap { display: grid; gap: 6px; }

/* 画面イメージ */
.mock { background: var(--surface); border: 1px solid var(--line); border-radius: 20px; padding: 22px; box-shadow: 0 18px 40px rgba(20, 30, 40, 0.10); min-width: 0; }
.mock-note { font-size: 12px; color: var(--muted); margin-top: 10px; }
.list-head, .doc-head, .quiz-head, .notice-top { display: flex; justify-content: space-between; align-items: center; gap: 10px; font-size: 13px; color: var(--muted); }
.list-head b, .doc-head b { color: var(--ink); font-size: 16px; }
.scroll-x { overflow-x: auto; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 14px; }
.chips span { background: var(--soft); border-radius: 999px; padding: 4px 12px; font-size: 13px; font-weight: 700; }

.mock-pet { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.pet-step { display: grid; gap: 8px; justify-items: center; font-size: 13px; font-weight: 700; text-align: center; flex: 1 1 0; min-width: 0; }
.pet-tile { width: 100%; aspect-ratio: 1; max-width: 140px; border-radius: 16px; display: grid; place-items: center; padding: 12px; }
.pet-photo { background: linear-gradient(160deg, #d9d6d1, #bfbab4); }
.pet-illust { background: var(--soft); }
.pet-acsta { background: #eef2f4; align-content: end; gap: 0; padding-bottom: 14px; }
.acsta-plate { width: 78%; border: 2px solid rgba(255,255,255,0.9); border-radius: 12px; background: rgba(255,255,255,0.55); box-shadow: 0 4px 10px rgba(0,0,0,0.12); padding: 6px 6px 2px; display: grid; justify-items: center; }
.acsta-plate b { font-size: 11px; letter-spacing: 0.1em; color: var(--brand-text); }
.acsta-base { width: 70%; height: 10px; border-radius: 6px; background: rgba(120,140,150,0.45); margin-top: 4px; }
.pet-arrow { color: var(--brand-text); font-weight: 800; font-size: 20px; }

.doc-sub { margin-top: 6px; font-size: 14px; font-weight: 700; }
.doc-table { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 13.5px; font-variant-numeric: tabular-nums; }
.doc-table th { text-align: left; font-size: 12px; color: var(--muted); font-weight: 500; border-bottom: 2px solid var(--ink); padding: 6px 4px; }
.doc-table td { padding: 7px 4px; border-bottom: 1px solid var(--line); }
.doc-table td:nth-child(n+2), .doc-table th:nth-child(n+2) { text-align: right; white-space: nowrap; }
.doc-table tfoot td { text-align: right; border-bottom: 0; }
.doc-table tfoot td:first-child { text-align: right; color: var(--muted); }
.doc-table tr.total td { font-weight: 800; font-size: 16px; border-top: 2px solid var(--ink); }
.doc-table tr.total td:last-child { background: var(--soft); }

.quiz-head .tag { background: var(--brand); color: var(--brand-ink); padding: 2px 10px; border-radius: 999px; font-weight: 700; font-size: 12px; }
.quiz-q { margin-top: 12px; font-weight: 700; }
.quiz-opts { margin: 12px 0 0; padding-left: 1.6em; display: grid; gap: 4px; font-size: 14.5px; }
.quiz-opts li.is-right { font-weight: 800; color: var(--accent); }
.quiz-opts li.is-right::after { content: "　正解"; font-size: 12px; }
.quiz-exp { margin-top: 12px; background: var(--soft); border-radius: 10px; padding: 10px 12px; font-size: 13.5px; display: grid; gap: 2px; }
.quiz-exp cite { font-style: normal; font-size: 12px; color: var(--muted); }
.quiz-bars { margin-top: 14px; display: grid; gap: 6px; font-size: 13px; }
.quiz-bars div { display: grid; grid-template-columns: 5em 1fr 3em; gap: 8px; align-items: center; }
.quiz-bars i { height: 8px; border-radius: 4px; background: linear-gradient(90deg, var(--brand) var(--v), #e9ecef var(--v)); }
.quiz-bars b { text-align: right; font-variant-numeric: tabular-nums; }

.mock-chat { display: grid; gap: 12px; }
.chat-row { display: grid; gap: 4px; max-width: 88%; }
.chat-row .who { font-size: 12px; color: var(--muted); font-weight: 700; }
.chat-row p { padding: 10px 14px; border-radius: 14px; font-size: 14.5px; }
.chat-row.ai p { background: var(--soft); border-top-left-radius: 4px; }
.chat-row.me { justify-self: end; text-align: right; }
.chat-row.me p { background: var(--brand); color: var(--brand-ink); border-top-right-radius: 4px; text-align: left; }
.chat-score { display: flex; gap: 8px; flex-wrap: wrap; border-top: 1px solid var(--line); padding-top: 12px; font-size: 13px; }
.chat-score span { background: #f1f3f5; border-radius: 8px; padding: 4px 10px; }
.chat-score b { color: var(--brand-text); }

.rows { list-style: none; margin: 12px 0 0; padding: 0; display: grid; }
.rows li { display: grid; grid-template-columns: 3em minmax(0, 1fr) auto; grid-template-areas: "d s a" ". k k"; gap: 0 10px; padding: 9px 0; border-bottom: 1px solid var(--line); font-size: 14px; font-variant-numeric: tabular-nums; }
.rows .d { grid-area: d; color: var(--muted); }
.rows .s { grid-area: s; font-weight: 700; }
.rows .a { grid-area: a; font-weight: 700; }
.rows .k { grid-area: k; font-size: 12.5px; color: var(--brand-text); }
.list-foot { margin-top: 10px; font-size: 13px; color: var(--muted); }

.checks { list-style: none; margin: 12px 0 0; padding: 0; display: grid; gap: 8px; font-size: 14.5px; }
.checks li { display: flex; gap: 10px; align-items: flex-start; }
.checks li::before { content: ""; flex: none; width: 18px; height: 18px; border: 2px solid var(--line); border-radius: 5px; margin-top: 4px; }
.checks li.done::before { background: var(--brand); border-color: var(--brand-text); box-shadow: inset 0 0 0 3px #fff; }
.calc { margin-top: 16px; background: var(--soft); border-radius: 12px; padding: 12px 14px; display: grid; gap: 6px; font-size: 13.5px; }
.calc b { font-size: 17px; }
.calc i { height: 8px; border-radius: 4px; background: linear-gradient(90deg, var(--brand) var(--v), #fff var(--v)); }
.calc small { color: var(--muted); font-size: 12px; }

.notice { background: #f8f9fa; border-radius: 16px; padding: 16px; display: grid; gap: 8px; border: 1px solid var(--line); }
.notice-top b { color: var(--ink); }
.notice-title { font-weight: 800; }
.notice-diff { font-size: 14px; display: flex; gap: 8px; align-items: baseline; }
.notice-diff .plus { flex: none; font-size: 11.5px; font-weight: 800; color: var(--brand-ink); background: var(--brand); border-radius: 6px; padding: 1px 6px; }
.notice-link { font-size: 13px; color: var(--accent); font-weight: 700; }

.essay { margin-top: 12px; font-size: 15px; line-height: 2; }
.essay mark { background: var(--soft); border-bottom: 2px solid var(--brand); padding: 0 2px; }
.essay-q { margin-top: 12px; border-left: 4px solid var(--brand); padding: 8px 12px; background: #f8f9fa; font-size: 14px; display: grid; gap: 2px; }
.essay-q b { color: var(--brand-text); font-size: 12.5px; }

.mock-line { background: #eef1f6; display: grid; gap: 14px; }
.line-bubble.them { justify-self: start; max-width: 80%; background: #fff; border-radius: 16px; border-top-left-radius: 4px; padding: 10px 14px; font-size: 14.5px; }
.line-ai { background: var(--surface); border-radius: 14px; padding: 14px; display: grid; gap: 8px; }
.line-ai .who { font-size: 12px; font-weight: 800; color: var(--brand-text); }
.line-ai ol { margin: 0; padding: 0; list-style: none; display: grid; gap: 8px; }
.line-ai li { background: var(--soft); border-radius: 10px; padding: 8px 12px; font-size: 14px; display: grid; gap: 2px; }
.line-ai li b { font-size: 12px; color: var(--brand-text); }
.line-ai .tip { font-size: 12.5px; color: var(--muted); }

.timeline { list-style: none; margin: 14px 0 0; padding: 0; display: grid; gap: 0; }
.timeline li { display: grid; grid-template-columns: 6.2em minmax(0, 1fr) auto; gap: 10px; padding: 10px 0 10px 18px; border-left: 2px solid var(--line); position: relative; font-size: 14px; align-items: baseline; }
.timeline li::before { content: ""; position: absolute; left: -7px; top: 16px; width: 12px; height: 12px; border-radius: 50%; background: #fff; border: 2px solid var(--line); }
.timeline li.done::before { background: var(--brand); border-color: var(--brand-text); }
.timeline li.next::before { border-color: var(--accent); background: var(--accent); }
.timeline .when { font-weight: 800; color: var(--brand-text); font-variant-numeric: tabular-nums; }
.timeline .st { font-size: 12px; color: var(--muted); white-space: nowrap; }
.timeline li.next .st { color: var(--accent); font-weight: 700; }

@media (max-width: 860px) {
  .hero .wrap, .signup .wrap { grid-template-columns: minmax(0, 1fr); gap: 28px; }
  .pains, .steps { grid-template-columns: minmax(0, 1fr); }
  .features { grid-template-columns: minmax(0, 1fr); }
  section.block { padding-block: 44px; }
}
@media (max-width: 480px) {
  .mock { padding: 16px; }
  .doc-table { font-size: 12px; }
  .doc-table th, .doc-table td { padding: 6px 2px; }
  .doc-table tr.total td { font-size: 14px; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
"""

FORM_JS = """
<script>
(function () {
  var FORM_ENDPOINT = "__ENDPOINT__";
  var form = document.getElementById("signup-form");
  var err = document.getElementById("signup-error");
  var thanks = document.getElementById("signup-thanks");
  var preview = document.getElementById("signup-preview");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var email = document.getElementById("signup-email").value.trim();
    if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {
      err.textContent = "メールアドレスの形式を確認してください（例：name@example.com）。";
      err.hidden = false;
      return;
    }
    err.hidden = true;
    var data = { service: "__SLUG__", email: email, answer: document.getElementById("signup-q").value };
    var done = function () { form.hidden = true; thanks.hidden = false; };
    if (!FORM_ENDPOINT) { preview.hidden = false; done(); return; }
    var btn = form.querySelector("button");
    btn.disabled = true; btn.textContent = "送信しています";
    fetch(FORM_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data) })
      .then(function (r) { if (!r.ok) throw new Error(); done(); })
      .catch(function () {
        btn.disabled = false; btn.textContent = "先行登録する（無料）";
        err.textContent = "送信できませんでした。通信状況を確認して、もう一度お試しください。";
        err.hidden = false;
      });
  });
})();
</script>
"""


def font_url(lp):
    return f"https://fonts.googleapis.com/css2?family={lp['font'][1]}&family=Noto+Sans+JP:wght@400;500;700&display=swap"


def render_lp(lp):
    c = lp["colors"]
    css = (LP_CSS.replace("__BG__", c["bg"]).replace("__SOFT__", c["soft"])
           .replace("__BRAND__", c["brand"]).replace("__BRAND_INK__", c["brand_ink"])
           .replace("__ACCENT__", c["accent"]).replace("__BRAND_TEXT__", c.get("brand_text", c["brand"])).replace("__FONT__", lp["font"][0]))
    plain_title = lp["title"].replace("<br>", "")
    pains = "".join(f"<li>{escape(p)}</li>" for p in lp["pains"])
    feats = "".join(f'<div class="feature"><h3>{escape(t)}</h3><p>{escape(d)}</p></div>' for t, d in lp["features"])
    steps = "".join(f"<li>{escape(s)}</li>" for s in lp["steps"])
    prices = "".join(f'<div class="price-row"><span>{escape(n)}</span><b>{escape(v)}</b></div>' for n, v in lp["price"])
    faq = "".join(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in lp["faq"])
    opts = '<option value="">選んでください（任意）</option>' + "".join(f'<option>{escape(o)}</option>' for o in lp["q_opts"])
    js = FORM_JS.replace("__ENDPOINT__", FORM_ENDPOINT).replace("__SLUG__", lp["slug"])
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(lp['brand'])}｜{escape(plain_title)}</title>
<meta name="description" content="{escape(lp['sub'])}">
<meta property="og:title" content="{escape(lp['brand'])}">
<meta property="og:description" content="{escape(lp['sub'])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{font_url(lp)}">
<!-- 計測タグ（Googleアナリティクス、Meta・TikTokのピクセル）は公開時にここへ入れる -->
<style>{css}</style>
</head>
<body>
<header class="topbar"><div class="wrap"><span class="logo">{escape(lp['brand'])}</span><span class="badge">事前登録受付中</span></div></header>

<main>
<section class="hero"><div class="wrap">
  <div>
    <p class="eyebrow">{escape(lp['eyebrow'])}</p>
    <h1>{lp['title']}</h1>
    <p class="sub">{escape(lp['sub'])}</p>
    <a class="cta" href="#signup">先行登録する（無料）</a>
    <span class="cta-note">現在準備中です。公開時にメールでお知らせします。</span>
  </div>
  {lp['mock']}
</div></section>

<section class="block alt"><div class="wrap">
  <h2 class="sec-title">こんなこと、ありませんか？</h2>
  <ul class="pains">{pains}</ul>
</div></section>

<section class="block"><div class="wrap">
  <h2 class="sec-title">{escape(lp['brand'])}でできること</h2>
  <div class="features">{feats}</div>
</div></section>

<section class="block alt"><div class="wrap">
  <h2 class="sec-title">使い方</h2>
  <ol class="steps">{steps}</ol>
</div></section>

<section class="block"><div class="wrap">
  <h2 class="sec-title">料金</h2>
  <div class="price-box">{prices}<p class="price-note">{escape(lp['price_note'])}</p><p class="perk">{escape(lp['perk'])}</p></div>
</div></section>

<section class="block alt"><div class="wrap">
  <h2 class="sec-title">よくある質問</h2>
  <div class="faq">{faq}</div>
</div></section>

<section class="block signup" id="signup"><div class="wrap">
  <div>
    <h2 class="sec-title">先行登録（無料）</h2>
    <p class="sec-lead">メールアドレスを登録すると、公開時にお知らせします。登録しても料金はかかりません。</p>
  </div>
  <div>
    <form class="card" id="signup-form" novalidate>
      <label for="signup-email">メールアドレス<input id="signup-email" type="email" autocomplete="email" placeholder="name@example.com" required></label>
      <label for="signup-q">{escape(lp['q_label'])}<select id="signup-q">{opts}</select></label>
      <p class="err" id="signup-error" role="alert" hidden></p>
      <button class="cta" type="submit">先行登録する（無料）</button>
      <p class="privacy">ご登録のメールアドレスは、このサービスの公開のご案内にのみ使用します。</p>
    </form>
    <div class="thanks" id="signup-thanks" hidden role="status">
      <h3>ご登録ありがとうございます</h3>
      <p>公開の準備ができしだい、メールでお知らせします。</p>
      <small id="signup-preview" hidden>確認用のページのため、今回の入力は送信されていません。</small>
    </div>
  </div>
</div></section>
</main>

<footer><div class="wrap">
  <span>{escape(lp['brand'])}</span>
  <span>運営：{escape(OPERATOR)}　お問い合わせ：{escape(CONTACT)}</span>
</div></footer>
{js}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# 確認用の一覧ページ（Artifact のトップページ。doctype なしで書く）
# ---------------------------------------------------------------------------

INDEX_CSS = """
:root { --bg: #f4f6f8; --surface: #ffffff; --fg: #182230; --muted: #5a6676; --line: #d9dfe6; --accent: #2d4f9e;
  --font-display: "Zen Kaku Gothic New", "Hiragino Sans", sans-serif; --font-body: "Noto Sans JP", "Hiragino Sans", sans-serif; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #11161d; --surface: #18202a; --fg: #e4e9ef; --muted: #99a4b3; --line: #2a3542; --accent: #8fb0ff; color-scheme: dark; } }
:root[data-theme="dark"] { --bg: #11161d; --surface: #18202a; --fg: #e4e9ef; --muted: #99a4b3; --line: #2a3542; --accent: #8fb0ff; color-scheme: dark; }
body { background: var(--bg); color: var(--fg); font-family: var(--font-body); font-size: 15px; line-height: 1.7; }
.wrap { max-width: 1040px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 40px 64px; display: grid; gap: 28px; }
h1 { font-family: var(--font-display); font-size: clamp(24px, 4vw, 34px); margin: 0; text-wrap: balance; }
.lead { color: var(--muted); max-width: 66ch; margin: 8px 0 0; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr)); gap: 14px; }
a.card { display: grid; gap: 10px; text-decoration: none; color: inherit; background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 16px; min-width: 0; }
a.card:hover { border-color: var(--accent); }
a.card:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.top { display: flex; align-items: center; gap: 10px; }
.swatch { width: 14px; height: 14px; border-radius: 4px; flex: none; }
.no { font-variant-numeric: tabular-nums; color: var(--muted); font-size: 13px; }
.brand { font-family: var(--font-display); font-weight: 700; font-size: 17px; }
.idea { color: var(--muted); font-size: 13.5px; }
.hl { font-size: 14px; }
.meta { display: flex; justify-content: space-between; gap: 8px; font-size: 13px; color: var(--muted); border-top: 1px solid var(--line); padding-top: 10px; }
.meta b { color: var(--fg); }
.todo { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 18px 20px; display: grid; gap: 8px; }
.todo h2 { font-family: var(--font-display); font-size: 18px; margin: 0; }
.todo ul { margin: 0; padding-left: 1.2em; display: grid; gap: 4px; }
"""


def render_index():
    cards = []
    for lp in LPS:
        price = " / ".join(v for _, v in lp["price"])
        cards.append(f"""<a class="card" href="lp/{lp['slug']}.html">
  <div class="top"><span class="swatch" style="background:{lp['colors']['brand']}"></span><span class="no">{lp['no']:02d}</span><span class="brand">{escape(lp['brand'])}</span></div>
  <span class="idea">{escape(lp['idea'])}</span>
  <span class="hl">{escape(lp['title'].replace('<br>', ''))}</span>
  <div class="meta"><span>予定価格 <b>{escape(price)}</b></span><span>ページを開く →</span></div>
</a>""")
    return f"""<title>事前登録LP 10本</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@700&family=Noto+Sans+JP:wght@400;500;700&display=swap">
<style>{INDEX_CSS}</style>
<div class="wrap">
  <header>
    <h1>事前登録LP 10本（確認用）</h1>
    <p class="lead">広告で反応を測るための事前登録ページです。商品はまだなく、メールアドレスの登録数で「欲しい人がいるか」を確かめます。カードを開くと各ページを確認できます。この一覧ページは確認用で、公開はしません。</p>
  </header>
  <div class="grid">
    {''.join(cards)}
  </div>
  <div class="todo">
    <h2>公開前に必要なこと</h2>
    <ul>
      <li>ドメインを取得し、各ページを公開する（Cloudflare Pages や Vercel の無料枠で公開できます）</li>
      <li>登録フォームの送信先をつなぐ（Formspree などの無料サービス）</li>
      <li>運営者名と連絡先を入れる（ページ下部）</li>
      <li>広告の計測タグを入れる（Googleアナリティクス、Meta・TikTokのピクセル）</li>
      <li>ページで約束している特典（割引クーポン、無料期間など）を、公開時に実際に用意する</li>
    </ul>
  </div>
</div>
"""


def main():
    # LP本体は手作りのデザイン版に置き換えたため、通常は一覧ページだけを書き出す。
    # 旧テンプレート版のLPを書き出したいときだけ --template-lps を付ける。
    import sys
    if "--template-lps" in sys.argv:
        out = ROOT / "lp"
        out.mkdir(exist_ok=True)
        for lp in LPS:
            (out / f"{lp['slug']}.html").write_text(render_lp(lp), encoding="utf-8")
        print(f"{len(LPS)} template LPs written to {out}")
    (ROOT / "index.html").write_text(render_index(), encoding="utf-8")
    print("index.html written")


if __name__ == "__main__":
    main()
