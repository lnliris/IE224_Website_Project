from django.shortcuts import render
from django.views import View
from products.models import Product, Category

class HomeView(View):
    '''
    Lớp quản lý trang chủ
    '''
    def get(self, request):
        '''
        Hàm hiển thị các sản phẩm

        Args:
            - request

        Output:
            - Render trang chủ với toàn bộ các sản phẩm theo template index.html
        '''
        # Lấy tất cả sản phẩm và danh mục
        products = Product.objects.all()  # Hoặc có thể lọc theo điều kiện như còn hàng
        categories = Category.objects.all()

        # Truyền các sản phẩm và danh mục vào context
        context = {
            'products': products,
            'categories': categories,
        }

        return render(request, 'index.html', context)
