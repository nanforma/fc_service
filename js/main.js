(function () {
  'use strict';

  var KEY = 'fc_lang';
  var root = document.documentElement;
  var pageLang = root.lang === 'ru' ? 'ru' : 'uk';
  var header = document.querySelector('.site-header');
  var burger = document.querySelector('.burger');
  var nav = document.getElementById('nav');

  function store(l) { try { localStorage.setItem(KEY, l); } catch (e) {} }
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }

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

  // Пропозиція змінити мову (лише якщо вибір ще не збережено)
  var TXT = {
    ru: { msg: 'Сайт доступен на русском языке. Переключить?', go: 'Перейти на русский', stay: 'Остаться на украинском' },
    uk: { msg: 'Сайт доступний українською мовою. Перейти?', go: 'Перейти на українську', stay: 'Залишитись на російській' }
  };
  var alt = root.getAttribute('data-alt');
  if (!stored() && alt) {
    var langs = (navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || '']);
    var detected = null;
    for (var i = 0; i < langs.length; i++) {
      var c = String(langs[i]).toLowerCase().slice(0, 2);
      if (c === 'uk' || c === 'ru') { detected = c; break; }
    }
    if (detected && detected !== pageLang) {
      var t = TXT[detected];
      var box = document.createElement('div');
      box.className = 'lang-banner';
      box.setAttribute('role', 'dialog');
      box.setAttribute('lang', detected);
      box.innerHTML = '<p></p><div class="btn-row"><button type="button" class="btn btn--primary btn--sm" data-go></button><button type="button" class="btn btn--ghost btn--sm" data-stay></button></div>';
      box.querySelector('p').textContent = t.msg;
      box.querySelector('[data-go]').textContent = t.go;
      box.querySelector('[data-stay]').textContent = t.stay;
      box.querySelector('[data-go]').addEventListener('click', function () {
        store(detected);
        location.href = new URL(alt, location.href).href + location.search + location.hash;
      });
      box.querySelector('[data-stay]').addEventListener('click', function () {
        store(pageLang);
        box.remove();
      });
      document.body.appendChild(box);
    }
  }
})();
