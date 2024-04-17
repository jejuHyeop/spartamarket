from django.shortcuts import render, redirect
from .models import Products
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q

# Create your views here.
def index(request):
    page = request.GET.get("page", 1)
    cate = request.GET.get("cate", "")
    sort = request.GET.get("sort","")
    keyword = request.GET.get("keyword", "")
    stockOut = request.GET.get("stockOut", False)
    saleProd = request.GET.get("saleProd", False)

    if keyword:
        if cate == "title":
            products = Products.objects.filter(title__contains=keyword)
        elif cate == "seller":
            products = Products.objects.filter(seller__username=keyword)
        elif cate == "hashtag":
            pass
    else:   
        products = Products.objects.all()

    if stockOut == 'false':
        products = products.filter(~Q(stock=0))
    if saleProd == 'true':
        products = products.filter(~Q(sale_price=0))

    if sort:
        if sort == "new":
            products = products.order_by("-created_at")
        elif sort == "cheap":
            products = products.order_by("display_price")
        elif sort == "expensive":
            products = products.order_by("-display_price")
        elif sort == "hits":
            products = products.order_by("-hits")
        elif sort == "likey":
            products = products.annotate(likey_count=Count('likey')).order_by('-likey_count')
        elif sort == "score":
            products = products.order_by("-score")
        
    pag = Paginator(products, 4)
    obj = pag.get_page(page)

    context = {
        "obj": obj,
        "page": page,
        "cate": cate,
        "keyword": keyword,
        "sort": sort,
        "stockOut": stockOut,
        "saleProd": saleProd,
    }
    return render(request, "products/index.html", context)

def detail(request, pid):
    product = Products.objects.get(id=pid)
    print(request.META.get('HTTP_REFERER'))
    if request.META.get('HTTP_REFERER') and not f"/{pid}/detail/" in request.META.get('HTTP_REFERER'):
        product.hits += 1
        product.save()
    context = {
        "p": product,
    }
    return render(request, "products/detail.html", context)

def create(request):
    if request.method == "POST":
        title = request.POST.get("productTitle")
        price = request.POST.get("productPrice")
        sale_price = request.POST.get("productSalePrice")
        description = request.POST.get("productDesc")
        image = request.FILES.get("productImage")
        stock = request.POST.get("productStock")
        seller = request.user
        display_price = price
        if sale_price:
            display_price = sale_price
        product = Products(title=title, price=price, stock=stock, display_price=display_price, description=description, image=image, seller=seller)
        product.save()
        return redirect('products:index')
    return render(request, "products/create.html")

def likey(request, pid):
    p = Products.objects.get(id=pid)
    user = request.user
    if user in p.likey.all():
        p.likey.remove(user)
    else:
        p.likey.add(user)
    return redirect("products:detail", pid)

def myprod(request, pid):
    p = Products.objects.get(id=pid)
    user = request.user
    if p in user.wishprod.all():
        user.wishprod.remove(p)
    else:
        user.wishprod.add(p)
    return redirect("products:detail", pid)

def mylist(request):
    if request.method == "POST":
        pid = request.POST.get("product_id")
        user = request.user
        p = Products.objects.get(id=pid)
        if p in user.wishprod.all():
            user.wishprod.remove(p)
        else:
            user.wishprod.add(p)
    user = request.user
    products = user.wishprod.all()
    context = {
        "products": products,
    }
    return render(request, "accounts/mylist.html", context)