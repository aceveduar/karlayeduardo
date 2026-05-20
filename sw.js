const CACHE = "ke-boda-v6";
const PRECACHE = [
  "./index.html",
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
  /* Solo cachear GET, ignorar Supabase (siempre en vivo) */
  if (e.request.method !== "GET") return;
  if (e.request.url.includes("supabase.co")) return;

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
