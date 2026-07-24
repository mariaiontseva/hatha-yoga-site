/* Lightbox for photo galleries — self-contained, no dependencies.
   Progressive enhancement: without JS every link still opens the image file.
   Groups: links inside one .gallery browse together (arrows / swipe / keys);
   a standalone image link opens alone. Captions come from the thumbnail alt. */
(function () {
  'use strict';

  var IMG_RE = /\.(jpe?g|png|gif|webp)([?#].*)?$/i;

  var links = Array.prototype.filter.call(
    document.querySelectorAll('a[href]'),
    function (a) {
      return IMG_RE.test(a.getAttribute('href')) && a.querySelector('img');
    });
  if (!links.length) return;

  // ---- grouping -----------------------------------------------------------
  var groups = [];                       // array of arrays of anchors
  var groupOf = new Map();               // anchor -> [groupIndex, indexInGroup]
  links.forEach(function (a) {
    var container = a.closest('.gallery');
    var g;
    if (container) {
      g = groups.find(function (grp) { return grp._c === container; });
      if (!g) { g = []; g._c = container; groups.push(g); }
    } else {
      g = []; g._c = null; groups.push(g);
    }
    groupOf.set(a, [groups.indexOf(g), g.length]);
    g.push(a);
  });

  // ---- overlay ------------------------------------------------------------
  var overlay = null, figImg, capEl, cntEl, btnPrev, btnNext, btnClose;
  var group = [], idx = 0, lastFocus = null;

  function build() {
    overlay = document.createElement('div');
    overlay.className = 'lb';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Photograph viewer');
    overlay.innerHTML =
      '<button type="button" class="lb-close" aria-label="Close (Esc)">&#215;</button>' +
      '<button type="button" class="lb-prev" aria-label="Previous photograph">&#8249;</button>' +
      '<figure class="lb-fig">' +
      '  <img class="lb-img" alt="">' +
      '  <figcaption class="lb-bar"><span class="lb-cap"></span>' +
      '  <span class="lb-count" aria-live="polite"></span></figcaption>' +
      '</figure>' +
      '<button type="button" class="lb-next" aria-label="Next photograph">&#8250;</button>';
    document.body.appendChild(overlay);

    figImg   = overlay.querySelector('.lb-img');
    capEl    = overlay.querySelector('.lb-cap');
    cntEl    = overlay.querySelector('.lb-count');
    btnPrev  = overlay.querySelector('.lb-prev');
    btnNext  = overlay.querySelector('.lb-next');
    btnClose = overlay.querySelector('.lb-close');

    btnClose.addEventListener('click', close);
    btnPrev.addEventListener('click', function () { move(-1); });
    btnNext.addEventListener('click', function () { move(1); });
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) close();   // click on the backdrop
    });

    // touch swipe
    var x0 = null;
    overlay.addEventListener('pointerdown', function (e) { x0 = e.clientX; });
    overlay.addEventListener('pointerup', function (e) {
      if (x0 === null) return;
      var dx = e.clientX - x0; x0 = null;
      if (Math.abs(dx) > 40) move(dx < 0 ? 1 : -1);
    });
  }

  function captionOf(a) {
    var t = a.querySelector('img');
    return (t && t.getAttribute('alt')) || '';
  }

  function show(i) {
    idx = (i + group.length) % group.length;
    var a = group[idx];
    figImg.src = a.getAttribute('href');
    figImg.alt = captionOf(a);
    capEl.textContent = captionOf(a);
    var multi = group.length > 1;
    cntEl.textContent = multi ? (idx + 1) + ' / ' + group.length : '';
    btnPrev.hidden = btnNext.hidden = !multi;
    // preload neighbours
    if (multi) {
      [idx + 1, idx - 1].forEach(function (n) {
        var b = group[(n + group.length) % group.length];
        (new Image()).src = b.getAttribute('href');
      });
    }
  }

  function move(d) { show(idx + d); }

  function open(a) {
    if (!overlay) build();
    var gi = groupOf.get(a);
    group = groups[gi[0]];
    lastFocus = a;
    overlay.style.display = 'flex';
    document.documentElement.style.overflow = 'hidden';
    show(gi[1]);
    document.addEventListener('keydown', onKey, true);
    btnClose.focus();
  }

  function close() {
    overlay.style.display = 'none';
    figImg.src = '';
    document.documentElement.style.overflow = '';
    document.removeEventListener('keydown', onKey, true);
    if (lastFocus) lastFocus.focus();
  }

  function onKey(e) {
    if (e.key === 'Escape') { e.preventDefault(); close(); return; }
    if (e.key === 'ArrowRight') { e.preventDefault(); move(1); return; }
    if (e.key === 'ArrowLeft')  { e.preventDefault(); move(-1); return; }
    if (e.key === 'Tab') {                    // focus trap over visible buttons
      var f = [btnClose, btnPrev, btnNext].filter(function (b) { return !b.hidden; });
      var i = f.indexOf(document.activeElement);
      e.preventDefault();
      var n = e.shiftKey ? (i <= 0 ? f.length - 1 : i - 1)
                         : (i === f.length - 1 ? 0 : i + 1);
      f[n].focus();
    }
  }

  links.forEach(function (a) {
    a.addEventListener('click', function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      e.preventDefault();
      open(a);
    });
  });
})();
