// 贈答送り状メーカー（public/app/okurijo/）の Meta 広告クリエイティブを作る。
// 使い方: NODE_PATH=$(npm root -g) node ads/creatives/src/okurijo-build.js
//   → ads/creatives/src/okurijo-{A,B}-{feed,square,story}.html を書き出し、
//     ads/creatives/okurijo-{A,B}-{feed,square,story}.png に撮る。
// 文言を直すときはこのファイルを直して再実行する（HTML は毎回上書きされる）。
"use strict";
const fs = require("fs");
const path = require("path");

const SRC = __dirname;
const OUT = path.resolve(__dirname, "..");

// ---------- アイコン（Phosphor Icons bold, MIT。ツール本体と同じもの） ----------
const ICON = {
  arrow: "M224.49,136.49l-72,72a12,12,0,0,1-17-17L187,140H40a12,12,0,0,1,0-24H187L135.51,64.48a12,12,0,0,1,17-17l72,72A12,12,0,0,1,224.49,136.49Z",
  ok: "M176.49,95.51a12,12,0,0,1,0,17l-56,56a12,12,0,0,1-17,0l-24-24a12,12,0,1,1,17-17L112,143l47.51-47.52A12,12,0,0,1,176.49,95.51ZM236,128A108,108,0,1,1,128,20,108.12,108.12,0,0,1,236,128Zm-24,0a84,84,0,1,0-84,84A84.09,84.09,0,0,0,212,128Z",
  warn: "M240.26,186.1,152.81,34.23h0a28.74,28.74,0,0,0-49.62,0L15.74,186.1a27.45,27.45,0,0,0,0,27.710A28.31,28.31,0,0,0,40.55,228h174.9a28.31,28.31,0,0,0,24.79-14.19A27.45,27.45,0,0,0,240.26,186.1Zm-20.8,15.7a4.460,4.460,0,0,1-4,2.2H40.55a4.46,4.46,0,0,1-4-2.2,3.56,3.56,0,0,1,0-3.73L124,46.2a4.77,4.77,0,0,1,8,0l87.44,151.87A3.56,3.56,0,0,1,219.46,201.8ZM116,136V104a12,12,0,0,1,24,0v32a12,12,0,0,1-24,0Zm28,40a16,16,0,1,1-16-16A16,16,0,0,1,144,176Z",
  user: "M234.38,210a123.36,123.36,0,0,0-60.78-53.23,76,76,0,1,0-91.2,0A123.36,123.36,0,0,0,21.62,210a12,12,0,1,0,20.77,12c18.12-31.32,50.12-50,85.61-50s67.49,18.69,85.61,50a12,12,0,0,0,20.77-12ZM76,96a52,52,0,1,1,52,52A52.06,52.06,0,0,1,76,96Z",
  csv: "M48,180c0,8.67,5.49,16,12,16a10.27,10.27,0,0,0,7.33-3.43,12,12,0,1,1,17.34,16.6A34,34,0,0,1,60,220C40.15,220,24,202,24,180s16.15-40,36-40a34,34,0,0,1,24.67,10.830,12,12,0,1,1-17.34,16.6A10.27,10.27,0,0,0,60,164C53.49,164,48,171.31,48,180Zm97.51-5.71c-5.13-3.45-11.33-5.24-16.8-6.82a79.5,79.5,0,0,1-7.91-2.59c2.45-1.18,9.71-1.3,16.070.33A12,12,0,0,0,143,142a69.24,69.24,0,0,0-12-1.86c-9.93-.66-18,1.08-24.1,5.17a24.45,24.45,0,0,0-10.69,17.76c-1.1,8.74,2.48,16.27,10.11,21.19,4.78,3.09,10.36,4.7,15.75,6.26,3,.89,7.94,2.3,9.88,3.53a2,2,0,0,1-.22.71c-1.36,1.55-9.57,1.79-16.39-.06a12,12,0,0,0-6.45,23.11A63.73,63.730,0,0,0,125.09,220c6.47,0,13.74-1.17,19.74-5.15a24.73,24.73,0,0,0,10.95-18C157,187.53,153.32,179.53,145.51,174.27ZM216,140.68A12,12,0,0,0,200.7,148L192,172.3,183.3,148A12,12,0,1,0,160.7,156l20,56a12,12,0,0,0,22.6,0l20-56A12,12,0,0,0,216,140.68ZM36,108V40A20,20,0,0,1,56,20h96a12,12,0,0,1,8.49,3.51l56,56A12,12,0,0,1,220,88v20a12,12,0,1,1-24,0v-4H148a12,12,0,0,1-12-12V44H60v64a12,12,0,1,1-24,0ZM160,80h23L160,57Z",
  truck: "M255.14,115.54l-14-35A19.89,19.89,0,0,0,222.58,68H196V64a12,12,0,0,0-12-12H32A20,20,0,0,0,12,72V184a20,20,0,0,0,20,20H46.06a36,36,0,0,0,67.88,0h44.12a36,36,0,0,0,67.88,0H236a20,20,0,0,0,20-20V120A21.7,21.7,0,0,0,255.14,115.54ZM196,92h23.88l6.4,16H196ZM80,204a12,12,0,1,1,12-12A12,12,0,0,1,80,204Zm92-41.92A36.32,36.32,0,0,0,158.06,180H113.94a36,36,0,0,0-67.88,0H36V140H172ZM172,116H36V76H172Zm20,88a12,12,0,1,1,12-12A12,12,0,0,1,192,204Zm40-24h-6.06A36.09,36.09,0,0,0,196,156.23V132h36Z",
  shield: "M208,36H48A20,20,0,0,0,28,56v56c0,54.29,26.32,87.22,48.4,105.29,23.71,19.39,47.44,26,48.44,26.29a12.1,12.1,0,0,0,6.32,0c1-.28,24.73-6.9,48.44-26.29,22.08-18.07,48.4-51,48.4-105.29V56A20,20,0,0,0,208,36Zm-4,76c0,35.71-13.09,64.69-38.91,86.15A126.28,126.28,0,0,1,128,219.38a126.14,126.14,0,0,1-37.090-21.23C65.09,176.69,52,147.71,52,112V60H204ZM79.51,144.49a12,12,0,1,1,17-17L112,143l47.51-47.52a12,12,0,0,1,17,17l-56,56a12,12,0,0,1-17,0Z"
};
const ic = (k, cls = "i") => `<svg class="${cls}" viewBox="0 0 256 256" aria-hidden="true"><path d="${ICON[k]}"/></svg>`;

