from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        
        # Sanitize legacy data (convert dictionaries to integers)
        for key, value in cart.items():
            if isinstance(value, dict):
                cart[key] = 1 # Or some other default quantity
                
        self.cart = cart

    def add(self, product, quantity, size):
        product_id = str(product.id)
        product_qty = int(quantity)
        size = str(size) if size else "None"
        
        # Unique key for product and size combination
        item_key = f"{product_id}_{size}"

        if item_key in self.cart:
            # If it's old data (just an int), update it
            if isinstance(self.cart[item_key], int):
                 self.cart[item_key] += product_qty
            else:
                 # Should not happen with new logic, but for safety
                 self.cart[item_key] = product_qty
        else:
            self.cart[item_key] = product_qty

        self.session.modified = True

    def __len__(self):
        return sum(self.cart.values())
    
    def get_prods(self):
        # We need to return product objects for each unique product ID in the cart
        product_ids = set()
        for key in self.cart.keys():
            pid = key.split('_')[0]
            product_ids.add(pid)
        
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_cart_items(self):
        # New method to get detailed item info including sizes
        product_ids = {key.split('_')[0] for key in self.cart.keys()}
        products = {str(p.id): p for p in Product.objects.filter(id__in=product_ids)}
        
        items = []
        for key, quantity in self.cart.items():
            parts = key.split('_')
            product_id = parts[0]
            size = parts[1] if len(parts) > 1 else None
            
            product = products.get(product_id)
            if product:
                items.append({
                    'product': product,
                    'quantity': quantity,
                    'size': size,
                    'key': key
                })
        return items

    def get_total(self):
        product_ids = {key.split('_')[0] for key in self.cart.keys()}
        products = {str(p.id): p for p in Product.objects.filter(id__in=product_ids)}
        
        total = 0
        for key, quantity in self.cart.items():
            product_id = key.split('_')[0]
            product = products.get(product_id)
            if product:
                price = product.offer_price if product.is_offer else product.price
                total += price * quantity
        return total
    
    def update(self, product_key, quantity):
        # product_key is now the compound key 'product_id_size'
        product_qty = int(quantity)
        self.cart[str(product_key)] = product_qty
        self.session.modified = True
        return self.cart
    
    def delete(self, product_key):
        if str(product_key) in self.cart:
            del self.cart[str(product_key)]
        self.session.modified = True
        