"""Builds command-centre/standalone/index.html from command-centre/index.html.
The same app, with the Firebase SDK, the config and the runtime loaded first, plus the PWA manifest and offline worker."""
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = '10.14.1'
src = open(f'{R}/command-centre/index.html', encoding='utf-8').read()
head = (f'<link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#0f766e"><link rel="icon" href="icon-192.png">'
        f'<script src="https://www.gstatic.com/firebasejs/{V}/firebase-app-compat.js"></script>'
        f'<script src="https://www.gstatic.com/firebasejs/{V}/firebase-auth-compat.js"></script>'
        f'<script src="https://www.gstatic.com/firebasejs/{V}/firebase-firestore-compat.js"></script>'
        f'<script src="https://www.gstatic.com/firebasejs/{V}/firebase-storage-compat.js"></script>'
        '<script src="formcraft-config.js"></script><script src="formcraft-runtime.js"></script>'
        "<script>if('serviceWorker' in navigator)addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));</script>")
i = src.index('<script>')
open(f'{R}/command-centre/standalone/index.html', 'w', encoding='utf-8').write(src[:i] + head + src[i:])
print('built command-centre/standalone/index.html')
