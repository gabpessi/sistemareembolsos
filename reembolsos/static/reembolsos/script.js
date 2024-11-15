function toggleText(button) {
    const row = button.closest('tr'); // Encontra a linha da tabela
    const cell = row.querySelector('.truncated'); // Encontra a célula com a descrição truncada
    const text = cell.querySelector('.text'); // Encontra o texto dentro da célula

    // Alterna a classe 'expanded' para expandir ou contrair o texto
    cell.classList.toggle('expanded');

    // Altera o texto do botão entre "+" e "-" conforme o estado
    if (cell.classList.contains('expanded')) {
        button.textContent = '-';
    } else {
        button.textContent = '+';
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const scrollTop = document.getElementById("scroll-top");
    const scrollBottom = document.getElementById("scroll-bottom");

    scrollTop.addEventListener("scroll", function () {
        scrollBottom.scrollLeft = scrollTop.scrollLeft;
    });

    scrollBottom.addEventListener("scroll", function () {
        scrollTop.scrollLeft = scrollBottom.scrollLeft;
    });
});