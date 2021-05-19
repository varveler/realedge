from django import forms


class OrdersFileForm(forms.Form):
    local_file = forms.FileField(widget=forms.ClearableFileInput(), required=False)