// ---------- 共通 CSS（ツール本体 public/app/okurijo/index.html と同じトークン） ----------
const CSS = `
:root {
  --kraft: #cfad7a; --kraft-d: #a98250; --kraft-l: #ead9b6; --kraft-ll: #f5ecd9;
  --paper: #fffcf5; --paper2: #f8f1e3; --ink: #2a2017; --ink2: #4d3e2d; --mut: #6b5841; --line: #dccaa6; --line2: #c9b38a;
  --shu: #b5381d; --shu-d: #8f2a14; --shu-l: #fbebe5; --ok: #2d6633; --ok-l: #e7f1e3;
  --warn: #8a5300; --warn-l: #fff2d3; --cool: #2b5f8e;
  --fd: "Yusei Magic", "BIZ UDPGothic", sans-serif;
  --fb: "BIZ UDPGothic", "Hiragino Sans", sans-serif;
  --fm: "BIZ UDGothic", ui-monospace, monospace;
}
*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; overflow: hidden; }
body { color: var(--ink); font-family: var(--fb); line-height: 1.5; font-variant-numeric: tabular-nums; }
p, h1 { margin: 0; }
svg.i { width: 1em; height: 1em; fill: currentColor; flex: none; display: inline-block; }
.ad { position: relative; overflow: hidden;
  background-color: var(--kraft);
  background-image:
    radial-gradient(ellipse at 50% 42%, rgba(255,240,205,.32), rgba(255,240,205,0) 62%),
    radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 58%, rgba(70,45,10,.20) 100%),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .35 0 0 0 0 .24 0 0 0 0 .1 0 0 0 .22 0'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)'/%3E%3C/svg%3E"),
    repeating-linear-gradient(90deg, rgba(90,60,20,.05) 0 3px, transparent 3px 9px);
}
.abs { position: absolute; }

/* 段ボールのフラップの折り目・ガムテープ */
.fold { position: absolute; left: 0; right: 0; height: 0; border-top: 3px solid rgba(110,75,30,.28); box-shadow: 0 3px 0 rgba(255,240,210,.35); }
.gum { position: absolute; background: rgba(250,240,205,.62); box-shadow: 0 1px 3px rgba(60,40,10,.25);
  border-left: 2px dashed rgba(120,90,40,.25); border-right: 2px dashed rgba(120,90,40,.25);
  background-image: repeating-linear-gradient(90deg, rgba(255,255,255,.18) 0 2px, transparent 2px 7px); }

/* ロゴ（ツールのヘッダーと同じ絵とフォント） */
.logo { display: inline-flex; align-items: center; gap: .38em; background: var(--kraft-l); border: .06em solid var(--ink); border-radius: .14em; padding: .22em .55em .22em .32em; box-shadow: 0 .09em 0 var(--ink); white-space: nowrap; }
.logo svg { width: 1.45em; height: 1.45em; flex: none; }
.logo b { font-family: var(--fd); font-weight: 400; line-height: 1.1; letter-spacing: .02em; }

/* はんこ（無料・登録不要） */
.stamp { display: inline-flex; align-items: center; gap: .32em; color: var(--shu); font-weight: 700; line-height: 1; white-space: nowrap;
  border: .11em solid var(--shu); outline: .05em solid var(--shu); outline-offset: .12em; border-radius: .2em;
  padding: .36em .6em .38em; background: rgba(255,252,245,.78); transform: rotate(-6deg); letter-spacing: .06em; }

/* 見出し */
.hl { font-family: var(--fd); font-weight: 400; line-height: 1.22; letter-spacing: .01em; color: var(--ink); white-space: nowrap; }
.hl .ln { display: block; }
.hl em { font-style: normal; color: var(--shu); }
.hl .mk { font-style: normal; background: linear-gradient(transparent 62%, rgba(255,252,245,.85) 62% 92%, transparent 92%); padding: 0 .04em; }

/* サブ（荷札テープ） */
.tape { display: inline-block; background: rgba(250,240,205,.9); padding: .28em .8em .32em; transform: rotate(-1.2deg); box-shadow: 0 .06em .12em rgba(60,40,10,.3);
  border-left: .06em dashed rgba(120,90,40,.3); border-right: .06em dashed rgba(120,90,40,.3); font-weight: 700; color: var(--ink2); white-space: nowrap; line-height: 1.3; }

/* ボタン（ツールの .btn.pri） */
.cta { display: inline-flex; align-items: center; justify-content: center; gap: .5em; font-weight: 700; line-height: 1.2; white-space: nowrap;
  background: var(--shu); color: #fff; border: .05em solid var(--shu-d); border-radius: .16em; padding: .62em 1.15em .64em 1.25em;
  box-shadow: 0 .14em 0 var(--shu-d), 0 .5em .9em -.3em rgba(60,25,5,.55); letter-spacing: .03em; }
.cta svg { width: 1.05em; height: 1.05em; fill: #fff; }

/* 表示例 */
.rei { position: absolute; display: inline-block; font-weight: 700; color: var(--shu); background: #fff; border: 2px solid var(--shu); border-radius: 3px; padding: 2px 9px 3px; font-size: 19px; letter-spacing: .12em; line-height: 1.2; z-index: 30; }

/* LINE 風のトーク画面 */
.chat { position: absolute; border: .12em solid var(--ink); border-radius: .9em; overflow: hidden; background: #8ea8c6; box-shadow: 0 .9em 1.4em -.8em rgba(40,25,5,.7); }
.chat-top { display: flex; align-items: center; gap: .5em; background: #26303d; color: #fff; padding: .5em .8em; font-weight: 700; font-size: .95em; }
.chat-top .back { width: .55em; height: .55em; border-left: .14em solid #fff; border-bottom: .14em solid #fff; transform: rotate(45deg); margin-right: .2em; }
.chat-body { padding: .8em .7em 1em .7em; display: grid; gap: .55em; }
.msg { display: grid; grid-template-columns: 1.9em minmax(0,1fr); gap: .45em; align-items: start; }
.av { width: 1.9em; height: 1.9em; border-radius: 50%; background: #efe3c9; display: grid; place-items: center; color: var(--mut); }
.av svg { width: 1.15em; height: 1.15em; fill: currentColor; }
.bub { position: relative; background: #fff; border-radius: .85em; padding: .5em .7em .55em; line-height: 1.5; color: #222; white-space: pre; width: max-content; max-width: 100%; }
.bub .gap { display: block; height: .45em; }
.bub::before { content: ""; position: absolute; left: -.35em; top: .35em; border: .3em solid transparent; border-right: .45em solid #fff; border-left: 0; }
.bub + .bub { margin-top: .4em; }
.bub + .bub::before { display: none; }
.tm { display: block; font-size: .6em; color: #eef3f8; margin-top: .25em; }

/* 届け先カード（小さな送り状。ツールの .rec） */
.rec { position: absolute; background: var(--paper); border: .09em solid var(--ink); border-radius: .2em; box-shadow: 0 .45em .8em -.45em rgba(60,40,10,.75);
  display: grid; grid-template-columns: auto minmax(0,1fr) auto; gap: .5em; align-items: start; padding: .78em .7em .62em; }
.rec::before { content: ""; position: absolute; left: 0; right: 0; top: -.09em; height: .38em;
  background: radial-gradient(circle at .3em 0, var(--kraft) .15em, transparent .18em) 0 0 / .62em .38em repeat-x; }
.rno { font-family: var(--fm); font-size: .62em; font-weight: 700; color: var(--shu); border: .12em solid var(--shu); border-radius: .12em; padding: 0 .3em; line-height: 1.55; margin-top: .3em; background: #fff; }
.rname { display: block; font-size: 1.04em; font-weight: 700; line-height: 1.3; white-space: nowrap; }
.rname small { font-size: .7em; margin-left: .2em; color: var(--ink2); }
.raddr { display: block; font-size: .7em; color: var(--ink2); line-height: 1.45; margin-top: .25em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.zipbox { display: inline-flex; align-items: center; gap: .08em; font-family: var(--fm); margin-right: .4em; vertical-align: .06em; }
.zipbox i { font-style: normal; display: inline-grid; place-items: center; width: 1.1em; height: 1.4em; border: .07em solid var(--shu); color: var(--ink); background: #fff; line-height: 1; }
.zipbox s { text-decoration: none; color: var(--shu); margin: 0 .05em; }
.zipbox .x { border-color: var(--shu); background: var(--shu-l); color: var(--shu-d); }
.rchips { display: flex; gap: .3em; margin-top: .4em; }
.tag { position: relative; display: inline-flex; align-items: center; padding: .1em .55em .1em 1.05em; background: var(--kraft-l); border: .05em solid var(--kraft-d); border-radius: .15em .6em .6em .15em; font-size: .66em; font-weight: 700; line-height: 1.35; white-space: nowrap; }
.tag::before { content: ""; position: absolute; left: .38em; top: 50%; width: .32em; height: .32em; margin-top: -.16em; border-radius: 50%; background: var(--paper); border: .05em solid var(--kraft-d); }
.badge { display: inline-flex; align-items: center; gap: .22em; font-size: .62em; font-weight: 700; padding: .12em .5em; border-radius: .8em; white-space: nowrap; }
.badge svg { width: 1.15em; height: 1.15em; fill: currentColor; }
.badge.err { background: var(--shu); color: #fff; }
.badge.wrn { background: var(--warn-l); color: var(--warn); border: .08em solid var(--warn); }
.badge.ok { background: var(--ok-l); color: var(--ok); }
.iss { grid-column: 2 / -1; font-size: .64em; font-weight: 700; line-height: 1.35; display: flex; gap: .3em; align-items: center; margin-top: -.15em; white-space: nowrap; }
.iss.err { color: var(--shu-d); } .iss.wrn { color: var(--warn); }
.iss svg { width: 1.1em; height: 1.1em; fill: currentColor; }
.badch { display: inline-grid; place-items: center; min-width: 1.3em; height: 1.3em; border: .1em solid var(--shu); border-radius: .12em; background: var(--shu-l); color: var(--ink); margin: 0 .05em; line-height: 1; }

/* CSV の表 */
.sheet { position: absolute; background: #fff; border: .09em solid var(--ink); border-radius: .2em; box-shadow: 0 .9em 1.4em -.8em rgba(40,25,5,.7); }
.sheet-tabs { position: absolute; left: .7em; bottom: 100%; display: flex; gap: .25em; }
.stab { font-size: .66em; font-weight: 700; padding: .35em .75em .3em; background: var(--kraft-ll); border: .12em solid var(--ink); border-bottom: 0; border-radius: .35em .35em 0 0; color: var(--ink2); white-space: nowrap; }
.stab.on { background: #fff; color: var(--ink); box-shadow: inset 0 .25em 0 var(--shu); position: relative; top: .12em; padding-bottom: .42em; }
.sheet-h { display: flex; align-items: center; gap: .35em; padding: .45em .6em; line-height: 1.45; background: var(--paper2); border-bottom: .06em solid var(--line2); font-weight: 700; font-size: .72em; white-space: nowrap; }
.sheet-h svg { width: 1.4em; height: 1.4em; fill: var(--ok); }
.sheet table { border-collapse: collapse; width: 100%; font-family: var(--fm); font-size: .62em; table-layout: fixed; }
.sheet th, .sheet td { border: .06em solid var(--line); padding: .32em .45em; text-align: left; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; line-height: 1.35; }
.sheet th { background: var(--paper2); color: var(--ink2); font-family: var(--fb); font-weight: 700; }
.sheet td.n, .sheet th.n { color: var(--mut); text-align: center; background: var(--paper2); font-size: .9em; }
.sheet tr:first-child th { border-top: 0; }
.sheet th:first-child, .sheet td:first-child { border-left: 0; } .sheet th:last-child, .sheet td:last-child { border-right: 0; }
.sheet tr:last-child td { border-bottom: 0; }

/* 運送会社 */
.carr { display: flex; gap: .35em; flex-wrap: nowrap; }
.car { display: inline-flex; align-items: center; gap: .35em; background: #fff; border: .07em solid var(--line2); border-radius: .2em; padding: .3em .6em; font-weight: 700; font-size: .7em; white-space: nowrap; }
.car .rad { width: .95em; height: .95em; border-radius: 50%; border: .12em solid var(--ink2); display: grid; place-items: center; background: #fff; }
.car.on { border-color: var(--ink); box-shadow: inset .28em 0 0 var(--shu); background: var(--paper); }
.car.on .rad::after { content: ""; width: .45em; height: .45em; border-radius: 50%; background: var(--shu); }

/* 水引風のひも（矢印） */
.cord { position: absolute; overflow: visible; }
`;

