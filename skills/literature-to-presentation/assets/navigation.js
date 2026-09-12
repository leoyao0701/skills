// SPDX-License-Identifier: MIT — Copyright (c) 2026 leoyao0701
(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const nav = document.querySelector('nav');
  let at = 0, all = false;
  function show(n, update = true) {
    at = Math.max(0, Math.min(n, slides.length - 1));
    slides.forEach((s, i) => { s.hidden = !all && i !== at; });
    nav.querySelector('[data-role="position"]').textContent = `${at + 1} / ${slides.length}`;
    if (update) history.replaceState(null, '', '#' + slides[at].id);
  }
  function fromHash() { const n = slides.findIndex(s => '#' + s.id === location.hash); show(Math.max(0, n), false); }
  nav.querySelector('[data-action="prev"]').onclick = () => show(at - 1);
  nav.querySelector('[data-action="next"]').onclick = () => show(at + 1);
  nav.querySelector('[data-action="show-all"]').onclick = e => { all = !all; e.target.textContent = all ? '逐页演示' : '连续阅读'; show(at); };
  nav.querySelector('[data-action="fullscreen"]').onclick = async () => { try { if (document.fullscreenElement) await document.exitFullscreen(); else await document.documentElement.requestFullscreen(); } catch (_) {} };
  window.addEventListener('keydown', e => { if (['INPUT', 'TEXTAREA', 'SELECT', 'BUTTON'].includes(e.target.tagName) || e.target.isContentEditable) return; if (['ArrowRight', 'PageDown', 'ArrowLeft', 'PageUp'].includes(e.key)) { e.preventDefault(); show(at + (['ArrowRight', 'PageDown'].includes(e.key) ? 1 : -1)); } });
  window.addEventListener('hashchange', fromHash);
  fromHash();
})();
