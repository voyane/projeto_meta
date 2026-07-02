document.addEventListener("DOMContentLoaded", () => {
    const menuBar = document.getElementById("menu-bars");
    const navMenu = document.getElementById("nav-menu");

    const userDropdown = document.querySelector(".user-dropdown");
    const userTrigger = document.querySelector(".user-trigger");

    const adminDropdown = document.querySelector(".admin-dropdown");
    const adminTrigger = document.querySelector(".admin-trigger");

    if (menuBar && navMenu) {
        menuBar.addEventListener("click", (e) => {
            e.stopPropagation();
            navMenu.classList.toggle("active");
        });
    }

    if (userDropdown && userTrigger) {
        userTrigger.addEventListener("click", (e) => {
            e.stopPropagation();

            userDropdown.classList.toggle("active");

            if (adminDropdown) {
                adminDropdown.classList.remove("active");
            }
        });
    }

    if (adminDropdown && adminTrigger) {
        adminTrigger.addEventListener("click", (e) => {
            e.stopPropagation();

            adminDropdown.classList.toggle("active");

            if (userDropdown) {
                userDropdown.classList.remove("active");
            }
        });
    }

    document.addEventListener("click", (e) => {
        if (navMenu && menuBar) {
            const clickedInsideMenu = navMenu.contains(e.target);
            const clickedMenuButton = menuBar.contains(e.target);

            if (!clickedInsideMenu && !clickedMenuButton) {
                navMenu.classList.remove("active");
            }
        }

        if (userDropdown && !userDropdown.contains(e.target)) {
            userDropdown.classList.remove("active");
        }

        if (adminDropdown && !adminDropdown.contains(e.target)) {
            adminDropdown.classList.remove("active");
        }
    });

    const navLinks = document.querySelectorAll(".nav-link");

    navLinks.forEach((link) => {
        link.addEventListener("click", () => {
            if (navMenu) {
                navMenu.classList.remove("active");
            }
        });
    });
});