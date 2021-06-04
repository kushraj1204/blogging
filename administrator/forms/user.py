from django.forms import ModelForm
from Users.models import CustomUser
from django.core.exceptions import ValidationError


class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        exclude = ['last_login', 'date_joined', 'activation', 'phone_activation_code']


class UserUpdateForm(ModelForm):

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = CustomUser.objects.filter(email=email).exclude(
            pk=self.instance.pk)

        if self.instance and self.instance.pk and not email_exists:
            return email
        else:
            raise ValidationError("This email has already been taken")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_exists = CustomUser.objects.filter(username=username).exclude(
            pk=self.instance.pk)
        if self.instance and self.instance.pk and not username_exists:
            return username
        else:
            raise ValidationError("This username has already been taken")

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone_exists = CustomUser.objects.filter(phone=phone).exclude(
            pk=self.instance.pk)
        if self.instance and self.instance.pk and not phone_exists:
            return phone
        else:
            raise ValidationError("This username has already been taken")

    class Meta:
        model = CustomUser
        exclude = ['last_login', 'date_joined', 'activation', 'phone_activation_code', 'password']
