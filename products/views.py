from django.shortcuts import render
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .form import SearchForm
from django.db.models import Q


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()  # Lấy tất cả danh mục
    products = Product.objects.filter(stock__gt=0)  # Chỉ lấy sản phẩm còn hàng

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)  # Lọc sản phẩm theo danh mục
    else:
        category = None  # Không có category_slug, sẽ hiển thị toàn bộ sản phẩm

    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'form': form,  # Truyền form vào context
    }

    return render(request, 'products.html', context)

def product_detail(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    context = {'product': product}
    return render(request, 'product_detail.html', context)

class ProductsView(View):
    def get(self, request):
        products = Product.objects.filter(stock__gt=0)  # Lấy sản phẩm còn hàng
        categories = Category.objects.all()  # Lấy tất cả danh mục

        # Xử lý tìm kiếm
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')

            if query:
                products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))  # Tìm theo tên hoặc mô tả

            if min_price is not None:
                products = products.filter(price__gte=min_price)  # Lọc giá >= min_price

            if max_price is not None:
                products = products.filter(price__lte=max_price)  # Lọc giá <= max_price


        context = {
            'products': products,
            'categories': categories,
        }
        return render(request, 'products.html', context)

