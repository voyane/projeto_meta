document.addEventListener("DOMContentLoaded", () => {
    inicializarFavoritos();
    inicializarRatings();
    inicializarBotoesCarrinho();
    inicializarCartDrawer();
    updateCartCount();
});

const csrfToken = document.querySelector("meta[name='csrf-token']")?.content;

/* =========================================================
   CHAT
========================================================= */

function toggleChat() {
    const chatBox = document.getElementById("chatBox");

    if (!chatBox) return;

    chatBox.style.display =
        chatBox.style.display === "flex" ? "none" : "flex";
}

function sendMessage() {
    const input = document.getElementById("chatInput");
    const chatBody = document.getElementById("chatBody");

    if (!input || !chatBody) return;

    const mensagem = input.value.trim();

    if (!mensagem) return;

    const userMsg = document.createElement("div");
    userMsg.classList.add("user-message");
    userMsg.textContent = mensagem;

    chatBody.appendChild(userMsg);
    chatBody.scrollTop = chatBody.scrollHeight;

    const numero = "258845421616";
    const url = `https://wa.me/${numero}?text=${encodeURIComponent(mensagem)}`;

    window.open(url, "_blank");

    input.value = "";
}

/* =========================================================
   FAVORITOS
========================================================= */

function inicializarFavoritos() {
    let favoritos = JSON.parse(
        localStorage.getItem("favoritos")
    ) || [];

    document.querySelectorAll(".favorito").forEach((btn) => {
        const id = btn.dataset.id;
        const icon = btn.querySelector("i");

        if (!id || !icon) return;

        if (favoritos.includes(id)) {
            icon.classList.add("active");
            icon.classList.remove("fa-regular");
            icon.classList.add("fa-solid");
        }

        btn.addEventListener("click", () => {
            if (favoritos.includes(id)) {
                favoritos = favoritos.filter(
                    favoritoId => favoritoId !== id
                );

                icon.classList.remove("active");
                icon.classList.remove("fa-solid");
                icon.classList.add("fa-regular");
            } else {
                favoritos.push(id);

                icon.classList.add("active");
                icon.classList.remove("fa-regular");
                icon.classList.add("fa-solid");
            }

            localStorage.setItem(
                "favoritos",
                JSON.stringify(favoritos)
            );
        });
    });
}

/* =========================================================
   RATING
========================================================= */

function inicializarRatings() {
    document.querySelectorAll(".rating").forEach((ratingDiv) => {
        const produtoId = ratingDiv.dataset.produto;
        const stars = ratingDiv.querySelectorAll("[data-star]");
        const mediaSpan = ratingDiv.querySelector(".media-rating");

        if (!produtoId || !stars.length) return;

        stars.forEach((star) => {
            star.addEventListener("click", async () => {
                const valor = Number(star.dataset.star);

                stars.forEach((item) => {
                    item.classList.toggle(
                        "active",
                        Number(item.dataset.star) <= valor
                    );
                });

                try {
                    const response = await fetch("/api/rating", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": csrfToken
                        },
                        body: JSON.stringify({
                            produto_id: produtoId,
                            valor: valor,
                            csrf_token: csrfToken
                        })
                    });

                    const data = await response.json();

                    if (data.login_required) {
                        const currentUrl =
                            window.location.pathname +
                            window.location.search;

                        window.location.href =
                            `/login?next=${encodeURIComponent(currentUrl)}`;

                        return;
                    }

                    if (data.success && mediaSpan) {
                        mediaSpan.textContent = data.media;
                    }

                    if (!data.success && data.message) {
                        showToast(data.message, "error");
                    }
                } catch (error) {
                    console.error("Erro ao enviar avaliação:", error);
                    showToast(
                        "Não foi possível enviar a avaliação.",
                        "error"
                    );
                }
            });
        });
    });
}

/* =========================================================
   TOAST
========================================================= */

function showToast(message, type = "success") {
    const container = document.getElementById("toast");

    if (!container) return;

    const toast = document.createElement("div");

    toast.className = `toast-msg toast-${type}`;

    const icon =
        type === "error"
            ? "fa-circle-xmark"
            : "fa-circle-check";

    toast.innerHTML = `
        <i class="fa-solid ${icon}"></i>
        <span></span>
    `;

    toast.querySelector("span").textContent = message;

    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add("toast-hide");

        setTimeout(() => {
            toast.remove();
        }, 400);
    }, 3000);
}

/* =========================================================
   CONTADOR DO CARRINHO
========================================================= */

async function updateCartCount() {
    try {
        const response = await fetch("/api/cart/count");
        const data = await response.json();

        const counter = document.getElementById("cartCount");

        if (counter) {
            counter.textContent = data.count ?? 0;
        }
    } catch (error) {
        console.warn("Contador do carrinho indisponível:", error);
    }
}

/* =========================================================
   ADICIONAR AO CARRINHO
========================================================= */

async function adicionarCarrinho(slug, button = null) {
    if (!slug) return;

    try {
        if (button) {
            button.disabled = true;
        }

        const response = await fetch("/api/cart/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                slug: slug,
                csrf_token: csrfToken
            })
        });

        const data = await response.json();

        if (data.login_required) {
            const currentUrl =
                window.location.pathname +
                window.location.search;

            window.location.href =
                `/login?next=${encodeURIComponent(currentUrl)}`;

            return;
        }

        if (data.success) {
            await updateCartCount();
            animarCarrinho();

            showToast(
                data.message || "Produto adicionado ao carrinho."
            );
        } else {
            showToast(
                data.message || "Não foi possível adicionar o produto.",
                "error"
            );
        }
    } catch (error) {
        console.error("Erro ao adicionar ao carrinho:", error);

        showToast(
            "Ocorreu um erro ao adicionar o produto.",
            "error"
        );
    } finally {
        if (button) {
            button.disabled = false;
        }
    }
}

function inicializarBotoesCarrinho() {
    document
        .querySelectorAll(".cart-btn[data-id]")
        .forEach((button) => {
            button.addEventListener("click", () => {
                const slug = button.dataset.id;

                adicionarCarrinho(slug, button);
            });
        });
}

/* =========================================================
   ANIMAÇÃO DO CARRINHO
========================================================= */

function animarCarrinho() {
    const cart = document.getElementById("cartCount");

    if (!cart) return;

    cart.classList.add("cart-bounce");

    setTimeout(() => {
        cart.classList.remove("cart-bounce");
    }, 500);
}

/* =========================================================
   CART DRAWER
========================================================= */

function inicializarCartDrawer() {
    const drawer = document.getElementById("cartDrawer");
    const openCart = document.getElementById("openCart");
    const closeCart = document.getElementById("closeCart");

    if (!drawer) return;

    openCart?.addEventListener("click", (event) => {
        event.preventDefault();
        drawer.classList.add("active");
    });

    closeCart?.addEventListener("click", () => {
        drawer.classList.remove("active");
    });

    document.addEventListener("click", (event) => {
        if (
            drawer.classList.contains("active") &&
            !drawer.contains(event.target) &&
            !openCart?.contains(event.target)
        ) {
            drawer.classList.remove("active");
        }
    });
}

/* =========================================================
   COMPRAR PELO WHATSAPP
========================================================= */

function comprarWhatsapp(nomeProduto, precoProduto = null) {
    const numero = "258845421616";

    let mensagem = `Olá, quero comprar o produto: ${nomeProduto}`;

    if (precoProduto) {
        mensagem += `\nPreço: ${precoProduto} MT`;
    }

    const url =
        `https://wa.me/${numero}?text=${encodeURIComponent(mensagem)}`;

    window.open(url, "_blank");
}
