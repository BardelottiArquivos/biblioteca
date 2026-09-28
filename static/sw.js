// static/sw.js
// =============================================
// SERVICE WORKER - PWA
// =============================================

const CACHE_NAME = 'biblioteca-saber-v1';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/css/acessibilidade.css',
    '/static/js/main.js',
    '/static/js/acessibilidade.js',
    '/static/manifest.json',
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(urlsToCache))
    );
    self.skipWaiting();
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return (
                response ||
                fetch(event.request)
                    .then((res) => {
                        // Só armazena requisições válidas
                        if (
                            !res ||
                            res.status !== 200 ||
                            res.type !== 'basic'
                        ) {
                            return res;
                        }
                        const resClone = res.clone();
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, resClone);
                        });
                        return res;
                    })
                    .catch(() => caches.match('/offline/'))
            );
        })
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((names) =>
            Promise.all(
                names.map((name) =>
                    name !== CACHE_NAME ? caches.delete(name) : null
                )
            )
        )
    );
    self.clients.claim();
});