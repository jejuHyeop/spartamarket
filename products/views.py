from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Products, HashTag
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
            products = Products.objects.filter(hashtags__name=keyword)
    else:   
        products = Products.objects.all()

    if stockOut == 'false':
        products = products.filter(~Q(stock=0))
    if saleProd == 'true':
        products = products.filter(~Q(sale_price=0))

    
    if not sort or sort == "new":
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
        hashtags = request.POST.getlist("productHashtag")  
        seller = request.user
        display_price = price
        if sale_price:
            display_price = sale_price
        else:
            sale_price = 0
        product = Products(title=title, price=price, stock=stock, sale_price=sale_price, display_price=display_price, description=description, image=image, seller=seller)
        
        product.save()

        for tag in hashtags:
            tag = tag.split()[0].replace("#", "")
            if not HashTag.objects.filter(name=tag).exists():
                hashtag = HashTag(name=tag)
                hashtag.save()
            else:
                hashtag = HashTag.objects.get(name=tag)
            product.hashtags.add(hashtag)

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

def mine(request, pid):
    p = Products.objects.get(id=pid)
    user = request.user
    if p in user.wishprod.all():
        user.wishprod.remove(p)
    else:
        user.wishprod.add(p)
    return redirect(request.META.get('HTTP_REFERER'))

def minelist(request):
    user = request.user
    products = user.wishprod.all()
    context = {
        "products": products,
    }
    return render(request, "products/minelist.html", context)

def update(request, pid):
    p = Products.objects.get(id=pid)
    if request.method == "POST":
        title = request.POST.get("productTitle")
        price = request.POST.get("productPrice")
        sale_price = request.POST.get("productSalePrice")
        description = request.POST.get("productDesc")
        image = request.FILES.get("productImage")
        stock = request.POST.get("productStock")
        hashtags = request.POST.getlist("productHashtag")
        display_price = price
        if sale_price:
            display_price = sale_price
            p.sale_price = sale_price
        else:
            p.sale_price = 0
        p.title = title
        p.price = price
        p.description = description
        p.display_price = display_price
        p.stock = stock
        if image:
            p.image.delete()
            p.image = image
        p.save()
        p.hashtags.clear()
        for tag in hashtags:
            tag = tag.split()[0].replace("#", "")
            if not HashTag.objects.filter(name=tag).exists():
                hashtag = HashTag(name=tag)
                hashtag.save()
            else:
                hashtag = HashTag.objects.get(name=tag)
            p.hashtags.add(hashtag)
        return redirect("products:detail", pid)
    context = {
        "p": p,
    }
    return render(request, "products/update.html", context)

def delete(request, pid):
    p = Products.objects.get(id=pid)
    if p.seller == request.user:
        p.image.delete()
        p.delete()
    return JsonResponse({"result": True})

def myprodlist(request):
    user = request.user
    products = user.products.all()
    context = {
        "products": products,
    }
    return render(request, "products/myprodlist.html", context)