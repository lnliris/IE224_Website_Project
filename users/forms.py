from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForms(forms.Form):
    username = forms.CharField(min_length=5, max_length=20, error_messages={
        "min_length": "Tên người dùng không được ít hơn 5 ký tự!",
        "max_length": "Tên người dùng đã vượt quá 15 ký tự!",
        "required": "Không được bỏ trống phần này!",
    })
    email = forms.EmailField(error_messages={
        "required": "Vui lòng nhập email!",
        "invalid": "Email không hợp lệ!",
    })
    first_name = forms.CharField(max_length=30, error_messages={
        "required": "Vui lòng nhập tên!",
    })
    last_name = forms.CharField(max_length=30, error_messages={
        "required": "Vui lòng nhập họ!",
    })
    password = forms.CharField(min_length=6, max_length=20, error_messages={
        "min_length": "Mật khẩu cần ít nhất 6 ký tự!",
        "max_length": "Mật khẩu đã vượt quá 20 ký tự!",
        "required": "Không được bỏ trống phần này!",
    })
    re_password = forms.CharField(min_length=6, max_length=20, error_messages={
        "min_length": "Vui lòng nhập lại mật khẩu!",
        "max_length": "Vui lòng nhập lại mật khẩu!",
        "required": "Vui lòng nhập lại mật khẩu!",
    })

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError("Mật khẩu nhập lại không khớp")
        return cleaned_data



class LoginForms(forms.Form):
    username = forms.CharField(label="Username or Email", min_length=5,
                               error_messages={
                                   "min_length":"Kiểm tra lại độ dài tên tài khoản!",
                                   "required":"Vui lòng nhập tài khoản!",
                               })

    password = forms.CharField(min_length=6, max_length=20,
                               error_messages={
                                   "min_length": "Kiểm tra lại độ dài mật khẩu!",
                                   "max_length": "Kiểm tra lại độ dài mật khẩu!",
                                   "required": "Vui lòng nhập mật khẩu!"
                               })

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']