from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, UpdateOrder
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required(login_url='/login')
def home(request):
    return render(request, "shop/home.html")


@login_required(login_url='/login')
def about(request):
    return render(request, "shop/about.html")


@login_required(login_url='/login')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        description = request.POST.get('description', '')
        contact = Contact(name=name, email=email, phone=phone, description=description)
        contact.save()
        check = True
        return render(request, "shop/contact.html", {'check': check})
    return render(request, "shop/contact.html")


@login_required(login_url='/login')
def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=order_id, email=email)
            if len(order) > 0:
                update = UpdateOrder.objects.filter(order_id=order_id)
                itemList = order[0].items
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.time})
                    response = json.dumps([updates, itemList], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, "shop/tracker.html")


@login_required(login_url='/login')
def productView(request, myid):
    product = Product.objects.filter(product_id=myid)
    return render(request, "shop/productView.html", {'product': product[0]})


@login_required(login_url='/login')
def checkOut(request):
    if request.method == "POST":
        items = request.POST.get('items', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '') + " " + request.POST.get("address2", '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items=items, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = UpdateOrder(order_id=order.order_id, update_desc="Order Placed Successfully")
        update.save()
        check = True
        order_id = order.order_id
        return render(request, "shop/checkout.html", {'check': check, 'order_id': order_id})
    return render(request, "shop/checkout.html")


@login_required(login_url='/login')
def search(request):
    return render(request, "shop/search.html")


@login_required(login_url='/login')
def smartphone(request):
    products = []
    subcategories = Product.objects.values('subcategory', 'product_id')
    subcats = {item['subcategory'] for item in subcategories}
    print(subcats)
    for subcat in subcats:
        prodtemp = Product.objects.filter(subcategory=subcat, category='Smartphone')
        n = len(prodtemp)
        if n > 0:
            if n % 4 == 0:
                number_of_slides = n // 4
            else:
                number_of_slides = n // 4 + 1
            products.append([prodtemp, range(1, number_of_slides), number_of_slides])

    params = {'allProducts': products, 'category': 'smartphone'}

    return render(request, "shop/products.html", params)


@login_required(login_url='/login')
def accessories(request):
    products = []
    subcategories = Product.objects.values('subcategory', 'product_id')
    subcats = {item['subcategory'] for item in subcategories}
    print(subcats)
    for subcat in subcats:
        prodtemp = Product.objects.filter(subcategory=subcat, category='Accessories')
        n = len(prodtemp)
        if n > 0:
            if n % 4 == 0:
                number_of_slides = n // 4
            else:
                number_of_slides = n // 4 + 1
            products.append([prodtemp, range(1, number_of_slides), number_of_slides])

    params = {'allProducts': products,'category': 'accessories'}

    return render(request, "shop/products.html", params)


@login_required(login_url='/login')
def television(request):
    products = []
    subcategories = Product.objects.values('subcategory', 'product_id')
    subcats = {item['subcategory'] for item in subcategories}
    print(subcats)
    for subcat in subcats:
        prodtemp = Product.objects.filter(subcategory=subcat, category='Television')
        n = len(prodtemp)
        if n > 0:
            if n % 4 == 0:
                number_of_slides = n // 4
            else:
                number_of_slides = n // 4 + 1
            products.append([prodtemp, range(1, number_of_slides), number_of_slides])
    print(products)
    params = {'allProducts': products,'category': 'television'}
    return render(request, "shop/products.html", params)


@login_required(login_url='/login')
def laptops(request):
    products = []
    subcategories = Product.objects.values('subcategory', 'product_id')
    subcats = {item['subcategory'] for item in subcategories}
    print(subcats)
    for subcat in subcats:
        prodtemp = Product.objects.filter(subcategory=subcat, category='Laptop')
        print(prodtemp)
        n = len(prodtemp)
        if n > 0:
            if n % 4 == 0:
                number_of_slides = n // 4
            else:
                number_of_slides = n // 4 + 1
            products.append([prodtemp, range(1, number_of_slides), number_of_slides])

    params = {'allProducts': products, 'category': 'laptops'}
    return render(request, "shop/products.html", params)


def searchMatch(query, item):
    query = query.lower()
    if query in item.description.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.subcategory.lower():
        return True
    else:
        return False


@login_required(login_url='/login')
def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'product_id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        if n % 4 == 0:
            number_of_slides = n // 4
        else:
            number_of_slides = n // 4 + 1
        if len(prod) != 0:
            allProds.append([prod, range(1, number_of_slides), number_of_slides])
    params = {'allProds': allProds, "msg": "", "query": query}
    if len(allProds) == 0:
        params = {'msg': f"No Results for {query} found"}
    return render(request, 'shop/search.html', params)


@login_required(login_url='/login')
def bestsellers(request):
    products = []
    categories = Product.objects.values('category', 'product_id')
    #cats = {item['category'] for item in categories}
    #p_ids = {item['product_id'] for item in categories}
    #print(f"from bestsellers {cats}")
    #print(f"from bestsellers {p_ids}")
    #for cat in cats:
        #prodtemp = Product.objects.filter(category=cat)
        #n = len(prodtemp)
        #print(f"{n} in {cat}")
        #if n > 0:
            #if n % 4 == 0:
                #number_of_slides = n // 4
            #else:
                #number_of_slides = n // 4 + 1
            #products.append([prodtemp, range(1, number_of_slides), number_of_slides])int
    orders = Order.objects.values('items')
    #print(orders)
    # for item in categories:
    #     if item['category']=='Smartphone':
    #         print(f"Smartphone: {item['product_id']}")
    #     if item['category']=='Laptop':
    #         print(f"Laptop: {item['product_id']}")
    #     if item['category']=='Accessories':
    #         print(f"Accessories: {item['product_id']}")
    #     if item['category']=='Television':
    #         print(f"TV: {item['product_id']}")
    p_list = []
    for i in range(1,72):
        count = 0
        for order in orders:
            order = json.loads(str(order['items']))
            for item in order:
                if item == f'pr{i}':
                    count += order[item][0]
        p_list.append([i, count])
    #print(p_list)
    s_id = [1, 5, 6]
    l_id = []
    t_id = [7]
    a_id = [2]
    for j in range(8,40):
        s_id.append(j)
    for j in range(40, 52):
        l_id.append(j)
    for j in range(52,63):
        t_id.append(j)
    for j in range(63,72):
        a_id.append(j)
    sphone = []
    ltop = []
    tv = []
    acc = []
    for p in p_list:
        if p[0] in s_id:
            sphone.append([p[1],p[0]])
        elif p[0] in l_id:
            ltop.append([p[1],p[0]])
        elif p[0] in t_id:
            tv.append([p[1],p[0]])
        elif p[0] in a_id:
            acc.append([p[1],p[0]])
    sphone = sorted(sphone)
    sphone = sphone[len(sphone)-4:]
    ltop = sorted(ltop)
    ltop = ltop[len(ltop)-4:]
    tv = sorted(tv)
    tv = tv[len(tv)-4:]
    acc = sorted(acc)
    acc = acc[len(acc)-4:]
    
    products = []
    prodtemp = Product.objects.filter(product_id=sphone[0][1])|Product.objects.filter(product_id=sphone[1][1])|Product.objects.filter(product_id=sphone[2][1])|Product.objects.filter(product_id=sphone[3][1])
    products.append([prodtemp, range(1,1) ,1])
    prodtemp = Product.objects.filter(product_id=ltop[0][1])|Product.objects.filter(product_id=ltop[1][1])|Product.objects.filter(product_id=ltop[2][1])|Product.objects.filter(product_id=ltop[3][1])
    products.append([prodtemp, range(1,1) ,1])
    prodtemp = Product.objects.filter(product_id=tv[0][1])|Product.objects.filter(product_id=tv[1][1])|Product.objects.filter(product_id=tv[2][1])|Product.objects.filter(product_id=tv[3][1])
    products.append([prodtemp, range(1,1) ,1])
    prodtemp = Product.objects.filter(product_id=acc[0][1])|Product.objects.filter(product_id=acc[1][1])|Product.objects.filter(product_id=acc[2][1])|Product.objects.filter(product_id=acc[3][1])
    products.append([prodtemp, range(1,1) ,1])
    #print(products)
    params = {'allProducts': products}
    return render(request, "shop/bestsellers.html", params)