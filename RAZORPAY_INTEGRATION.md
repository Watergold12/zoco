# Razorpay Standard Checkout Integration - ZOCO

## Summary

Razorpay Standard Checkout has been successfully integrated into the ZOCO Django e-commerce application. This enables secure payment processing with a modal-based checkout experience.

## Files Created/Modified

### Created Files
- None (all configuration uses existing .env)

### Modified Files

1. **[zoco/.env](zoco/.env)**
   - Added `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` credentials

2. **[.gitignore](.gitignore)**
   - Added `.env` to prevent accidental credential commits

3. **[zoco/requirements.txt](zoco/requirements.txt)**
   - Added `razorpay==1.5.1` SDK dependency

4. **[zoco/payment/views.py](zoco/payment/views.py)**
   - Added `create_razorpay_order()` - API endpoint to create Razorpay orders
   - Added `verify_razorpay_payment()` - API endpoint to verify payment signatures
   - Imported necessary modules: `razorpay`, `hmac`, `hashlib`, `csrf_exempt`
   - Initialized Razorpay client with credentials from environment variables

5. **[zoco/payment/urls.py](zoco/payment/urls.py)**
   - Added route `payment/api/create-order/` → `create_razorpay_order`
   - Added route `payment/api/verify-payment/` → `verify_razorpay_payment`

6. **[zoco/payment/templates/payment/checkout.html](zoco/payment/templates/payment/checkout.html)**
   - Updated pay button with ID `payButton` and onclick handler
   - Added Razorpay checkout script tag
   - Added complete JavaScript checkout flow with 3 steps:
     1. Create order on backend
     2. Open Razorpay modal with order details
     3. Verify payment signature after completion

## How It Works

### Payment Flow

1. **User clicks "Pay" button** on checkout page
2. **Frontend creates Razorpay order**
   - Calls `POST /payment/api/create-order/`
   - Backend creates order via Razorpay API
   - Returns `razorpay_order_id`, `razorpay_key_id`, and amount
3. **Razorpay checkout modal opens**
   - User enters payment details
   - Razorpay handles payment processing
4. **Payment verified on backend**
   - Calls `POST /payment/api/verify-payment/`
   - Backend verifies HMAC-SHA256 signature
   - Order is created in database if signature is valid
   - Cart is cleared
5. **User redirected to success page**
   - Order ID displayed to user

### Security Features

- **HMAC-SHA256 Signature Verification**: Ensures payment authenticity
- **CSRF Protection**: Django CSRF tokens on all backend requests
- **Environment Variables**: Never hardcode credentials in source code
- **Server-side Verification**: Payment never marked as complete without signature verification
- **Minimum Amount Check**: Orders under ₹1 (100 paise) are rejected

## API Endpoints

### POST `/payment/api/create-order/`
**Purpose**: Create a Razorpay order

**Request**:
- Method: POST
- Authentication: Requires authenticated user
- No request body needed

**Response** (Success - 200):
```json
{
    "success": true,
    "razorpay_order_id": "order_1234567890",
    "razorpay_key_id": "rzp_test_T0jbUqTXKrYcYq",
    "amount": 50000,
    "user_email": "user@example.com",
    "user_name": "John Doe"
}
```

**Response** (Error - 401/400/500):
```json
{
    "success": false,
    "message": "Error creating order: ..."
}
```

### POST `/payment/api/verify-payment/`
**Purpose**: Verify Razorpay payment and create order

**Request** (JSON):
```json
{
    "razorpay_payment_id": "pay_1234567890",
    "razorpay_order_id": "order_1234567890",
    "razorpay_signature": "9ef4dffbfd84f1318f6739a3ce19f9d85851857ae648f114332d8401e0949a3d"
}
```

**Response** (Success - 200):
```json
{
    "success": true,
    "message": "Payment verified successfully",
    "order_id": 42,
    "redirect_url": "/payment/payment_success/"
}
```

**Response** (Error - 400/500):
```json
{
    "success": false,
    "message": "Payment signature verification failed"
}
```

## Environment Variables

The following environment variables must be set in `.env`:

