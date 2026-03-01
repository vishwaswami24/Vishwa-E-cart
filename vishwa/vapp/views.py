from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from vapp.models import Product,Cart,Order,OrderHistory,UserInfo,Review,Wishlist,ContactMessage
from django.db.models import Q,Avg
import random
import razorpay
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.

 
def products(request):
    query = request.GET.get('q', '')
    if query:
        p = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(pdetails__icontains=query) | 
            Q(brand__icontains=query),
            is_active=True
        )
    else:
        p = Product.objects.filter(is_active=True)
    context = {'data': p, 'query': query}
    return render(request, 'products.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('iname')
        email = request.POST.get('imail')
        mobile = request.POST.get('imobile')
        msg = request.POST.get('imsg')
        
        ContactMessage.objects.create(name=name, email=email, mobile=mobile, message=msg)
        messages.success(request, 'Thank you! Your message has been sent successfully.')
        return redirect('/contact')
    
    context = {}
    if request.user.is_authenticated:
        u = User.objects.filter(id=request.user.id)
        context['data'] = u
    return render(request, 'contact.html', context)

def home(request):
    p = Product.objects.filter(is_active=True)[:3]
    context = {'data': p}
    return render(request, 'index.html', context)

def about(request):
    context={}
    u=User.objects.filter(id=request.user.id)
    context['data']=u 
    return render(request,'about.html',context)

def prodetails(request):
    context={}
    u=User.objects.filter(id=request.user.id)
    context['data']=u
    return render(request,'product_details.html',context)

def register(request):
    context={}
    if request.method == "GET":
        return render(request,'register.html')
    else:
        # Verify reCAPTCHA
        import requests
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe',
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        
        if not result.get('success'):
            context['errmsg']="Please complete the reCAPTCHA verification"
            return render(request,'register.html',context)
        
        f=request.POST['ufname']
        l=request.POST['ulname']
        n=request.POST['uemail']
        p=request.POST['upass']
        cp=request.POST['ucpass']

        if  f=='' or l=='' or n=='' or p=='' or cp=='':
            context['errmsg']="Fields cannot be empty!!"
            return render(request,'register.html',context)
        elif p!=cp:
            context['errmsg']="Password and Confirm Password didn't matched."
            return render(request,'register.html',context)
        elif len(p)<8:
            context['errmsg']="Password must be at least 8 characters"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(username=n,email=n,first_name=f,last_name=l)
                u.set_password(p)
                u.save()
                context['success']="User Created Successfully!"
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="User with same Username already exists.\nPlease Login."
                return render(request,'register.html',context)

# user django built-in framework functions
def user_login(request):
    if request.method=="GET":
        return render(request,'login.html')
    else:
        name=request.POST['uname']
        upass=request.POST['upass']
        #authenticate
        u=authenticate(username=name,password=upass)
        if u is not None:
            login(request,u)
            
            # Transfer session cart to database
            cart_session = request.session.get('cart', {})
            if cart_session:
                user_obj = User.objects.get(id=u.id)
                for pid, qty in cart_session.items():
                    try:
                        product = Product.objects.get(id=pid)
                        # Check if item already exists in cart
                        existing_cart = Cart.objects.filter(userid=user_obj, pid=product)
                        if not existing_cart.exists():
                            Cart.objects.create(userid=user_obj, pid=product, qty=qty)
                    except Product.DoesNotExist:
                        pass
                # Clear session cart
                request.session['cart'] = {}
                request.session.modified = True
                # Redirect to place order if cart had items
                return redirect('/placeorder')
            
            return redirect('/products')
        else:
            context={}
            context['errmsg']="Invalid username and password !!!"
            return render(request,'login.html',context)

def user_logout(request):
    logout(request)
    return redirect('/products')  

# user profile edit function 
def profile(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            m=UserInfo.objects.filter(userid=request.user.id)
            context={}
            context['data']=m
            return render(request,'profile.html',context)
        else:
            name=request.POST['fname']
            sname=request.POST['lname']
            gen=request.POST['inlineRadioOptions']
            mo=request.POST['mobile']
            add=request.POST['add']
            city=request.POST['city']
            pin=request.POST['pin']
            mail=request.POST['mail']
            co=request.POST['country']
            st=request.POST['state']
            profile_image = request.FILES.get('profile_image')
            dob=request.POST.get('dob')

            u=User.objects.filter(id=request.user.id)
            ui=UserInfo.objects.filter(userid=request.user.id)
            u.update(username=mail,email=mail,first_name=name,last_name=sname)
            n=len(ui)
            if n==0:
                ui=UserInfo.objects.create(userid=u[0],gender=gen,mobile=mo,address=add,city=city,pincode=pin,country=co,state=st,profile_image=profile_image,date_of_birth=dob)
                ui.save()
            else:
                ui_obj = ui.first()
                ui_obj.gender = gen
                ui_obj.mobile = mo
                ui_obj.address = add
                ui_obj.city = city
                ui_obj.pincode = pin
                ui_obj.country = co
                ui_obj.state = st
                ui_obj.date_of_birth = dob
                if profile_image:
                    ui_obj.profile_image = profile_image
                ui_obj.save()
            return redirect('/profile')
    else:
        return redirect('/login')

#category filter
def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    context={}
    context['data']=p
    return render(request,'products.html',context)

#Sort Price Filter
def sortprice(request,sv):
    if sv=='1':
        t='-price'
    else:
        t='price'
    p=Product.objects.order_by(t).filter(is_active=True)
    context={}
    context['data']=p       
    return render(request,'products.html',context)

def pricefilter(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    p=Product.objects.filter(q1 & q2)
    context={}
    context['data']=p
    return render(request,'products.html',context)

def product_details(request, pid):
    p = Product.objects.filter(id=pid)
    context = {'data': p}
    
    if p.exists():
        product = p.first()
        related = Product.objects.filter(cat=product.cat, is_active=True).exclude(id=pid)[:4]
        reviews = Review.objects.filter(product=product).order_by('-created_at')
        
        user_review = None
        in_wishlist = False
        if request.user.is_authenticated:
            user_review = Review.objects.filter(product=product, user=request.user).first()
            in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
        
        context.update({
            'related_products': related,
            'reviews': reviews,
            'user_review': user_review,
            'in_wishlist': in_wishlist
        })
    
    return render(request, 'product_details.html', context)

def cart(request,pid):
    u=User.objects.filter(id=request.user.id) if request.user.is_authenticated else None
    p=Product.objects.filter(id=pid)
    qty = int(request.GET.get('qty', 1))
    buynow = request.GET.get('buynow', '0')

    if p.exists() and p[0].stock < qty:
        messages.error(request, 'Insufficient stock available!')
        return redirect(f'/product_details/{pid}')

    if request.user.is_authenticated:
        q1=Q(userid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        context={}
        context['data']=p
        if n==1:
            messages.warning(request, 'Product already exists in the cart!')
        else:
            c=Cart.objects.create(userid=u[0],pid=p[0], qty=qty)
            c.save()
            messages.success(request, 'Product added successfully to cart!')
        
        # Redirect to checkout if buynow parameter is present
        if buynow == '1':
            return redirect('/placeorder')
        return redirect(f'/product_details/{pid}')
    else:
        # For buy now, redirect to login
        if buynow == '1':
            return redirect('/login')
        
        # Store cart items in session for non-authenticated users
        cart_session = request.session.get('cart', {})
        if str(pid) in cart_session:
            messages.warning(request, 'Product already exists in the cart!')
        else:
            cart_session[str(pid)] = qty
            request.session['cart'] = cart_session
            messages.success(request, 'Product added successfully to cart!')
        return redirect(f'/product_details/{pid}')

def placeorder(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    c=Cart.objects.filter(userid=request.user.id)
    oid=random.randrange(1000,9999)
    for x in c:
        amount=x.qty*x.pid.price
        o=Order.objects.create(orderid=oid,qty=x.qty,pid=x.pid,userid=x.userid,amt=amount)
        o.save()
        x.delete()      
    return redirect('/fetchorder')

def fetchorderdetails(request):
    u=User.objects.filter(id=request.user.id)
    orders=Order.objects.filter(userid=request.user.id)
    sum=0
    for x in orders:
        sum=sum+x.amt
    
    context={}
    context['data']=u
    context['orders']=orders
    context['tamount']=sum
    context['n']=len(orders)
    return render(request,'placeorder.html',context)

def viewcart(request):
    if not request.user.is_authenticated:
        # Handle session cart for non-authenticated users
        cart_session = request.session.get('cart', {})
        cart_items = []
        sum = 0
        for pid, qty in cart_session.items():
            try:
                product = Product.objects.get(id=pid)
                item_total = product.price * qty
                sum += item_total
                cart_items.append({
                    'cart_item': {'pid': product, 'qty': qty, 'id': pid},
                    'item_total': item_total
                })
            except Product.DoesNotExist:
                pass
        
        context = {
            'c': cart_items,
            'total': sum,
            'n': len(cart_items)
        }
        return render(request, 'cart.html', context)
    
    u=User.objects.filter(id=request.user.id)
    c=Cart.objects.filter(userid=request.user.id)
    sum=0
    cart_items = []
    for x in c:
        item_total = x.pid.price * x.qty
        sum += item_total
        cart_items.append({
            'cart_item': x,
            'item_total': item_total
        })

    context={}
    context['data']=u
    context['c']=cart_items
    context['total']=sum
    context['n']=len(c)
    return render(request,'cart.html',context)

def updateqty(request,x,cid):
    if not request.user.is_authenticated:
        # Handle session cart quantity update
        cart_session = request.session.get('cart', {})
        if str(cid) in cart_session:
            q = cart_session[str(cid)]
            if x=='1':
                q = q + 1
            elif q > 1:
                q = q - 1
            else:
                # Remove item if quantity is 1 and user presses minus
                del cart_session[str(cid)]
                request.session['cart'] = cart_session
                request.session.modified = True
                return redirect('/viewcart')
            cart_session[str(cid)] = q
            request.session['cart'] = cart_session
            request.session.modified = True
        return redirect('/viewcart')
    
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    if x=='1':
        q=q+1
        c.update(qty=q)
    elif q>1:
        q=q-1
        c.update(qty=q)
    else:
        # Remove item if quantity is 1 and user presses minus
        c.delete()
    return redirect('/viewcart')        
    
def removecart(request,cid):
    if not request.user.is_authenticated:
        # Handle session cart removal
        cart_session = request.session.get('cart', {})
        if str(cid) in cart_session:
            del cart_session[str(cid)]
            request.session['cart'] = cart_session
            request.session.modified = True
        return redirect('/viewcart')
    
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')  

def removeord(request,oid):
    o=Order.objects.filter(id=oid)
    o.delete()
    return redirect('/fetchorder')  

def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_kXFXF8rCgidqau", "s8SRf1vqU2sXYTGzj6QvWftJ"))
    orders=Order.objects.filter(userid=request.user.id)
    sum=0
    for x in orders:
        sum=sum+x.amt
        oid=x.orderid

    data = { "amount": sum*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['payment']=payment
    context['amount']=sum
    return render(request,'pay.html',context)

def paymentsuccess(request):
    from django.template.loader import render_to_string
    import os
    from django.conf import settings
    import threading

    # Get user and order details
    u = User.objects.filter(id=request.user.id)
    o = Order.objects.filter(userid=request.user.id)

    # Calculate total
    total_amount = sum(x.amt for x in o)

    # Prepare invoice context
    from datetime import datetime
    current_datetime = datetime.now()
    user_info = u[0].userinfo_set.first() if u[0].userinfo_set.exists() else None
    invoice_context = {
        'name': f"{u[0].first_name} {u[0].last_name}",
        'address': getattr(user_info, 'address', 'N/A') if user_info else 'N/A',
        'city': getattr(user_info, 'city', 'N/A') if user_info else 'N/A',
        'state': getattr(user_info, 'state', 'N/A') if user_info else 'N/A',
        'pin': getattr(user_info, 'pincode', 'N/A') if user_info else 'N/A',
        'countrycode': getattr(user_info, 'country', 'N/A') if user_info else 'N/A',
        'code': getattr(user_info, 'pincode', 'N/A') if user_info else 'N/A',
        'sales': o,
        'total': total_amount,
        'company': 'Vishwa E-cart Pvt. Ltd.',
        'order_date': current_datetime,
        'invoice_date': current_datetime
    }

    # Render HTML email content
    html_content = render_to_string('invoice.html', invoice_context)
    email_to = u[0].email

    # Send email in background thread
    def send_email_async():
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.image import MIMEImage
        
        msg = MIMEMultipart('related')
        msg['Subject'] = "Vishwa E-cart - Order Confirmation & Invoice"
        msg['From'] = "swamivishwa0@gmail.com"
        msg['To'] = email_to
        
        msg_alternative = MIMEMultipart('alternative')
        msg.attach(msg_alternative)
        msg_alternative.attach(MIMEText(html_content, 'html'))
        
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                msg_image = MIMEImage(f.read())
                msg_image.add_header('Content-ID', '<logo.png>')
                msg.attach(msg_image)
        
        try:
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"Email sending failed: {e}")
    
    threading.Thread(target=send_email_async, daemon=True).start()

    # Move orders to history and delete from orders
    for x in o:
        oh = OrderHistory.objects.create(orderid=x.orderid, qty=x.qty, pid=x.pid, userid=x.userid, amt=x.amt)
        oh.save()
        x.delete()

    context = {}
    context['data'] = u
    return render(request, 'paymentsuccess.html', context)

def shipping(request):
    context={}
    u=User.objects.filter(id=request.user.id)
    context['data']=u
    return render(request,'shipping.html',context)

def privacy(request):
    context={}
    u=User.objects.filter(id=request.user.id)
    context['data']=u
    return render(request,'privacy.html',context)

def terms(request):
    context={}
    u=User.objects.filter(id=request.user.id)
    context['data']=u
    return render(request,'terms.html',context)

def cart_count(request):
    if request.user.is_authenticated:
        count = Cart.objects.filter(userid=request.user.id).count()
    else:
        cart_session = request.session.get('cart', {})
        count = len(cart_session)
    return JsonResponse({'count': count})

def orders(request):
    if request.user.is_authenticated:
        orders = OrderHistory.objects.filter(userid=request.user.id).order_by('-date')
        context = {
            'orders': orders,
            'user': request.user
        }
        return render(request, 'orders.html', context)
    else:
        return redirect('/login')

def add_review(request, pid):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        product = Product.objects.get(id=pid)
        
        Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        messages.success(request, 'Review submitted successfully!')
    
    return redirect(f'/product_details/{pid}')

def toggle_wishlist(request, pid):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)
    
    product = Product.objects.get(id=pid)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product)
    
    if wishlist_item.exists():
        wishlist_item.delete()
        return JsonResponse({'status': 'removed', 'message': 'Removed from wishlist'})
    else:
        Wishlist.objects.create(user=request.user, product=product)
        return JsonResponse({'status': 'added', 'message': 'Added to wishlist'})

def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    items = Wishlist.objects.filter(user=request.user).select_related('product')
    context = {'wishlist_items': items}
    return render(request, 'wishlist.html', context)
