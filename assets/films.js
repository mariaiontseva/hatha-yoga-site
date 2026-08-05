/* Films page: open a video in a large lightbox instead of the small card.
   No dependencies. Progressive enhancement: without JS every card is still a
   plain link to youtube.com. Nothing is requested from YouTube until the
   visitor clicks, and the embed is youtube-nocookie, so no YouTube cookies
   are set on this site before then. Arrows step through the videos of the
   same section. Keyboard: Esc closes, ←/→ move, Tab is trapped inside. */
(function () {
  'use strict';

  var cards = Array.prototype.slice.call(
    document.querySelectorAll('a.ytcard[data-yt]'));
  if (!cards.length) return;

  // ---- grouping: one group per section grid ------------------------------
  var groups = [], indexOf = new Map();
  cards.forEach(function (a) {
    var grid = a.closest('.ytgrid');
    var g = groups.find(function (x) { return x._grid === grid; });
    if (!g) { g = []; g._grid = grid; groups.push(g); }
    indexOf.set(a, [groups.indexOf(g), g.length]);
    g.push(a);
  });

  // ---- overlay -----------------------------------------------------------
  var box = null, frame, capEl, cntEl, btnPrev, btnNext, btnClose, srcEl;
  var group = [], idx = 0, lastFocus = null;

  function build() {
    box = document.createElement('div');
    box.className = 'vlb';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Video player');
    box.innerHTML =
      '<button type="button" class="vlb-close" aria-label="Close (Esc)">&#215;</button>' +
      '<button type="button" class="vlb-prev" aria-label="Previous video">&#8249;</button>' +
      '<div class="vlb-stage">' +
      '  <div class="vlb-frame"></div>' +
      '  <div class="vlb-bar">' +
      '    <span class="vlb-cap"></span>' +
      '    <span class="vlb-meta">' +
      '      <span class="vlb-src"></span>' +
      '      <span class="vlb-count" aria-live="polite"></span>' +
      '    </span>' +
      '  </div>' +
      '</div>' +
      '<button type="button" class="vlb-next" aria-label="Next video">&#8250;</button>';
    document.body.appendChild(box);

    frame    = box.querySelector('.vlb-frame');
    capEl    = box.querySelector('.vlb-cap');
    srcEl    = box.querySelector('.vlb-src');
    cntEl    = box.querySelector('.vlb-count');
    btnPrev  = box.querySelector('.vlb-prev');
    btnNext  = box.querySelector('.vlb-next');
    btnClose = box.querySelector('.vlb-close');

    btnClose.addEventListener('click', close);
    btnPrev.addEventListener('click', function () { move(-1); });
    btnNext.addEventListener('click', function () { move(1); });
    box.addEventListener('click', function (e) {
      if (e.target === box || e.target.classList.contains('vlb-stage')) close();
    });
  }

  function show(i) {
    idx = (i + group.length) % group.length;
    var a = group[idx];
    var src = a.querySelector('.ytcard-src');
    frame.innerHTML = '';
    var f = document.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/' + a.dataset.yt +
            '?autoplay=1&rel=0';
    f.title = a.querySelector('.ytcard-title').textContent;
    f.setAttribute('allow',
      'autoplay; encrypted-media; picture-in-picture; fullscreen');
    f.setAttribute('allowfullscreen', '');
    frame.appendChild(f);

    capEl.textContent = a.querySelector('.ytcard-title').textContent;
    srcEl.textContent = src ? src.textContent : '';
    var multi = group.length > 1;
    cntEl.textContent = multi ? (idx + 1) + ' / ' + group.length : '';
    btnPrev.hidden = btnNext.hidden = !multi;
  }

  function move(d) { show(idx + d); }

  function open(a) {
    if (!box) build();
    var g = indexOf.get(a);
    group = groups[g[0]];
    lastFocus = a;
    box.style.display = 'flex';
    document.documentElement.style.overflow = 'hidden';
    show(g[1]);
    document.addEventListener('keydown', onKey, true);
    btnClose.focus();
  }

  function close() {
    box.style.display = 'none';
    frame.innerHTML = '';                 // stops playback
    document.documentElement.style.overflow = '';
    document.removeEventListener('keydown', onKey, true);
    if (lastFocus) lastFocus.focus();
  }

  function onKey(e) {
    if (e.key === 'Escape') { e.preventDefault(); close(); return; }
    if (e.key === 'ArrowRight') { e.preventDefault(); move(1); return; }
    if (e.key === 'ArrowLeft')  { e.preventDefault(); move(-1); return; }
    if (e.key === 'Tab') {
      var f = [btnClose, btnPrev, btnNext].filter(function (b) { return !b.hidden; });
      var i = f.indexOf(document.activeElement);
      e.preventDefault();
      var n = e.shiftKey ? (i <= 0 ? f.length - 1 : i - 1)
                         : (i === f.length - 1 ? 0 : i + 1);
      f[n].focus();
    }
  }

  cards.forEach(function (a) {
    a.addEventListener('click', function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      e.preventDefault();
      open(a);
    });
  });
})();