```
RAZORPAY_KEY_ID=rzp_test_T0jbUqTXKrYcYq
RAZORPAY_KEY_SECRET=u1XiCMK1VrxXjEVe5tnkcKrM
```

**Important**: Never commit `.env` to version control. It's already added to `.gitignore`.

## Testing

### Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Django development server**:
   ```bash
   python manage.py runserver
   ```

3. **Access the checkout page**:
   - Navigate to: `http://localhost:8000/payment/checkout/`
   - Ensure you're logged in

### Manual Testing Steps

1. **Add products to cart**
   - Browse products and add to cart

2. **Go to checkout**
   - Click "Proceed to Checkout"
   - Fill in shipping address
   - Click "Deliver Here"

3. **Initiate Razorpay payment**
   - Click "Pay ₹[amount]" button
   - Razorpay modal should open

4. **Complete payment** (Test Mode)
   - Use Razorpay test card: `4111 1111 1111 1111`
   - Expiry: Any future date (e.g., `12/25`)
   - CVV: Any 3 digits (e.g., `123`)
   - Click "Pay"

5. **Verify success**
   - Should see success message
   - Redirected to payment success page
   - Order created in database

### Test Card Numbers (Razorpay Test Mode)

| Card Type | Card Number | Result |
|-----------|-------------|--------|
| Visa | 4111 1111 1111 1111 | Success |
| Mastercard | 5555 5555 5555 4444 | Success |
| Amex | 3782 822463 10005 | Success |
| Invalid | 4111 1111 1111 1112 | Fails |

See more: https://razorpay.com/docs/payments/payment-gateway/test-mode/test-cards/

## Production Setup

### Before Going Live

1. **Switch to Live Credentials**
   - Replace test credentials in `.env` with live Razorpay keys
   - Test thoroughly with small amounts first

2. **Enable HTTPS**
   - Razorpay requires HTTPS for production

3. **Update Django Settings**
   - Set `DEBUG=False`
   - Add production domain to `ALLOWED_HOSTS`
   - Update `CSRF_TRUSTED_ORIGINS` to include production domain

4. **Database Backups**
   - Ensure regular backups before going live

## Troubleshooting

### "Razorpay client not initialized"
- Check `.env` file has `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`
- Ensure `python-dotenv` is installed: `pip install python-dotenv`

### "Payment signature verification failed"
- Verify the `RAZORPAY_KEY_SECRET` matches your Razorpay account
- Check that signature was calculated correctly with HMAC-SHA256

### "Cart is empty" error
- Ensure products are added to cart before checkout
- Check session is not cleared prematurely

### Razorpay modal doesn't open
- Verify Razorpay script is loaded: Check browser console for errors
- Check `RAZORPAY_KEY_ID` is correct in environment variables
- Ensure amount is >= ₹1 (100 paise)

### CSRF Token errors
- Verify CSRF token is included in all POST requests
- Check Django CSRF middleware is enabled in settings

## Key Implementation Details

### Signature Verification
```python
generated_signature = hmac.new(
    key_secret.encode(),
    f'{razorpay_order_id}|{razorpay_payment_id}'.encode(),
    hashlib.sha256
).hexdigest()
```

### Amount Conversion
- Frontend displays amounts in ₹ (INR)
- Razorpay API uses paise: 1 INR = 100 paise
- Minimum: 100 paise = ₹1

### Order Model
- Order created only after payment verification
- Cart cleared after successful order creation
- User profile updated with empty cart

## Reference Documentation

- **Razorpay Integration**: https://razorpay.com/docs/payments/payment-gateway/web-integration/standard/integration-steps/
- **Razorpay Python SDK**: https://github.com/razorpay/razorpay-python
- **Signature Verification**: https://razorpay.com/docs/payments/payment-gateway/web-integration/verify-signature/

## Support

For issues or questions:
1. Check Razorpay documentation: https://razorpay.com/docs/
2. Review test card options: https://razorpay.com/docs/payments/payment-gateway/test-mode/test-cards/
3. Contact Razorpay support: support@razorpay.com
