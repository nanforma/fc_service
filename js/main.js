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
})();
