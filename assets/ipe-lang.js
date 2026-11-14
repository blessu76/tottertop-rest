/* ipe-lang.js · ipe_web_kit.langswitch — 생성 파일(python3 -m ipe_web_kit.langswitch js). 손으로 고치지 않는다. */
(function (root) {
  'use strict';
  var SUPPORTED = ["en", "ko", "ja", "zh-Hant", "es", "pt-BR", "fr", "de", "id", "th", "vi", "tr"];
  var DEFAULT = "en";
  var ALIASES = {"in": "id"};
  var ZH_HANT_REGIONS = ["hk", "mo", "tw"];
  var KEY = "ipe_lang";
  var BOT = /bot|crawl|spider|slurp|bingpreview|facebookexternalhit|lighthouse|pagespeed|preview/i;
  function split(tag) { return String(tag == null ? '' : tag).trim().toLowerCase().split(/[-_]/).filter(Boolean); }
  function zhHant(rest) {
    var script = null, region = null, i, p;
    for (i = 0; i < rest.length; i++) { p = rest[i]; if (script === null && p.length === 4 && /^[a-z]+$/.test(p)) script = p; }
    for (i = 0; i < rest.length; i++) { p = rest[i]; if (region === null && p.length === 2 && /^[a-z]+$/.test(p)) region = p; }
    return script === 'hant' || (script === null && ZH_HANT_REGIONS.indexOf(region) >= 0);
  }
  function resolve(tag) {
    var parts = split(tag), code, rest, i;
    if (!parts.length) return DEFAULT;
    code = Object.prototype.hasOwnProperty.call(ALIASES, parts[0]) ? ALIASES[parts[0]] : parts[0];
    rest = parts.slice(1);
    if (code === 'zh') return zhHant(rest) ? 'zh-Hant' : DEFAULT;
    if (code === 'pt') return 'pt-BR';
    for (i = 0; i < SUPPORTED.length; i++) if (SUPPORTED[i].toLowerCase() === code) return SUPPORTED[i];
    return DEFAULT;
  }
  function pick(tags) {
    var i, got;
    for (i = 0; i < (tags || []).length; i++) {
      got = resolve(tags[i]);
      if (got !== DEFAULT || split(tags[i])[0] === 'en') return got;
    }
    return DEFAULT;
  }
  function stored() {
    try { var v = root.localStorage.getItem(KEY); return v ? resolve(v) : null; } catch (e) { return null; }
  }
  function run() {
    var tag = root.document && root.document.currentScript;
    if (!tag || tag.getAttribute('data-redirect') === null) return;
    var nav = root.navigator || {};
    if (BOT.test(nav.userAgent || '')) return;
    var sel = root.document.getElementById("ipe-lang-select");
    if (!sel) return;
    var want = stored() || pick(nav.languages && nav.languages.length ? nav.languages : [nav.language]);
    var cur = sel.options[sel.selectedIndex], i;
    if (cur && cur.lang === want) return;
    for (i = 0; i < sel.options.length; i++) {
      if (sel.options[i].lang === want && sel.options[i].value) { root.location.replace(sel.options[i].value); return; }
    }
  }
  root.IpeLang = { resolve: resolve, pick: pick, stored: stored, SUPPORTED: SUPPORTED };
  run();
})(typeof window !== 'undefined' ? window : this);
