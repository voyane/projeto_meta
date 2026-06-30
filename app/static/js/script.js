
//-------------CHAT--------------------------
function toggleChat(){
    const chatBox = document.getElementById("chatBox");
    chatBox.style.display = chatBox.style.display === "flex" ? "none" : "flex";
}
function sendMessage(){
    const input = document.getElementById("chatInput");
    const chatBody = document.getElementById("chatBody");

    if(input.value.trim() === "") return;

    //====Mensagem do usuário===================
    const userMsg = document.createElement("div");
    userMsg.classList.add("user-message");
    userMsg.textContent = input.value;
    chatBody.appendChild(userMsg);
    chatBody.scrollTop = chatBody.scrollHeight;

    //=====Enviar para WhatsApp==================
    const numero = "258845421616"; // seu número
    const texto = encodeURIComponent(input.value);
    const url = `https://wa.me/${numero}?text=${texto}`;
    window.open(url, "_blank");

    input.value = "";
}

//=====================FAVORITOS=============================
let favoritos = JSON.parse(localStorage.getItem("favoritos")) || [];

document.querySelectorAll(".favorito").forEach(btn => {
    const id = btn.dataset.id;
    const icon = btn.querySelector("i");

    if(favoritos.includes(id)){
        icon.classList.add("active");
    }

    btn.addEventListener("click", () => {
        icon.classList.toggle("active");

        if(favoritos.includes(id)){
            favoritos = favoritos.filter(f => f !== id);
        } else {
            favoritos.push(id);
        }

        localStorage.setItem("favoritos", JSON.stringify(favoritos));
    });
});

/* =================RATING======================== */
document.querySelectorAll(".rating").forEach(ratingDiv => {
    const produtoId = ratingDiv.dataset.produto;
    const stars = ratingDiv.querySelectorAll("i");
    const mediaSpan = ratingDiv.querySelector(".media-rating"); // só do produto atual

    stars.forEach(star => {
        star.addEventListener("click", async () => {
            const valor = Number(star.dataset.star);
            // ===== UI instantânea =====
            stars.forEach(s => {
                s.classList.toggle("active", Number(s.dataset.star) <= valor);
            });
            // ===== envia para Flask =====
            try {
                const response = await fetch("/api/rating", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ produto_id: produtoId, valor: valor })
                });

                const data = await response.json();

                // Se não estiver logado, redireciona para login
                if (data.login_required) {
                    const currentUrl = window.location.pathname + window.location.search;
                    window.location.href = `/login?next=${encodeURIComponent(currentUrl)}`;
                    return;
                }
                // Atualiza média no produto correto
                if (data.success && mediaSpan) {
                    mediaSpan.innerText = "⭐ " + data.media;
                }
            } catch (err) {
                console.error("Erro ao enviar rating:", err);
            }
        });
    });
});
/* ===============TOAST============================ */
function showToast(msg){
    const container = document.getElementById("toast");
    if(!container) return;

    const toast = document.createElement("div");
    toast.className = "toast-msg";
    toast.innerHTML = `
        <i class="fa-solid fa-circle-check"></i>
        <span>${msg}</span>
    `;
    container.appendChild(toast);

    setTimeout(()=>{
        toast.classList.add("toast-hide");
        setTimeout(()=>toast.remove(),400);
    },3000);
}

//==================CARRINHO (FLASK API)========================

//==================ATUALIZAR CONTADOR==========================
async function updateCartCount(){
    try{
        const res = await fetch("/api/cart/count");
        const data = await res.json();
        const counter = document.getElementById("cartCount");
        if(counter){
            counter.textContent = data.count;
        }
    }catch(err){
        console.log("Contador Indisponível!");
    }
}

//==================ADICIONAR PRODUTO(CARRINHO)=======================
async function adicionarCarrinho(slug){
    try{
        const res = await fetch("/api/cart/add",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body: JSON.stringify({ slug: slug })
        });

        const data = await res.json();

        if(data.login_required){
            // redireciona para login e mantém página atual
            const currentUrl = window.location.pathname + window.location.search;
            window.location.href = `/login?next=${encodeURIComponent(currentUrl)}`;
            return;
        }

        if(data.success){
            updateCartCount();
            animarCarrinho();
            showToast("Produto adicionado ao carrinho 🛒");
        }

    }catch(error){
        console.error(error);
    }
}

//=================ANIMAÇÃO DO BOTÃO==================================
function animarCarrinho(){
    const cart = document.getElementById("cartCount");

    cart.style.transform = "scale(1.4)";
    setTimeout(()=>{
        cart.style.transform = "scale(1)";
    },200);
}

//==============EVENTO BOTÃO ADICIONAR=====================
document.querySelectorAll(".cart-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        const slug = btn.dataset.id;
        adicionarCarrinho(slug);
    });
});

//=============CART DRAWER (visual)========================
const drawer = document.getElementById("cartDrawer");
const openCart = document.getElementById("openCart");
const closeCart = document.getElementById("closeCart");

openCart?.addEventListener("click", () =>
    drawer.classList.add("active")
);
closeCart?.addEventListener("click", () =>
    drawer.classList.remove("active")
);

//=====================INIT=================================
document.addEventListener("DOMContentLoaded", updateCartCount);

//==================COMPRAR WHATSAPP===========================

function comprarWhatsapp(nomeProduto){
    const numero = "258845421616";
    const mensagem = `Olá, quero comprar o produto: ${nomeProduto}`;
    const url = `https://wa.me/${numero}?text=${encodeURIComponent(mensagem)}`;
    window.open(url, "_blank");
}

//================= INIT =============================
document.addEventListener("DOMContentLoaded", updateCartCount);