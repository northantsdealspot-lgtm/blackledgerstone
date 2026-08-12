const CACHE='blackledgerstone-v2.2.0-live';
const CORE=['./','./index.html','./styles.css','./app.js','./manifest.webmanifest','./raven-192.png','./raven-512.png','./live-intelligence.html','./raven-match.html'];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(CORE)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key!==CACHE).map(key=>caches.delete(key)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{
 if(event.request.method!=='GET') return;
 const url=new URL(event.request.url);
 if(url.origin!==location.origin) return;
 event.respondWith(fetch(event.request).then(response=>{
   if(response && response.ok){const copy=response.clone();caches.open(CACHE).then(cache=>cache.put(event.request,copy));}
   return response;
 }).catch(()=>caches.match(event.request).then(hit=>hit||caches.match('./index.html'))));
});
