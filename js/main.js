(function () {
  'use strict';

  var KEY = 'fc_lang';
  var header = document.querySelector('.site-header');
  var burger = document.querySelector('.burger');
  var nav = document.getElementById('nav');

  function store(l) { try { localStorage.setItem(KEY, l); } catch (e) {} }

  // Тінь шапки при прокрутці
  function onScroll() {
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 8);
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Мобільне меню
  if (burger && nav) {
    var icon = burger.querySelector('use');
    var setOpen = function (open) {
      nav.classList.toggle('is-open', open);
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', burger.getAttribute(open ? 'data-label-close' : 'data-label-open') || '');
      if (icon) icon.setAttribute('href', open ? '#i-close' : '#i-menu');
    };
    burger.addEventListener('click', function () { setOpen(!nav.classList.contains('is-open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('click', function (e) {
      if (!nav.contains(e.target) && !burger.contains(e.target)) setOpen(false);
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
  }

  // Перемикач мови запам'ятовує вибір
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-lang-switch]');
    if (a) store(a.getAttribute('data-lang-switch'));
  });

  // Плавна прокрутка до якоря (~1500 мс, з розгоном і гальмуванням)
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function smoothTo(y, ms) {
    var start = window.pageYOffset, dist = y - start, t0 = null;
    document.documentElement.style.scrollBehavior = 'auto';
    function step(ts) {
      if (t0 === null) t0 = ts;
      var p = Math.min((ts - t0) / ms, 1);
      window.scrollTo(0, start + dist * ease(p));
      if (p < 1) requestAnimationFrame(step);
      else document.documentElement.style.scrollBehavior = '';
    }
    requestAnimationFrame(step);
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.hero-scroll');
    if (!a || reduce) return;
    var target = document.querySelector(a.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    var offset = header ? header.offsetHeight : 0;
    var y = target.getBoundingClientRect().top + window.pageYOffset - offset;
    smoothTo(Math.max(0, y), 1500);
    if (history.replaceState) history.replaceState(null, '', a.getAttribute('href'));
  });
})();
