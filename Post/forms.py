from django import forms
from .models import *

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ("image","eduction","bio","country")

        # For stylings

        widgets = { 
            'image':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'eduction': forms.Textarea(attrs={'class':'form-control','placeholder':'Enter about your eductaion'}),
            'bio':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter about your life'}),
            'country': forms.TextInput(attrs={'class':'form-control'})
        }


        

