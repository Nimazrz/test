from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import PhoneForm, CodeForm, OrderForm
from account.models import ShopUser
from orders.models import Order, OrderItem
import random
from cart.cart import Cart
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
import requests
import json


# Create your views here.

def phone_verification(request):
    if request.user.is_authenticated:
        return redirect('orders:create_order')
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if ShopUser.objects.filter(phone=phone).exists():
                return redirect('shop:index')
            else:
                phone = request.session['phone'] = phone
                tokens = {'token': ''.join(random.choices('0123456789', k=6))}
                request.session['verification_code'] = tokens['token']
                print(tokens)  # sms
                messages.success(request, 'verification code is sent')
                return redirect('orders:code_verification')

    else:
        form = PhoneForm()
    return render(request, 'verify_phone.html', {'form': form})


def code_verification(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data['verification_code']
            token = request.session['verification_code']
            if verification_code == token:
                user = ShopUser.objects.create(phone=request.session['phone'])
                password = ''.join(random.choices('0123456789', k=6))
                print(f'your defautl account password is {password}')  # sms
                user.set_password(''.join(password))
                user.save()
                del request.session['verification_code']
                del request.session['phone']
                messages.success(request, 'verification is completed')
                return redirect('orders:create_order')
            else:
                messages.error(request, 'verification code is invalid')
    else:
        form = CodeForm()
    return render(request, 'verify_code.html', {'form': form})


def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.buyer = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'], weight=item['weight'])
            cart.clear()
            request.session['order_id'] = order.id
            return redirect('orders:request')

    else:
        form = OrderForm()
    return render(request, 'order_create.html', {'form': form})


#? sandbox merchant
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'

ZP_API_REQUEST = f"https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://sandbox.zarinpal.com/pg/StartPay/"

# Important: need to edit for real server.
CallbackURL = 'http://127.0.0.1:8000/order/verify/'



def send_request(request):
    try:
        order = Order.objects.get(id=request.session['order_id'])
        description = ', '.join(item.product.name for item in order.items.all())

        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_final_cost(),
            "Description": description,
            "Phone": request.user.phone,
            "CallbackURL": settings.CALLBACK_URL,
        }
        data = json.dumps(data)
        headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}

        print("Sending data:", data)  # Debug line to see the data being sent
        print("Headers:", headers)  # Debug line to see the headers

        response = requests.post(settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        print("Response status code:", response.status_code)  # Debug line to see the status code
        print("Response text:", response.text)  # Debug line to see the response text

        if response.status_code == 200:
            response_json = response.json()
            print("Response JSON:", response_json)  # Debug line to see the JSON response

            authority = response_json.get('Authority')
            if response_json.get('Status') == 100:
                for item in order.items.all():
                    item.product.inventory -= item.quantity
                    item.product.save()
                order.paid = True
                order.save()
                return redirect(settings.ZP_API_STARTPAY + authority)
            else:
                return HttpResponse(f'Error: Status {response_json.get("Status")}')
        else:
            return HttpResponse(f'Response failed with status code {response.status_code}')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')
    except Exception as e:
        print(f'Error details: {str(e)}')  # Print the exact error
        return HttpResponse(f'An error occurred: {str(e)}')


def verify(request):
    order = Order.objects.get(id=request.session['order_id'])

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_final_cost(),
        "Authority": request.GET.get('Authority'),
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            reference_id = response_json['RefID']
            if response_json['Status'] == 100:
                return HttpResponse(f'successful , RefID: {reference_id}')
            else:
                return HttpResponse('Error')
        del request.session['order_id']
        return HttpResponse('verify response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')
