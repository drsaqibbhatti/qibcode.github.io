/* QibCode — main.js: theme, mobile navigation and footer year. */
(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.add('js');

  var THEME_KEY = 'qib-theme';
  var darkQuery = window.matchMedia('(prefers-color-scheme: dark)');
  var toggles = document.querySelectorAll('[data-theme-toggle]');

  function currentTheme() {
    return root.getAttribute('data-theme') || (darkQuery.matches ? 'dark' : 'light');
  }

  function labelToggles() {
    var next = currentTheme() === 'dark' ? 'light' : 'dark';
    toggles.forEach(function (btn) {
      btn.setAttribute('aria-label', 'Switch to ' + next + ' theme');
      btn.title = 'Switch to ' + next + ' theme';
    });
  }

  toggles.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var next = currentTheme() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
      labelToggles();
    });
  });
  labelToggles();

  var nav = document.querySelector('[data-nav]');
  var burger = document.querySelector('[data-nav-toggle]');
  var menu = document.querySelector('.nav__menu');

  if (nav) {
    var onScroll = function () { nav.classList.toggle('is-scrolled', window.scrollY > 4); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    menu.addEventListener('click', function (event) {
      if (event.target.closest('a')) {
        menu.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
        burger.setAttribute('aria-label', 'Open menu');
      }
    });
  }

  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
