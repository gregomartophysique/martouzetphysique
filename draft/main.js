(function () {
    "use strict";

    // Fonction pour ajuster la hauteur
    function fullHeight() {
        var elements = document.querySelectorAll('.js-fullheight');
        var height = window.innerHeight;

        elements.forEach(function (el) {
            el.style.height = height + 'px';
        });
    }

    // Appel initial
    fullHeight();

    // Mise à jour lors du redimensionnement
    window.addEventListener('resize', fullHeight);

    // Gestion du clic sur le bouton
    var sidebarCollapse = document.getElementById('sidebarCollapse');
    var sidebar = document.getElementById('sidebar');

    if (sidebarCollapse && sidebar) {
        sidebarCollapse.addEventListener('click', function () {
            sidebar.classList.toggle('active');
        });
    }

})();


document.querySelectorAll('.submenu-toggle').forEach(toggle => {
    toggle.addEventListener('click', function (e) {
        e.preventDefault();

        const submenu = this.nextElementSibling;


        submenu.classList.toggle('open');
        this.classList.toggle('open');
    });
});
