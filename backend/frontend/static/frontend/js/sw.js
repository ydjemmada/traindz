const CACHE_NAME = 'sntf-cache-v1';
const ASSETS_TO_CACHE = [
    '/',
    '/static/frontend/css/style.css',
    '/static/frontend/js/app.js',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
    'https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap'
];

// Install event: Cache static assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                return cache.addAll(ASSETS_TO_CACHE);
            })
    );
});

// Activate event: Clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Fetch event: Network first for API, Cache first for static
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // API requests: Network first, fall back to cache (if we implement API caching later)
    // For now, just network first for API to ensure fresh data
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(
            fetch(event.request)
                .catch(() => {
                    // Optional: Return cached API response if available
                    return caches.match(event.request);
                })
        );
        return;
    }

    // Static assets: Cache first
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                return response || fetch(event.request);
            })
    );
});
