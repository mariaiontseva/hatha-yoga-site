/* Tabs (Films / Podcasts) — no dependencies.
   Without JS both panels are simply visible one after the other, so the page
   still reads fine. The URL hash keeps a chosen tab shareable. */
(function () {
  'use strict';
  var list = document.querySelector('.tabs');
  if (!list) return;
  var tabs = Array.prototype.slice.call(list.querySelectorAll('.tab'));

  function show(tab, push) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.classList.toggle('is-on', on);
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      var panel = document.getElementById(t.getAttribute('aria-controls'));
      panel.hidden = !on;
      panel.classList.toggle('is-on', on);
    });
    if (push) history.replaceState(null, '', '#' + tab.id.replace('tab-', ''));
  }

  tabs.forEach(function (t) {
    t.addEventListener('click', function () { show(t, true); });
    t.addEventListener('keydown', function (e) {
      var i = tabs.indexOf(t);
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        e.preventDefault();
        var next = tabs[(i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length];
        next.focus();
        show(next, true);
      }
    });
  });

  var wanted = document.getElementById('tab-' + location.hash.replace('#', ''));
  show(wanted && tabs.indexOf(wanted) > -1 ? wanted : tabs[0], false);
})();
