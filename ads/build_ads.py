"""ads_data.py から Google 広告エディタ用CSVと、広告運用プランのページを作る。

使い方: python3 ads/build_ads.py
"""

import csv
import sys
import unicodedata
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ads_data import ADS, DOMAIN  # noqa: E402

HERE = Path(__file__).parent
DAYS = 14
MEDIA = {"google": "Google 検索広告", "meta": "Instagram / Facebook", "tiktok": "TikTok"}
UTM = {"google": ("google", "cpc"), "meta": ("meta", "paid_social"), "tiktok": ("tiktok", "paid_social")}


def width(s):
    """Google 広告の文字数（全角=2、半角=1）。"""
    return sum(2 if unicodedata.east_asian_width(c) in "FWA" else 1 for c in s)


def url(slug, media):
    src, med = UTM[media]
    return f"{DOMAIN}/{slug}?utm_source={src}&utm_medium={med}&utm_campaign={slug}"


def check():
    errors = []
    for a in ADS:
        for h in a["headlines"]:
            if width(h) > 30:
                errors.append(f"{a['slug']} 見出し {width(h)}/30: {h}")
        for d in a["descriptions"]:
            if width(d) > 90:
                errors.append(f"{a['slug']} 説明文 {width(d)}/90: {d}")
        for p in a["paths"]:
            if width(p) > 15:
                errors.append(f"{a['slug']} パス {width(p)}/15: {p}")
        if not 3 <= len(a["headlines"]) <= 15:
            errors.append(f"{a['slug']} 見出しの数 {len(a['headlines'])}（3〜15）")
        if not 2 <= len(a["descriptions"]) <= 4:
            errors.append(f"{a['slug']} 説明文の数 {len(a['descriptions'])}（2〜4）")
    return errors


def write_csv():
    cols = (["Campaign", "Campaign Type", "Networks", "Budget", "Budget type", "Bid Strategy Type", "Campaign Status",
             "Ad Group", "Ad Group Status", "Max CPC", "Keyword", "Criterion Type", "Ad type"]
            + [f"Headline {i}" for i in range(1, 16)] + [f"Description {i}" for i in range(1, 5)]
            + ["Path 1", "Path 2", "Final URL", "Status"])
    rows = []
    for a in ADS:
        if "google" not in a["budget"]:
            continue
        camp = f"LP_{a['slug']}_{a['name']}"
        group = f"{a['slug']}_main"
        daily = round(a["budget"]["google"] / DAYS)
        rows.append({"Campaign": camp, "Campaign Type": "Search", "Networks": "Google search", "Budget": daily,
                     "Budget type": "Daily", "Bid Strategy Type": "Maximize clicks", "Campaign Status": "Paused"})
        rows.append({"Campaign": camp, "Ad Group": group, "Ad Group Status": "Enabled", "Max CPC": 150})
        for k in a["keywords"]:
            rows.append({"Campaign": camp, "Ad Group": group, "Keyword": k, "Criterion Type": "Phrase", "Status": "Enabled"})
        for n in a["negatives"]:
            rows.append({"Campaign": camp, "Keyword": n, "Criterion Type": "Campaign Negative Phrase", "Status": "Enabled"})
        ad = {"Campaign": camp, "Ad Group": group, "Ad type": "Responsive search ad",
              "Path 1": a["paths"][0], "Path 2": a["paths"][1], "Final URL": url(a["slug"], "google"), "Status": "Enabled"}
        for i, h in enumerate(a["headlines"], 1):
            ad[f"Headline {i}"] = h
        for i, d in enumerate(a["descriptions"], 1):
            ad[f"Description {i}"] = d
        rows.append(ad)
    out = HERE / "google-ads-editor.csv"
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    return out


