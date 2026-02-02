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

function showToast() {
    const toast = document.getElementById('successToast');
    if (!toast) return;
    toast.classList.add('active');
    setTimeout(() => {
        toast.classList.remove('active');
    }, 2000);
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('loginToast')) {
        loginToast();
    }

    // Simple Search Functionality
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');

    if (searchInput && searchResults) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            if (query.length === 0) {
                searchResults.innerHTML = `
                    <div id="initial-state" style="text-align: center; color: var(--color-gray-400); padding: 4rem; grid-column: 1 / -1;">
                        <p style="font-size: 1.125rem; font-style: italic;">Start typing to search our premium collection...</p>
                    </div>
                `;
                return;
            }
            if (query.length < 2) {
                searchResults.innerHTML = `
                    <div style="text-align: center; color: var(--color-gray-400); padding: 4rem; grid-column: 1 / -1;">
                        <p>Keep typing...</p>
                    </div>
                `;
                return;
            }

            const filtered = products.filter(p => 
                p.name.toLowerCase().includes(query) || 
                p.category.toLowerCase().includes(query)
            );

            renderSearchResults(filtered);
        });
    }

    function renderSearchResults(results) {
        if (results.length === 0) {
            searchResults.innerHTML = `
                <div style="text-align: center; color: var(--color-gray-400); padding: 4rem; grid-column: 1 / -1;">
                    <p style="font-size: 1.25rem;">No products found matching your search.</p>
                    <p style="margin-top: 1rem;">Try searching for "silk", "set", or "panties".</p>
                </div>
            `;
            return;
        }

        searchResults.innerHTML = results.map(product => `
            <div class="product-card scroll-reveal visible">
                <div class="product-image-container aspect-square bg-white shadow-sm">
                    <img src="${product.img}" alt="${product.name}" class="product-img">
                    ${product.isNew ? `
                        <div class="new-badge">
                            <span class="new-badge-text">New In</span>
                        </div>
                    ` : ''}
                    <div class="product-overlay">
                        <a href="/product/${product.id}" class="add-cart-btn">
                            View Product
                        </a>
                    </div>
                </div>
                <div class="product-info">
                    <a class="product-title" href="/product/${product.id}">${product.name}</a>
                    <p class="product-price">₹${product.price}</p>
                </div>
            </div>
        `).join('');
    }
});


