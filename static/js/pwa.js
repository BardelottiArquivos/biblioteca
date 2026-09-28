// static/js/pwa.js
// =============================================
// INSTALAÇÃO PWA
// =============================================

let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;

    const banner = document.createElement('div');
    banner.className = 'pwa-install-banner';
    banner.innerHTML = `
        <span>📱 Instale a Biblioteca do Saber</span>
        <button id="pwa-install-btn">Instalar</button>
        <button id="pwa-dismiss-btn">Agora não</button>
    `;
    document.body.appendChild(banner);

    document.getElementById('pwa-install-btn').addEventListener('click', async () => {
        banner.remove();
        deferredPrompt.prompt();
        await deferredPrompt.userChoice;
        deferredPrompt = null;
    });

    document.getElementById('pwa-dismiss-btn').addEventListener('click', () => {
        banner.remove();
    });
});
