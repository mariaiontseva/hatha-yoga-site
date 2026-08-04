/* Click-to-play YouTube cards (Films page) — no dependencies.
   A card is a plain link to youtube.com until clicked; on click the
   thumbnail is swapped for a youtube-nocookie embed, so no YouTube
   cookies are set on this site before the visitor chooses to play. */
(function () {
  'use strict';
  document.querySelectorAll('a.ytcard[data-yt]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      e.preventDefault();
      var box = a.querySelector('.ytcard-img');
      if (a.dataset.playing) return;
      a.dataset.playing = '1';
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' +
              a.dataset.yt + '?autoplay=1';
      f.title = a.querySelector('.ytcard-title').textContent;
      f.setAttribute('allow',
        'autoplay; encrypted-media; picture-in-picture; fullscreen');
      f.setAttribute('allowfullscreen', '');
      box.innerHTML = '';
      box.appendChild(f);
    });
  });
})();
