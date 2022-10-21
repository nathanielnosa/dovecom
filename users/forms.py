from django import forms
from .models import Profile


class Userprofile(forms.ModelForm):
    password1 = forms.CharField(label=('Password'),widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label=('Confirm Password'),widget=forms.PasswordInput(attrs={'class':'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Profile
        fields = ['fullname','email','username','password1','password2','profile_pix']
        widgets={
            'fullname':forms.TextInput(attrs={'class':'form-control'}),
            'profile_pix':forms.FileInput(attrs={'class':'form-control','type':'file'})
        }

class Updateprofile(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Profile
        fields = ['fullname','email','username','profile_pix']
        widgets={
            'fullname':forms.TextInput(attrs={'class':'form-control'}),
            'profile_pix':forms.FileInput(attrs={'class':'form-control','type':'file'})
        }