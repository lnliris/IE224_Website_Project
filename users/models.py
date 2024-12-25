from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class MyUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        '''
        Hàm tạo người dùng

        Args:
            - first_name: họ
            - last_name: tên
            - username: tên đăng nhập
            - email: email người dùng
            - password: mật khẩu

        Output:
            - biến người dùng là người dùng đã được tạo.
        '''
        if not email:
            raise ValueError('Cần nhập email để tạo người dùng!')

        if not username:
            raise ValueError('Cần nhập tên người dùng để tạo người dùng!')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        '''
        Hàm tạo admin

        Args:
            - first_name: họ
            - last_name: tên
            - username: tên đăng nhập
            - email: email người dùng
            - password: mật khẩu

        Output:
            - biến người dùng là admin đã được tạo.
        '''
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.role = 'Admin'  # Default role for superusers
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    '''
    Class User kế thừa từ AbstractBaseUser của django.
    '''
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('User', 'User'),
        ('Guest', 'Guest'),
    )

    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    role            = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Guest')

    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(default=timezone.now)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superadmin   = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        '''
        Hàm kiểm tra quyền của user.
        '''
        if self.role == 'Admin':
            return True
        if self.role == 'User' and perm.startswith('user.'):
            return True
        return False

    def has_module_perms(self, app_label):
        '''
        Hàm kiểm tra quyền của user theo module

        Args:
            - app_label (str): tên của module ứng dụng.
        '''
        if self.role in ['Admin', 'User']:
            return True
        return False
    
    def get_orders(self):
        '''
        Hàm lấy danh sách các đơn hàng

        Args:

        Output:
            - Trả về lazy query của các đơn hàng người dùng đã đặt.

        '''
        return self.order_set.all() 

class UserProfile(models.Model):
    '''
    Các thông tin thêm của user (nhóm chưa triển khai)
    '''
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'