CSS = """
:root { --bg: #f4f6f8; --surface: #ffffff; --fg: #182230; --muted: #5a6676; --line: #d9dfe6; --accent: #2d4f9e; --soft: #e8eef9;
  --ok: #1d7a52; --warn: #9a6510; --warn-soft: #fbf0db;
  --font-display: "Zen Kaku Gothic New", "Hiragino Sans", sans-serif; --font-body: "Noto Sans JP", "Hiragino Sans", sans-serif; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #11161d; --surface: #18202a; --fg: #e4e9ef; --muted: #99a4b3; --line: #2a3542; --accent: #8fb0ff; --soft: #1d2a45; --ok: #5fd39b; --warn: #f0b85a; --warn-soft: #3a2d14; color-scheme: dark; } }
:root[data-theme="dark"] { --bg: #11161d; --surface: #18202a; --fg: #e4e9ef; --muted: #99a4b3; --line: #2a3542; --accent: #8fb0ff; --soft: #1d2a45; --ok: #5fd39b; --warn: #f0b85a; --warn-soft: #3a2d14; color-scheme: dark; }
body { background: var(--bg); color: var(--fg); font-family: var(--font-body); font-size: 15px; line-height: 1.75; }
.wrap { max-width: 1060px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 40px 72px; display: grid; gap: 40px; }
h1, h2, h3 { font-family: var(--font-display); margin: 0; text-wrap: balance; line-height: 1.35; }
h1 { font-size: clamp(25px, 4vw, 34px); }
h2 { font-size: 21px; }
h3 { font-size: 15px; color: var(--muted); font-weight: 700; letter-spacing: 0.04em; }
p { margin: 0; }
.lead { color: var(--muted); max-width: 68ch; margin-top: 8px; }
section { display: grid; gap: 16px; min-width: 0; }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 20px; display: grid; gap: 14px; min-width: 0; }
.scroll { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 14px; }
th, td { text-align: left; padding: 9px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { font-size: 12px; color: var(--muted); font-weight: 500; }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
tfoot td { font-weight: 700; border-bottom: 0; }
.todo { display: grid; gap: 10px; counter-reset: t; margin: 0; padding: 0; list-style: none; }
.todo li { counter-increment: t; display: grid; grid-template-columns: 2em 1fr; gap: 8px; }
.todo li::before { content: counter(t); font-weight: 700; color: var(--accent); font-variant-numeric: tabular-nums; }
.todo b { display: block; }
.todo span { color: var(--muted); font-size: 14px; }
.svc-head { display: flex; align-items: baseline; justify-content: space-between; gap: 10px; flex-wrap: wrap; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; }
.chip { background: var(--soft); border-radius: 999px; padding: 2px 10px; font-size: 12.5px; font-weight: 700; color: var(--accent); }
.grid2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
ul.copy { margin: 0; padding: 0; list-style: none; display: grid; gap: 6px; }
ul.copy li { display: flex; justify-content: space-between; gap: 10px; background: var(--bg); border-radius: 8px; padding: 6px 10px; font-size: 14px; }
ul.copy li small { color: var(--muted); font-variant-numeric: tabular-nums; white-space: nowrap; }
.kw { font-size: 14px; color: var(--fg); }
.neg { font-size: 13px; color: var(--muted); }
pre.meta { white-space: pre-wrap; background: var(--bg); border-radius: 8px; padding: 10px 12px; margin: 0; font-family: var(--font-body); font-size: 14px; }
.url { font-size: 12.5px; word-break: break-all; color: var(--muted); }
.note { background: var(--warn-soft); color: var(--fg); border-radius: 8px; padding: 8px 12px; font-size: 13.5px; }
.gallery { display: grid; grid-template-columns: 1fr 0.56fr 1.9fr; gap: 10px; align-items: start; }
.gallery img { width: 100%; height: auto; border-radius: 8px; border: 1px solid var(--line); display: block; }
.rule { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
.rule div { border-top: 3px solid var(--accent); padding-top: 10px; display: grid; gap: 4px; }
.rule b { font-size: 15px; }
.rule span { color: var(--muted); font-size: 13.5px; }
@media (max-width: 760px) { .grid2, .rule { grid-template-columns: minmax(0, 1fr); } .gallery { grid-template-columns: 1fr 1fr; } .gallery img:last-child { grid-column: 1 / -1; } }
"""


def li(items, limit):
    return "".join(f"<li><span>{escape(x)}</span><small>{width(x)}/{limit}</small></li>" for x in items)


