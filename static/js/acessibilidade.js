// static/js/acessibilidade.js
// =============================================
// SCRIPT DE ACESSIBILIDADE
// =============================================

function setCookie(name, value, days) {
    const d = new Date();
    d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${d.toUTCString()};path=/`;
}

function getCookie(name) {
    const match = document.cookie.match(
        new RegExp('(^| )' + name + '=([^;]+)')
    );
    return match ? match[2] : null;
}

document.addEventListener('DOMContentLoaded', () => {
    // Aplica preferências salvas
    if (getCookie('alto_contraste') === 'true') {
        document.body.classList.add('alto-contraste');
    }
    if (getCookie('fonte_dislexia') === 'true') {
        document.body.classList.add('fonte-dislexia');
    }
    const tamanho = getCookie('tamanho_fonte') || 'media';
    document.body.classList.add('fonte-' + tamanho);

    // Botões
    const btnContraste = document.getElementById('toggle-contrast');
    const btnDislexia = document.getElementById('toggle-dyslexia');
    const btnAumentar = document.getElementById('increase-font');
    const btnDiminuir = document.getElementById('decrease-font');

    if (btnContraste) {
        btnContraste.addEventListener('click', () => {
            document.body.classList.toggle('alto-contraste');
            setCookie(
                'alto_contraste',
                document.body.classList.contains('alto-contraste'),
                365
            );
        });
    }

    if (btnDislexia) {
        btnDislexia.addEventListener('click', () => {
            document.body.classList.toggle('fonte-dislexia');
            setCookie(
                'fonte_dislexia',
                document.body.classList.contains('fonte-dislexia'),
                365
            );
        });
    }

    const tamanhos = ['pequena', 'media', 'grande', 'extra'];

    function mudarTamanho(delta) {
        const atual = tamanhos.findIndex((t) =>
            document.body.classList.contains('fonte-' + t)
        );
        const novo = Math.max(0, Math.min(tamanhos.length - 1, atual + delta));

        tamanhos.forEach((t) => document.body.classList.remove('fonte-' + t));
        document.body.classList.add('fonte-' + tamanhos[novo]);
        setCookie('tamanho_fonte', tamanhos[novo], 365);
    }

    if (btnAumentar) {
        btnAumentar.addEventListener('click', () => mudarTamanho(1));
    }
    if (btnDiminuir) {
        btnDiminuir.addEventListener('click', () => mudarTamanho(-1));
    }
});