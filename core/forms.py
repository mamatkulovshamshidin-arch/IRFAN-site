from django import forms
from django.core.validators import RegexValidator
from .models import Registration, ContactMessage

class RegistrationForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput, label='')
    class Meta:
        model = Registration
        fields = ['full_name','phone','email','age','city','education_level','learning_format','notes','consent']
        widgets = {'notes': forms.Textarea(attrs={'rows':4, 'placeholder':'Кааласаңыз, кошумча маалымат жазыңыз'})}

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 7 or age > 100:
            raise forms.ValidationError('Жашыңызды 7ден 100гө чейинки сан менен жазыңыз.')
        return age

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        RegexValidator(
            regex=r'^\+?[0-9 ()-]{7,32}$',
            message='Телефон номерин туура форматта жазыңыз.',
        )(phone)
        return phone

    def clean_website(self):
        if self.cleaned_data['website']:
            raise forms.ValidationError('Арызды жөнөтүү мүмкүн болгон жок.')
        return ''

class ContactForm(forms.ModelForm):
    class Meta:
        model=ContactMessage; fields=['name','phone','email','message']
        widgets={'message':forms.Textarea(attrs={'rows':5})}