def write_plan():
    total = {m: 0 for m in MEDIA}
    rows = []
    for a in ADS:
        cells = "".join(f'<td class="num">{a["budget"].get(m, 0):,}円</td>' if a["budget"].get(m) else '<td class="num">—</td>' for m in MEDIA)
        for m in MEDIA:
            total[m] += a["budget"].get(m, 0)
        rows.append(f"<tr><td><b>{escape(a['name'])}</b><br><span class='neg'>{escape(a['idea'])}</span></td>{cells}<td class='num'>{sum(a['budget'].values()):,}円</td></tr>")
    grand = sum(total.values())
    foot = "".join(f'<td class="num">{total[m]:,}円</td>' for m in MEDIA)
    budget_table = f"""<div class="card scroll"><table>
<thead><tr><th>サービス</th>{''.join(f'<th class="num">{v}</th>' for v in MEDIA.values())}<th class="num">合計</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
<tfoot><tr><td>合計（2週間）</td>{foot}<td class="num">{grand:,}円</td></tr></tfoot></table></div>"""

    svcs = []
    for a in ADS:
        media = "".join(f'<span class="chip">{MEDIA[m]} {v:,}円</span>' for m, v in a["budget"].items())
        urls = "".join(f'<p class="url"><b>{MEDIA[m]}</b>：{escape(url(a["slug"], m))}</p>' for m in a["budget"])
        meta = ""
        if a["meta"]:
            label = "TikTok" if "meta" not in a["budget"] else "Instagram / Facebook"
            meta = f"""<div><h3>{label} の広告文</h3>
<pre class="meta">{escape(a['meta']['primary'])}</pre>
<p style="margin-top:6px;font-size:14px"><b>見出し：</b>{escape(a['meta']['headline'])}　<b>ボタン横の説明：</b>{escape(a['meta']['description'])}</p>
<p class="neg" style="margin-top:4px">配信先：{escape(a['audience'])}</p></div>"""
        google = ""
        if "google" in a["budget"]:
            google = f"""<div class="grid2">
<div><h3>検索広告の見出し（{len(a['headlines'])}本）</h3><ul class="copy">{li(a['headlines'], 30)}</ul></div>
<div><h3>説明文（{len(a['descriptions'])}本）</h3><ul class="copy">{li(a['descriptions'], 90)}</ul>
<h3 style="margin-top:14px">キーワード（フレーズ一致）</h3><p class="kw">{escape(' ／ '.join(a['keywords']))}</p>
<p class="neg">除外：{escape(' ／ '.join(a['negatives']))}</p></div></div>"""
        note = f'<p class="note">{escape(a["note"])}</p>' if a["note"] else ""
        gallery = f"""<div class="gallery">
<img src="creatives/{a['slug']}-square.png" alt="{escape(a['name'])}の広告画像（正方形）" loading="lazy">
<img src="creatives/{a['slug']}-story.png" alt="{escape(a['name'])}の広告画像（縦長）" loading="lazy">
<img src="creatives/{a['slug']}-landscape.png" alt="{escape(a['name'])}の広告画像（横長）" loading="lazy"></div>"""
        svcs.append(f"""<div class="card" id="{a['slug']}">
<div class="svc-head"><h2>{escape(a['name'])}</h2><div class="chips">{media}</div></div>
{gallery}{google}{meta}
<div><h3>リンク先（計測用パラメータつき）</h3>{urls}</div>{note}</div>""")

    html = f"""<title>広告運用プラン</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@700&family=Noto+Sans+JP:wght@400;500;700&display=swap">
<style>{CSS}</style>
<div class="wrap">
<header>
  <h1>広告運用プラン（事前登録LP 10本）</h1>
  <p class="lead">10本のLPに少額の広告を2週間出し、「先行登録してくれる人がどれくらいいるか」を比べます。反応が良かった2〜3本だけ、本当に作ります。広告文の右の数字は Google 広告の文字数（全角=2）です。</p>
</header>

<section>
  <h2>判断の基準</h2>
  <div class="rule">
    <div><b>登録率 8%以上</b><span>クリックした人のうち先行登録した人。ここまで来れば有望。作る候補にする。</span></div>
    <div><b>3〜8%</b><span>見出しや画像を差し替えて、もう1週間様子を見る。</span></div>
    <div><b>3%未満</b><span>広告費1万円か150クリックを使った時点で止める。</span></div>
  </div>
  <p class="neg">目安の数字です。1件の登録にかかった広告費（＝広告費÷登録数）も合わせて見ます。</p>
</section>

<section>
  <h2>予算（2週間）</h2>
  {budget_table}
</section>

<section>
  <h2>あなたにお願いしたいこと</h2>
  <div class="card"><ol class="todo">
    <li><div><b>Google アナリティクス 4 のプロパティを作り、「測定ID」（G-から始まる）を教える</b><span>analytics.google.com → 管理 → プロパティを作成 → ウェブ ストリームで lp.site-forge.jp を登録</span></div></li>
    <li><div><b>Google 広告のアカウントを作り、支払い方法を登録する</b><span>ads.google.com。作成後、「目標 → コンバージョン → ウェブサイト」で「見込み顧客フォームの送信」を作ると出るタグID（AW-）とラベルを教える</span></div></li>
    <li><div><b>Meta ビジネス（Instagram / Facebook 広告）を作り、ピクセルIDを教える</b><span>business.facebook.com → イベントマネージャ → データソースを追加 → ウェブ。ペット・解体見積・志望理由書で使う</span></div></li>
    <li><div><b>TikTok 広告のアカウントを作り、ピクセルIDを教える</b><span>ads.tiktok.com。恋愛ナビで使う（Meta は出会い関連の広告に事前許可が必要なため）</span></div></li>
  </ol></div>
  <p class="neg">IDを受け取ったら、10本のLPにまとめて設定します。Google 広告の検索広告は、取り込み用のファイル（ads/google-ads-editor.csv）を用意済みです。すべて「一時停止」の状態で入るので、確認してから配信を始められます。</p>
</section>

<section>
  <h2>サービスごとの広告</h2>
  {''.join(svcs)}
</section>
</div>
"""
    out = HERE / "plan.html"
    out.write_text(html, encoding="utf-8")
    return out, grand


if __name__ == "__main__":
    errs = check()
    if errs:
        print("\n".join(errs))
        sys.exit(1)
    print("lengths ok")
    print(write_csv())
    out, grand = write_plan()
    print(out, f"total {grand:,}")
