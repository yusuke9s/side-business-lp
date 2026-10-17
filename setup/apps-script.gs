/**
 * 事前登録LPのフォーム受付（Google Apps Script）
 *
 * Googleスプレッドシートの「拡張機能 > Apps Script」に貼り付けて、
 * ウェブアプリとしてデプロイする。手順は setup/SETUP.md を参照。
 *
 * 登録があるたびに「登録」シートへ1行追加する。
 */

const SHEET_NAME = '登録';
const HEADERS = ['受信日時', 'サービス', 'メールアドレス', '質問の回答', 'ページ', 'URLパラメータ', '参照元', '送信日時（端末）'];
const SERVICES = ['pet', 'kaitai', 'eisei', 'koumuin', 'receipt', 'taikyo', 'watch', 'shibou', 'renai', 'souzoku'];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const data = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    const email = String(data.email || '').trim();
    const service = String(data.service || '');
    // 形式がおかしい送信は記録しない
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || SERVICES.indexOf(service) === -1) {
      return json_({ ok: false });
    }
    getSheet_().appendRow([
      new Date(),
      service,
      email,
      clip_(data.answer),
      clip_(data.page),
      clip_(data.query),
      clip_(data.referrer),
      clip_(data.sentAt),
    ]);
    return json_({ ok: true });
  } finally {
    lock.releaseLock();
  }
}

// ブラウザでウェブアプリのURLを開いたときの動作確認用
function doGet() {
  return json_({ ok: true, message: '受付中です' });
}

function getSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    // 最初のシートを「登録」として使う（見出し行が無ければ入れる）
    sheet = ss.getSheets()[0];
    sheet.setName(SHEET_NAME);
    if (sheet.getLastRow() === 0) sheet.appendRow(HEADERS);
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function clip_(v) {
  // 数式として解釈されないよう先頭の記号を無害化し、長さを制限する
  const s = String(v == null ? '' : v).slice(0, 500);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
