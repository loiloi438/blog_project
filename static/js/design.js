// design.js - adds lazy-loading, like-button AJAX, and simple UI helpers
(function(){
  'use strict';

  function getCookie(name){
    let cookieValue = null;
    if (document.cookie && document.cookie !== ''){
      const cookies = document.cookie.split(';');
      for (let i=0;i<cookies.length;i++){
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length+1) === (name + '=')){
          cookieValue = decodeURIComponent(cookie.substring(name.length+1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function initLazy(){
    const imgs = document.querySelectorAll('img.lazy-img');
    if (!('IntersectionObserver' in window) || imgs.length===0){
      imgs.forEach(img=>{if(img.dataset.src) img.src = img.dataset.src; img.classList.add('loaded')});
      return;
    }
    const io = new IntersectionObserver((entries, obs)=>{
      entries.forEach(entry=>{
        if(entry.isIntersecting){
          const img = entry.target;
          if(img.dataset.src) img.src = img.dataset.src;
          img.addEventListener('load', ()=> img.classList.add('loaded'));
          obs.unobserve(img);
        }
      });
    },{rootMargin:'200px'});
    imgs.forEach(i=>io.observe(i));
  }

  function csrfFetch(url, opts){
    opts = opts || {};
    opts.headers = opts.headers || {};
    // Ensure cookies (session) are sent so Django sees authenticated user
    if (!opts.credentials) opts.credentials = 'same-origin';
    // Ensure CSRF and X-Requested-With for Django AJAX handling
    if (!opts.headers['X-CSRFToken']){
      opts.headers['X-CSRFToken'] = getCookie('csrftoken');
    }
    if (!opts.headers['X-Requested-With']){
      opts.headers['X-Requested-With'] = 'XMLHttpRequest';
    }
    return fetch(url, opts);
  }

  function initLikeButtons(){
    document.querySelectorAll('.like-btn').forEach(btn=>{
      btn.addEventListener('click', async function(e){
        const url = btn.dataset.url || btn.getAttribute('data-url');
        console.debug('[design] like click', {btn, url});
        console.debug('[design] csrftoken cookie=', getCookie('csrftoken'));
        if(!url) { btn.classList.add('pulse-once'); setTimeout(()=>btn.classList.remove('pulse-once'), 700); return; }
        try{
          btn.disabled = true;
          // visual feedback
          const oldContent = btn.innerHTML;
          btn.innerHTML = '...';
          const res = await csrfFetch(url, {method:'POST'});
          console.debug('[design] fetch status', res.status, url);
          if(res.status === 403){
            // Not authenticated: redirect to login page preserving next
            window.location = '/login/?next=' + encodeURIComponent(window.location.pathname);
            return;
          }
          if(!res.ok){
            const txt = await res.text().catch(()=>'<no body>');
            alert('Erreur like: ' + res.status + '\n' + txt);
            throw new Error('Network');
          }
          const data = await res.json();
          console.debug('[design] like response json', data);
          if(data.liked){
            btn.classList.add('liked');
            btn.title = 'Vous aimez';
            btn.innerHTML = '❤️';
          } else {
            btn.classList.remove('liked');
            btn.title = 'Aimer';
            btn.innerHTML = '🤍';
          }
          const counter = document.querySelector(btn.dataset.counter || btn.getAttribute('data-counter'));
          if(counter && typeof data.likes_count !== 'undefined') counter.textContent = data.likes_count;
          // small pulse
          btn.classList.add('pulse-once'); setTimeout(()=>btn.classList.remove('pulse-once'), 700);
        }catch(err){
          console.warn('[design] Like failed', err);
          // restore a visual state if something went wrong
          try{ btn.innerHTML = oldContent }catch(e){}
        }finally{ btn.disabled = false }
      })
    })
  }

  function revealOnLoad(){
    document.querySelectorAll('.fade-in').forEach(el=>el.classList.add('show'));
  }

  document.addEventListener('DOMContentLoaded', function(){
    initLazy();
    initLikeButtons();
    setTimeout(revealOnLoad, 120);
  });

})();
