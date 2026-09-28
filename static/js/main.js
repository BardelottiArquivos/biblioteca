// static/js/main.js
// =============================================
// SCRIPT PRINCIPAL - BIBLIOTECA DO SABER
// =============================================

// Registra o Service Worker (PWA)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker
            .register('/static/sw.js')
            .then((reg) => console.log('SW registrado:', reg.scope))
            .catch((err) => console.error('Erro no SW:', err));
    });
}

// Auto-remove alertas após 5 segundos
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.alert').forEach((msg) => {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.5s';
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 500);
        }, 5000);
    });
});
