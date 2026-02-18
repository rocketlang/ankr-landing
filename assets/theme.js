(function(){
  const root = document.documentElement;
  const saved = localStorage.getItem('ankr-theme') || 'night';
  root.setAttribute('data-theme', saved);
  document.querySelectorAll('.th-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.t === saved);
    btn.addEventListener('click', () => {
      const t = btn.dataset.t;
      root.setAttribute('data-theme', t);
      localStorage.setItem('ankr-theme', t);
      document.querySelectorAll('.th-btn').forEach(b => b.classList.toggle('active', b.dataset.t === t));
    });
  });
})();
