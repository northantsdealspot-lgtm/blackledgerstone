const CACHE='blackledgerstone-v4-raven-command';
const CORE=['./','./raven-scout.html','./raven.html','./index.html','./styles.css','./app.js','./manifest.webmanifest','./raven-192.png','./raven-512.png','./live-intelligence.html','./raven-match.html','./data/leads.json'];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(CORE)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key!==CACHE).map(key=>caches.delete(key)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{
 if(event.request.method!=='GET') return;
 const url=new URL(event.request.url);
 if(url.origin!==location.origin) return;
 if(url.pathname.endsWith('/data/leads.json')){
   event.respondWith(fetch(event.request,{cache:'no-store'}).then(response=>{
     if(response&&response.ok){const copy=response.clone();caches.open(CACHE).then(cache=>cache.put('./data/leads.json',copy));}
     return response;
   }).catch(()=>caches.match('./data/leads.json')));
   return;
 }
 event.respondWith(fetch(event.request).then(response=>{
   if(response&&response.ok){const copy=response.clone();caches.open(CACHE).then(cache=>cache.put(event.request,copy));}
   return response;
 }).catch(()=>caches.match(event.request).then(hit=>hit||caches.match('./raven-scout.html'))));
});
