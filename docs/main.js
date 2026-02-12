document.querySelectorAll('.submenu-toggle').forEach(toggle => {
    toggle.addEventListener('click', function (e) {
        e.preventDefault();

        const submenu = this.nextElementSibling;


        submenu.classList.toggle('open');
        this.classList.toggle('open');
    });
});




/*
    Katex
*/

macro_katex = {
    '\\dd': '\\mathrm{d}',
    '\\dv': '\\frac{\\dd{#1}}{\\dd{#2}}',
    '\\vect': '\\overrightarrow{#1}',
    '\\R': '\\mathbb{R}'
}

