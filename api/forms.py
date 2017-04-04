from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(render_value=False),
    )
    confirm_new_password = forms.CharField(
        label='Confirm New password',
        widget=forms.PasswordInput(render_value=False),
    )

    class Meta:
        model = User

    def clean(self):
        new_password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_new_password']
        if new_password != confirm_password:
            raise forms.ValidationError(u'Passwords are not equal')
        return self.cleaned_data
