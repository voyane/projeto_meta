document.querySelectorAll(".btn-increase").forEach(btn => {
    btn.addEventListener("click", () => {
        updateQty(btn.dataset.id, "increase");
    });
});

document.querySelectorAll(".btn-decrease").forEach(btn => {
    btn.addEventListener("click", () => {
        updateQty(btn.dataset.id, "decrease");
    });
});

document.querySelectorAll(".btn-remove").forEach(btn => {
    btn.addEventListener("click", () => {
        removeItem(btn.dataset.id);
    });
});

const checkoutBtn = document.querySelector(".checkout-btn");
const paymentResult = document.getElementById("paymentResult");
const paymentResultTitle = document.getElementById("paymentResultTitle");
const paymentResultText = document.getElementById("paymentResultText");
const paymentProofLink = document.getElementById("paymentProofLink");

if (checkoutBtn) {
    checkoutBtn.addEventListener("click", finalizeOrder);
}

function updateQty(itemId, action) {
    fetch("/api/cart/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({item_id: itemId, action: action})
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            location.reload();
        }
    })
    .catch(err => console.error(err));
}

function finalizeOrder() {
    const selectedPayment = document.querySelector(
        "input[name='payment_method']:checked"
    );
    const paymentMethod = selectedPayment ? selectedPayment.value : "mpesa";

    checkoutBtn.disabled = true;
    checkoutBtn.textContent = "A finalizar...";

    fetch("/api/cart/checkout", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({payment_method: paymentMethod})
    })
    .then(res => res.json())
    .then(data => {
        if (data.success && data.manual_payment) {
            showPaymentInstructions(data);
            checkoutBtn.disabled = false;
            checkoutBtn.textContent = "Finalizar Pedido";
            return;
        }

        if (data.success && data.whatsapp_url) {
            window.location.href = data.whatsapp_url;
            return;
        }

        alert(data.message || "Não foi possível finalizar o pedido.");
        checkoutBtn.disabled = false;
        checkoutBtn.textContent = "Finalizar Pedido";
    })
    .catch(err => {
        console.error(err);
        alert("Ocorreu um erro ao finalizar o pedido.");
        checkoutBtn.disabled = false;
        checkoutBtn.textContent = "Finalizar Pedido";
    });
}

function showPaymentInstructions(data) {
    if (!paymentResult) {
        alert(data.instructions || "Pagamento registado.");
        return;
    }

    paymentResultTitle.textContent = `Pagamento por ${data.payment_label}`;
    paymentResultText.textContent =
        `${data.instructions}\n` +
        `Número: ${data.payment_number}\n` +
        `Total: ${data.total}\n\n` +
        "Depois de pagar, envie o comprovativo pelo WhatsApp.";
    paymentProofLink.href = data.proof_whatsapp_url;
    paymentResult.hidden = false;
}

function removeItem(itemId) {
    fetch("/api/cart/remove", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({item_id: itemId})
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            location.reload();
        }
    })
    .catch(err => console.error(err));
}
