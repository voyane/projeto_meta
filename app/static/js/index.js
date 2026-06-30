
//-------------------Comprar Whatsapp-----
function comprarWhatsapp(){
    const numero = "258845421616";
    const mensagem = encodeURIComponent(
        "Olá, quero saber mais dos suplementos da Metamorphose Fit Shop."
    );
    window.open(`https://wa.me/${numero}?text=${mensagem}`, "_blank");
}

// ================= SLIDER =================

const list = document.querySelector('.slider .list');
const items = document.querySelectorAll('.slider .list .item');
const dots = document.querySelectorAll('.slider .dots li');
const prev = document.getElementById('prev');
const next = document.getElementById('next');

let active = 0;
const total = items.length;

let autoSlide = setInterval(nextSlide, 5000);

// mover slider
function reloadSlider(){

    list.style.transform = `translateX(-${active * 100}%)`;

    // atualizar dots
    document.querySelector('.dots li.active')
        .classList.remove('active');

    dots[active].classList.add('active');

    // reiniciar autoplay
    clearInterval(autoSlide);
    autoSlide = setInterval(nextSlide, 5000);
}

// próximo
function nextSlide(){
    active++;
    if(active >= total){
        active = 0;
    }
    reloadSlider();
}

// anterior
function prevSlide(){
    active--;
    if(active < 0){
        active = total - 1;
    }
    reloadSlider();
}

next.addEventListener('click', nextSlide);
prev.addEventListener('click', prevSlide);

// clicar nos dots
dots.forEach((dot, index)=>{
    dot.addEventListener('click', ()=>{
        active = index;
        reloadSlider();
    });
});

//--------Modal-Baixar Imagem--------
function openImage(src){
    const modal = document.getElementById("imageModal");
    const img = document.getElementById("modalImg");
    const download = document.getElementById("downloadBtn");

    img.src = src;
    download.href = src;

    modal.classList.add("active");
}

function closeImage(){
    document.getElementById("imageModal").classList.remove("active");
}
//----------------Product Section Fade ----------------------
const fades = document.querySelectorAll(".product-fade");

fades.forEach(fade => {

    const images = fade.querySelectorAll("img");
    let index = 0;

    images[index].classList.add("active");

    setInterval(() => {

        images[index].classList.remove("active");

        index = (index + 1) % images.length;

        images[index].classList.add("active");

    }, 5000);

});

//---------------------Testimonials Sections-------
const swiper = new Swiper('.slider-wrapper', {
  loop: true,
  spaceBetween: 25,

  // If we need pagination
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
    dynamicBullets: true,
  },

  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },

  breakpoints: {
    0: {
        slidesPerView: 1
    },
    768: {
        slidesPerView: 2
    },
    1024: {
        slidesPerView: 3
    }
  }
});

//---------------COntacto-------------------------

const textarea = document.getElementById("mensagem");
const contador = document.getElementById("contador");

textarea.addEventListener("input", () => {
    contador.textContent = `${textarea.value.length} / 300`;
});

document.getElementById("contactForm").addEventListener("submit", function(e){
    e.preventDefault();

    let nome = document.getElementById("nome").value;
    let contacto = document.getElementById("contactoCliente").value;
    let mensagem = document.getElementById("mensagem").value;

    let texto = `Olá, meu nome é ${nome}.
Meu contacto é ${contacto}.

Estou procurando o seguinte suplemento:
${mensagem}

Enviei uma imagem em anexo.`;

    let numeroWhatsApp = "258845421616"; // coloque seu número aqui

    let url = `https://wa.me/${numeroWhatsApp}?text=${encodeURIComponent(texto)}`;

    window.open(url, "_blank");
});

//-------------CHAT-----------------------
function toggleChat(){
    const chatBox = document.getElementById("chatBox");
    chatBox.style.display = chatBox.style.display === "flex" ? "none" : "flex";
}
function sendMessage(){
    const input = document.getElementById("chatInput");
    const chatBody = document.getElementById("chatBody");

    if(input.value.trim() === "") return;

    // Mensagem do usuário
    const userMsg = document.createElement("div");
    userMsg.classList.add("user-message");
    userMsg.textContent = input.value;
    chatBody.appendChild(userMsg);

    chatBody.scrollTop = chatBody.scrollHeight;

    // Enviar para WhatsApp
    const numero = "258845421616"; // seu número
    const texto = encodeURIComponent(input.value);
    const url = `https://wa.me/${numero}?text=${texto}`;
    
    window.open(url, "_blank");

    input.value = "";
}