// ---------- 部品 ----------
const LOGO_SVG = `<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M5 9.5 L13 3 H35 V37 H13 L5 30.5 Z" fill="#d9b680" stroke="#2a2017" stroke-width="2"/><circle cx="12" cy="20" r="3" fill="#fffcf5" stroke="#2a2017" stroke-width="1.8"/><path d="M12 17 C 6 10, 2 12, 1 6" fill="none" stroke="#b5381d" stroke-width="1.8" stroke-linecap="round"/><path d="M19 12h11M19 17h11M19 22h11M19 27h7" stroke="#2a2017" stroke-width="2"/><rect x="25.5" y="25" width="7" height="7" fill="none" stroke="#b5381d" stroke-width="1.6" transform="rotate(-8 29 28.5)"/></svg>`;
const logo = (x, y, fs) => `<div class="abs logo" style="left:${x}px;top:${y}px;font-size:${fs}px">${LOGO_SVG}<b>贈答送り状メーカー</b></div>`;
const stamp = (x, y, fs) => `<div class="abs stamp" style="left:${x}px;top:${y}px;font-size:${fs}px">無料・登録不要</div>`;
const cta = (x, y, fs, extra = "") => `<div class="abs cta" style="left:${x}px;top:${y}px;font-size:${fs}px;${extra}">無料で使ってみる${ic("arrow")}</div>`;
const sub = (x, y, fs, text) => `<div class="abs tape" style="left:${x}px;top:${y}px;font-size:${fs}px">${text}</div>`;
const rei = (x, y) => `<span class="rei" style="left:${x}px;top:${y}px">表示例</span>`;

