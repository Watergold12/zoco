import json
from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session

        self.request = request 

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Normalize legacy formats into: {product_id: {"quantity": int, "size": str|None}}
        normalized_cart = {}
        for key, value in cart.items():
            size = None
            quantity = 0

            if isinstance(value, dict):
                quantity = int(value.get('quantity') or value.get('qty') or 0)
                size = value.get('size')
            else:
                quantity = int(value)

            if isinstance(key, str) and '_' in key:
                product_id, parsed_size = key.split('_', 1)
                key = product_id
                if not size:
                    size = parsed_size

            if size in ("", "None"):
                size = None

            key = str(key)
            if key in normalized_cart:
                normalized_cart[key]["quantity"] += quantity
                if size:
                    normalized_cart[key]["size"] = size
            else:
                normalized_cart[key] = {
                    "quantity": quantity,
                    "size": str(size) if size else None
                }

        self.cart = normalized_cart
        self.session['session_key'] = self.cart

    def add(self, product, quantity, size=None):
        if isinstance(product, Product):
            product_id = str(product.id)
        else:
            product_id = str(product)
        product_qty = int(quantity)
        size = str(size) if size else None

        if product_id in self.cart:
            existing_item = self.cart[product_id]
            if isinstance(existing_item, dict):
                existing_item["quantity"] = int(existing_item.get("quantity", 0)) + product_qty
                if size:
                    existing_item["size"] = size
            else:
                self.cart[product_id] = {
                    "quantity": int(existing_item) + product_qty,
                    "size": size
                }
        else:
            self.cart[product_id] = {
                "quantity": product_qty,
                "size": size
            }

        self.session.modified = True

        # deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            user_cart = json.dumps(self.cart)
            # Save user_cart to profile model
            current_user.update(old_cart=str(user_cart))

    def __len__(self):
        total = 0
        for item in self.cart.values():
            if isinstance(item, dict):
                total += int(item.get("quantity", 0))
            else:
                total += int(item)
        return total
    
    def get_prods(self):
        products = Product.objects.filter(id__in=self.cart.keys())
        return products
    
    def get_cart_items(self):
        # New method to get detailed item info including sizes
        products = {str(p.id): p for p in Product.objects.filter(id__in=self.cart.keys())}
        
        items = []
        for product_id, item in self.cart.items():
            if isinstance(item, dict):
                quantity = int(item.get("quantity", 0))
                size = item.get("size")
            else:
                quantity = int(item)
                size = None

            product = products.get(str(product_id))
            if product:
                items.append({
                    'product': product,
                    'quantity': quantity,
                    'size': size,
                    'key': str(product_id)
                })
        return items

    def get_total(self):
        products = {str(p.id): p for p in Product.objects.filter(id__in=self.cart.keys())}
        
        total = 0
        for product_id, item in self.cart.items():
            if isinstance(item, dict):
                quantity = int(item.get("quantity", 0))
            else:
                quantity = int(item)

            product = products.get(str(product_id))
            if product:
                price = product.offer_price if product.is_offer else product.price
                total += price * quantity
        return total
    
    def update(self, product_key, quantity):
        # product_key is just the product_id now
        product_qty = int(quantity)
        product_id = str(product_key)
        if product_id in self.cart and isinstance(self.cart[product_id], dict):
            self.cart[product_id]["quantity"] = product_qty
        else:
            self.cart[product_id] = {"quantity": product_qty, "size": None}
        self.session.modified = True
        return self.cart
    
    def delete(self, product_key):
        product_id = str(product_key)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        
