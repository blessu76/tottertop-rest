(function(){
  document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.langs a[hreflang]');if(a){try{localStorage.setItem('site-lang',a.getAttribute('hreflang'))}catch(x){}}});
  document.addEventListener('change',function(e){var s=e.target;if(!s.matches||!s.matches('select[data-lang-switch]'))return;try{localStorage.setItem('site-lang',s.options[s.selectedIndex].lang)}catch(x){}location.href=s.value});
  var b=document.querySelector('.theme');if(!b)return;
  var root=document.documentElement;
  function dark(){var t=root.getAttribute('data-theme');return t?t==='dark':window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches}
  function label(){b.setAttribute('aria-label',dark()?b.dataset.light:b.dataset.dark)}
  b.addEventListener('click',function(){var n=dark()?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('site-theme',n)}catch(e){}label()});
  label();
})();
