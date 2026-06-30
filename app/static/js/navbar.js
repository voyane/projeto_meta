const menuBar = document.getElementById('menu-bars');
const navMenu = document.getElementById('nav-menu');

if (menuBar && navMenu){
    menuBar.addEventListener('click', () => {
        menuBar.classList.toggle('active');
        navMenu.classList.toggle('active');
    });
}

// FECHAR MENU AO CLICAR FORA (MOBILE)
document.addEventListener('click', (e) => {

    const isClickInsideMenu = navMenu.contains(e.target);
    const isClickOnToggle = menuBar.contains(e.target);

    if (!isClickInsideMenu && !isClickOnToggle) {
        navMenu.classList.remove('active');
        menuBar.classList.remove('active');
    }
});

/* ========= USER DROPDOWN ========= */

const userDropdown = document.querySelector(".user-dropdown");
const trigger = document.querySelector(".user-trigger");

if(trigger){
    trigger.addEventListener("click", () => {
        userDropdown.classList.toggle("active");
    });

    // fechar ao clicar fora
    document.addEventListener("click", (e) => {
        if(!userDropdown.contains(e.target)){
            userDropdown.classList.remove("active");
        }
    });
}