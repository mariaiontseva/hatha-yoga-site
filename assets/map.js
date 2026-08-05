/* Fieldwork map (Gallery) — Leaflet + MarkerCluster, both self-hosted.

   One marker per site, not per photograph: clicking never spiderfies. A click
   on a site — or on a cluster of sites — opens a photograph strip below the
   map; the strip walks between the sites of a cluster and opens a lightbox.
   Hovering a marker shows a preview card. The whole widget can go fullscreen.

   Data comes from a <script type="application/json" id="map-data"> block that
   the build writes. A site whose photographs carry their own coordinates is
   split into several markers automatically (see build/places.py). */
(function () {
  'use strict';

  var host = document.getElementById('fieldmap');
  var dataEl = document.getElementById('map-data');
  if (!host || !dataEl) return;

  var places = JSON.parse(dataEl.textContent).filter(function (p) { return p.count; });
  if (!places.length) return;
  var root = host.dataset.root || '../../';
  var MOBILE = window.matchMedia('(max-width: 700px)');

  var TILES = 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png';
  var ATTR = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' +
             ' contributors, &copy; <a href="https://carto.com/attributions">CARTO</a>';

  var map, cluster, strip, lightbox;
  var state = { list: [], pos: 0, mode: 'single', lightbox: null };

  if (document.readyState === 'complete') start();
  else window.addEventListener('load', start);

  // ---------------------------------------------------------------- helpers
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  function img(file) { return root + 'hyp/assets/img/' + encodeURI(file); }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                'August', 'September', 'October', 'November', 'December'];
  function longDate(iso) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || '');
    return m ? Number(m[3]) + ' ' + MONTHS[Number(m[2]) - 1] + ' ' + m[1] : '';
  }
  /** "6–8 March 2016", "11–14 March 2016", "March 2016" or "" */
  function dateRange(dates) {
    if (!dates || !dates.length) return '';
    if (dates.length === 1) return longDate(dates[0]);
    var a = /^(\d{4})-(\d{2})-(\d{2})$/.exec(dates[0]);
    var b = /^(\d{4})-(\d{2})-(\d{2})$/.exec(dates[dates.length - 1]);
    if (!a || !b) return longDate(dates[0]);
    if (a[1] === b[1] && a[2] === b[2]) {
      return Number(a[3]) + '–' + Number(b[3]) + ' ' +
             MONTHS[Number(a[2]) - 1] + ' ' + a[1];
    }
    return longDate(dates[0]) + ' – ' + longDate(dates[dates.length - 1]);
  }
  function plural(n, one, many) { return n + ' ' + (n === 1 ? one : many); }

  // ------------------------------------------------------------------- map
  function start() {
    var canvas = el('div', 'fieldmap-canvas');
    host.appendChild(canvas);

    map = L.map(canvas, {
      scrollWheelZoom: false, attributionControl: true, zoomControl: true
    });
    L.tileLayer(TILES, {
      attribution: ATTR, maxZoom: 20, subdomains: 'abcd', tileSize: 256
    }).addTo(map);

    cluster = L.markerClusterGroup({
      showCoverageOnHover: false,
      spiderfyOnMaxZoom: false,      // no spider — the strip replaces it
      zoomToBoundsOnClick: false,    // a cluster opens the strip instead
      maxClusterRadius: 54,
      iconCreateFunction: clusterIcon
    });
    cluster.on('clusterclick', function (e) {
      var sites = e.layer.getAllChildMarkers()
        .map(function (m) { return m.__place; })
        .sort(function (a, b) { return b.count - a.count; });
      openStrip(sites, 0, 'cluster');
    });
    cluster.on('clustermouseover', function (e) {
      showTip(e.layer.getLatLng(), tipCluster(
        e.layer.getAllChildMarkers().map(function (m) { return m.__place; })));
    });
    cluster.on('clustermouseout', hideTip);

    var bounds = [];
    places.forEach(function (p) {
      var m = L.marker([p.lat, p.lon], { icon: siteIcon(p), title: p.name });
      m.__place = p;
      m.on('click', function () { openStrip([p], 0, 'single'); });
      m.on('mouseover', function () { showTip(m.getLatLng(), tipSite(p)); });
      m.on('mouseout', hideTip);
      cluster.addLayer(m);
      bounds.push([p.lat, p.lon]);
    });
    map.addLayer(cluster);
    map.invalidateSize();
    map.fitBounds(bounds, { padding: [46, 46] });

    map.on('click', closeStrip);
    map.on('focus', function () { map.scrollWheelZoom.enable(); });
    map.on('blur', function () { map.scrollWheelZoom.disable(); });

    host.appendChild(fullscreenButton());
    buildStrip();
    document.addEventListener('keydown', onKey);
  }

  // ---------------------------------------------------------------- markers
  function siteIcon(p) {
    if (p.count > 1) {
      return L.divIcon({
        className: 'fm-site', iconSize: L.point(30, 30),
        html: '<span>' + p.count + '</span>'
      });
    }
    return L.divIcon({ className: 'fm-dot', iconSize: L.point(16, 16), html: '<span></span>' });
  }

  function clusterIcon(c) {
    var photos = c.getAllChildMarkers().reduce(function (n, m) {
      return n + m.__place.count;
    }, 0);
    var big = photos >= 15;
    return L.divIcon({
      className: 'fm-cluster' + (big ? ' is-big' : ''),
      iconSize: L.point(big ? 48 : 40, big ? 48 : 40),
      html: '<span>' + photos + '</span>'
    });
  }

  // ------------------------------------------------------------ hover cards
  var tip = null, tipTimer = null;
  function showTip(latlng, html) {
    if (MOBILE.matches) return;               // touch taps straight through
    clearTimeout(tipTimer);
    tipTimer = setTimeout(function () {
      hideTip();
      tip = L.popup({
        className: 'fm-tip', closeButton: false, autoPan: true,
        autoPanPadding: L.point(12, 12), offset: L.point(0, -16),
        maxWidth: 336, minWidth: 336
      }).setLatLng(latlng).setContent(html).openOn(map);
    }, 90);
  }
  function hideTip() {
    clearTimeout(tipTimer);
    if (tip) { map.closePopup(tip); tip = null; }
  }

  /** Grid of up to 6 thumbnails; the 6th carries a "+N" veil when there
      are more. Four or fewer photographs use a roomier 2×2. */
  function tipGrid(photos, total) {
    var max = photos.length <= 4 ? 4 : 6;
    var shown = photos.slice(0, max);
    var extra = total - shown.length;
    var cells = shown.map(function (ph, i) {
      var veil = (extra > 0 && i === shown.length - 1)
        ? '<span class="fm-tip-more">+' + extra + '</span>' : '';
      return '<span class="fm-tip-cell"><img src="' + img(ph.file) +
        '" alt="" loading="lazy">' + veil + '</span>';
    }).join('');
    return '<span class="fm-tip-grid' + (max === 4 ? ' is-quad' : '') + '">' +
      cells + '</span>';
  }

  function tipBody(name, lines, allLabel) {
    return '<span class="fm-tip-body">' +
      '<span class="fm-tip-name">' + esc(name) + '</span>' +
      lines.filter(Boolean).map(function (l, i) {
        return '<span class="fm-tip-line' + (i ? ' is-dim' : '') + '">' +
          esc(l) + '</span>';
      }).join('') +
      '<span class="fm-tip-all">' + esc(allLabel) + '<span>&rarr;</span></span>' +
      '</span>';
  }

  function tipSite(p) {
    return tipGrid(p.photos, p.count) +
      tipBody(p.name, [p.region, dateRange(p.dates)],
              'All ' + plural(p.count, 'photograph', 'photographs'));
  }

  function tipCluster(sites) {
    var photos = sites.reduce(function (n, s) { return n + s.count; }, 0);
    // one thumbnail per place, so the grid shows what is actually grouped
    var lead = sites.map(function (s) { return s.photos[0]; });
    return tipGrid(lead, photos) +
      tipBody(plural(sites.length, 'place', 'places'),
              [sites.map(function (s) { return s.name; }).join(' · '),
               plural(photos, 'photograph', 'photographs')],
              'Browse these places');
  }

  // ----------------------------------------------------------------- strip
  function buildStrip() {
    strip = el('div', 'fm-strip');
    strip.innerHTML =
      '<button type="button" class="fm-strip-close" aria-label="Close (Esc)">&#10005;</button>' +
      '<div class="fm-strip-info">' +
      '  <span class="fm-strip-pos"></span>' +
      '  <h3 class="fm-strip-name"></h3>' +
      '  <span class="fm-strip-meta"></span>' +
      '</div>' +
      '<div class="fm-strip-reel">' +
      '  <span class="fm-strip-count"></span>' +
      '  <button type="button" class="fm-reel-nav is-prev" aria-label="Scroll left">&#8249;</button>' +
      '  <div class="fm-reel"></div>' +
      '  <button type="button" class="fm-reel-nav is-next" aria-label="Scroll right">&#8250;</button>' +
      '</div>' +
      // a child of the strip, not of the info block: on desktop it sits in
      // the info block's bottom corner, on mobile it becomes the full-width
      // button at the foot of the sheet
      '<a class="fm-strip-all" href="#"><span class="fm-all-short"></span>' +
      '<span class="fm-all-long"></span></a>';
    host.appendChild(strip);

    strip.querySelector('.fm-strip-close').addEventListener('click', closeStrip);
    var reel = strip.querySelector('.fm-reel');
    reel.addEventListener('scroll', refreshCounter, { passive: true });
    reel.addEventListener('wheel', function (e) {       // vertical wheel scrolls it
      if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
        e.preventDefault(); reel.scrollLeft += e.deltaY;
      }
    }, { passive: false });
    strip.querySelector('.is-prev').addEventListener('click', function () {
      reel.scrollBy({ left: -450, behavior: 'smooth' });
    });
    strip.querySelector('.is-next').addEventListener('click', function () {
      reel.scrollBy({ left: 450, behavior: 'smooth' });
    });
  }

  function openStrip(list, pos, mode) {
    hideTip();
    state.list = list; state.pos = pos; state.mode = mode;
    var p = list[pos];
    if (mode === 'single') map.panTo([p.lat, p.lon], { animate: true });
    host.classList.add('has-strip');
    renderStrip(false);
    setTimeout(function () {
      map.invalidateSize();
      map.panBy([0, MOBILE.matches ? 0 : 90], { animate: true });
    }, 60);
  }

  function closeStrip() {
    if (state.lightbox !== null) return;      // lightbox closes first
    host.classList.remove('has-strip');
    setTimeout(function () { map.invalidateSize(); }, 400);
  }

  function goPlace(delta) {
    var next = state.pos + delta;
    if (next < 0 || next >= state.list.length) return;
    state.pos = next;
    renderStrip(true);
  }

  function renderStrip(animate) {
    var p = state.list[state.pos];
    var reel = strip.querySelector('.fm-reel');

    strip.querySelector('.fm-strip-name').textContent = p.name;
    strip.querySelector('.fm-strip-pos').textContent =
      state.mode === 'cluster' ? (state.pos + 1) + ' / ' + state.list.length : '';
    strip.querySelector('.fm-strip-meta').innerHTML =
      esc(p.region) + (dateRange(p.dates) ? '<br>' + esc(dateRange(p.dates)) : '');
    var all = strip.querySelector('.fm-strip-all');
    all.href = root + 'hyp/' + p.slug + '/';
    all.querySelector('.fm-all-short').textContent = 'All ' + p.count;
    all.querySelector('.fm-all-long').textContent =
      'All ' + plural(p.count, 'photograph', 'photographs');

    function fill() {
      reel.innerHTML = '';
      if (state.mode === 'cluster' && state.pos > 0) {
        reel.appendChild(neighbour('back', state.list[state.pos - 1]));
      }
      p.photos.forEach(function (ph, i) {
        var b = el('button', 'fm-shot');
        b.type = 'button';
        b.innerHTML = '<img src="' + img(ph.file) + '" alt="' + esc(ph.alt || '') + '" loading="lazy">' +
          '<span class="fm-shot-label">View ' + (i + 1) + ' / ' + p.count + '</span>';
        b.addEventListener('click', function () { openLightbox(i); });
        reel.appendChild(b);
      });
      if (state.mode === 'cluster' && state.pos < state.list.length - 1) {
        reel.appendChild(neighbour('next', state.list[state.pos + 1]));
      }
      reel.scrollLeft = 0;
      // once more after layout: the strip is still sliding in on the first
      // pass, so widths are not final yet and the count would be wrong
      requestAnimationFrame(function () {
        reel.scrollLeft = 0;
        refreshCounter();
      });
    }

    if (animate) {
      reel.classList.add('is-swapping');
      setTimeout(function () { fill(); reel.classList.remove('is-swapping'); }, 200);
    } else {
      fill();
    }
  }

  function neighbour(dir, p) {
    var b = el('button', 'fm-neighbour is-' + dir);
    b.type = 'button';
    b.innerHTML = dir === 'next'
      ? '<span class="fm-neighbour-kicker">Next place</span>' +
        '<span class="fm-neighbour-name">' + esc(p.name) + '</span>' +
        '<span class="fm-neighbour-meta">' + plural(p.count, 'photo', 'photos') + ' &rarr;</span>'
      : '<span class="fm-neighbour-kicker">&larr; Back</span>' +
        '<span class="fm-neighbour-name">' + esc(p.name) + '</span>';
    b.addEventListener('click', function () { goPlace(dir === 'next' ? 1 : -1); });
    return b;
  }

  function refreshCounter() {
    var reel = strip.querySelector('.fm-reel');
    var p = state.list[state.pos];
    if (!p) return;
    var shots = reel.querySelectorAll('.fm-shot');
    if (!shots.length) return;
    var w = shots[0].getBoundingClientRect().width + 2;
    var first = Math.max(1, Math.min(p.count, Math.round(reel.scrollLeft / w) + 1));
    var last = Math.max(first, Math.min(p.count, first + Math.floor(reel.clientWidth / w) - 1));
    strip.querySelector('.fm-strip-count').textContent =
      first + '–' + last + ' of ' + p.count;
  }

  // -------------------------------------------------------------- lightbox
  function openLightbox(i) {
    if (!lightbox) buildLightbox();
    state.lightbox = i;
    renderLightbox();
    lightbox.classList.add('is-open');
    lightbox.querySelector('.fm-lb-close').focus();
  }
  function closeLightbox() {
    state.lightbox = null;
    lightbox.classList.remove('is-open');
    lightbox.querySelector('.fm-lb-img').removeAttribute('src');
  }
  function moveLightbox(d) {
    var p = state.list[state.pos];
    state.lightbox = (state.lightbox + d + p.count) % p.count;
    renderLightbox();
  }
  function buildLightbox() {
    lightbox = el('div', 'fm-lb');
    lightbox.setAttribute('role', 'dialog');
    lightbox.setAttribute('aria-modal', 'true');
    lightbox.innerHTML =
      '<div class="fm-lb-head"><span class="fm-lb-title"></span>' +
      '<button type="button" class="fm-lb-close" aria-label="Close (Esc)">&#10005;</button></div>' +
      '<button type="button" class="fm-lb-nav is-prev" aria-label="Previous">&#8249;</button>' +
      '<img class="fm-lb-img" alt="">' +
      '<button type="button" class="fm-lb-nav is-next" aria-label="Next">&#8250;</button>' +
      '<span class="fm-lb-hint">&larr;/&rarr; to browse &middot; Esc to close</span>';
    host.appendChild(lightbox);
    lightbox.querySelector('.fm-lb-close').addEventListener('click', closeLightbox);
    lightbox.querySelector('.is-prev').addEventListener('click', function () { moveLightbox(-1); });
    lightbox.querySelector('.is-next').addEventListener('click', function () { moveLightbox(1); });
    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) closeLightbox();
    });
  }
  function renderLightbox() {
    var p = state.list[state.pos], ph = p.photos[state.lightbox];
    lightbox.querySelector('.fm-lb-title').textContent =
      (state.lightbox + 1) + ' / ' + p.count + ' — ' + p.name;
    var im = lightbox.querySelector('.fm-lb-img');
    im.src = img(ph.file);
    im.alt = ph.alt || p.name;
    var multi = p.count > 1;
    lightbox.querySelector('.is-prev').hidden = !multi;
    lightbox.querySelector('.is-next').hidden = !multi;
  }

  // ------------------------------------------------------------ fullscreen
  function fullscreenButton() {
    var b = el('button', 'fm-fs', '&#9974;');
    b.type = 'button';
    b.setAttribute('aria-label', 'Toggle fullscreen');
    b.addEventListener('click', function () {
      if (document.fullscreenElement) document.exitFullscreen();
      else if (host.requestFullscreen) host.requestFullscreen();
    });
    document.addEventListener('fullscreenchange', function () {
      host.classList.toggle('is-fs', document.fullscreenElement === host);
      setTimeout(function () { map.invalidateSize(); }, 120);
    });
    return b;
  }

  // -------------------------------------------------------------- keyboard
  function onKey(e) {
    if (state.lightbox !== null) {
      if (e.key === 'Escape') { e.preventDefault(); closeLightbox(); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); moveLightbox(1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); moveLightbox(-1); }
      return;
    }
    if (!host.classList.contains('has-strip')) return;
    if (e.key === 'Escape') {
      if (document.fullscreenElement) return;   // Esc leaves fullscreen first
      e.preventDefault(); closeStrip();
    } else if (state.mode === 'cluster' && e.key === 'ArrowRight') {
      e.preventDefault(); goPlace(1);
    } else if (state.mode === 'cluster' && e.key === 'ArrowLeft') {
      e.preventDefault(); goPlace(-1);
    }
  }
})();
