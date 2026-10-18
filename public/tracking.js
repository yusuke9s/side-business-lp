// 計測タグの読み込みと、先行登録の完了イベント送信（全LP共通）。
// IDは tracking-config.js で設定する。空のIDのサービスは読み込まない。
(function () {
  var C = window.TRACKING || {};

  function load(src) {
    var s = document.createElement("script");
    s.async = true;
    s.src = src;
    document.head.appendChild(s);
  }

  // Google アナリティクス 4 / Google 広告
  if (C.ga4 || C.googleAds) {
    load("https://www.googletagmanager.com/gtag/js?id=" + (C.ga4 || C.googleAds));
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    if (C.ga4) window.gtag("config", C.ga4);
    if (C.googleAds) window.gtag("config", C.googleAds);
  }

  // Meta ピクセル
  if (C.metaPixel) {
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = [];
      t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    window.fbq("init", C.metaPixel);
    window.fbq("track", "PageView");
  }

  // TikTok ピクセル
  if (C.tiktokPixel) {
    !function (w, d, t) {
      w.TiktokAnalyticsObject = t; var ttq = w[t] = w[t] || [];
      ttq.methods = ["page", "track", "identify", "instances", "debug", "on", "off", "once", "ready", "alias", "group", "enableCookie", "disableCookie"];
      ttq.setAndDefer = function (t, e) { t[e] = function () { t.push([e].concat(Array.prototype.slice.call(arguments, 0))); }; };
      for (var i = 0; i < ttq.methods.length; i++) ttq.setAndDefer(ttq, ttq.methods[i]);
      ttq.load = function (e, n) {
        var r = "https://analytics.tiktok.com/i18n/pixel/events.js";
        ttq._i = ttq._i || {}; ttq._i[e] = []; ttq._i[e]._u = r; ttq._t = ttq._t || {}; ttq._t[e] = +new Date; ttq._o = ttq._o || {}; ttq._o[e] = n || {};
        var s = d.createElement("script"); s.type = "text/javascript"; s.async = !0; s.src = r + "?sdkid=" + e + "&lib=" + t;
        var f = d.getElementsByTagName("script")[0]; f.parentNode.insertBefore(s, f);
      };
      ttq.load(C.tiktokPixel); ttq.page();
    }(window, document, "ttq");
  }

  // 先行登録の完了を各サービスに送る（フォーム送信の完了時にLPから呼ばれる）
  window.trackLead = function (service) {
    try {
      if (window.gtag && C.ga4) window.gtag("event", "generate_lead", { service: service });
      if (window.gtag && C.googleAds && C.googleAdsLabel) window.gtag("event", "conversion", { send_to: C.googleAds + "/" + C.googleAdsLabel });
      if (window.fbq) window.fbq("track", "Lead", { content_name: service });
      if (window.ttq) window.ttq.track("SubmitForm", { content_name: service });
    } catch (e) { /* 計測の失敗で登録の流れを止めない */ }
  };
})();
