(function () {
    var cards = document.querySelectorAll('.bolo[data-preco]');
    var barra = document.getElementById('barra-pedido');
    if (!cards.length || !barra) return;

    var totalEl = document.getElementById('barra-total');
    var itensEl = document.getElementById('barra-itens');

    function atualizar() {
        var total = 0;
        var itens = 0;
        cards.forEach(function (card) {
            var input = card.querySelector('input[type=number]');
            if (!input) return;
            var qtd = parseInt(input.value, 10) || 0;
            itens += qtd;
            total += qtd * parseFloat(card.dataset.preco);
        });
        totalEl.textContent = 'R$ ' + total.toFixed(2).replace('.', ',');
        itensEl.textContent = itens + (itens === 1 ? ' item' : ' itens');
        barra.classList.toggle('ativa', itens > 0);
    }

    cards.forEach(function (card) {
        var input = card.querySelector('input[type=number]');
        if (!input) return;
        var max = parseInt(input.max, 10) || 0;

        card.querySelectorAll('[data-passo]').forEach(function (botao) {
            botao.addEventListener('click', function () {
                var novo = (parseInt(input.value, 10) || 0) + parseInt(botao.dataset.passo, 10);
                input.value = Math.min(Math.max(novo, 0), max);
                atualizar();
            });
        });

        input.addEventListener('input', atualizar);
    });

    atualizar();
})();