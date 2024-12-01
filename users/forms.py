from django import forms

class RegisterForms(forms.Form):
    username = forms.CharField(min_length=5,
                               max_length=20,
                               error_messages={
                                   "min_length":"Tên người dùng không được ít hơn 5 ký tự!",
                                   "max_length":"Tên người dùng đã vượt quá 15 ký tự!",
                                   "required":"Không được bỏ trống phần này!",
                               })

    password = forms.CharField(min_length=6, 
                               max_length=20,
                               error_messages={
                                   "min_length": "Mật khẩu cần ít nhất 6 ký tự!",
                                   "max_length": "Mật khẩu đã vượt quá 20 ký tự!",
                                   "required": "Không được bỏ trống phần này!",
                               })

    re_password = forms.CharField(min_length=6, 
                                  max_length=20,
                                  error_messages={
                                      "min_length": "Vui lòng nhập lại mật khẩu!",
                                      "max_length": "Vui lòng nhập lại mật khẩu!",
                                      "required": "Vui lòng nhập lại mật khẩu!",
                                   })
    
    def clean(self):
        clean_data = super(RegisterForms, self).clean()
        pw = clean_data.get('password')
        re_pw = clean_data.get('re_password')
        if pw != re_pw:
            raise forms.ValidationError("Mật khẩu nhập lại không khớp")

        return clean_data



class LoginForms(forms.Form):
    username = forms.CharField(min_length=5, max_length=20,
                               error_messages={
                                   "min_length":"Kiểm tra lại độ dài tên tài khoản!",
                                   "max_length":"Kiểm tra lại độ dài tên tài khoản!",
                                   "required":"Vui lòng nhập tài khoản!",
                               })

    password = forms.CharField(min_length=6, max_length=20,
                               error_messages={
                                   "min_length": "Kiểm tra lại độ dài mật khẩu!",
                                   "max_length": "Kiểm tra lại độ dài mật khẩu!",
                                   "required": "Vui lòng nhập mật khẩu!"
                               })

    remembered = forms.BooleanField(required=False)
