from django.shortcuts import render
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()  # Lấy tất cả danh mục
    products = Product.objects.filter(stock__gt=0)  # Chỉ lấy sản phẩm còn hàng
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'products.html', context)
def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)  # Tìm sản phẩm theo slug
    context = {'product': product}
    return render(request, 'products.html', context)

class ProductsView(View):
    def get(self, request):
        return render(request, 'products.html')