const zip = (s, bad) => `<span class="zipbox">${s.slice(0, 3).split("").map(d => `<i>${d}</i>`).join("")}<s>-</s>${s.slice(3).split("").map((d, k) => `<i${bad && k === 3 ? ' class="x"' : ""}>${d}</i>`).join("")}</span>`;

// 届け先（ツールのサンプル注文と同じ架空の人・住所）
const R = {
  takahashi: { no: "01", name: `<span class="badch">髙</span>橋 誠`, zip: "1540001", addr: "東京都世田谷区池尻2-31-24", tag: "りんご サンふじ 5kg", st: "err", iss: ["err", "「髙」は送り状に使えない字です。「高」に直せます"] },
  yamamoto: { no: "02", name: "山本 由美子", zip: "5600082", addr: "大阪府豊中市新千里東町3-5-12", tag: "りんご サンふじ 10kg", st: "ok" },
  midori: { no: "03", name: "株式会社みどり商事 総務部", hon: "御中", zip: "0600042", addr: "北海道札幌市中央区大通西10-4", tag: "りんごジュース 1L×6本", st: "ok" },
  tanaka: { no: "04", name: "田中 健一", zip: "8120011", addr: "福岡県福岡市博多区博多駅前4-10-8", tag: "シャインマスカット 2房", st: "ok" },
  nakamura: { no: "05", name: "中村 さくら", zip: "9000015", addr: "沖縄県那覇市久茂地2-22-10", tag: "りんご サンふじ 5kg", st: "wrn", iss: ["wrn", "建物名が長すぎます（ヤマトは全角16文字まで）"] }
};
function rec(r, x, y, w, fs, opt = {}) {
  const st = r.st === "err" ? `<span class="badge err">${ic("warn")}要確認</span>` : r.st === "wrn" ? `<span class="badge wrn">${ic("warn")}文字数</span>` : `<span class="badge ok">${ic("ok")}OK</span>`;
  const iss = r.iss && !opt.noIss ? `<div class="iss ${r.iss[0]}">${ic("warn")}${r.iss[1]}</div>` : "";
  const rot = opt.rot ? `transform:rotate(${opt.rot}deg);` : "";
  return `<div class="rec" style="left:${x}px;top:${y}px;width:${w}px;font-size:${fs}px;${rot}${opt.z ? "z-index:" + opt.z + ";" : ""}">
  <span class="rno">${r.no}</span>
  <div style="min-width:0"><b class="rname">${r.name}<small>${r.hon || "様"}</small></b>
  ${opt.noAddr ? "" : `<span class="raddr">${zip(r.zip)}${r.addr}</span>`}
  ${opt.noTag ? "" : `<div class="rchips"><span class="tag">${r.tag}</span></div>`}</div>
  <div>${st}</div>${iss}
</div>`;
}

