const CACHE = "ke-boda-v10";
const PRECACHE = [
  "./assets/flores-1.webp",
  "./assets/flores-2.webp",
  "./assets/flores-3.webp",
  "./assets/flores-4.webp",
  "./assets/flores-5.webp",
  "./assets/Karla y Froyland/novios.webp",
  "./assets/Karla y Froyland/kye-1.jpg",
  "./assets/Karla y Froyland/kye-2.jpg",
  "./manifest.json"
];

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) { return c.addAll(PRECACHE); })
  );
  self.skipWaiting();
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.filter(function (k) { return k !== CACHE; })
            .map(function (k) { return caches.delete(k); })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener("fetch", function (e) {
  if (e.request.method !== "GET") return;
  if (e.request.url.includes("supabase.co")) return;

  var isHTML = e.request.headers.get("accept") &&
               e.request.headers.get("accept").includes("text/html");

  if (isHTML) {
    /* HTML: network-first — siempre intenta la red para recibir cambios,
       usa caché solo si no hay conexión (modo offline). */
    e.respondWith(
      fetch(e.request).then(function (res) {
        if (res && res.status === 200) {
          var clone = res.clone();
          caches.open(CACHE).then(function (c) { c.put(e.request, clone); });
        }
        return res;
      }).catch(function () {
        return caches.match(e.request);
      })
    );
    return;
  }

  /* Assets (imágenes, manifest): cache-first — no cambian frecuentemente */
  e.respondWith(
    caches.match(e.request).then(function (cached) {
      return cached || fetch(e.request).then(function (res) {
        if (res && res.status === 200 && res.type === "basic") {
          var clone = res.clone();
          caches.open(CACHE).then(function (c) { c.put(e.request, clone); });
        }
        return res;
      });
    })
  );
});
