/* Veritas Hospitality Advisors: cookie consent for Google Analytics (GA4).
   The Google tag is in every page's <head> in a consent-denied state (Google Consent Mode). Clicking "Accept" switches analytics_storage to granted.
   Declining, or not choosing, sets no analytics cookies.
   The choice is stored in this browser (localStorage key "veritas_consent") and can be changed from the Privacy Policy page. */
(function () {
  'use strict';
  var GA_ID = 'G-X7QRDJ87V3';
  var KEY = 'veritas_consent';
  if (window.clarity && !(function(){try{var v=JSON.parse(localStorage.getItem(KEY));return v&&v.choice==='granted';}catch(e){return false;}})()) window.clarity('consent', false); // Clarity runs cookieless until analytics are accepted
  var isLocal = /^(localhost|127\.0\.0\.1)$/.test(location.hostname);

  function read() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY));
      return v && (v.choice === 'granted' || v.choice === 'denied') ? v.choice : null;
    } catch (e) { return null; }
  }
  function write(choice) {
    try { localStorage.setItem(KEY, JSON.stringify({ choice: choice, date: new Date().toISOString() })); } catch (e) {}
  }

  function loadGA() {
    if (window.clarity) window.clarity('consent', true);
    if (window.__veritasGALoaded) return;
    window.__veritasGALoaded = true;
    if (isLocal) { window.__veritasGAWouldLoad = true; return; } // never send test traffic from a local preview
    window['ga-disable-' + GA_ID] = false;
    window.dataLayer = window.dataLayer || [];
    if (!window.gtag) { window.gtag = function () { window.dataLayer.push(arguments); }; }
    window.gtag('consent', 'update', { analytics_storage: 'granted' });
  }

  function clearGACookies() {
    if (window.clarity) window.clarity('consent', false);
    window['ga-disable-' + GA_ID] = true;
    window.__veritasGALoaded = false;
    if (window.gtag) { window.gtag('consent', 'update', { analytics_storage: 'denied' }); }
    var names = ['_ga', '_ga_' + GA_ID.replace('G-', ''), '_gid', '_gat', '_clck', '_clsk', 'CLID', 'ANONCHK', 'MR', 'MUID', 'SM'];
    var host = location.hostname.split('.');
    var domains = [location.hostname, '.' + location.hostname];
    if (host.length > 2) domains.push('.' + host.slice(-2).join('.'));
    names.forEach(function (n) {
      domains.forEach(function (d) {
        document.cookie = n + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=' + d;
      });
      document.cookie = n + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
    });
  }

  function css() {
    var st = document.createElement('style');
    st.id = 'veritas-consent-css';
    st.textContent =
      '#veritas-consent{position:fixed;left:0;right:0;bottom:0;z-index:9999;background:#0D1B2A;color:#F5F4EF;border-top:2px solid #A57426;' +
      'font-family:"Public Sans",sans-serif;font-size:.86rem;line-height:1.55;padding:18px 24px;box-shadow:0 -6px 24px rgba(0,0,0,.25)}' +
      '#veritas-consent .vc-inner{max-width:1100px;margin:0 auto;display:flex;gap:20px;align-items:center;justify-content:space-between;flex-wrap:wrap}' +
      '#veritas-consent p{margin:0;flex:1 1 420px;color:rgba(245,244,239,.88)}' +
      '#veritas-consent a{color:#F5F4EF;text-decoration:underline}' +
      '#veritas-consent .vc-btns{display:flex;gap:12px;flex-wrap:wrap}' +
      '#veritas-consent button{font-family:inherit;font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;padding:11px 22px;cursor:pointer;border-radius:0;min-width:120px;' +
      'border:1px solid #F5F4EF;background:transparent;color:#F5F4EF}' +
      '#veritas-consent button.vc-accept{background:#F5F4EF;color:#0D1B2A}' +
      '#veritas-consent button:hover,#veritas-consent button:focus-visible{outline:2px solid #A57426;outline-offset:2px}' +
      '@media print{#veritas-consent{display:none}}';
    document.head.appendChild(st);
  }

  function hide() {
    var b = document.getElementById('veritas-consent');
    if (b) b.parentNode.removeChild(b);
  }

  function choose(choice) {
    var previous = read();
    write(choice);
    if (choice === 'granted') loadGA();
    else if (previous === 'granted' || window.__veritasGALoaded) clearGACookies();
    hide();
  }

  function show() {
    if (document.getElementById('veritas-consent')) return;
    if (!document.getElementById('veritas-consent-css')) css();
    var d = document.createElement('div');
    d.id = 'veritas-consent';
    d.setAttribute('role', 'dialog');
    d.setAttribute('aria-label', 'Cookie choice');
    d.innerHTML =
      '<div class="vc-inner"><p>We use Google Analytics cookies to understand how this website is used. They are optional, and we do not use advertising cookies. ' +
      'You can change your choice at any time. <a href="/legal.html#cookies">Privacy Policy</a></p>' +
      '<div class="vc-btns"><button type="button" class="vc-decline">Decline</button><button type="button" class="vc-accept">Accept analytics</button></div></div>';
    document.body.appendChild(d);
    d.querySelector('.vc-accept').addEventListener('click', function () { choose('granted'); });
    d.querySelector('.vc-decline').addEventListener('click', function () { choose('denied'); });
  }

  function init() {
    var c = read();
    if (c === 'granted') loadGA();
    else if (c === null) show();
    var links = document.querySelectorAll('[data-cookie-settings]');
    for (var i = 0; i < links.length; i++) {
      links[i].addEventListener('click', function (e) { e.preventDefault(); show(); });
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
