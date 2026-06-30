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