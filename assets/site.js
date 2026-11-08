(function(){
  /* an explicit language choice wins over the browser language the root page follows (see langpick.js) */
  document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.lang a[hreflang],.foot-langs a[hreflang],.langs a[hreflang]');if(a){try{localStorage.setItem('site-lang',a.getAttribute('hreflang'))}catch(x){}}});
  var b=document.querySelector('.theme');if(!b)return;
  var root=document.documentElement;
  function dark(){var t=root.getAttribute('data-theme');return t?t==='dark':window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches}
  function label(){b.setAttribute('aria-label',dark()?b.dataset.light:b.dataset.dark)}
  b.addEventListener('click',function(){var n=dark()?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('site-theme',n)}catch(e){}label()});
  label();
  document.addEventListener('click',function(e){var d=document.querySelector('.lang[open]');if(d&&!d.contains(e.target))d.removeAttribute('open')});
})();