function chat(x, y, w, fs, lines, opt = {}) {
  return `<div class="chat" style="left:${x}px;top:${y}px;width:${w}px;font-size:${fs}px;${opt.rot ? `transform:rotate(${opt.rot}deg);` : ""}">
  <div class="chat-top"><span class="back"></span>佐藤 恵子</div>
  <div class="chat-body">
    <div class="msg"><span class="av">${ic("user")}</span><div>
      ${lines.map(l => `<div class="bub">${l.split("\n").map(t => t ? t : '<span class="gap"></span>').join("\n").replace(/\n<span/g, "<span").replace(/span>\n/g, "span>")}</div>`).join("")}
      <span class="tm">18:42</span></div></div>
  </div>
</div>`;
}
const CHAT_A = [
  "お歳暮お願いします！",
  "髙橋誠さん 世田谷区池尻\n2-31-24 グリーンハイツ203\n5kgを1箱\n\n山本由美子様〒5600082\n豊中市新千里東町3-5-12\n10kg 14時以降で\n\nあと中村さんにも5kgを…"
];

function sheet(x, y, w, fs, rows, opt = {}) {
  const tabs = `<div class="sheet-tabs"><span class="stab on">ヤマト B2クラウド</span><span class="stab">佐川 e飛伝Ⅲ</span><span class="stab">ゆうパック</span></div>`;
  const head = `<tr><th class="n" style="width:1.9em"></th><th style="width:${opt.c1 || 30}%">お届け先名</th><th style="width:${opt.c2 || 22}%">郵便番号</th><th>住所</th></tr>`;
  const body = rows.map((r, k) => `<tr><td class="n">${k + 1}</td><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td></tr>`).join("");
  return `<div class="sheet" style="left:${x}px;top:${y}px;width:${w}px;font-size:${fs}px;${opt.rot ? `transform:rotate(${opt.rot}deg);` : ""}">
  ${opt.tabs === false ? "" : tabs}
  <div class="sheet-h">${ic("csv")}${opt.file || "送り状_取り込み用.csv"}</div>
  <table>${head}${body}</table>
</div>`;
}
const ROWS = [
  ["高橋 誠", "154-0001", "東京都世田谷区池尻2-31-24"],
  ["山本 由美子", "560-0082", "大阪府豊中市新千里東町3-5-12"],
  ["株式会社みどり商事", "060-0042", "北海道札幌市中央区大通西10-4"],
  ["田中 健一", "812-0011", "福岡県福岡市博多区博多駅前4-10-8"],
  ["中村 さくら", "900-0015", "沖縄県那覇市久茂地2-22-10"]
];

