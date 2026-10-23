/* Veritas Hospitality Advisors: click-to-enlarge for images inside any element marked data-lightbox.
   Click or press Enter on an image to open it full size; Esc, the close button or a click outside closes it; arrow keys or the arrow buttons move between images.
   Images inside an element marked data-lightbox-group open together as a grid instead (all images of that group side by side). */
(function () {
  'use strict';
  var imgs = [];
  var current = -1;
  var opener = null;
  var box, bigImg, caption, closeBtn, prevBtn, nextBtn, grid;

  function injectCss() {
    if (document.getElementById('veritas-lightbox-css')) return;
    var st = document.createElement('style');
    st.id = 'veritas-lightbox-css';
    st.textContent =
      '[data-lightbox] img{cursor:zoom-in}' +
      '[data-lightbox] img:focus-visible{outline:2px solid #A57426;outline-offset:3px}' +
      '#veritas-lightbox{position:fixed;inset:0;z-index:10000;background:rgba(13,27,42,.94);display:none;align-items:center;justify-content:center;flex-direction:column;padding:56px 56px 24px;font-family:"Public Sans",sans-serif}' +
      '#veritas-lightbox.open{display:flex}' +
      '#veritas-lightbox .vl-img{max-width:92vw;max-height:80vh;object-fit:contain;background:#F5F4EF;box-shadow:0 8px 40px rgba(0,0,0,.45)}' +
      '#veritas-lightbox .vl-cap{margin:16px 0 0;color:rgba(245,244,239,.85);font-size:.82rem;line-height:1.5;text-align:center;max-width:80ch}' +
      '#veritas-lightbox button{position:absolute;background:transparent;border:1px solid rgba(245,244,239,.6);color:#F5F4EF;cursor:pointer;font-family:inherit;line-height:1;border-radius:0}' +
      '#veritas-lightbox button:hover,#veritas-lightbox button:focus-visible{background:#F5F4EF;color:#0D1B2A;outline:2px solid #A57426;outline-offset:2px}' +
      '#veritas-lightbox .vl-close{top:16px;right:16px;width:44px;height:44px;font-size:1.5rem}' +
      '#veritas-lightbox .vl-prev,#veritas-lightbox .vl-next{top:50%;width:44px;height:44px;font-size:1.5rem;transform:translateY(-50%)}' +
      '#veritas-lightbox .vl-prev{left:12px}#veritas-lightbox .vl-next{right:12px}' +
      '#veritas-lightbox .vl-grid{display:none;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;max-width:94vw;max-height:86vh;overflow:auto;align-items:start}' +
      '#veritas-lightbox.grid-mode .vl-grid{display:grid}' +
      '#veritas-lightbox.grid-mode .vl-img,#veritas-lightbox.grid-mode .vl-cap,#veritas-lightbox.grid-mode .vl-prev,#veritas-lightbox.grid-mode .vl-next{display:none}' +
      '#veritas-lightbox .vl-grid figure{margin:0}' +
      '#veritas-lightbox .vl-grid img{display:block;width:100%;max-height:72vh;object-fit:contain;background:#F5F4EF;box-shadow:0 8px 40px rgba(0,0,0,.45)}' +
      '#veritas-lightbox .vl-grid figcaption{margin-top:10px;color:rgba(245,244,239,.85);font-size:.8rem;line-height:1.5;text-align:center}' +
      '@media(max-width:640px){#veritas-lightbox .vl-grid{grid-template-columns:1fr}#veritas-lightbox{padding:60px 12px 16px}#veritas-lightbox .vl-prev{left:6px}#veritas-lightbox .vl-next{right:6px}}';
    document.head.appendChild(st);
  }

  function build() {
    box = document.createElement('div');
    box.id = 'veritas-lightbox';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Enlarged image');
    box.innerHTML =
      '<button type="button" class="vl-close" aria-label="Close enlarged image">&times;</button>' +
      '<button type="button" class="vl-prev" aria-label="Previous image">&#8249;</button>' +
      '<img class="vl-img" alt="">' +
      '<button type="button" class="vl-next" aria-label="Next image">&#8250;</button>' +
      '<p class="vl-cap"></p>' +
      '<div class="vl-grid"></div>';
    document.body.appendChild(box);
    bigImg = box.querySelector('.vl-img');
    caption = box.querySelector('.vl-cap');
    grid = box.querySelector('.vl-grid');
    closeBtn = box.querySelector('.vl-close');
    prevBtn = box.querySelector('.vl-prev');
    nextBtn = box.querySelector('.vl-next');
    closeBtn.addEventListener('click', close);
    prevBtn.addEventListener('click', function (e) { e.stopPropagation(); step(-1); });
    nextBtn.addEventListener('click', function (e) { e.stopPropagation(); step(1); });
    box.addEventListener('click', function (e) { if (e.target === box || e.target === caption) close(); });
    document.addEventListener('keydown', function (e) {
      if (!box.classList.contains('open')) return;
      var gridMode = box.classList.contains('grid-mode');
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowLeft' && !gridMode) step(-1);
      else if (e.key === 'ArrowRight' && !gridMode) step(1);
      else if (e.key === 'Tab') {
        var f = gridMode ? [closeBtn] : [closeBtn, prevBtn, nextBtn].filter(function (b) { return b.style.display !== 'none'; });
        var i = f.indexOf(document.activeElement);
        e.preventDefault();
        f[(i + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus();
      }
    });
  }

  function show(i) {
    current = (i + imgs.length) % imgs.length;
    var im = imgs[current];
    bigImg.src = im.currentSrc || im.src;
    bigImg.alt = im.alt;
    caption.textContent = im.alt;
    var many = imgs.length > 1;
    prevBtn.style.display = many ? '' : 'none';
    nextBtn.style.display = many ? '' : 'none';
  }

  function showGrid(group) {
    grid.innerHTML = '';
    group.querySelectorAll('img').forEach(function (im) {
      var fig = document.createElement('figure');
      var g = document.createElement('img');
      g.src = im.currentSrc || im.src;
      g.alt = im.alt;
      var cap = document.createElement('figcaption');
      cap.textContent = im.alt;
      fig.appendChild(g);
      fig.appendChild(cap);
      grid.appendChild(fig);
    });
    box.classList.add('grid-mode');
  }

  function open(i, from, group) {
    opener = from;
    if (group) { showGrid(group); } else { box.classList.remove('grid-mode'); show(i); }
    box.classList.add('open');
    document.documentElement.style.overflow = 'hidden';
    closeBtn.focus();
  }

  function close() {
    box.classList.remove('open');
    box.classList.remove('grid-mode');
    grid.innerHTML = '';
    document.documentElement.style.overflow = '';
    bigImg.removeAttribute('src');
    if (opener && opener.focus) opener.focus();
  }

  function step(d) { show(current + d); }

  function init() {
    var scopes = document.querySelectorAll('[data-lightbox]');
    if (!scopes.length) return;
    injectCss();
    build();
    scopes.forEach(function (s) {
      s.querySelectorAll('img').forEach(function (im) {
        var idx = imgs.push(im) - 1;
        im.setAttribute('tabindex', '0');
        im.setAttribute('role', 'button');
        im.setAttribute('aria-label', 'Enlarge image: ' + im.alt);
        var grp = im.closest('[data-lightbox-group]');
        im.addEventListener('click', function () { open(idx, im, grp); });
        im.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(idx, im, grp); } });
      });
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
