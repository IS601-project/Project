from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from kingdomkicks.models import Category, Product, Checkout  # assuming your Category model is in models.py


def admin(request):
    product_count = Product.objects.count()
    category_count = Category.objects.count()
    return render(request, 'admin/admin.html', {'product_count': product_count, 'category_count': category_count})


def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('list_categories')  # replace 'success_page' with the name of your success page
    else:
        return render(request, 'admin/add_category.html')


def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'admin/list_categories.html', {'categories': categories})


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.save()
        return redirect('list_categories')
    else:
        return render(request, 'admin/edit_category.html', {'category': category})


def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('list_categories')


def add_product(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        sku = request.POST.get('sku')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        size = request.POST.get('size')
        quantity = request.POST.get('quantity')
        Product.objects.create(name=name, sku=sku, description=description, price=price, image=image, category=category,
                               size=size, quantity=quantity)
        return redirect('list_products')
    else:
        return render(request, 'admin/add_product.html', {'categories': categories})


def list_products(request):
    products = Product.objects.all()
    print(products)
    return render(request, 'admin/list_products.html', {'products': products})


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.sku = request.POST.get('sku')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.category = request.POST.get('category')
        product.size = request.POST.get('size')
        product.quantity = request.POST.get('quantity')
        product.save()
        return redirect('list_products')
    else:
        return render(request, 'admin/edit_product.html', {'product': product})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('list_products')


def list_checkout(request):
    checkouts = Checkout.objects.all()
    return render(request, 'admin/list_checkout.html', {'checkouts': checkouts})


# site views`

def index(request):
    random_ads = Product.objects.order_by('?')[:4]
    random_all = Product.objects.order_by('?')

    return render(request, 'site/index.html', {'random_products': random_ads, 'random_all': random_all})


def women(request):
    sort = request.GET.get('sort', 'name')
    name = request.GET.get('name', '')
    category = request.GET.get('category', '')
    if sort not in ['name', 'price', '-price']:
        sort = 'name'
    products = Product.objects.filter(name__icontains=name, category__icontains=category).order_by(sort)
    categories = Category.objects.all()
    return render(request, 'site/product_list.html', {'products': products, 'categories': categories})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    return render(request, 'site/product_detail.html', {'product': product, 'related_products': related_products})


def cart(request):
    product_ids = request.session.get('cart', [])
    print(product_ids)
    _cart_products = Product.objects.filter(id__in=product_ids)
    print(_cart_products)
    cart_products = []
    for id in product_ids:
        cart_products.append(Product.objects.get(id=id))

    print(cart_products)
    subtotal = 0
    tax = Decimal(0.06)
    for p in cart_products:
        subtotal += p.price
    tax = round(subtotal * tax)
    total = subtotal + tax

    shipping = 7.75
    if subtotal > 250:
        shipping = "FREE"
    else:
        total = total + Decimal(shipping)
        shipping = "$ 7.75"

    return render(request, 'site/cart.html',
                  {'cart_products': cart_products, 'subtotal': subtotal, 'tax': tax, 'total': total,
                   'shipping': shipping})


def add_to_cart(request, product_id):
    cart_list = request.session.get('cart', [])
    cart_list.append(product_id)
    request.session['cart'] = cart_list
    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
    request.session['cart'] = cart
    return redirect('cart')


def checkout(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email_address = request.POST.get('email_address')
        delivery_location = request.POST.get('delivery_location')

        cart = request.session.get('cart', [])
        for product_id in cart:
            product = Product.objects.get(id=product_id)
            product.quantity -= 1
            product.save()

        checkout = Checkout.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email_address=email_address,
            delivery_location=delivery_location,
            product_ids=','.join(str(id) for id in cart),
        )
        checkout.save()
        request.session['cart'] = []

        return render(request, 'site/checkout_success.html')
    else:
        return render(request, 'site/checkout.html')
