document.querySelectorAll('.submenu-toggle').forEach(toggle => {
    toggle.addEventListener('click', function (e) {
        e.preventDefault();

        const submenu = this.nextElementSibling;


        submenu.classList.toggle('open');
        this.classList.toggle('open');
    });
});
