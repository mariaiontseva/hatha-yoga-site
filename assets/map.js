/* Fieldwork map (Gallery) — Leaflet + MarkerCluster, both self-hosted.

   Click-to-load: nothing is fetched from the tile server until the visitor
   presses "Show map", so no third-party request leaves this page on its own.
   Data comes from a <script type="application/json" id="map-data"> block that
   the build writes; each photograph carries its own point, so real clusters
   appear as soon as photographs have their own coordinates — until then they
   sit on their site's point and cluster into one pin per site. */
(function () {
  'use strict';

  var host = document.getElementById('fieldmap');
  if (!host) return;
  var dataEl = document.getElementById('map-data');
  if (!dataEl) return;
  var places = JSON.parse(dataEl.textContent);
  var root = host.dataset.root || '../../';

  var TILES = 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png';
  var ATTR = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' +
             ' contributors, &copy; <a href="https://carto.com/attributions">CARTO</a>';

  host.querySelector('.fieldmap-load').addEventListener('click', start);

  function start() {
    host.classList.add('is-live');
    host.querySelector('.fieldmap-cover').remove();
    var el = document.createElement('div');
    el.className = 'fieldmap-canvas';
    host.appendChild(el);

    var map = L.map(el, { scrollWheelZoom: false, attributionControl: true });
    L.tileLayer(TILES, { attribution: ATTR, maxZoom: 19, subdomains: 'abcd' }).addTo(map);

    var cluster = L.markerClusterGroup({
      showCoverageOnHover: false,
      maxClusterRadius: 46,
      iconCreateFunction: function (c) {
        var n = c.getChildCount();
        return L.divIcon({
          html: '<span>' + n + '</span>',
          className: 'fm-cluster',
          iconSize: L.point(38, 38)
        });
      }
    });

    var bounds = [];
    places.forEach(function (p) {
      if (!p.count) return;
      p.photos.forEach(function (ph, i) {
        var m = L.marker([ph.lat, ph.lon], {
          icon: L.divIcon({
            className: 'fm-pin',
            html: '<span></span>',
            iconSize: L.point(16, 16)
          }),
          title: p.name
        });
        m.bindPopup(popup(p, ph), { minWidth: 210, closeButton: true });
        cluster.addLayer(m);
        bounds.push([ph.lat, ph.lon]);
      });
    });
    map.addLayer(cluster);
    map.fitBounds(bounds, { padding: [40, 40] });

    // scroll-zoom only once the map has focus, so the page still scrolls
    map.on('focus', function () { map.scrollWheelZoom.enable(); });
    map.on('blur', function () { map.scrollWheelZoom.disable(); });
  }

  function popup(p, ph) {
    var img = ph.file
      ? '<img src="' + root + 'hyp/assets/img/' + encodeURI(ph.file) + '" alt="" loading="lazy">'
      : '';
    var when = ph.date ? formatDate(ph.date) : (p.dates.length ? formatDate(p.dates[0]) : '');
    return '<div class="fm-pop">' + img +
      '<strong>' + p.name + '</strong>' +
      '<span class="fm-pop-region">' + p.region + '</span>' +
      (when ? '<span class="fm-pop-date">' + when + '</span>' : '') +
      '<a href="' + root + 'hyp/' + p.slug + '/">All ' + p.count +
      ' photographs &rarr;</a></div>';
  }

  function formatDate(iso) {
    var MONTHS = ['January','February','March','April','May','June','July',
                  'August','September','October','November','December'];
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso);
    if (!m) return iso;
    return Number(m[3]) + ' ' + MONTHS[Number(m[2]) - 1] + ' ' + m[1];
  }
})();
