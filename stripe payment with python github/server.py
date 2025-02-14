import os
from flask import Flask, redirect, jsonify, request, current_app
import stripe

stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'secret key test code')

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

YOUR_DOMAIN = 'Write Your domain' 

@app.route('/', methods=['GET'])
def get_index():
    return current_app.send_static_file('index.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:

        price_id = 'priceid'  
        
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'pricid', 
                    'quantity': 1,
                },
            ],
            mode='payment', 
            success_url=f'{YOUR_DOMAIN}/success.html?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{YOUR_DOMAIN}/cancel.html',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':

    if not stripe.api_key or 'sk_live_' not in stripe.api_key:
        print("Stripe live secret key is not set. Please set it in your environment variables.")
        exit(1)
    
    app.run(port=4242, debug=False)