// 水引のような紅白のひもで矢印を描く。d は SVG パス、(w,h) はキャンバス
function cord(x, y, w, h, d, head) {
  return `<svg class="cord" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px" viewBox="0 0 ${w} ${h}">
  <path d="${d}" fill="none" stroke="rgba(60,30,5,.25)" stroke-width="15" stroke-linecap="round" transform="translate(0 4)"/>
  <path d="${d}" fill="none" stroke="#b5381d" stroke-width="13" stroke-linecap="round"/>
  <path d="${d}" fill="none" stroke="#fffcf5" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="1 0"/>
  <path d="${head}" fill="#b5381d" stroke="#8f2a14" stroke-width="3" stroke-linejoin="round"/>
</svg>`;
}

// りんご（産直の箱から少しのぞく）
const apple = (x, y, s, rot = 0, id = "a") => `<svg class="abs" style="left:${x}px;top:${y}px;width:${s}px;height:${s}px;transform:rotate(${rot}deg);filter:drop-shadow(0 ${s * .06}px ${s * .05}px rgba(60,30,5,.45))" viewBox="0 0 100 100">
  <defs><radialGradient id="g${id}" cx="35%" cy="35%" r="70%"><stop offset="0" stop-color="#e4573a"/><stop offset=".55" stop-color="#b5281a"/><stop offset="1" stop-color="#7d170e"/></radialGradient></defs>
  <path d="M50 26 C 40 18, 14 18, 12 46 C 10 72, 30 94, 44 92 C 48 91, 52 91, 56 92 C 70 94, 90 72, 88 46 C 86 18, 60 18, 50 26 Z" fill="url(#g${id})"/>
  <path d="M26 40 C 28 32, 34 29, 40 30" stroke="rgba(255,235,200,.75)" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M50 27 C 50 18, 52 12, 56 7" stroke="#5a3a1a" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M55 15 C 62 5, 76 6, 80 10 C 74 18, 62 20, 55 15 Z" fill="#3d7a3a"/>
</svg>`;

// 段ボール箱（正面）＋送り状。水引の帯つき
function box(x, y, w, h) {
  return `<div class="abs" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;background:#c79d62;border:3px solid var(--ink);border-radius:4px;box-shadow:0 18px 26px -16px rgba(40,25,5,.8);
    background-image:repeating-linear-gradient(90deg, rgba(90,60,20,.07) 0 3px, transparent 3px 9px),linear-gradient(#b98d52 0 18px, transparent 18px);">
    <div style="position:absolute;left:0;right:0;top:18px;border-top:3px solid rgba(60,40,10,.45)"></div>
    <div style="position:absolute;left:44%;width:12%;top:0;bottom:0;background:rgba(250,240,205,.6);border-left:2px dashed rgba(120,90,40,.3);border-right:2px dashed rgba(120,90,40,.3)"></div>
  </div>`;
}

