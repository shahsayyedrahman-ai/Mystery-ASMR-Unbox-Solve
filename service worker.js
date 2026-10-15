/* ==========================================================================
   Mystery ASMR: Unbox & Solve — Service Worker (V1.0 Release Candidate)
   Offline App Shell Caching & Lifecycle Management
   ========================================================================== */

const CACHE_NAME = 'mystery-asmr-v1.0.0-rc1';

const CORE_ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icons/icon-44.png',
  './icons/icon-71.png',
  './icons/icon-150.png',
  './icons/icon-192.png',
  './icons/icon-310.png',
  './icons/icon-512.png',
  './icons/icon-maskable-192.png',
  './icons/icon-maskable-512.png',
  './icons/icon.svg'
];

// Install: Pre-cache core shell resources and activate immediately
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(CORE_ASSETS).catch(err => {
        console.warn('[PWA SW] Pre-caching non-fatal warning:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

// Activate: Clean up previous cache generations and claim clients
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.map(k => {
          if (k.startsWith('mystery-asmr-') && k !== CACHE_NAME) {
            console.log('[PWA SW] Purging obsolete cache:', k);
            return caches.delete(k);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: Stale-While-Revalidate / Cache-First strategy for local shell
self.addEventListener('fetch', event => {
  const req = event.request;

  // Only handle GET requests and same-origin / local scope requests
  if (req.method !== 'GET') return;
  if (!req.url.startsWith(self.location.origin)) return;

  event.respondWith(
    caches.match(req).then(cachedResponse => {
      // Background revalidation attempt (fails gracefully if offline)
      const networkFetch = fetch(req).then(networkResponse => {
        if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(req, responseToCache);
          });
        }
        return networkResponse;
      }).catch(() => {
        // Network unavailable (offline) - ignore background revalidation error
        return null;
      });

      // If already cached, return immediately for instant offline launch
      if (cachedResponse) {
        return cachedResponse;
      }

      // Otherwise wait for the network response
      return networkFetch.then(networkResponse => {
        if (networkResponse) return networkResponse;

        // Fallback for navigation requests when offline
        if (req.mode === 'navigate') {
          return caches.match('./index.html').then(fallback => {
            return fallback || caches.match('./');
          });
        }

        return new Response('Offline resource unavailable', {
          status: 503,
          statusText: 'Service Unavailable',
          headers: new Headers({ 'Content-Type': 'text/plain' })
        });
      });
    })
  );
});
