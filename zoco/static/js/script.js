// Cart State (PERSISTED)
let cart = JSON.parse(localStorage.getItem('zoco_cart')) || [];

// --- UTILITIES ---
const formatPrice = (price) => `₹${price.toLocaleString()}`;

function login_Toast() {
    const toast = document.getElementById('loginToast');
    if (!toast) return;
    toast.classList.add('active');
    setTimeout(() => {
        toast.classList.remove('active');
    }, 2000);
}

function loginToast() {
    login_Toast();
}

function removeFromCart(id) {
    console.log('Removing item ID:', id);
    console.log('Cart before:', cart.length, 'items');
    
    // Filter out the item
    cart = cart.filter(item => item.id !== id);
    
    console.log('Cart after:', cart.length, 'items');

}

function changeQty(id, delta) {
    console.log('Changing qty for ID:', id, 'Delta:', delta);
    
    const item = cart.find(i => i.id === id);
    if (item) {
        item.qty += delta;
        console.log('New quantity:', item.qty);
        
        if (item.qty <= 0) {
            removeFromCart(id);
        } else {

        }
    }
}

function getCartCount() {
    return cart.reduce((acc, item) => acc + item.qty, 0);
}

function getCartTotal() {
    return cart.reduce((acc, item) => acc + (item.price * item.qty), 0);
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
            <div class="search-result-item" onclick="window.location.href='{% url 'collections' %}'">
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
    console.log('DOM loaded - Initializing cart');
    console.log('Cart from localStorage:', cart);

    // Search Listener
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', handleSearch);
    }

    const loginToast = document.getElementById('loginToast');
    if (loginToast) {
        setTimeout(() => {
            loginToast.classList.add('active');
        }, 100);
        setTimeout(() => {
            loginToast.classList.remove('active');
        }, 3000);
    }
    
    console.log('Cart initialized with', cart.length, 'items');
});