// ---------- ページ ----------
function page(title, W, H, body) {
  return `<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>${title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=BIZ+UDPGothic:wght@400;700&family=BIZ+UDGothic:wght@700&family=Yusei+Magic&display=swap">
<style>${CSS}
html, body { width: ${W}px; height: ${H}px; }
.ad { width: ${W}px; height: ${H}px; }
</style>
</head>
<body><div class="ad">
${body}
</div></body>
</html>
`;
}

const HL_A = (fs, x, y, lines) => `<h1 class="abs hl" style="left:${x}px;top:${y}px;font-size:${fs}px">${lines.map(l => `<span class="ln">${l}</span>`).join("")}</h1>`;
const SUB_A = "ヤマト・佐川・ゆうパックの取り込み用ファイルを作る無料ツール";
const SUB_B = "届け先の一覧から、ヤマト・佐川・ゆうパックの取り込み用CSVへ";

const designs = {};
const carRow = (x, y, fs) => `<div class="abs carr" style="${x === "c" ? "left:0;right:0;justify-content:center" : `left:${x}px`};top:${y}px;font-size:${fs}px">${["ヤマト B2クラウド", "佐川 e飛伝Ⅲ", "ゆうパック"].map((c, k) => `<span class="car${k ? "" : " on"}"><span class="rad"></span>${c}</span>`).join("")}</div>`;

// ===== A: LINE の吹き出し → 届け先カード =====
designs["A-feed"] = [1080, 1350, () => `
<div class="fold" style="top:1214px"></div>
<div class="gum" style="left:-60px;top:28px;width:300px;height:64px;transform:rotate(-38deg)"></div>
${logo(56, 52, 38)}
${stamp(772, 62, 34)}
${HL_A(84, 56, 168, ["LINEの贈答注文を、", `<span class="mk">打ち直さずに</span><em>送り状へ。</em>`])}
${sub(52, 400, 30, SUB_A)}
${chat(44, 530, 444, 24, CHAT_A, { rot: -2 })}
${cord(452, 600, 120, 120, "M10 100 C 30 40, 60 30, 84 44", "M76 22 L110 52 L68 66 Z")}
${rec(R.takahashi, 556, 540, 480, 25)}
${rec(R.yamamoto, 556, 732, 480, 25)}
${rec(R.nakamura, 556, 880, 480, 25)}
${rei(940, 508)}
${carRow(556, 1066, 23)}
${cta(56, 1172, 40)}
${apple(900, 1180, 104, 10, "f1")}
`];

designs["A-square"] = [1080, 1080, () => `
<div class="gum" style="left:-70px;top:22px;width:280px;height:58px;transform:rotate(-38deg)"></div>
${logo(56, 44, 34)}
${stamp(786, 50, 31)}
${HL_A(72, 56, 138, ["LINEの贈答注文を、", `<span class="mk">打ち直さずに</span><em>送り状へ。</em>`])}
${sub(52, 330, 27, SUB_A)}
${chat(42, 438, 430, 21, CHAT_A, { rot: -2 })}
${cord(440, 500, 120, 120, "M10 100 C 30 40, 60 30, 84 44", "M76 22 L110 52 L68 66 Z")}
${rec(R.takahashi, 548, 446, 488, 23)}
${rec(R.yamamoto, 548, 622, 488, 23)}
${rec(R.nakamura, 548, 760, 488, 23, { noIss: true })}
${rei(948, 412)}
${cta(548, 940, 34, "width:488px")}
`];

designs["A-story"] = [1080, 1920, () => `
<div class="gum" style="left:-80px;top:70px;width:420px;height:80px;transform:rotate(-30deg)"></div>
<div class="gum" style="right:-100px;bottom:90px;width:440px;height:80px;transform:rotate(-30deg)"></div>
<div class="fold" style="top:1712px"></div>
${apple(70, 1730, 120, -12, "s1")}${apple(170, 1756, 104, 14, "s2")}
${logo(60, 276, 40)}
${stamp(744, 286, 36)}
${HL_A(106, 60, 400, ["LINEの贈答注文を、", `<span class="mk">打ち直さずに</span>`, `<em>送り状へ。</em>`])}
${sub(56, 812, 30, SUB_A)}
${chat(48, 930, 486, 25, CHAT_A, { rot: -2 })}
${cord(490, 1000, 120, 120, "M10 100 C 30 40, 60 30, 84 44", "M76 22 L110 52 L68 66 Z")}
${rec(R.takahashi, 588, 940, 448, 24)}
${rec(R.yamamoto, 588, 1124, 448, 24)}
${rec(R.nakamura, 588, 1266, 448, 24)}
${rei(944, 904)}
${carRow("c", 1466, 27)}
${cta(86, 1550, 46, "width:908px")}
`];

