// Cart State (PERSISTED)
let cart = JSON.parse(localStorage.getItem('zoco_cart')) || [];

// --- UTILITIES ---
const formatPrice = (price) => `₹${price.toLocaleString()}`;

// --- CART FUNCTIONS ---
function saveCart() {
    localStorage.setItem('zoco_cart', JSON.stringify(cart));
    updateCartUI();
}

function addToCart(id) {
    const product = products.find(p => p.id === id);
    if (!product) return;

    const existing = cart.find(item => item.id === id);
    if (existing) {
        existing.qty++;
    } else {
        cart.push({ ...product, qty: 1 });
    }

    saveCart();

    // UI Feedback
    showToast();

    // Open cart automatically
    const drawer = document.getElementById('cartDrawer');
    if (drawer && drawer.classList.contains('closed')) {
        toggleCart();
    }
}

function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    saveCart();
}

function changeQty(id, delta) {
    const item = cart.find(i => i.id === id);
    if (item) {
        item.qty += delta;
        if (item.qty <= 0) {
            removeFromCart(id);
        } else {
            saveCart();
        }
    }
}

function getCartCount() {
    return cart.reduce((acc, item) => acc + item.qty, 0);
}

function getCartTotal() {
    return cart.reduce((acc, item) => acc + (item.price * item.qty), 0);
}

// --- UI UPDATE FUNCTIONS ---
function updateCartUI() {
    const list = document.getElementById('cartList');
    const empty = document.getElementById('emptyCart');
    const footer = document.getElementById('cartFooter');
    const badge = document.getElementById('cartBadgeCount');
    const totalDisplay = document.getElementById('cartTotalDisplay') || document.getElementById('cartTotal');
    const subtotalDisplay = document.getElementById('cartSubtotal');

    // Update Badge
    if (badge) {
        badge.innerText = getCartCount();
        if (getCartCount() > 0) {
            badge.classList.remove('hidden');
            badge.classList.add('flex');
        } else {
            // Optional: hide badge if 0
            // badge.classList.add('hidden'); // Uncomment if you want to hide it
        }
    }

    // Update Cart Content
    if (!list) return;

    if (cart.length === 0) {
        list.classList.add('hidden');
        if (empty) empty.classList.remove('hidden');
        if (footer) footer.classList.add('hidden');
    } else {
        list.classList.remove('hidden');
        if (empty) empty.classList.add('hidden');
        if (footer) footer.classList.remove('hidden');

        list.innerHTML = cart.map(item => `
            <div class="cart-item">
                <div class="cart-item-img-wrapper">
                    <img src="${item.img}" class="cart-item-img">
                </div>
                <div class="cart-item-details">
                    <h4 class="cart-item-title">${item.name}</h4>
                    <p class="cart-item-price">${formatPrice(item.price)}</p>
                    
                    <div class="cart-qty-wrapper">
                         <div class="cart-qty-input">
                            <button onclick="changeQty(${item.id}, -1)" class="cart-qty-btn">-</button>
                            <span class="cart-qty-display">${item.qty}</span>
                            <button onclick="changeQty(${item.id}, 1)" class="cart-qty-btn">+</button>
                         </div>
                    </div>
                </div>
                <button onclick="removeFromCart(${item.id})" class="cart-remove-btn">
                    <i class="fa-solid fa-trash-can"></i>
                </button>
            </div>
        `).join('');

        const total = getCartTotal();
        if (totalDisplay) totalDisplay.innerText = formatPrice(total);
        if (subtotalDisplay) subtotalDisplay.innerText = formatPrice(total);
    }
}

function toggleCart() {
    const drawer = document.getElementById('cartDrawer');
    const overlay = document.getElementById('cartOverlay');
    if (!drawer || !overlay) return;

    if (drawer.classList.contains('closed')) {
        drawer.classList.replace('closed', 'open');
        overlay.classList.remove('hidden');
        setTimeout(() => overlay.classList.add('active'), 10);
        document.body.style.overflow = 'hidden';
    } else {
        drawer.classList.replace('open', 'closed');
        overlay.classList.remove('active');
        setTimeout(() => overlay.classList.add('hidden'), 500);
        document.body.style.overflow = 'auto';
    }
}

// --- SEARCH FUNCTIONS ---
function toggleSearch() {
    const overlay = document.getElementById('searchOverlay');
    const input = document.getElementById('searchInput');
    if (!overlay) return;

    if (overlay.classList.contains('hidden')) {
        overlay.classList.remove('hidden');
        setTimeout(() => {
            overlay.classList.add('active');
            if (input) input.focus();
        }, 10);
        document.body.style.overflow = 'hidden';
    } else {
        overlay.classList.remove('active');
        setTimeout(() => overlay.classList.add('hidden'), 500);
        document.body.style.overflow = 'auto';
    }
}

function handleSearch(e) {
    const query = e.target.value.toLowerCase().trim();
    const resultsContainer = document.getElementById('searchResults');

    if (query.length === 0) {
        resultsContainer.innerHTML = '';
        return;
    }

    const filtered = products.filter(p =>
        p.name.toLowerCase().includes(query) ||
        p.category.toLowerCase().includes(query)
    );

    if (filtered.length === 0) {
        resultsContainer.innerHTML = `
            <div style="text-align: center; padding: 2.5rem 0;">
                <p style="color: var(--color-gray-400); font-style: italic; font-size: 0.875rem;">No pieces found matching "${query}"</p>
            </div>
        `;
    } else {
        resultsContainer.innerHTML = filtered.map(p => `
            <div class="search-result-item" onclick="window.location.href='collections.html'">
                <div class="search-result-img-wrapper">
                    <img src="${p.img}" class="search-result-img">
                </div>
                <div>
                    <h4 class="search-result-title">${p.name}</h4>
                    <p class="search-result-category">${p.category}</p>
                    <p class="search-result-price">${formatPrice(p.price)}</p>
                </div>
                <div class="search-result-action">
                     <button onclick="event.stopPropagation(); addToCart(${p.id}); toggleSearch();" class="search-add-btn">Add</button>
                </div>
            </div>
        `).join('');
    }
}

function showToast() {
    const toast = document.getElementById('successToast');
    if (!toast) return;
    toast.classList.add('active');
    setTimeout(() => {
        toast.classList.remove('active');
    }, 2000);
}

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    updateCartUI();

    // Search Listener
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', handleSearch);
    }
});