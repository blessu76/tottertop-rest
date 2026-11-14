(function(){
  var b=document.querySelector('.theme');if(!b)return;
  var root=document.documentElement;
  function dark(){var t=root.getAttribute('data-theme');return t?t==='dark':window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches}
  function label(){b.setAttribute('aria-label',dark()?b.dataset.light:b.dataset.dark)}
  b.addEventListener('click',function(){var n=dark()?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('site-theme',n)}catch(e){}label()});
  label();
})();