// ===== B: 束になった送り状 → CSV（運送会社のタブ） =====
const HL_B = (fs, x, y) => `<h1 class="abs hl" style="left:${x}px;top:${y}px;font-size:${fs}px"><span class="ln">お歳暮の送り状、</span><span class="ln"><em>まとめて一気に。</em></span></h1>`;
const stack = (x, y, w, fs, dy, list, rots) => list.map((r, k) => rec(r, x + k * 6, y + k * dy, w, fs, { noIss: true, noTag: k < list.length - 1, noAddr: k < list.length - 1, rot: rots[k], z: k + 1 })).join("");
const STACK = [R.tanaka, R.midori, R.yamamoto, R.takahashi];

designs["B-feed"] = [1080, 1350, () => `
<div class="gum" style="right:-70px;top:24px;width:320px;height:64px;transform:rotate(36deg)"></div>
<div class="fold" style="top:1214px"></div>
${logo(56, 52, 38)}
${stamp(772, 62, 34)}
${HL_B(104, 56, 160)}
${sub(52, 432, 29, SUB_B)}
${stack(44, 534, 540, 24, 58, STACK, [-4, -3, -2, -1])}
${cord(604, 590, 220, 260, "M10 30 C 130 10, 180 80, 170 196", "M140 188 L170 234 L198 182 Z")}
${sheet(330, 916, 710, 26, ROWS.slice(0, 4), { c1: 30, c2: 23 })}
${rei(948, 880)}
${apple(160, 1066, 96, -10, "f1")}
${cta(56, 1172, 40)}
`];

designs["B-square"] = [1080, 1080, () => `
<div class="gum" style="right:-70px;top:20px;width:300px;height:58px;transform:rotate(36deg)"></div>
${logo(56, 44, 34)}
${stamp(786, 50, 31)}
${HL_B(90, 56, 130)}
${sub(52, 366, 26, SUB_B)}
${stack(40, 484, 470, 25, 64, STACK, [-4, -3, -2, -1])}
${cord(466, 560, 120, 120, "M10 100 C 30 40, 60 30, 84 44", "M76 22 L110 52 L68 66 Z")}
${sheet(560, 560, 480, 25, ROWS, { c1: 34, c2: 27 })}
${rei(56, 450)}
${cta(56, 914, 36)}
${apple(800, 880, 110, -8, "q1")}${apple(910, 904, 96, 14, "q2")}
`];

designs["B-story"] = [1080, 1920, () => `
<div class="gum" style="right:-90px;top:80px;width:440px;height:80px;transform:rotate(32deg)"></div>
<div class="gum" style="left:-110px;bottom:100px;width:460px;height:80px;transform:rotate(32deg)"></div>
<div class="fold" style="top:1712px"></div>
${apple(760, 1730, 118, -8, "t1")}${apple(870, 1758, 104, 16, "t2")}
${logo(60, 276, 40)}
${stamp(744, 286, 36)}
${HL_B(118, 60, 410)}
${sub(56, 722, 31, SUB_B)}
${stack(56, 840, 640, 29, 70, STACK, [-4, -3, -2, -1])}
${cord(720, 880, 220, 300, "M10 40 C 140 20, 200 100, 180 230", "M150 222 L180 268 L208 214 Z")}
${sheet(86, 1300, 908, 28, ROWS.slice(0, 4), { c1: 28, c2: 21 })}
${rei(56, 804)}
${cta(86, 1556, 46, "width:908px")}
`];

// ---------- 書き出しと撮影 ----------
async function main() {
  const only = process.argv[2];
  const { chromium } = require("playwright");
  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
  for (const [key, [W, H, fn]] of Object.entries(designs)) {
    if (only && !key.startsWith(only)) continue;
    const name = `okurijo-${key}`;
    const html = page(`贈答送り状メーカー 広告 ${key} ${W}x${H}`, W, H, fn());
    const file = path.join(SRC, name + ".html");
    fs.writeFileSync(file, html);
    const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
    const pg = await ctx.newPage();
    await pg.goto("file://" + file, { waitUntil: "networkidle" });
    await pg.evaluate(async () => {
      await Promise.all([
        document.fonts.load('400 40px "Yusei Magic"', "LINEの贈答注文を打ち直さずに送り状へお歳暮まとめて一気"),
        document.fonts.load('700 20px "BIZ UDPGothic"', "無料で使ってみる髙橋"),
        document.fonts.load('700 20px "BIZ UDGothic"', "0123456789")
      ]);
      await document.fonts.ready;
    });
    await pg.waitForTimeout(300);
    await pg.screenshot({ path: path.join(OUT, name + ".png"), clip: { x: 0, y: 0, width: W, height: H } });
    await ctx.close();
    console.log("wrote", name);
  }
  await browser.close();
}
main().catch(e => { console.error(e); process.exit(1); });
