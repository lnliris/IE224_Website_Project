from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Tìm kiếm sản phẩm...', 'class': 'form-control'})
    )
    min_price = forms.DecimalField(
        required=False,
        label='Giá tối thiểu',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    max_price = forms.DecimalField(
        required=False,
        label='Giá tối đa',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
class FilterForm(forms.Form):

    PRODUCT_TYPE_CHOICES = (
        ('Official', 'Chính hãng'),
        ('Pro', 'Pro'),
        ('Regular', 'Bình thường'),
    )

    color_choices = (
        ('Red', 'Đỏ'),
        ('Blue', 'Xanh'),
        ('Black', 'Đen'),
        ('White', 'Trắng'),
        ('Yellow', 'Vàng'),
        # Thêm các màu khác nếu cần
    )

    material_choices = (
        ('Natural Rubber', 'Cao su tự nhiên'),
        ('Synthetic Rubber', 'Cao su nhân tạo'),
        ('EVA', 'EVA'),
        ('Carbon Fiber', 'Sợi carbon'),
    )

    product_type = forms.ChoiceField(
        choices=PRODUCT_TYPE_CHOICES,
        required=False,
        label="Loại sản phẩm"
    )

    color = forms.MultipleChoiceField(
        choices=color_choices,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Màu sắc"
    )
    material = forms.MultipleChoiceField(
        choices=material_choices,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Chất liệu"
    )
