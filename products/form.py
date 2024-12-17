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
