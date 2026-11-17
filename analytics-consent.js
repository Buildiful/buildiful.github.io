/* Optional, opt-in GA4. Nothing is sent to Google before consent. */
(() => {
  'use strict';
  const tag = document.currentScript;
  const measurementId = tag?.dataset.measurementId || '';
  const toolName = tag?.dataset.toolName || 'Buildiful 365';
  const privacyUrl = tag?.dataset.privacyUrl || './privacy.html';
  // Shared across Buildiful projects, as in the released app consent modules.
  const KEY = 'buildiful.analytics.consent.v1';
  const localFile = location.protocol === 'file:';
  let accepted = false;
  let loaded = false;
  const slugs = new Set([...document.querySelectorAll('.tool-card[data-slug]')].map(el=>el.dataset.slug));
  function readChoice() {try {return JSON.parse(localStorage.getItem(KEY)||'null')?.choice||null;} catch {return null;}}
  function saveChoice(choice) {try {localStorage.setItem(KEY,JSON.stringify({choice,timestamp:new Date().toISOString()}));} catch {}}
  function loadGA() {
    if (!accepted || loaded || localFile || !/^G-[A-Z0-9]+$/.test(measurementId)) return;
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function(){window.dataLayer.push(arguments);};
    window.gtag('js',new Date());
    window.gtag('set',{allow_google_signals:false,allow_ad_personalization_signals:false});
    window.gtag('config',measurementId,{
      send_page_view:false,allow_google_signals:false,allow_ad_personalization_signals:false,
      page_location:location.origin+location.pathname,page_path:location.pathname,page_title:document.title
    });
    window.gtag('event','page_view',{page_location:location.origin+location.pathname,page_path:location.pathname,page_title:document.title,tool_name:toolName});
    const script=document.createElement('script');
    script.async=true;
    script.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(measurementId);
    document.head.append(script);
  }
  function close(){document.getElementById('buildiful-consent-banner')?.remove();}
  function choose(choice){
    const hadAnalytics=accepted && loaded;
    saveChoice(choice);accepted=choice==='accepted';close();
    if(accepted)loadGA();
    else if(hadAnalytics){
      try{window.gtag?.('consent','update',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});}catch{}
      location.reload();
    }
  }
  function openSettings(){
    if(localFile){window.alert('Analytics is disabled in local files.');return;}
    close();
    const dialog=document.createElement('aside');dialog.className='consent-banner';dialog.id='buildiful-consent-banner';
    dialog.setAttribute('role','dialog');dialog.setAttribute('aria-label','Optional analytics');
    const heading=document.createElement('strong');heading.textContent='Help us improve Buildiful 365?';
    const description=document.createElement('p');description.textContent='We would like to count visits and which tools people open. No search terms or tool content are collected. Everything works without analytics.';
    const actions=document.createElement('div');actions.className='consent-actions';
    const privacy=document.createElement('a');privacy.href=privacyUrl;privacy.textContent='Privacy';
    const no=document.createElement('button');no.type='button';no.textContent='No thanks';no.addEventListener('click',()=>choose('declined'));
    const yes=document.createElement('button');yes.type='button';yes.textContent='Allow';yes.addEventListener('click',()=>choose('accepted'));
    actions.append(privacy,no,yes);dialog.append(heading,description,actions);document.body.append(dialog);
  }
  function track(event,details={}){
    if(!accepted||!loaded||typeof window.gtag!=='function')return;
    if(!['tool_open','source_open'].includes(event)||!slugs.has(details.slug))return;
    window.gtag('event',event,{tool_name:toolName,tool_slug:details.slug});
  }
  window.buildifulAnalytics={openSettings,track,get accepted(){return accepted;}};
  if(localFile)return;
  const saved=readChoice();
  if(saved==='accepted'){accepted=true;loadGA();}
  else if(saved!=='declined')openSettings();
})();
